from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField
import database

KV_VIEWS = '''
<DaftarAkunScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.95, 0.98, 0.95, 1
        
        MDTopAppBar:
            title: "DAFTAR AKUN (COA)"
            md_bg_color: 0.12, 0.45, 0.12, 1
            elevation: 4
            left_action_items: [["arrow-left", lambda x: app.back_to_main()]]
            
        MDBoxLayout:
            size_hint_y: None
            height: "50dp"
            padding: ["16dp", "8dp", "16dp", "8dp"]
            spacing: "10dp"
            MDRaisedButton:
                text: "Tambah Akun"
                md_bg_color: 0.12, 0.45, 0.12, 1
                on_release: root.open_add_account_dialog()
            MDRaisedButton:
                text: "Segarkan"
                md_bg_color: 0.12, 0.45, 0.12, 1
                on_release: root.on_enter()

        MDBoxLayout:
            id: table_container
            orientation: 'vertical'
            padding: "16dp"
            radius: 12
            md_bg_color: 1, 1, 1, 1

<JurnalUmumScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.95, 0.98, 0.95, 1
        
        MDTopAppBar:
            title: "JURNAL UMUM"
            md_bg_color: 0.12, 0.45, 0.12, 1
            elevation: 4
            left_action_items: [["arrow-left", lambda x: app.back_to_main()]]
            
        MDBoxLayout:
            size_hint_y: None
            height: "50dp"
            orientation: 'horizontal'
            padding: ["16dp", "4dp", "16dp", "4dp"]
            spacing: "10dp"
            
            MDRaisedButton:
                id: btn_month
                text: "Semua Bulan"
                size_hint_x: 0.5
                md_bg_color: 0.12, 0.45, 0.12, 1
                on_release: root.open_month_menu()
                
            MDRaisedButton:
                id: btn_year
                text: "Semua Tahun"
                size_hint_x: 0.5
                md_bg_color: 0.12, 0.45, 0.12, 1
                on_release: root.open_year_menu()
                
        MDBoxLayout:
            id: table_container
            orientation: 'vertical'
            padding: "16dp"
            radius: 12
            md_bg_color: 1, 1, 1, 1

<BukuBesarScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.95, 0.98, 0.95, 1
        
        MDTopAppBar:
            title: "BUKU BESAR"
            md_bg_color: 0.12, 0.45, 0.12, 1
            elevation: 4
            left_action_items: [["arrow-left", lambda x: app.back_to_main()]]
            
        MDBoxLayout:
            orientation: 'vertical'
            padding: "16dp"
            spacing: "12dp"
            
            MDBoxLayout:
                size_hint_y: None
                height: "50dp"
                orientation: 'horizontal'
                spacing: "10dp"
                
                MDLabel:
                    text: "Pilih Akun:"
                    bold: True
                    size_hint_x: 0.3
                    pos_hint: {"center_y": 0.5}
                    
                MDRaisedButton:
                    id: btn_select_account
                    text: "101 - Kas & Bank"
                    size_hint_x: 0.7
                    md_bg_color: 0.12, 0.45, 0.12, 1
                    on_release: root.open_account_menu()
                    
            MDBoxLayout:
                size_hint_y: None
                height: "50dp"
                orientation: 'horizontal'
                spacing: "10dp"
                
                MDRaisedButton:
                    id: btn_month
                    text: "Semua Bulan"
                    size_hint_x: 0.5
                    md_bg_color: 0.12, 0.45, 0.12, 1
                    on_release: root.open_month_menu()
                    
                MDRaisedButton:
                    id: btn_year
                    text: "Semua Tahun"
                    size_hint_x: 0.5
                    md_bg_color: 0.12, 0.45, 0.12, 1
                    on_release: root.open_year_menu()
                    
            MDBoxLayout:
                id: table_container
                orientation: 'vertical'
                radius: 12
                md_bg_color: 1, 1, 1, 1
                padding: "4dp"

<NeracaSaldoScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.95, 0.98, 0.95, 1
        
        MDTopAppBar:
            title: "NERACA SALDO"
            md_bg_color: 0.12, 0.45, 0.12, 1
            elevation: 4
            left_action_items: [["arrow-left", lambda x: app.back_to_main()]]
            
        MDBoxLayout:
            orientation: 'vertical'
            padding: "16dp"
            spacing: "12dp"
            
            MDBoxLayout:
                size_hint_y: None
                height: "50dp"
                orientation: 'horizontal'
                spacing: "10dp"
                
                MDRaisedButton:
                    id: btn_month
                    text: "Semua Bulan"
                    size_hint_x: 0.5
                    md_bg_color: 0.12, 0.45, 0.12, 1
                    on_release: root.open_month_menu()
                    
                MDRaisedButton:
                    id: btn_year
                    text: "Semua Tahun"
                    size_hint_x: 0.5
                    md_bg_color: 0.12, 0.45, 0.12, 1
                    on_release: root.open_year_menu()
                    
            MDBoxLayout:
                id: table_container
                orientation: 'vertical'
                size_hint_y: 0.65
                radius: 12
                md_bg_color: 1, 1, 1, 1
                padding: "4dp"
                
            MDCard:
                size_hint_y: 0.35
                padding: "16dp"
                radius: 12
                md_bg_color: 0.12, 0.45, 0.12, 0.08
                elevation: 0
                orientation: 'vertical'
                spacing: "4dp"
                
                MDBoxLayout:
                    orientation: 'horizontal'
                    MDLabel:
                        text: "TOTAL DEBIT:"
                        bold: True
                    MDLabel:
                        id: lbl_total_debit
                        text: "Rp 0"
                        bold: True
                        halign: "right"
                        theme_text_color: "Custom"
                        text_color: 0.12, 0.5, 0.12, 1
                        
                MDBoxLayout:
                    orientation: 'horizontal'
                    MDLabel:
                        text: "TOTAL KREDIT:"
                        bold: True
                    MDLabel:
                        id: lbl_total_kredit
                        text: "Rp 0"
                        bold: True
                        halign: "right"
                        theme_text_color: "Custom"
                        text_color: 0.12, 0.5, 0.12, 1
                        
                MDLabel:
                    id: lbl_status_balance
                    text: "Status: Balance"
                    bold: True
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: 0.12, 0.45, 0.12, 1
                    font_style: "Caption"

<LabaRugiScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.95, 0.98, 0.95, 1
        
        MDTopAppBar:
            title: "LAPORAN LABA RUGI"
            md_bg_color: 0.12, 0.45, 0.12, 1
            elevation: 4
            left_action_items: [["arrow-left", lambda x: app.back_to_main()]]
            
        MDBoxLayout:
            size_hint_y: None
            height: "50dp"
            orientation: 'horizontal'
            padding: ["20dp", "4dp", "20dp", "4dp"]
            spacing: "10dp"
            
            MDRaisedButton:
                id: btn_month
                text: "Semua Bulan"
                size_hint_x: 0.5
                md_bg_color: 0.12, 0.45, 0.12, 1
                on_release: root.open_month_menu()
                
            MDRaisedButton:
                id: btn_year
                text: "Semua Tahun"
                size_hint_x: 0.5
                md_bg_color: 0.12, 0.45, 0.12, 1
                on_release: root.open_year_menu()
                
        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                adaptive_height: True
                padding: "20dp"
                spacing: "16dp"
                
                MDCard:
                    size_hint_y: None
                    height: "700dp"
                    padding: "20dp"
                    radius: 15
                    elevation: 2
                    orientation: 'vertical'
                    spacing: "8dp"
                    md_bg_color: 1, 1, 1, 1
                    
                    MDLabel:
                        text: "IKHTISAR LABA RUGI"
                        bold: True
                        font_style: "H6"
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: 0.12, 0.45, 0.12, 1
                        
                    MDSeparator:
                    
                    # Revenue
                    MDLabel:
                        text: "PENDAPATAN"
                        bold: True
                        font_style: "Subtitle2"
                        theme_text_color: "Custom"
                        text_color: 0.12, 0.45, 0.12, 1
                        
                    MDBoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: "25dp"
                        MDLabel:
                            text: "  Pendapatan Penjualan Sapi"
                        MDLabel:
                            id: lbl_pendapatan
                            text: "Rp 0"
                            halign: "right"
                            
                    MDSeparator:

                    # Harga Pokok Penjualan (HPP)
                    MDLabel:
                        text: "HARGA POKOK PENJUALAN (HPP)"
                        bold: True
                        font_style: "Subtitle2"
                        theme_text_color: "Custom"
                        text_color: 0.8, 0.4, 0.0, 1
                        
                    MDBoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: "25dp"
                        MDLabel:
                            text: "  Harga Pokok Penjualan Sapi"
                        MDLabel:
                            id: lbl_hpp_sapi
                            text: "Rp 0"
                            halign: "right"

                    MDBoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: "25dp"
                        MDLabel:
                            text: "  Beban Transportasi Pembelian"
                        MDLabel:
                            id: lbl_beban_transport
                            text: "Rp 0"
                            halign: "right"

                    MDBoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: "30dp"
                        MDLabel:
                            text: "TOTAL HPP:"
                            bold: True
                        MDLabel:
                            id: lbl_total_hpp
                            text: "Rp 0"
                            bold: True
                            halign: "right"
                            
                    MDSeparator:

                    # Laba Kotor
                    MDBoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: "30dp"
                        MDLabel:
                            text: "LABA KOTOR:"
                            bold: True
                        MDLabel:
                            id: lbl_laba_kotor
                            text: "Rp 0"
                            bold: True
                            halign: "right"
                            theme_text_color: "Custom"
                            text_color: 0.12, 0.45, 0.12, 1

                    MDSeparator:
                    
                    # Expense
                    MDLabel:
                        text: "BEBAN OPERASIONAL"
                        bold: True
                        font_style: "Subtitle2"
                        theme_text_color: "Custom"
                        text_color: 0.8, 0.2, 0.2, 1
                        
                    MDBoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: "25dp"
                        MDLabel:
                            text: "  Beban Pakan"
                        MDLabel:
                            id: lbl_beban_pakan
                            text: "Rp 0"
                            halign: "right"
                            
                    MDBoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: "25dp"
                        MDLabel:
                            text: "  Beban Kesehatan Ternak"
                        MDLabel:
                            id: lbl_beban_kesehatan
                            text: "Rp 0"
                            halign: "right"

                    MDBoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: "25dp"
                        MDLabel:
                            text: "  Beban Gaji"
                        MDLabel:
                            id: lbl_beban_gaji
                            text: "Rp 0"
                            halign: "right"

                    MDBoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: "25dp"
                        MDLabel:
                            text: "  Beban Listrik & Air Kandang"
                        MDLabel:
                            id: lbl_beban_listrik
                            text: "Rp 0"
                            halign: "right"

                    MDBoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: "25dp"
                        MDLabel:
                            text: "  Beban Penyusutan Kandang & Alat"
                        MDLabel:
                            id: lbl_beban_penyusutan
                            text: "Rp 0"
                            halign: "right"
                            
                    MDBoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: "25dp"
                        MDLabel:
                            text: "  Beban Operasional Lainnya"
                        MDLabel:
                            id: lbl_beban_lain
                            text: "Rp 0"
                            halign: "right"
                            
                    MDBoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: "30dp"
                        MDLabel:
                            text: "TOTAL BEBAN:"
                            bold: True
                        MDLabel:
                            id: lbl_total_beban
                            text: "Rp 0"
                            bold: True
                            halign: "right"
                            
                    MDSeparator:
                    
                    # Net Profit
                    MDBoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: "40dp"
                        MDLabel:
                            text: "LABA RUGI BERSIH:"
                            bold: True
                            font_style: "H6"
                        MDLabel:
                            id: lbl_laba_bersih
                            text: "Rp 0"
                            bold: True
                            font_style: "H6"
                            halign: "right"
                            theme_text_color: "Custom"
                            text_color: 0.12, 0.5, 0.12, 1
'''

