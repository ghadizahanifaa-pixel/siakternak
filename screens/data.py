from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem, IconLeftWidget
import database

KV = '''
<DataScreen>:
    MDFloatLayout:
        md_bg_color: 0.95, 0.98, 0.95, 1

        # Main Content Layout (Hidden during loading)
        MDBoxLayout:
            id: main_content
            opacity: 0
            disabled: True
            orientation: 'vertical'
            padding: ["16dp", "16dp", "16dp", "75dp"]
            spacing: "16dp"

            # Header Area
            MDBoxLayout:
                size_hint_y: None
                height: "50dp"
                orientation: 'horizontal'
                
                MDLabel:
                    text: "PENGELOLAAN DATA KEUANGAN"
                    bold: True
                    font_style: "H6"
                    theme_text_color: "Custom"
                    text_color: 0.12, 0.45, 0.12, 1
                    
                MDIconButton:
                    icon: "history"
                    user_font_size: "28sp"
                    theme_text_color: "Custom"
                    text_color: 0.12, 0.5, 0.12, 1
                    tooltip: "Riwayat Transaksi"
                    on_release: root.show_history_popup()
                    
                MDIconButton:
                    icon: "file-excel"
                    user_font_size: "28sp"
                    theme_text_color: "Custom"
                    text_color: 0.12, 0.5, 0.12, 1
                    tooltip: "Export Excel"
                    on_release: root.export_excel()

            # Switch Tab (Segmented Style)
            MDBoxLayout:
                size_hint_y: None
                height: "45dp"
                orientation: 'horizontal'
                spacing: "10dp"
                
                MDRaisedButton:
                    id: btn_tab_pemasukan
                    text: "Pemasukan (Sapi)"
                    size_hint_x: 0.5
                    md_bg_color: 0.12, 0.45, 0.12, 1  # Default active
                    on_release: root.switch_tab("pemasukan")
                    
                MDRaisedButton:
                    id: btn_tab_pengeluaran
                    text: "Pengeluaran (Operasional)"
                    size_hint_x: 0.5
                    md_bg_color: 0.75, 0.82, 0.75, 1  # Default inactive
                    text_color: 0.12, 0.45, 0.12, 1
                    on_release: root.switch_tab("pengeluaran")

            # Table Widget Container
            MDBoxLayout:
                id: table_container
                orientation: 'vertical'
                radius: 12
                padding: "4dp"
                md_bg_color: 1, 1, 1, 1

        # Action Buttons Container (Bottom Right)
        MDFloatingActionButton:
            id: btn_add
            icon: "plus"
            md_bg_color: 0.12, 0.45, 0.12, 1
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            pos_hint: {"right": 0.95, "y": 0.03}
            on_release: root.open_add_dialog()
            opacity: 0
            disabled: True

        # Simulated Javascript/SPA Loading Screen overlay
        MDBoxLayout:
            id: loading_layout
            orientation: 'vertical'
            spacing: "12dp"
            size_hint: (None, None)
            size: ("220dp", "150dp")
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            
            MDSpinner:
                size_hint: (None, None)
                size: ("46dp", "46dp")
                pos_hint: {"center_x": 0.5}
                active: True
                color: 0.12, 0.45, 0.12, 1
                
            MDLabel:
                text: "Memuat Data..."
                halign: "center"
                bold: True
                font_style: "Caption"
                theme_text_color: "Custom"
                text_color: 0.12, 0.45, 0.12, 1
'''

Builder.load_string(KV)

