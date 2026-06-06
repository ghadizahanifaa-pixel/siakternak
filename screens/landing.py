from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.fitimage import FitImage  # Ensure FitImage is registered
import database
import os

KV_LANDING = '''
<LandingScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.95, 0.98, 0.95, 1

        MDTopAppBar:
            title: "SIAKTERNAK HUB & BRANDING"
            md_bg_color: 0.12, 0.45, 0.12, 1
            elevation: 4
            right_action_items: [["cow", lambda x: root.switch_to_order_form()], ["login", lambda x: root.switch_to_login()]]

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                adaptive_height: True
                padding: "16dp"
                spacing: "16dp"

                # Welcome Banner Card
                MDCard:
                    size_hint_y: None
                    height: "130dp"
                    padding: "16dp"
                    radius: 20
                    md_bg_color: 0.12, 0.45, 0.12, 1
                    orientation: 'vertical'
                    elevation: 2
                    
                    MDLabel:
                        text: "SIAKTERNAK BRANDING HUB"
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 0.8
                        bold: True
                        font_style: "Subtitle2"
                    MDLabel:
                        text: "Temukan Sapi Pedaging Terbaik"
                        halign: "center"
                        font_style: "H5"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1
                        bold: True
                    MDLabel:
                        text: "Sapi sehat, terawat, & siap kirim dari peternakan modern."
                        halign: "center"
                        font_style: "Caption"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 0.8

                MDLabel:
                    text: "SAPI UNGGULAN KAMI"
                    bold: True
                    font_style: "Subtitle1"
                    theme_text_color: "Custom"
                    text_color: 0.12, 0.45, 0.12, 1
                    size_hint_y: None
                    height: "30dp"

                # 1. Brahman Card
                MDCard:
                    size_hint_y: None
                    height: "330dp"
                    radius: 16
                    orientation: 'vertical'
                    elevation: 1
                    md_bg_color: 1, 1, 1, 1

                    FitImage:
                        source: "screens/gambar/sapi brahman.jpeg"
                        size_hint_y: None
                        height: "140dp"
                        radius: [16, 16, 0, 0]

                    MDBoxLayout:
                        orientation: 'vertical'
                        padding: "12dp"
                        spacing: "6dp"

                        MDLabel:
                            text: "Sapi Brahman"
                            bold: True
                            font_style: "Subtitle1"
                        MDLabel:
                            text: "Detail Sapi (Template):"
                            bold: True
                            font_style: "Caption"
                            theme_text_color: "Secondary"
                        MDLabel:
                            text: "• Estimasi Bobot: 600 - 850 Kg\\n• Umur: 2 - 3 Tahun\\n• Kondisi: Sehat, Bebas Penyakit Mulut & Kuku\\n• Khas: Punuk besar, adaptasi tropis tinggi, daging tebal."
                            font_style: "Caption"
                            theme_text_color: "Secondary"
                        
                        MDRaisedButton:
                            text: "PESAN SAPI BRAHMAN"
                            size_hint_x: 1
                            md_bg_color: 0.12, 0.45, 0.12, 1
                            on_release: root.switch_to_order_form("Brahman")

                # 2. Simental Card
                MDCard:
                    size_hint_y: None
                    height: "330dp"
                    radius: 16
                    orientation: 'vertical'
                    elevation: 1
                    md_bg_color: 1, 1, 1, 1

                    FitImage:
                        source: "screens/gambar/sapi simental.jpeg"
                        size_hint_y: None
                        height: "140dp"
                        radius: [16, 16, 0, 0]

                    MDBoxLayout:
                        orientation: 'vertical'
                        padding: "12dp"
                        spacing: "6dp"

                        MDLabel:
                            text: "Sapi Simental"
                            bold: True
                            font_style: "Subtitle1"
                        MDLabel:
                            text: "Detail Sapi (Template):"
                            bold: True
                            font_style: "Caption"
                            theme_text_color: "Secondary"
                        MDLabel:
                            text: "• Estimasi Bobot: 650 - 900 Kg\\n• Umur: 2 - 3 Tahun\\n• Kondisi: Sehat, Bebas Penyakit Mulut & Kuku\\n• Khas: Pertumbuhan cepat, postur tinggi besar, karkas tinggi."
                            font_style: "Caption"
                            theme_text_color: "Secondary"
                        
                        MDRaisedButton:
                            text: "PESAN SAPI SIMENTAL"
                            size_hint_x: 1
                            md_bg_color: 0.12, 0.45, 0.12, 1
                            on_release: root.switch_to_order_form("Simental")

                # 3. Limosin Card
                MDCard:
                    size_hint_y: None
                    height: "330dp"
                    radius: 16
                    orientation: 'vertical'
                    elevation: 1
                    md_bg_color: 1, 1, 1, 1

                    FitImage:
                        source: "screens/gambar/sapi limosin .jpeg"
                        size_hint_y: None
                        height: "140dp"
                        radius: [16, 16, 0, 0]

                    MDBoxLayout:
                        orientation: 'vertical'
                        padding: "12dp"
                        spacing: "6dp"

                        MDLabel:
                            text: "Sapi Limosin"
                            bold: True
                            font_style: "Subtitle1"
                        MDLabel:
                            text: "Detail Sapi (Template):"
                            bold: True
                            font_style: "Caption"
                            theme_text_color: "Secondary"
                        MDLabel:
                            text: "• Estimasi Bobot: 700 - 950 Kg\\n• Umur: 2 - 3 Tahun\\n• Kondisi: Sehat, Bebas Penyakit Mulut & Kuku\\n• Khas: Serat daging empuk, tulang tipis, persentase daging tinggi."
                            font_style: "Caption"
                            theme_text_color: "Secondary"
                        
                        MDRaisedButton:
                            text: "PESAN SAPI LIMOSIN"
                            size_hint_x: 1
                            md_bg_color: 0.12, 0.45, 0.12, 1
                            on_release: root.switch_to_order_form("Limosin")

                # 4. Ongole Card
                MDCard:
                    size_hint_y: None
                    height: "330dp"
                    radius: 16
                    orientation: 'vertical'
                    elevation: 1
                    md_bg_color: 1, 1, 1, 1

                    FitImage:
                        source: "screens/gambar/sapi peternakan ongole.jpeg"
                        size_hint_y: None
                        height: "140dp"
                        radius: [16, 16, 0, 0]

                    MDBoxLayout:
                        orientation: 'vertical'
                        padding: "12dp"
                        spacing: "6dp"

                        MDLabel:
                            text: "Sapi Ongole"
                            bold: True
                            font_style: "Subtitle1"
                        MDLabel:
                            text: "Detail Sapi (Template):"
                            bold: True
                            font_style: "Caption"
                            theme_text_color: "Secondary"
                        MDLabel:
                            text: "• Estimasi Bobot: 500 - 750 Kg\\n• Umur: 2 - 3 Tahun\\n• Kondisi: Sehat, Bebas Penyakit Mulut & Kuku\\n• Khas: Punuk besar menonjol, tangguh bekerja, tahan pakan kasar."
                            font_style: "Caption"
                            theme_text_color: "Secondary"
                        
                        MDRaisedButton:
                            text: "PESAN SAPI ONGOLE"
                            size_hint_x: 1
                            md_bg_color: 0.12, 0.45, 0.12, 1
                            on_release: root.switch_to_order_form("Ongole")

<OrderFormScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.95, 0.98, 0.95, 1

        MDTopAppBar:
            title: "FORM PEMESANAN SAPI"
            md_bg_color: 0.12, 0.45, 0.12, 1
            elevation: 4
            left_action_items: [["arrow-left", lambda x: root.back_to_landing()]]

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                adaptive_height: True
                padding: "20dp"
                spacing: "16dp"

                MDCard:
                    size_hint_y: None
                    height: "470dp"
                    padding: "20dp"
                    radius: 15
                    elevation: 1
                    orientation: 'vertical'
                    spacing: "12dp"
                    md_bg_color: 1, 1, 1, 1

                    MDLabel:
                        text: "Formulir Pemesanan Sapi"
                        bold: True
                        font_style: "Subtitle1"
                        theme_text_color: "Custom"
                        text_color: 0.12, 0.45, 0.12, 1

                    MDLabel:
                        id: lbl_stock_sapi
                        text: "Stok Sapi Tersedia: Loading..."
                        bold: True
                        font_style: "Caption"
                        theme_text_color: "Custom"
                        text_color: 0.12, 0.5, 0.12, 1

                    MDTextField:
                        id: txt_nama
                        hint_text: "Nama Lengkap"
                        mode: "rectangle"
                        line_color_focus: 0.12, 0.45, 0.12, 1

                    MDTextField:
                        id: txt_wa
                        hint_text: "No. WhatsApp Aktif"
                        input_filter: "int"
                        mode: "rectangle"
                        line_color_focus: 0.12, 0.45, 0.12, 1

                    MDBoxLayout:
                        size_hint_y: None
                        height: "50dp"
                        orientation: 'horizontal'
                        spacing: "10dp"

                        MDLabel:
                            text: "Jenis Sapi:"
                            bold: True
                            size_hint_x: 0.3
                            pos_hint: {"center_y": 0.5}

                        MDRaisedButton:
                            id: btn_jenis_sapi
                            text: "Pilih Jenis Sapi"
                            size_hint_x: 0.7
                            md_bg_color: 0.12, 0.45, 0.12, 1
                            on_release: root.open_jenis_menu()

                    MDTextField:
                        id: txt_jumlah
                        hint_text: "Jumlah Sapi (Ekor)"
                        input_filter: "int"
                        mode: "rectangle"
                        line_color_focus: 0.12, 0.45, 0.12, 1

                    MDTextField:
                        id: txt_keterangan
                        hint_text: "Keterangan / Catatan Tambahan"
                        mode: "rectangle"
                        multiline: True
                        size_hint_y: None
                        height: "80dp"
                        line_color_focus: 0.12, 0.45, 0.12, 1

                    MDRaisedButton:
                        text: "KIRIM PESANAN SAPI"
                        size_hint_x: 1
                        md_bg_color: 0.12, 0.45, 0.12, 1
                        on_release: root.submit_order()

<OrderSuccessScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.95, 0.98, 0.95, 1

        MDTopAppBar:
            title: "PESANAN BERHASIL"
            md_bg_color: 0.12, 0.45, 0.12, 1
            elevation: 4
            left_action_items: [["arrow-left", lambda x: root.back_to_landing()]]

        MDBoxLayout:
            orientation: 'vertical'
            padding: "30dp"
            spacing: "20dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            size_hint_y: None
            height: "450dp"

            MDIcon:
                icon: "check-circle"
                halign: "center"
                font_size: "100sp"
                theme_text_color: "Custom"
                text_color: 0.12, 0.5, 0.12, 1

            MDLabel:
                text: "Pemesanan Sapi Berhasil!"
                halign: "center"
                bold: True
                font_style: "H5"
                theme_text_color: "Custom"
                text_color: 0.12, 0.45, 0.12, 1

            MDLabel:
                text: "Terima kasih atas pesanan Anda. Pesanan Anda telah masuk ke sistem kami dengan status Pending. Silakan hubungi admin di WhatsApp untuk konfirmasi dan proses pembayaran."
                halign: "center"
                font_style: "Body2"
                theme_text_color: "Secondary"

            MDRaisedButton:
                text: "HUBUNGI ADMIN VIA WHATSAPP"
                size_hint_x: 0.85
                pos_hint: {"center_x": 0.5}
                md_bg_color: 0.12, 0.5, 0.12, 1
                icon: "whatsapp"
                on_release: root.open_whatsapp()

            MDFlatButton:
                text: "KEMBALI KE BERANDA UTAMA"
                size_hint_x: 0.85
                pos_hint: {"center_x": 0.5}
                theme_text_color: "Custom"
                text_color: 0.12, 0.45, 0.12, 1
                on_release: root.back_to_landing()
'''