Builder.load_string(KV_VIEWS)

class DaftarAkunScreen(MDScreen):
    dialog = None

    def on_enter(self):
        self.load_coa_table()

    def load_coa_table(self):
        container = self.ids.table_container
        container.clear_widgets()
        column_data = [
            ("Kode Akun", dp(20)),
            ("Nama Akun", dp(50)),
            ("Klasifikasi", dp(30))
        ]
        rows = database.get_coa()
        table = MDDataTable(
            use_pagination=True,
            rows_num=8,
            column_data=column_data,
            row_data=rows,
            elevation=0
        )
        container.add_widget(table)

    def open_add_account_dialog(self):
        self.add_code_field = MDTextField(hint_text="Kode Akun", mode="rectangle")
        self.add_name_field = MDTextField(hint_text="Nama Akun", mode="rectangle")
        self.add_classification_field = MDTextField(hint_text="Klasifikasi (Aset, Beban, Pendapatan, HPP)", mode="rectangle")

        content = BoxLayout(orientation='vertical', spacing='12dp', padding='12dp')
        content.add_widget(self.add_code_field)
        content.add_widget(self.add_name_field)
        content.add_widget(self.add_classification_field)

        self.dialog = MDDialog(
            title="Tambah Akun Baru",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="BATAL", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(text="SIMPAN", md_bg_color=(0.12, 0.45, 0.12, 1), on_release=self.save_new_account)
            ]
        )
        self.dialog.open()

    def save_new_account(self, *args):
        code = self.add_code_field.text.strip()
        name = self.add_name_field.text.strip()
        classification = self.add_classification_field.text.strip()

        if not code or not name or not classification:
            self.add_code_field.error = not bool(code)
            self.add_name_field.error = not bool(name)
            self.add_classification_field.error = not bool(classification)
            return

        success = database.add_coa_account(code, name, classification)
        if not success:
            self.add_code_field.error = True
            self.add_code_field.helper_text = "Kode akun sudah ada"
            self.add_code_field.helper_text_mode = "on"
            return

        self.dialog.dismiss()
        self.load_coa_table()