class DataScreen(MDScreen):
    active_tab = "pemasukan"
    table = None
    dialog = None
    current_ids = []  # Maps row index in MDDataTable to SQLite ID

    def on_enter(self):
        self.trigger_loading()

    def switch_tab(self, tab_name):
        if self.active_tab == tab_name:
            return
        
        self.active_tab = tab_name
        
        # Update colors to highlight active tab
        if tab_name == "pemasukan":
            self.ids.btn_tab_pemasukan.md_bg_color = (0.12, 0.45, 0.12, 1)
            self.ids.btn_tab_pemasukan.text_color = (1, 1, 1, 1)
            self.ids.btn_tab_pengeluaran.md_bg_color = (0.75, 0.82, 0.75, 1)
            self.ids.btn_tab_pengeluaran.text_color = (0.12, 0.45, 0.12, 1)
        else:
            self.ids.btn_tab_pemasukan.md_bg_color = (0.75, 0.82, 0.75, 1)
            self.ids.btn_tab_pemasukan.text_color = (0.12, 0.45, 0.12, 1)
            self.ids.btn_tab_pengeluaran.md_bg_color = (0.12, 0.45, 0.12, 1)
            self.ids.btn_tab_pengeluaran.text_color = (1, 1, 1, 1)
            
        self.trigger_loading()

    def trigger_loading(self):
        # Reset views to loading state
        self.ids.main_content.opacity = 0
        self.ids.main_content.disabled = True
        self.ids.btn_add.opacity = 0
        self.ids.btn_add.disabled = True
        self.ids.loading_layout.opacity = 1
        self.ids.loading_layout.disabled = False
        
        # Delay actual rendering to simulate loading preview (SPA style)
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self.finish_loading(), 0.4)

    def finish_loading(self):
        self.load_table()
        
        # Reveal actual content
        self.ids.main_content.opacity = 1
        self.ids.main_content.disabled = False
        self.ids.btn_add.opacity = 1
        self.ids.btn_add.disabled = False
        self.ids.loading_layout.opacity = 0
        self.ids.loading_layout.disabled = True

    def load_table(self):
        container = self.ids.table_container
        container.clear_widgets()
        self.current_ids = []

        if self.active_tab == "pemasukan":
            # Load pemasukan
            # Total width expanded to make table full-width (225dp proportion)
            column_data = [
                ("No", dp(30)),
                ("Jumlah Sapi (Ekor)", dp(95)),
                ("Total Penjualan", dp(100))
            ]
            rows = database.get_all_pemasukan()
            row_data = []
            for i, r in enumerate(rows, start=1):
                # r = (id, jumlah_sapi, total_harga, tanggal)
                self.current_ids.append(r[0])
                row_data.append((str(i), f"{r[1]} Ekor", f"Rp {r[2]:,}"))
        else:
            # Load pengeluaran
            # Total width expanded to make table full-width (225dp proportion)
            column_data = [
                ("No", dp(25)),
                ("Produk", dp(80)),
                ("Kategori", dp(60)),
                ("Nominal", dp(60))
            ]
            rows = database.get_all_pengeluaran()
            row_data = []
            for i, r in enumerate(rows, start=1):
                # r = (id, produk, kategori, nominal, tanggal)
                self.current_ids.append(r[0])
                row_data.append((str(i), str(r[1]), str(r[2]), f"Rp {r[3]:,}"))

        self.table = MDDataTable(
            use_pagination=True,
            rows_num=7,
            column_data=column_data,
            row_data=row_data,
            elevation=0
        )
        self.table.bind(on_row_press=self.on_row_press)
        container.add_widget(self.table)

    def on_row_press(self, instance_table, instance_row):
        # Calculate which row index was clicked
        cell_index = instance_row.index
        cols = len(instance_table.column_data)
        row_idx = cell_index // cols
        
        if row_idx < len(self.current_ids):
            db_id = self.current_ids[row_idx]
            self.open_edit_dialog(db_id)

    def open_add_dialog(self):
        if self.active_tab == "pemasukan":
            self.add_field1 = MDTextField(hint_text="Jumlah Sapi (Ekor)", input_filter="int", mode="rectangle")
            self.add_field2 = MDTextField(hint_text="Total Penjualan (Rp)", input_filter="int", mode="rectangle")
            
            content = BoxLayout(orientation="vertical", size_hint_y=None, height="130dp", spacing="10dp")
            content.add_widget(self.add_field1)
            content.add_widget(self.add_field2)
            
            self.dialog = MDDialog(
                title="Input Pemasukan Baru",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(text="BATAL", on_release=lambda x: self.dialog.dismiss()),
                    MDRaisedButton(text="SIMPAN", md_bg_color=(0.12, 0.45, 0.12, 1), on_release=self.save_new_pemasukan)
                ]
            )
        else:
            self.add_field1 = MDTextField(hint_text="Nama Produk", mode="rectangle")
            self.add_field2 = MDTextField(hint_text="Kategori (Pakan, Susu, dll)", mode="rectangle")
            self.add_field3 = MDTextField(hint_text="Nominal (Rp)", input_filter="int", mode="rectangle")
            
            content = BoxLayout(orientation="vertical", size_hint_y=None, height="195dp", spacing="10dp")
            content.add_widget(self.add_field1)
            content.add_widget(self.add_field2)
            content.add_widget(self.add_field3)
            
            self.dialog = MDDialog(
                title="Input Pengeluaran Baru",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(text="BATAL", on_release=lambda x: self.dialog.dismiss()),
                    MDRaisedButton(text="SIMPAN", md_bg_color=(0.12, 0.45, 0.12, 1), on_release=self.save_new_pengeluaran)
                ]
            )
        self.dialog.open()

    def save_new_pemasukan(self, *args):
        val1 = self.add_field1.text.strip()
        val2 = self.add_field2.text.strip()
        if val1 and val2:
            database.add_pemasukan(int(val1), int(val2))
            self.dialog.dismiss()
            self.trigger_loading()

    def save_new_pengeluaran(self, *args):
        val1 = self.add_field1.text.strip()
        val2 = self.add_field2.text.strip()
        val3 = self.add_field3.text.strip()
        if val1 and val2 and val3:
            database.add_pengeluaran(val1, val2, int(val3))
            self.dialog.dismiss()
            self.trigger_loading()

    def open_edit_dialog(self, db_id):
        self.temp_edit_id = db_id
        conn = database.get_connection()
        c = conn.cursor()
        
        if self.active_tab == "pemasukan":
            c.execute("SELECT jumlah_sapi, total_harga FROM pemasukan WHERE id=?", (db_id,))
            row = c.fetchone()
            conn.close()
            if not row: return
            
            self.edit_field1 = MDTextField(text=str(row[0]), hint_text="Jumlah Sapi (Ekor)", input_filter="int", mode="rectangle")
            self.edit_field2 = MDTextField(text=str(row[1]), hint_text="Total Penjualan (Rp)", input_filter="int", mode="rectangle")
            
            content = BoxLayout(orientation="vertical", size_hint_y=None, height="130dp", spacing="10dp")
            content.add_widget(self.edit_field1)
            content.add_widget(self.edit_field2)
            
            self.dialog = MDDialog(
                title="Edit Pemasukan",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(text="HAPUS", text_color=(0.8, 0.2, 0.2, 1), on_release=self.delete_item),
                    MDFlatButton(text="BATAL", on_release=lambda x: self.dialog.dismiss()),
                    MDRaisedButton(text="UPDATE", md_bg_color=(0.12, 0.45, 0.12, 1), on_release=self.update_pemasukan)
                ]
            )
        else:
            c.execute("SELECT produk, kategori, nominal FROM pengeluaran WHERE id=?", (db_id,))
            row = c.fetchone()
            conn.close()
            if not row: return
            
            self.edit_field1 = MDTextField(text=str(row[0]), hint_text="Nama Produk", mode="rectangle")
            self.edit_field2 = MDTextField(text=str(row[1]), hint_text="Kategori (Pakan, Susu, dll)", mode="rectangle")
            self.edit_field3 = MDTextField(text=str(row[2]), hint_text="Nominal (Rp)", input_filter="int", mode="rectangle")
            
            content = BoxLayout(orientation="vertical", size_hint_y=None, height="195dp", spacing="10dp")
            content.add_widget(self.edit_field1)
            content.add_widget(self.edit_field2)
            content.add_widget(self.edit_field3)
            
            self.dialog = MDDialog(
                title="Edit Pengeluaran",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(text="HAPUS", text_color=(0.8, 0.2, 0.2, 1), on_release=self.delete_item),
                    MDFlatButton(text="BATAL", on_release=lambda x: self.dialog.dismiss()),
                    MDRaisedButton(text="UPDATE", md_bg_color=(0.12, 0.45, 0.12, 1), on_release=self.update_pengeluaran)
                ]
            )
        self.dialog.open()

    def update_pemasukan(self, *args):
        val1 = self.edit_field1.text.strip()
        val2 = self.edit_field2.text.strip()
        if val1 and val2:
            database.update_pemasukan(self.temp_edit_id, int(val1), int(val2))
            self.dialog.dismiss()
            self.trigger_loading()

    def update_pengeluaran(self, *args):
        val1 = self.edit_field1.text.strip()
        val2 = self.edit_field2.text.strip()
        val3 = self.edit_field3.text.strip()
        if val1 and val2 and val3:
            database.update_pengeluaran(self.temp_edit_id, val1, val2, int(val3))
            self.dialog.dismiss()
            self.trigger_loading()

    def delete_item(self, *args):
        self.dialog.dismiss()
        confirm_dlg = MDDialog(
            title="Hapus Data?",
            text="Apakah Anda yakin ingin menghapus data ini secara permanen?",
            buttons=[
                MDFlatButton(text="BATAL", on_release=lambda x: confirm_dlg.dismiss()),
                MDRaisedButton(text="HAPUS", md_bg_color=(0.8, 0.2, 0.2, 1), on_release=lambda x: self.execute_delete(confirm_dlg))
            ]
        )
        confirm_dlg.open()

    def execute_delete(self, confirm_dlg):
        confirm_dlg.dismiss()
        if self.active_tab == "pemasukan":
            database.delete_pemasukan(self.temp_edit_id)
        else:
            database.delete_pengeluaran(self.temp_edit_id)
        self.trigger_loading()

    def show_history_popup(self):
        history_data = database.get_recent_history(20)
        
        list_widget = MDList()
        if not history_data:
            list_widget.add_widget(TwoLineAvatarIconListItem(
                text="Belum ada riwayat transaksi",
                secondary_text="Tambahkan data pemasukan/pengeluaran baru"
            ))
        else:
            for item in history_data:
                tipe, db_id, detail, nominal, tanggal = item
                icon_name = "arrow-up-bold-circle" if tipe == "Pemasukan" else "arrow-down-bold-circle"
                icon_color = (0.12, 0.5, 0.12, 1) if tipe == "Pemasukan" else (0.8, 0.2, 0.2, 1)
                
                list_item = TwoLineAvatarIconListItem(
                    text=f"{detail} | Rp {nominal:,}",
                    secondary_text=f"{tanggal} | {tipe}",
                )
                left_widget = IconLeftWidget(icon=icon_name, theme_text_color="Custom", text_color=icon_color)
                list_item.add_widget(left_widget)
                list_widget.add_widget(list_item)
                
        scroll = ScrollView(size_hint_y=None, height=dp(300))
        scroll.add_widget(list_widget)
        
        history_dlg = MDDialog(
            title="Jurnal Aktivitas Terbaru",
            type="custom",
            content_cls=scroll,
            buttons=[
                MDFlatButton(text="TUTUP", on_release=lambda x: history_dlg.dismiss())
            ]
        )
        history_dlg.open()

    def export_excel(self):
        try:
            filepath = database.export_to_excel("Laporan_Siakternak.xlsx")
            success_dlg = MDDialog(
                title="Export Berhasil!",
                text=f"Seluruh data pemasukan dan pengeluaran berhasil diexport ke file Excel.\\n\\nLokasi: {filepath}",
                buttons=[
                    MDRaisedButton(text="OK", md_bg_color=(0.12, 0.45, 0.12, 1), on_release=lambda x: success_dlg.dismiss())
                ]
            )
            success_dlg.open()
        except Exception as e:
            err_dlg = MDDialog(
                title="Export Gagal",
                text=f"Terjadi kesalahan saat export Excel: {str(e)}",
                buttons=[
                    MDRaisedButton(text="TUTUP", on_release=lambda x: err_dlg.dismiss())
                ]
            )
            err_dlg.open()
