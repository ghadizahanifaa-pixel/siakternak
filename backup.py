import sqlite3
import os
from datetime import datetime
from fpdf import FPDF
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.list import ThreeLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDFloatingActionButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
import hashlib


# ==========================================
# DATABASE LOGIC
# ==========================================
def init_db():
    conn = sqlite3.connect('siakternak.db')
    c = conn.cursor()

    # Tabel untuk transaksii
    c.execute('''CREATE TABLE IF NOT EXISTS transaksi 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  jenis TEXT, kategori TEXT, jumlah INTEGER, 
                  tanggal TEXT)''')

    # Tabel untuk user
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  username TEXT UNIQUE, password TEXT, 
                  nama_lengkap TEXT, created_at TEXT)''')

    # Insert default admin jika belum ada
    c.execute("SELECT * FROM users WHERE username='admin'")
    if not c.fetchone():
        default_password = hashlib.sha256("admin123".encode()).hexdigest()
        c.execute("INSERT INTO users (username, password, nama_lengkap, created_at) VALUES (?,?,?,?)",
                  ("admin", default_password, "Administrator", datetime.now().strftime("%d/%m/%Y %H:%M")))

    conn.commit()
    conn.close()


# ==========================================
# UI DESIGN (KV LANGUAGE)
# ==========================================
KV = '''
<DataItem>:
    text: root.kategori
    secondary_text: root.jumlah
    IconLeftWidget:
        icon: "table-edit"
        theme_text_color: "Custom"
        text_color: 0.1, 0.4, 0.1, 1
    IconRightWidget:
        icon: "delete-outline"
        theme_text_color: "Custom"
        text_color: 0.8, 0.2, 0.2, 1
        on_release: app.confirm_delete(root.db_id, root.kategori)

<HistoryItem>:
    text: root.kategori
    secondary_text: root.tanggal
    tertiary_text: root.jenis + " | " + root.jumlah
    IconLeftWidget:
        icon: "history"
        theme_text_color: "Custom"
        text_color: 0.5, 0.5, 0.5, 1

<LoginScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        padding: "40dp"
        spacing: "20dp"
        md_bg_color: 0.95, 0.97, 0.95, 1

        MDBoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.3
            spacing: "10dp"

            MDIcon:
                icon: "cow"
                halign: "center"
                font_size: "80sp"
                theme_text_color: "Custom"
                text_color: 0.1, 0.4, 0.1, 1

            MDLabel:
                text: "SIAKTERNAK PRO"
                halign: "center"
                font_style: "H4"
                theme_text_color: "Custom"
                text_color: 0.1, 0.4, 0.1, 1
                bold: True

            MDLabel:
                text: "Sistem Informasi Akuntansi Peternakan"
                halign: "center"
                font_style: "Caption"
                theme_text_color: "Custom"
                text_color: 0.3, 0.5, 0.3, 1

        MDBoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.5
            spacing: "15dp"
            padding: "20dp"

            MDTextField:
                id: username_input
                hint_text: "Username"
                icon_right: "account"
                mode: "rectangle"
                size_hint_x: 0.8
                pos_hint: {"center_x": 0.5}

            MDTextField:
                id: password_input
                hint_text: "Password"
                icon_right: "eye-off"
                password: True
                mode: "rectangle"
                size_hint_x: 0.8
                pos_hint: {"center_x": 0.5}

            MDRaisedButton:
                text: "LOGIN"
                md_bg_color: 0.1, 0.4, 0.1, 1
                size_hint: 0.8, None
                height: "50dp"
                pos_hint: {"center_x": 0.5}
                on_release: app.verify_login()

            MDLabel:
                id: error_label
                text: ""
                halign: "center"
                theme_text_color: "Error"
                font_style: "Caption"

        MDBoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.2
            spacing: "5dp"

            MDLabel:
                text: "© 2024 SIAKTERNAK Management System"
                halign: "center"
                font_style: "Caption"
                theme_text_color: "Custom"
                text_color: 0.5, 0.5, 0.5, 1

