from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.menu import MDDropdownMenu
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
                id: table_container
                orientation: 'vertical'
                size_hint_y: 0.75
                radius: 12
                md_bg_color: 1, 1, 1, 1
                padding: "4dp"
                
            MDCard:
                size_hint_y: 0.25
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
            
        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                adaptive_height: True
                padding: "20dp"
                spacing: "16dp"
                
                MDCard:
                    size_hint_y: None
                    height: "380dp"
                    padding: "20dp"
                    radius: 15
                    elevation: 2
                    orientation: 'vertical'
                    spacing: "12dp"
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
                            text: "LABA BERSIH:"
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
    def on_enter(self):
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


class JurnalUmumScreen(MDScreen):
    def on_enter(self):
        container = self.ids.table_container
        container.clear_widgets()
        column_data = [
            ("Tanggal", dp(22)),
            ("Kode", dp(13)),
            ("Nama Rekening / Akun", dp(33)),
            ("Debit", dp(16)),
            ("Kredit", dp(16))
        ]
        rows = database.get_jurnal_umum()
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
        rows = database.get_buku_besar(self.selected_code)
        
        table = MDDataTable(
            use_pagination=True,
            rows_num=8,
            column_data=column_data,
            row_data=rows,
            elevation=0
        )
        container.add_widget(table)


class NeracaSaldoScreen(MDScreen):
    def on_enter(self):
        container = self.ids.table_container
        container.clear_widgets()
        
        column_data = [
            ("Kode", dp(15)),
            ("Nama Akun", dp(45)),
            ("Debit", dp(20)),
            ("Kredit", dp(20))
        ]
        rows, total_debit, total_kredit = database.get_neraca_saldo()
        
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
    def on_enter(self):
        data = database.get_laba_rugi()
        self.ids.lbl_pendapatan.text = f"Rp {data['pendapatan']:,}"
        self.ids.lbl_beban_pakan.text = f"Rp {data['beban_pakan']:,}"
        self.ids.lbl_beban_kesehatan.text = f"Rp {data['beban_kesehatan']:,}"
        self.ids.lbl_beban_lain.text = f"Rp {data['beban_lain']:,}"
        self.ids.lbl_total_beban.text = f"Rp {data['total_beban']:,}"
        
        laba = data['laba_bersih']
        self.ids.lbl_laba_bersih.text = f"Rp {laba:,}"
        if laba >= 0:
            self.ids.lbl_laba_bersih.text_color = (0.12, 0.5, 0.12, 1)
        else:
            self.ids.lbl_laba_bersih.text_color = (0.8, 0.2, 0.2, 1)