Builder.load_string(KV_LANDING)

class LandingScreen(MDScreen):
    def switch_to_login(self):
        self.manager.transition.direction = "left"
        self.manager.current = "login"

    def switch_to_order_form(self, breed=""):
        order_screen = self.manager.get_screen("order_form")
        if breed:
            order_screen.set_preselected_breed(breed)
        self.manager.transition.direction = "left"
        self.manager.current = "order_form"


class OrderFormScreen(MDScreen):
    jenis_menu = None
    selected_jenis = "Brahman"
    current_stock = 0

    def on_enter(self):
        self.load_stock_info()
        self.ids.txt_nama.text = ""
        self.ids.txt_wa.text = ""
        self.ids.txt_jumlah.text = ""
        self.ids.txt_keterangan.text = ""

    def load_stock_info(self):
        summary = database.get_inventory_summary()
        self.current_stock = summary.get('sapi', 0)
        self.ids.lbl_stock_sapi.text = f"Stok Sapi Tersedia: {self.current_stock} ekor"

    def set_preselected_breed(self, breed):
        self.selected_jenis = breed
        self.ids.btn_jenis_sapi.text = breed

    def open_jenis_menu(self):
        breeds = ["Brahman", "Simental", "Limosin", "Ongole"]
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": b,
                "on_release": lambda x=b: self.set_jenis(x),
            } for b in breeds
        ]
        self.jenis_menu = MDDropdownMenu(
            caller=self.ids.btn_jenis_sapi,
            items=menu_items,
            width=dp(180),
        )
        self.jenis_menu.open()

    def set_jenis(self, breed):
        self.selected_jenis = breed
        self.ids.btn_jenis_sapi.text = breed
        if self.jenis_menu:
            self.jenis_menu.dismiss()

    def back_to_landing(self):
        self.manager.transition.direction = "right"
        self.manager.current = "landing"

    def submit_order(self):
        nama = self.ids.txt_nama.text.strip()
        wa = self.ids.txt_wa.text.strip()
        jumlah = self.ids.txt_jumlah.text.strip()
        keterangan = self.ids.txt_keterangan.text.strip()

        if not nama or not wa or not jumlah:
            self.show_dialog("Error", "Mohon isi Nama, No WA, dan Jumlah Sapi!")
            return

        try:
            qty = int(jumlah)
            if qty <= 0:
                self.show_dialog("Error", "Jumlah sapi harus lebih dari 0!")
                return
        except ValueError:
            self.show_dialog("Error", "Jumlah sapi harus berupa angka!")
            return

        if qty > self.current_stock:
            self.show_dialog("Stok Kurang", f"Maaf, stok sapi saat ini hanya tersedia {self.current_stock} ekor.")
            return

        # Add to database
        database.add_pesanan(nama, wa, self.selected_jenis, qty, keterangan)
        
        # Switch to success screen
        self.manager.transition.direction = "left"
        self.manager.current = "order_success"

    def show_dialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    md_bg_color=(0.12, 0.45, 0.12, 1),
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()


class OrderSuccessScreen(MDScreen):
    def back_to_landing(self):
        self.manager.transition.direction = "right"
        self.manager.current = "landing"

    def open_whatsapp(self):
        # Admin number: 081228764532
        import webbrowser
        phone = "6281228764532"  # convert to international format
        message = "Halo Admin SIAKTERNAK, saya ingin mengkonfirmasi pemesanan sapi saya."
        url = f"https://wa.me/{phone}?text={message.replace(' ', '%20')}"
        webbrowser.open(url)