class JurnalUmumScreen(MDScreen):
    selected_month = "Semua"
    selected_year = "Semua"
    month_menu = None
    year_menu = None

    def on_enter(self):
        self.load_journal()

    def open_month_menu(self):
        months = [
            ("Semua", "Semua Bulan"), ("01", "Januari"), ("02", "Februari"), ("03", "Maret"),
            ("04", "April"), ("05", "Mei"), ("06", "Juni"), ("07", "Juli"),
            ("08", "Agustus"), ("09", "September"), ("10", "Oktober"), ("11", "November"),
            ("12", "Desember")
        ]
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": text,
                "on_release": lambda m_val=val, m_text=text: self.set_month(m_val, m_text),
            } for val, text in months
        ]
        self.month_menu = MDDropdownMenu(
            caller=self.ids.btn_month,
            items=menu_items,
            width=dp(180),
        )
        self.month_menu.open()

    def set_month(self, val, text):
        self.selected_month = val
        self.ids.btn_month.text = text
        if self.month_menu:
            self.month_menu.dismiss()
        self.load_journal()

    def open_year_menu(self):
        years = [
            ("Semua", "Semua Tahun"), ("2026", "2026"), ("2027", "2027"),
            ("2028", "2028"), ("2029", "2029")
        ]
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": text,
                "on_release": lambda y_val=val, y_text=text: self.set_year(y_val, y_text),
            } for val, text in years
        ]
        self.year_menu = MDDropdownMenu(
            caller=self.ids.btn_year,
            items=menu_items,
            width=dp(180),
        )
        self.year_menu.open()

    def set_year(self, val, text):
        self.selected_year = val
        self.ids.btn_year.text = text
        if self.year_menu:
            self.year_menu.dismiss()
        self.load_journal()

    def load_journal(self):
        container = self.ids.table_container
        container.clear_widgets()
        column_data = [
            ("Tanggal", dp(22)),
            ("Kode", dp(13)),
            ("Nama Rekening / Akun", dp(33)),
            ("Debit", dp(16)),
            ("Kredit", dp(16))
        ]
        rows = database.get_jurnal_umum(self.selected_month, self.selected_year)
        table = MDDataTable(
            use_pagination=True,
            rows_num=10,
            column_data=column_data,
            row_data=rows,
            elevation=0
        )
        container.add_widget(table)