<MainScreen>:
    BoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "SIAKTERNAK MANAGEMENT PRO"
            md_bg_color: 0.1, 0.4, 0.1, 1
            elevation: 4
            right_action_items: [["logout", lambda x: app.logout()]]

        MDBottomNavigation:
            panel_color: 1, 1, 1, 1
            selected_color_indicator: 0.1, 0.4, 0.1, 1

            MDBottomNavigationItem:
                name: 'screen_dash'
                text: 'Beranda'
                icon: 'home'
                on_tab_press: app.load_dashboard_data()

                MDBoxLayout:
                    orientation: 'vertical'
                    padding: "16dp"
                    spacing: "16dp"
                    md_bg_color: 0.95, 0.97, 0.95, 1

                    MDCard:
                        size_hint: 1, None
                        height: "140dp"
                        padding: "16dp"
                        radius: 20
                        md_bg_color: 0.1, 0.4, 0.1, 1
                        orientation: 'vertical'
                        MDLabel:
                            text: "ESTIMASI LABA BERSIH"
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: 1, 1, 1, 0.7
                        MDLabel:
                            id: laba_label
                            text: "Rp 0"
                            halign: "center"
                            font_style: "H4"
                            theme_text_color: "Custom"
                            text_color: 1, 1, 1, 1

                    MDGridLayout:
                        cols: 2
                        spacing: "12dp"
                        size_hint_y: None
                        height: "100dp"

                        MDCard:
                            padding: "10dp"
                            radius: 15
                            orientation: 'vertical'
                            MDLabel:
                                text: "Total Masuk"
                                font_style: "Caption"
                                halign: "center"
                            MDLabel:
                                id: total_in_label
                                text: "Rp 0"
                                halign: "center"
                                color: 0.1, 0.5, 0.1, 1
                                bold: True

                        MDCard:
                            padding: "10dp"
                            radius: 15
                            orientation: 'vertical'
                            MDLabel:
                                text: "Total Keluar"
                                font_style: "Caption"
                                halign: "center"
                            MDLabel:
                                id: total_out_label
                                text: "Rp 0"
                                halign: "center"
                                color: 0.8, 0.2, 0.2, 1
                                bold: True

                    MDLabel:
                        text: "Input Cepat"
                        font_style: "Subtitle1"
                        size_hint_y: None
                        height: "40dp"

                    MDGridLayout:
                        cols: 3
                        spacing: "10dp"
                        size_hint_y: None
                        height: "80dp"
                        MDIconButton:
                            icon: "cow"
                            user_font_size: "40sp"
                            md_bg_color: 0.8, 0.9, 0.8, 1
                            on_release: app.open_quick_dialog("Pemasukan", "Jual Sapi")
                        MDIconButton:
                            icon: "food-apple"
                            user_font_size: "40sp"
                            md_bg_color: 0.9, 0.8, 0.8, 1
                            on_release: app.open_quick_dialog("Pengeluaran", "Beli Pakan")
                        MDIconButton:
                            icon: "medical-bag"
                            user_font_size: "40sp"
                            md_bg_color: 0.8, 0.8, 0.9, 1
                            on_release: app.open_quick_dialog("Pengeluaran", "Kesehatan")
                    Widget:

            MDBottomNavigationItem:
                name: 'screen_data'
                text: 'Data'
                icon: 'table-large'
                on_tab_press: app.load_table_data()

                MDFloatLayout:
                    md_bg_color: 0.95, 0.97, 0.95, 1

                    MDBoxLayout:
                        orientation: 'vertical'
                        padding: ["10dp", "60dp", "10dp", "10dp"]
                        ScrollView:
                            MDList:
                                id: table_data_list

                    MDLabel:
                        text: "PENGELOLAAN DATA INPUTAN"
                        bold: True
                        halign: "center"
                        pos_hint: {"top": 0.98}
                        size_hint_y: None
                        height: "50dp"

                    MDFloatingActionButton:
                        icon: "plus"
                        md_bg_color: 0.1, 0.4, 0.1, 1
                        pos_hint: {"center_x": .85, "center_y": .12}
                        on_release: app.open_add_dialog()

            MDBottomNavigationItem:
                name: 'screen_history'
                text: 'Riwayat'
                icon: 'history'
                on_tab_press: app.load_history_log()

                MDBoxLayout:
                    orientation: 'vertical'
                    padding: "10dp"
                    MDLabel:
                        text: "JURNAL AKTIVITAS"
                        font_style: "Caption"
                        halign: "center"
                    ScrollView:
                        MDList:
                            id: history_log_list

            MDBottomNavigationItem:
                name: 'screen_report'
                text: 'Laporan'
                icon: 'file-pdf-box'

                MDBoxLayout:
                    orientation: 'vertical'
                    padding: "40dp"
                    spacing: "20dp"
                    md_bg_color: 0.95, 0.97, 0.95, 1
                    MDIcon:
                        icon: "file-document-edit"
                        halign: "center"
                        font_size: "80sp"
                    MDRaisedButton:
                        text: "CETAK LAPORAN PDF"
                        pos_hint: {"center_x": .5}
                        md_bg_color: 0.1, 0.4, 0.1, 1
                        on_release: app.create_pdf_report()
