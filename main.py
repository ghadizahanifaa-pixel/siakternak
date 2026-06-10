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
from kivymd.uix.list import (
    TwoLineAvatarIconListItem,
    IconLeftWidget,
    IconRightWidget,
    OneLineIconListItem
)

# Ensure path includes local directories
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import database
from screens import (
    LoginScreen,
    BerandaScreen,
    DataScreen,
    InventarisScreen,
    KeuanganScreen,
    DaftarAkunScreen,
    JurnalUmumScreen,
    BukuBesarScreen,
    NeracaSaldoScreen,
    LabaRugiScreen,
    LandingScreen,
    OrderFormScreen,
    OrderSuccessScreen,
    PembeliScreen
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
            right_action_items: [["account-cog", lambda x: app.open_profile_dialog()], ["logout", lambda x: app.logout()]]

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
                id: tab_pembeli
                name: 'screen_pembeli'
                text: 'Data Pembeli'
                icon: 'account-multiple-outline'
                on_tab_press: app.on_tab_switch("pembeli")

            MDBottomNavigationItem:
                id: tab_data
                name: 'screen_data'
                text: 'Data'
                icon: 'table-large'
                on_tab_press: app.on_tab_switch("data")

            MDBottomNavigationItem:
                id: tab_inventaris
                name: 'screen_inventaris'
                text: 'Inventaris'
                icon: 'cow'
                on_tab_press: app.on_tab_switch("inventaris")

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
    pembeli_screen = None
    data_screen = None
    inventaris_screen = None
    keuangan_screen = None

    def on_kv_post(self, base_widget):
        # Instantiate modular screens
        self.beranda_screen = BerandaScreen()
        self.pembeli_screen = PembeliScreen()
        self.data_screen = DataScreen()
        self.inventaris_screen = InventarisScreen()
        self.keuangan_screen = KeuanganScreen()

        # Bind screens to their corresponding navigation tabs
        self.ids.tab_dash.add_widget(self.beranda_screen)
        self.ids.tab_pembeli.add_widget(self.pembeli_screen)
        self.ids.tab_data.add_widget(self.data_screen)
        self.ids.tab_inventaris.add_widget(self.inventaris_screen)
        self.ids.tab_finance.add_widget(self.keuangan_screen)


class UserListDialogContent(BoxLayout):
    pass

KV_PROFILE = '''
<UserListDialogContent>:
    orientation: 'vertical'
    size_hint_y: None
    height: "260dp"
    ScrollView:
        MDList:
            id: user_list
'''
Builder.load_string(KV_PROFILE)


class SiakTernakApp(MDApp):
    current_user = StringProperty("")
    logged_in_username = StringProperty("")
    dialog = None

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"
        
        # Initialize database tables
        database.init_db()

        # Create MDScreenManager
        self.sm = MDScreenManager()

        # Create screens
        self.landing_screen = LandingScreen(name='landing')
        self.order_form_screen = OrderFormScreen(name='order_form')
        self.order_success_screen = OrderSuccessScreen(name='order_success')
        self.login_screen = LoginScreen(name='login')
        self.main_screen = MainScreen(name='main')
        
        # Create accounting sub-screens
        self.coa_screen = DaftarAkunScreen(name='coa')
        self.jurnal_screen = JurnalUmumScreen(name='jurnal')
        self.buku_besar_screen = BukuBesarScreen(name='buku_besar')
        self.neraca_screen = NeracaSaldoScreen(name='neraca')
        self.laba_rugi_screen = LabaRugiScreen(name='laba_rugi')

        self.sm.add_widget(self.landing_screen)
        self.sm.add_widget(self.order_form_screen)
        self.sm.add_widget(self.order_success_screen)
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

    def back_to_landing(self):
        self.sm.transition.direction = 'right'
        self.sm.current = 'landing'

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
            self.logged_in_username = username
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
        self.logged_in_username = ""
        self.sm.transition.direction = 'right'
        self.sm.current = 'login'

    def on_tab_switch(self, tab_name):
        if not self.main_screen:
            return
            
        if tab_name == "beranda" and self.main_screen.beranda_screen:
            self.main_screen.beranda_screen.trigger_loading()
        elif tab_name == "pembeli" and self.main_screen.pembeli_screen:
            self.main_screen.pembeli_screen.trigger_loading()
        elif tab_name == "data" and self.main_screen.data_screen:
            self.main_screen.data_screen.trigger_loading()
        elif tab_name == "inventaris" and self.main_screen.inventaris_screen:
            self.main_screen.inventaris_screen.trigger_loading()
        elif tab_name == "keuangan" and self.main_screen.keuangan_screen:
            self.main_screen.keuangan_screen.trigger_loading()

    # --- USER PROFILE & MANAGEMENT DIALOGS ---
    def open_profile_dialog(self):
        content = BoxLayout(orientation="vertical", size_hint_y=None, height="180dp", spacing="5dp")
        
        item1 = OneLineIconListItem(text="Ubah Password")
        item1.add_widget(IconLeftWidget(icon="key-change"))
        item1.bind(on_release=lambda x: self.open_change_password_dialog())
        
        item2 = OneLineIconListItem(text="Registrasi User Baru")
        item2.add_widget(IconLeftWidget(icon="account-plus"))
        item2.bind(on_release=lambda x: self.open_register_dialog())
        
        item3 = OneLineIconListItem(text="Daftar & Hapus User")
        item3.add_widget(IconLeftWidget(icon="account-multiple"))
        item3.bind(on_release=lambda x: self.open_user_list_dialog())
        
        content.add_widget(item1)
        content.add_widget(item2)
        content.add_widget(item3)
        
        self.profile_main_dialog = MDDialog(
            title="Manajemen Pengguna",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="TUTUP", on_release=lambda x: self.profile_main_dialog.dismiss())
            ]
        )
        self.profile_main_dialog.open()

    def open_change_password_dialog(self):
        if hasattr(self, 'profile_main_dialog') and self.profile_main_dialog:
            self.profile_main_dialog.dismiss()
            
        self.change_pwd_input = MDTextField(
            hint_text="Password Baru",
            password=True,
            mode="rectangle"
        )
        
        self.dialog = MDDialog(
            title="Ubah Password",
            type="custom",
            content_cls=BoxLayout(orientation="vertical", size_hint_y=None, height="60dp"),
            buttons=[
                MDFlatButton(text="BATAL", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(
                    text="SIMPAN",
                    md_bg_color=(0.12, 0.45, 0.12, 1),
                    on_release=self.save_new_password
                )
            ],
        )
        self.dialog.content_cls.add_widget(self.change_pwd_input)
        self.dialog.open()

    def save_new_password(self, *args):
        new_pwd = self.change_pwd_input.text.strip()
        if new_pwd:
            database.change_password(self.logged_in_username, new_pwd)
            self.dialog.dismiss()
            self.show_alert("Sukses", "Password berhasil diubah.")

    def open_register_dialog(self):
        if hasattr(self, 'profile_main_dialog') and self.profile_main_dialog:
            self.profile_main_dialog.dismiss()
            
        self.reg_username = MDTextField(hint_text="Username", mode="rectangle")
        self.reg_fullname = MDTextField(hint_text="Nama Lengkap", mode="rectangle")
        self.reg_password = MDTextField(hint_text="Password", password=True, mode="rectangle")
        
        content = BoxLayout(orientation="vertical", size_hint_y=None, height="195dp", spacing="10dp")
        content.add_widget(self.reg_username)
        content.add_widget(self.reg_fullname)
        content.add_widget(self.reg_password)
        
        self.dialog = MDDialog(
            title="Registrasi User Baru",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="BATAL", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(
                    text="DAFTAR",
                    md_bg_color=(0.12, 0.45, 0.12, 1),
                    on_release=self.save_new_user
                )
            ],
        )
        self.dialog.open()

    def save_new_user(self, *args):
        uname = self.reg_username.text.strip()
        fullname = self.reg_fullname.text.strip()
        pwd = self.reg_password.text.strip()
        
        if uname and fullname and pwd:
            success = database.register_user(uname, fullname, pwd)
            self.dialog.dismiss()
            if success:
                self.show_alert("Sukses", f"User @{uname} berhasil didaftarkan.")
            else:
                self.show_alert("Error", f"Username @{uname} sudah digunakan.")

    def open_user_list_dialog(self):
        if hasattr(self, 'profile_main_dialog') and self.profile_main_dialog:
            self.profile_main_dialog.dismiss()
            
        self.user_list_content = UserListDialogContent()
        self.load_users_to_list()
        
        self.dialog = MDDialog(
            title="Daftar Pengguna",
            type="custom",
            content_cls=self.user_list_content,
            buttons=[
                MDFlatButton(text="TUTUP", on_release=lambda x: self.dialog.dismiss())
            ],
        )
        self.dialog.open()

    def load_users_to_list(self):
        self.user_list_content.ids.user_list.clear_widgets()
        users = database.get_all_users()
        for u in users:
            # u = (id, username, nama_lengkap, created_at)
            item = TwoLineAvatarIconListItem(
                text=f"{u[2]} (@{u[1]})",
                secondary_text=f"Dibuat: {u[3]}"
            )
            item.add_widget(IconLeftWidget(icon="account"))
            
            if u[1] != "admin":
                trash_btn = IconRightWidget(
                    icon="trash-can-outline",
                    theme_text_color="Custom",
                    text_color=(0.8, 0.2, 0.2, 1),
                    on_release=lambda x, uname=u[1]: self.confirm_delete_user(uname)
                )
                item.add_widget(trash_btn)
                
            self.user_list_content.ids.user_list.add_widget(item)

    def confirm_delete_user(self, username):
        self.dialog.dismiss()
        
        self.confirm_dialog = MDDialog(
            title="Konfirmasi Hapus",
            text=f"Apakah Anda yakin ingin menghapus user @{username}?",
            buttons=[
                MDFlatButton(text="BATAL", on_release=lambda x: self.reopen_user_list_after_confirm()),
                MDRaisedButton(
                    text="HAPUS",
                    md_bg_color=(0.8, 0.2, 0.2, 1),
                    on_release=lambda x, uname=username: self.delete_user_action(uname)
                )
            ]
        )
        self.confirm_dialog.open()

    def reopen_user_list_after_confirm(self):
        self.confirm_dialog.dismiss()
        self.open_user_list_dialog()

    def delete_user_action(self, username):
        self.confirm_dialog.dismiss()
        database.delete_user(username)
        self.open_user_list_dialog()

    def show_alert(self, title, text):
        alert = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    md_bg_color=(0.12, 0.45, 0.12, 1),
                    on_release=lambda x: alert.dismiss()
                )
            ]
        )
        alert.open()

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