class BukuBesarScreen(MDScreen):
    menu = None
    selected_code = "101"
    selected_month = "Semua"
    selected_year = "Semua"
    month_menu = None
    year_menu = None

    def on_enter(self):
        self.load_ledger()

    def open_account_menu(self):
        coa = database.get_coa()
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{code} - {name}",
                "on_release": lambda x=f"{code} - {name}", c=code: self.set_account(x, c),
            } for code, name, _ in coa
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.btn_select_account,
            items=menu_items,
            width=dp(240),
        )
        self.menu.open()

    def set_account(self, text_item, code):
        self.ids.btn_select_account.text = text_item
        self.selected_code = code
        if self.menu:
            self.menu.dismiss()
        self.load_ledger()

    def open_month_menu(self):
        months = [
            ("Semua", "Semua Bulan"), ("01", "Januari"), ("02", "Februari"), ("03", "Maret"),
            ("04", "April"), ("05", "Mei"), ("06", "Juni"), ("07", "Juli"),
            ("08", "Agustus"), ("09", "September"), ("10", "Oktober"), ("11", "November"),
            ("12", "Desember")
        ]
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": text,
                "on_release": lambda m_val=val, m_text=text: self.set_month(m_val, m_text),
            } for val, text in months
        ]
        self.month_menu = MDDropdownMenu(
            caller=self.ids.btn_month,
            items=menu_items,
            width=dp(180),
        )
        self.month_menu.open()

    def set_month(self, val, text):
        self.selected_month = val
        self.ids.btn_month.text = text
        if self.month_menu:
            self.month_menu.dismiss()
        self.load_ledger()

    def open_year_menu(self):
        years = [
            ("Semua", "Semua Tahun"), ("2026", "2026"), ("2027", "2027"),
            ("2028", "2028"), ("2029", "2029")
        ]
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": text,
                "on_release": lambda y_val=val, y_text=text: self.set_year(y_val, y_text),
            } for val, text in years
        ]
        self.year_menu = MDDropdownMenu(
            caller=self.ids.btn_year,
            items=menu_items,
            width=dp(180),
        )
        self.year_menu.open()

    def set_year(self, val, text):
        self.selected_year = val
        self.ids.btn_year.text = text
        if self.year_menu:
            self.year_menu.dismiss()
        self.load_ledger()

    def load_ledger(self):
        container = self.ids.table_container
        container.clear_widgets()
        
        column_data = [
            ("Tanggal", dp(22)),
            ("Keterangan", dp(28)),
            ("Debit", dp(17)),
            ("Kredit", dp(17)),
            ("Saldo", dp(18))
        ]
        rows = database.get_buku_besar(self.selected_code, self.selected_month, self.selected_year)
        
        table = MDDataTable(
            use_pagination=True,
            rows_num=8,
            column_data=column_data,
            row_data=rows,
            elevation=0
        )
        container.add_widget(table)


