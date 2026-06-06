import sys
import os
from datetime import datetime
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivy.uix.boxlayout import BoxLayout

# Ensure path includes local directories
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import database
from screens import (
    LoginScreen,
    BerandaScreen,
    DataScreen,
    KeuanganScreen,
    DaftarAkunScreen,
    JurnalUmumScreen,
    BukuBesarScreen,
    NeracaSaldoScreen,
    LabaRugiScreen
)

KV_MAIN = '''
<MainScreen>:
    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            id: top_app_bar
            title: "SIAKTERNAK MANAGEMENT PRO"
            md_bg_color: 0.12, 0.45, 0.12, 1
            elevation: 4
            right_action_items: [["logout", lambda x: app.logout()]]

        MDBottomNavigation:
            id: bottom_nav
            panel_color: 1, 1, 1, 1
            selected_color_indicator: 0.12, 0.45, 0.12, 1

            MDBottomNavigationItem:
                id: tab_dash
                name: 'screen_dash'
                text: 'Beranda'
                icon: 'home'
                on_tab_press: app.on_tab_switch("beranda")

            MDBottomNavigationItem:
                id: tab_data
                name: 'screen_data'
                text: 'Data'
                icon: 'table-large'
                on_tab_press: app.on_tab_switch("data")

            MDBottomNavigationItem:
                id: tab_finance
                name: 'screen_finance'
                text: 'Keuangan'
                icon: 'wallet-outline'
                on_tab_press: app.on_tab_switch("keuangan")
'''

Builder.load_string(KV_MAIN)

class MainScreen(MDScreen):
    beranda_screen = None
    data_screen = None
    keuangan_screen = None

    def on_kv_post(self, base_widget):
        # Instantiate modular screens
        self.beranda_screen = BerandaScreen()
        self.data_screen = DataScreen()
        self.keuangan_screen = KeuanganScreen()

        # Bind screens to their corresponding navigation tabs
        self.ids.tab_dash.add_widget(self.beranda_screen)
        self.ids.tab_data.add_widget(self.data_screen)
        self.ids.tab_finance.add_widget(self.keuangan_screen)


class SiakTernakApp(MDApp):
    current_user = StringProperty("")
    dialog = None

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"
        
        # Initialize database tables
        database.init_db()

        # Create MDScreenManager
        self.sm = MDScreenManager()

        # Create screens
        self.login_screen = LoginScreen(name='login')
        self.main_screen = MainScreen(name='main')
        
        # Create accounting sub-screens
        self.coa_screen = DaftarAkunScreen(name='coa')
        self.jurnal_screen = JurnalUmumScreen(name='jurnal')
        self.buku_besar_screen = BukuBesarScreen(name='buku_besar')
        self.neraca_screen = NeracaSaldoScreen(name='neraca')
        self.laba_rugi_screen = LabaRugiScreen(name='laba_rugi')

        self.sm.add_widget(self.login_screen)
        self.sm.add_widget(self.main_screen)
        self.sm.add_widget(self.coa_screen)
        self.sm.add_widget(self.jurnal_screen)
        self.sm.add_widget(self.buku_besar_screen)
        self.sm.add_widget(self.neraca_screen)
        self.sm.add_widget(self.laba_rugi_screen)

        # Set initial screen
        self.sm.current = 'login'
        return self.sm

    def switch_accounting_screen(self, screen_type):
        self.sm.transition.direction = 'left'
        self.sm.current = screen_type

    def back_to_main(self):
        self.sm.transition.direction = 'right'
        self.sm.current = 'main'

    def verify_login(self):
        username = self.login_screen.ids.username_input.text.strip()
        password = self.login_screen.ids.password_input.text.strip()
        error_label = self.login_screen.ids.error_label

        if not username or not password:
            error_label.text = "Username dan password harus diisi!"
            return

        user = database.verify_user(username, password)
        if user:
            # user = (id, username, password, nama_lengkap, created_at)
            self.current_user = user[3] if user[3] else username
            error_label.text = ""
            self.sm.current = 'main'
            
            # Switch to Beranda tab and trigger its load
            self.main_screen.ids.bottom_nav.switch_tab('screen_dash')
            self.on_tab_switch("beranda")
        else:
            error_label.text = "Username atau password salah!"

    def logout(self):
        self.login_screen.ids.username_input.text = ""
        self.login_screen.ids.password_input.text = ""
        self.login_screen.ids.error_label.text = ""
        self.sm.current = 'login'

    def on_tab_switch(self, tab_name):
        if not self.main_screen:
            return
            
        if tab_name == "beranda" and self.main_screen.beranda_screen:
            self.main_screen.beranda_screen.trigger_loading()
        elif tab_name == "data" and self.main_screen.data_screen:
            self.main_screen.data_screen.trigger_loading()
        elif tab_name == "keuangan" and self.main_screen.keuangan_screen:
            self.main_screen.keuangan_screen.trigger_loading()

    # --- QUICK DIALOG SYSTEM ---
    def open_quick_dialog(self, jenis, kat):
        self.temp_quick_jenis = jenis
        self.temp_quick_kat = kat
        
        self.quick_input = MDTextField(
            hint_text="Nominal Rp",
            input_filter="int",
            mode="rectangle"
        )
        
        self.dialog = MDDialog(
            title=f"Catat Cepat {kat}",
            type="custom",
            content_cls=BoxLayout(orientation="vertical", size_hint_y=None, height="60dp"),
            buttons=[
                MDFlatButton(text="BATAL", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(
                    text="SIMPAN",
                    md_bg_color=(0.12, 0.45, 0.12, 1),
                    on_release=self.save_quick_data
                )
            ],
        )
        self.dialog.content_cls.add_widget(self.quick_input)
        self.dialog.open()

    def save_quick_data(self, *args):
        nominal = self.quick_input.text.strip()
        if nominal:
            if self.temp_quick_jenis == "Pemasukan":
                # Save quick income (selling cows)
                database.add_pemasukan(jumlah_sapi=1, total_harga=int(nominal))
            else:
                # Save quick expense (feed or health)
                # Map standard products
                prod_name = self.temp_quick_kat
                cat_name = "Pakan" if "Pakan" in self.temp_quick_kat else "Kesehatan"
                database.add_pengeluaran(produk=prod_name, kategori=cat_name, nominal=int(nominal))
                
            self.dialog.dismiss()
            # Reload dashboard data
            if self.main_screen.beranda_screen:
                self.main_screen.beranda_screen.load_data()


if __name__ == '__main__':
    SiakTernakApp().run()