'''


class DataItem(ThreeLineAvatarIconListItem):
    db_id = NumericProperty()
    kategori = StringProperty()
    jumlah = StringProperty()


class HistoryItem(ThreeLineAvatarIconListItem):
    jenis = StringProperty()
    kategori = StringProperty()
    tanggal = StringProperty()
    jumlah = StringProperty()


class LoginScreen(MDScreen):
    pass


class MainScreen(MDScreen):
    pass


class SiakTernakApp(MDApp):
    dialog = None
    current_user = StringProperty("")

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"
        init_db()

        # Buat ScreenManager
        self.sm = MDScreenManager()

        # Load KV dan tambahkan screens
        Builder.load_string(KV)

        # Buat instance screens
        login_screen = LoginScreen(name='login')
        main_screen = MainScreen(name='main')

        # Tambahkan ke ScreenManager
        self.sm.add_widget(login_screen)
        self.sm.add_widget(main_screen)

        # Set screen awal ke login
        self.sm.current = 'login'

        return self.sm

    def verify_login(self):
        login_screen = self.sm.get_screen('login')
        username = login_screen.ids.username_input.text
        password = login_screen.ids.password_input.text
        error_label = login_screen.ids.error_label

        if not username or not password:
            error_label.text = "Username dan password harus diisi!"
            return

        # Hash password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Verify credentials
        conn = sqlite3.connect('siakternak.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?",
                  (username, hashed_password))
        user = c.fetchone()
        conn.close()

        if user:
            self.current_user = user[3] if user[3] else username  # nama_lengkap
            error_label.text = ""
            self.sm.current = 'main'
            self.load_dashboard_data()
        else:
            error_label.text = "Username atau password salah!"

    def logout(self):
        # Clear inputs dan kembali ke login
        login_screen = self.sm.get_screen('login')
        login_screen.ids.username_input.text = ""
        login_screen.ids.password_input.text = ""
        login_screen.ids.error_label.text = ""
        self.sm.current = 'login'

    def load_dashboard_data(self):
        conn = sqlite3.connect('siakternak.db')
        c = conn.cursor()
        c.execute("SELECT SUM(jumlah) FROM transaksi WHERE jenis='Pemasukan'")
        in_val = c.fetchone()[0] or 0
        c.execute("SELECT SUM(jumlah) FROM transaksi WHERE jenis='Pengeluaran'")
        out_val = c.fetchone()[0] or 0
        conn.close()

        main_screen = self.sm.get_screen('main')
        main_screen.ids.total_in_label.text = f"Rp {in_val:,}"
        main_screen.ids.total_out_label.text = f"Rp {out_val:,}"
        main_screen.ids.laba_label.text = f"Rp {in_val - out_val:,}"

    def load_table_data(self):
        container = self.sm.get_screen('main').ids.table_data_list
        container.clear_widgets()
        conn = sqlite3.connect('siakternak.db')
        c = conn.cursor()
        c.execute("SELECT id, kategori, jumlah FROM transaksi ORDER BY id DESC")
        rows = c.fetchall()
        conn.close()

        for row in rows:
            item = DataItem(
                db_id=row[0],
                kategori=str(row[1]),
                jumlah=f"Rp {row[2]:,}"
            )
            item.bind(on_release=lambda x: self.open_edit_dialog(x))
            container.add_widget(item)

    def load_history_log(self):
        container = self.sm.get_screen('main').ids.history_log_list
        container.clear_widgets()
        conn = sqlite3.connect('siakternak.db')
        c = conn.cursor()
        c.execute("SELECT jenis, kategori, jumlah, tanggal FROM transaksi ORDER BY id DESC")
        rows = c.fetchall()
        conn.close()

        for row in rows:
            container.add_widget(HistoryItem(
                jenis=str(row[0]),
                kategori=str(row[1]),
                jumlah=f"Rp {row[2]:,}",
                tanggal=str(row[3])
            ))

    def open_edit_dialog(self, item):
        self.temp_id = item.db_id
        self.edit_kat = MDTextField(text=item.kategori, hint_text="Ubah Nama Data")
        self.edit_jml = MDTextField(text=item.jumlah.replace("Rp ", "").replace(",", ""), input_filter="int")

        self.dialog = MDDialog(
            title="Update Data Inputan",
            type="custom",
            content_cls=BoxLayout(orientation="vertical", size_hint_y=None, height="120dp"),
            buttons=[
                MDFlatButton(text="BATAL", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(text="SIMPAN", on_release=self.update_data)
            ],
        )
        self.dialog.content_cls.add_widget(self.edit_kat)
        self.dialog.content_cls.add_widget(self.edit_jml)
        self.dialog.open()

    def update_data(self, *args):
        conn = sqlite3.connect('siakternak.db')
        c = conn.cursor()
        c.execute("UPDATE transaksi SET kategori=?, jumlah=? WHERE id=?",
                  (self.edit_kat.text, int(self.edit_jml.text), self.temp_id))
        conn.commit()
        conn.close()
        self.dialog.dismiss()
        self.load_table_data()
        self.load_dashboard_data()

    def confirm_delete(self, db_id, kat):
        self.temp_id = db_id
        self.dialog = MDDialog(
            title="Hapus permanen?",
            text=f"Data '{kat}' akan dihapus dari tabel.",
            buttons=[
                MDFlatButton(text="BATAL", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(text="HAPUS", md_bg_color=(0.8, 0.2, 0.2, 1), on_release=self.delete_data)
            ],
        )
        self.dialog.open()

    def delete_data(self, *args):
        conn = sqlite3.connect('siakternak.db')
        c = conn.cursor()
        c.execute("DELETE FROM transaksi WHERE id=?", (self.temp_id,))
        conn.commit()
        conn.close()
        self.dialog.dismiss()
        self.load_table_data()
        self.load_dashboard_data()

    def open_add_dialog(self):
        self.add_jenis = MDTextField(hint_text="Pemasukan / Pengeluaran")
        self.add_kat = MDTextField(hint_text="Kategori (Sapi, Susu, dll)")
        self.add_jml = MDTextField(hint_text="Nominal Rp", input_filter="int")

        self.dialog = MDDialog(
            title="Input Data Baru",
            type="custom",
            content_cls=BoxLayout(orientation="vertical", size_hint_y=None, height="180dp"),
            buttons=[
                MDFlatButton(text="BATAL", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(text="INPUT KE TABEL", on_release=self.save_new_data)
            ],
        )
        self.dialog.content_cls.add_widget(self.add_jenis)
        self.dialog.content_cls.add_widget(self.add_kat)
        self.dialog.content_cls.add_widget(self.add_jml)
        self.dialog.open()

    def save_new_data(self, *args):
        if self.add_jenis.text and self.add_jml.text:
            self.execute_save(self.add_jenis.text.capitalize(), self.add_kat.text, self.add_jml.text)
            self.dialog.dismiss()
            self.load_table_data()
            self.load_dashboard_data()

    def open_quick_dialog(self, jenis, kat):
        self.temp_jenis = jenis
        self.temp_kat = kat
        self.quick_input = MDTextField(hint_text="Masukkan Nominal Rp", input_filter="int")
        self.dialog = MDDialog(
            title=f"Catat {kat}",
            type="custom",
            content_cls=BoxLayout(orientation="vertical", size_hint_y=None, height="60dp"),
            buttons=[
                MDFlatButton(text="BATAL", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(text="SIMPAN", on_release=self.save_quick_data)
            ],
        )
        self.dialog.content_cls.add_widget(self.quick_input)
        self.dialog.open()

    def save_quick_data(self, *args):
        if self.quick_input.text:
            self.execute_save(self.temp_jenis, self.temp_kat, self.quick_input.text)
            self.dialog.dismiss()
            self.load_dashboard_data()

    def execute_save(self, jenis, kat, jml):
        conn = sqlite3.connect('siakternak.db')
        c = conn.cursor()
        tgl = datetime.now().strftime("%d/%m/%Y %H:%M")
        c.execute("INSERT INTO transaksi (jenis, kategori, jumlah, tanggal) VALUES (?,?,?,?)",
                  (jenis, kat, int(jml), tgl))
        conn.commit()
        conn.close()

    def create_pdf_report(self):
        conn = sqlite3.connect('siakternak.db')
        c = conn.cursor()
        c.execute("SELECT * FROM transaksi")
        rows = c.fetchall()
        conn.close()
        if not rows:
            MDDialog(title="Info", text="Tidak ada data untuk dicetak.").open()
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(190, 10, "LAPORAN MANAJEMEN SIAKTERNAK", 0, 1, 'C')
        pdf.set_font("Arial", "", 10)
        pdf.cell(190, 8, f"Dicetak oleh: {self.current_user} | {datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 1, 'C')
        pdf.ln(10)
        for r in rows:
            pdf.set_font("Arial", "", 10)
            pdf.cell(190, 8, f"{r[4]} | {r[1]} | {r[2]} | Rp {r[3]:,}", 1, 1)

        filename = "Laporan_Siakternak_Pro.pdf"
        pdf.output(filename)
        MDDialog(
            title="Sukses",
            text=f"Laporan berhasil dicetak!\nFile: {filename}\n\nOleh: {self.current_user}"
        ).open()


if __name__ == '__main__':
    SiakTernakApp().run()