class NeracaSaldoScreen(MDScreen):
    selected_month = "Semua"
    selected_year = "Semua"
    month_menu = None
    year_menu = None

    def on_enter(self):
        self.load_neraca()

    def open_month_menu(self):
        months = [
            ("Semua", "Semua Bulan"), ("01", "Januari"), ("02", "Februari"), ("03", "Maret"),
            ("04", "April"), ("05", "Mei"), ("06", "Juni"), ("07", "Juli"),
            ("08", "Agustus"), ("09", "September"), ("10", "Oktober"), ("11", "November"),
            ("12", "Desember")
        ]
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": text,
                "on_release": lambda m_val=val, m_text=text: self.set_month(m_val, m_text),
            } for val, text in months
        ]
        self.month_menu = MDDropdownMenu(
            caller=self.ids.btn_month,
            items=menu_items,
            width=dp(180),
        )
        self.month_menu.open()

    def set_month(self, val, text):
        self.selected_month = val
        self.ids.btn_month.text = text
        if self.month_menu:
            self.month_menu.dismiss()
        self.load_neraca()

    def open_year_menu(self):
        years = [
            ("Semua", "Semua Tahun"), ("2026", "2026"), ("2027", "2027"),
            ("2028", "2028"), ("2029", "2029")
        ]
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": text,
                "on_release": lambda y_val=val, y_text=text: self.set_year(y_val, y_text),
            } for val, text in years
        ]
        self.year_menu = MDDropdownMenu(
            caller=self.ids.btn_year,
            items=menu_items,
            width=dp(180),
        )
        self.year_menu.open()

    def set_year(self, val, text):
        self.selected_year = val
        self.ids.btn_year.text = text
        if self.year_menu:
            self.year_menu.dismiss()
        self.load_neraca()

    def load_neraca(self):
        container = self.ids.table_container
        container.clear_widgets()
        
        column_data = [
            ("Kode", dp(15)),
            ("Nama Akun", dp(45)),
            ("Debit", dp(20)),
            ("Kredit", dp(20))
        ]
        rows, total_debit, total_kredit = database.get_neraca_saldo(self.selected_month, self.selected_year)
        
        table = MDDataTable(
            use_pagination=False,
            column_data=column_data,
            row_data=rows,
            elevation=0
        )
        container.add_widget(table)
        
        self.ids.lbl_total_debit.text = f"Rp {total_debit:,}"
        self.ids.lbl_total_kredit.text = f"Rp {total_kredit:,}"
        
        if total_debit == total_kredit:
            self.ids.lbl_status_balance.text = "Status: Balance (Debit = Kredit)"
            self.ids.lbl_status_balance.text_color = (0.12, 0.45, 0.12, 1)
        else:
            self.ids.lbl_status_balance.text = "Status: Tidak Balance (Periksa Input)"
            self.ids.lbl_status_balance.text_color = (0.8, 0.2, 0.2, 1)


class LabaRugiScreen(MDScreen):
    selected_month = "Semua"
    selected_year = "Semua"
    month_menu = None
    year_menu = None

    def on_enter(self):
        self.load_laba_rugi()

    def open_month_menu(self):
        months = [
            ("Semua", "Semua Bulan"), ("01", "Januari"), ("02", "Februari"), ("03", "Maret"),
            ("04", "April"), ("05", "Mei"), ("06", "Juni"), ("07", "Juli"),
            ("08", "Agustus"), ("09", "September"), ("10", "Oktober"), ("11", "November"),
            ("12", "Desember")
        ]
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": text,
                "on_release": lambda m_val=val, m_text=text: self.set_month(m_val, m_text),
            } for val, text in months
        ]
        self.month_menu = MDDropdownMenu(
            caller=self.ids.btn_month,
            items=menu_items,
            width=dp(180),
        )
        self.month_menu.open()

    def set_month(self, val, text):
        self.selected_month = val
        self.ids.btn_month.text = text
        if self.month_menu:
            self.month_menu.dismiss()
        self.load_laba_rugi()

    def open_year_menu(self):
        years = [
            ("Semua", "Semua Tahun"), ("2026", "2026"), ("2027", "2027"),
            ("2028", "2028"), ("2029", "2029")
        ]
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": text,
                "on_release": lambda y_val=val, y_text=text: self.set_year(y_val, y_text),
            } for val, text in years
        ]
        self.year_menu = MDDropdownMenu(
            caller=self.ids.btn_year,
            items=menu_items,
            width=dp(180),
        )
        self.year_menu.open()

    def set_year(self, val, text):
        self.selected_year = val
        self.ids.btn_year.text = text
        if self.year_menu:
            self.year_menu.dismiss()
        self.load_laba_rugi()

    def load_laba_rugi(self):
        data = database.get_laba_rugi(self.selected_month, self.selected_year)
        self.ids.lbl_pendapatan.text = f"Rp {data['pendapatan']:,}"
        
        self.ids.lbl_hpp_sapi.text = f"Rp {data['hpp_sapi']:,}"
        self.ids.lbl_beban_transport.text = f"Rp {data['beban_transport']:,}"
        self.ids.lbl_total_hpp.text = f"Rp {data['total_hpp']:,}"
        
        laba_kotor = data['pendapatan'] - data['total_hpp']
        self.ids.lbl_laba_kotor.text = f"Rp {laba_kotor:,}"
        
        self.ids.lbl_beban_pakan.text = f"Rp {data['beban_pakan']:,}"
        self.ids.lbl_beban_kesehatan.text = f"Rp {data['beban_kesehatan']:,}"
        self.ids.lbl_beban_gaji.text = f"Rp {data['beban_gaji']:,}"
        self.ids.lbl_beban_listrik.text = f"Rp {data['beban_listrik']:,}"
        self.ids.lbl_beban_penyusutan.text = f"Rp {data['beban_penyusutan']:,}"
        self.ids.lbl_beban_lain.text = f"Rp {data['beban_lain']:,}"
        self.ids.lbl_total_beban.text = f"Rp {data['total_beban']:,}"
        
        laba = data['laba_bersih']
        self.ids.lbl_laba_bersih.text = f"Rp {laba:,}"
        if laba >= 0:
            self.ids.lbl_laba_bersih.text_color = (0.12, 0.5, 0.12, 1)
        else:
            self.ids.lbl_laba_bersih.text_color = (0.8, 0.2, 0.2, 1)
