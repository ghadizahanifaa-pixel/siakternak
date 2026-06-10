from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
import database

KV = '''
<InventarisScreen>:
    MDFloatLayout:
        md_bg_color: 0.95, 0.98, 0.95, 1

        # Main Layout (Hidden during loading)
        MDBoxLayout:
            id: main_content
            opacity: 0
            disabled: True
            orientation: 'vertical'
            padding: ["16dp", "16dp", "16dp", "75dp"]
            spacing: "12dp"

            # Header Area
            MDLabel:
                text: "INVENTARIS & STOK BARANG"
                bold: True
                font_style: "H6"
                theme_text_color: "Custom"
                text_color: 0.12, 0.45, 0.12, 1
                size_hint_y: None
                height: "35dp"
                halign: "center"

            # 3-Column Grid stock indicators
            MDGridLayout:
                cols: 3
                spacing: "12dp"
                size_hint_y: None
                height: "100dp"

                MDCard:
                    padding: "12dp"
                    radius: 15
                    orientation: 'vertical'
                    elevation: 1
                    md_bg_color: 0.12, 0.45, 0.12, 1
                    canvas:
                        Color:
                            rgba: 0.12, 0.45, 0.12, 1
                        RoundedRectangle:
                            size: self.size
                            pos: self.pos
                            radius: [15, ]
                    MDLabel:
                        text: "STOK SAPI"
                        font_style: "Subtitle2"
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 0.7
                        bold: True
                    MDLabel:
                        id: lbl_stock_sapi
                        text: "0 Ekor"
                        halign: "center"
                        font_style: "H5"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1
                        bold: True

                MDCard:
                    padding: "12dp"
                    radius: 15
                    orientation: 'vertical'
                    elevation: 1
                    md_bg_color: 0.12, 0.45, 0.12, 0.08
                    MDLabel:
                        text: "STOK PAKAN"
                        font_style: "Subtitle2"
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: 0.12, 0.45, 0.12, 0.7
                        bold: True
                    MDLabel:
                        id: lbl_stock_pakan
                        text: "0 Pcs"
                        halign: "center"
                        font_style: "H5"
                        theme_text_color: "Custom"
                        text_color: 0.12, 0.45, 0.12, 1
                        bold: True

                MDCard:
                    padding: "12dp"
                    radius: 15
                    orientation: 'vertical'
                    elevation: 1
                    md_bg_color: 0.12, 0.45, 0.12, 0.08
                    MDLabel:
                        text: "STOK OBAT"
                        font_style: "Subtitle2"
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: 0.12, 0.45, 0.12, 0.7
                        bold: True
                    MDLabel:
                        id: lbl_stock_obat
                        text: "0 Pcs"
                        halign: "center"
                        font_style: "H5"
                        theme_text_color: "Custom"
                        text_color: 0.12, 0.45, 0.12, 1
                        bold: True

            # Table Container
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
                text: "Memuat Inventaris..."
                halign: "center"
                bold: True
                font_style: "Caption"
                theme_text_color: "Custom"
                text_color: 0.12, 0.45, 0.12, 1
'''

Builder.load_string(KV)

class InventarisScreen(MDScreen):
    table = None
    dialog = None
    dropdown_menu = None
    current_ids = []
    selected_tipe = "Masuk"

    def on_enter(self):
        self.trigger_loading()

    def trigger_loading(self):
        self.ids.main_content.opacity = 0
        self.ids.main_content.disabled = True
        self.ids.btn_add.opacity = 0
        self.ids.btn_add.disabled = True
        self.ids.loading_layout.opacity = 1
        self.ids.loading_layout.disabled = False
        
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self.finish_loading(), 0.4)

    def finish_loading(self):
        self.load_summary()
        self.load_table()
        
        self.ids.main_content.opacity = 1
        self.ids.main_content.disabled = False
        self.ids.btn_add.opacity = 1
        self.ids.btn_add.disabled = False
        self.ids.loading_layout.opacity = 0
        self.ids.loading_layout.disabled = True

    def load_summary(self):
        summary = database.get_inventory_summary()
        self.ids.lbl_stock_sapi.text = f"{summary['sapi']} Ekor"
        self.ids.lbl_stock_pakan.text = f"{summary['pakan']} Pcs"
        self.ids.lbl_stock_obat.text = f"{summary['obat']} Pcs"

    def load_table(self):
        container = self.ids.table_container
        container.clear_widgets()
        self.current_ids = []

        column_data = [
            ("No", dp(15)),
            ("Nama Barang / Hal", dp(60)),
            ("Tipe Mutasi", dp(35)),
            ("Jumlah", dp(25)),
            ("Tanggal", dp(45)),
            ("Keterangan", dp(60))
        ]
        
        rows = database.get_all_inventaris()
        row_data = []
        for i, r in enumerate(rows, start=1):
            # r = (id, nama_barang, tipe_transaksi, jumlah, tanggal, keterangan)
            self.current_ids.append(r[0])
            qty_str = f"+{r[3]}" if r[2] == 'Masuk' else f"-{r[3]}"
            row_data.append((str(i), str(r[1]), str(r[2]), qty_str, str(r[4][:10]), str(r[5] or '')))

        self.table = MDDataTable(
            use_pagination=True,
            rows_num=5,
            column_data=column_data,
            row_data=row_data,
            elevation=0
        )
        self.table.bind(on_row_press=self.on_row_press)
        container.add_widget(self.table)

    def on_row_press(self, instance_table, instance_row):
        cell_index = instance_row.index
        cols = len(instance_table.column_data)
        row_idx = cell_index // cols
        
        if row_idx < len(self.current_ids):
            db_id = self.current_ids[row_idx]
            self.open_edit_dialog(db_id)

    def open_add_dialog(self):
        self.selected_tipe = "Masuk"
        
        # Textfield for name of item
        self.add_field_name = MDTextField(
            text="Sapi",
            hint_text="Nama Barang (contoh: Sapi, Pakan Sapi)",
            mode="rectangle"
        )
        
        # Dropdown selection button for type
        self.btn_select_type = MDRaisedButton(
            text="Tipe: Masuk",
            md_bg_color=(0.12, 0.45, 0.12, 1),
            size_hint_x=1,
            on_release=self.open_type_dropdown
        )
        
        self.add_field_qty = MDTextField(
            hint_text="Jumlah",
            input_filter="int",
            mode="rectangle"
        )
        self.add_field_desc = MDTextField(
            hint_text="Keterangan",
            mode="rectangle"
        )
        
        content = BoxLayout(orientation="vertical", size_hint_y=None, height="260dp", spacing="10dp")
        content.add_widget(self.add_field_name)
        content.add_widget(self.btn_select_type)
        content.add_widget(self.add_field_qty)
        content.add_widget(self.add_field_desc)
        
        self.dialog = MDDialog(
            title="Tambah Mutasi Inventaris",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="BATAL", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(
                    text="SIMPAN",
                    md_bg_color=(0.12, 0.45, 0.12, 1),
                    on_release=self.save_new_inventaris
                )
            ]
        )
        self.dialog.open()

    def open_type_dropdown(self, button):
        items = ["Masuk", "Keluar"]
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": item,
                "on_release": lambda x=item: self.set_selected_type(x)
            } for item in items
        ]
        self.dropdown_menu = MDDropdownMenu(
            caller=button,
            items=menu_items,
            width=dp(200)
        )
        self.dropdown_menu.open()

    def set_selected_type(self, item_name):
        self.selected_tipe = item_name
        self.btn_select_type.text = f"Tipe: {item_name}"
        if self.dropdown_menu:
            self.dropdown_menu.dismiss()

    def save_new_inventaris(self, *args):
        name = self.add_field_name.text.strip()
        qty = self.add_field_qty.text.strip()
        desc = self.add_field_desc.text.strip()
        if name and qty:
            database.add_inventaris_manual(name, self.selected_tipe, int(qty), desc)
            self.dialog.dismiss()
            self.trigger_loading()

    def open_edit_dialog(self, db_id):
        conn = database.get_connection()
        c = conn.cursor()
        c.execute("SELECT nama_barang, tipe_transaksi, jumlah, keterangan, pemasukan_id, pengeluaran_id FROM inventaris WHERE id=?", (db_id,))
        row = c.fetchone()
        conn.close()
        
        if not row:
            return
            
        nama_barang, tipe, jumlah, keterangan, pemasukan_id, pengeluaran_id = row
        
        if pemasukan_id is not None or pengeluaran_id is not None:
            source = "Pemasukan (Penjualan)" if pemasukan_id is not None else "Pengeluaran (Pembelian)"
            self.dialog = MDDialog(
                title="Info Mutasi Otomatis",
                text=f"Mutasi ini disinkronisasi otomatis dari {source}. Silakan ubah data melalui menu Keuangan/Data.",
                buttons=[
                    MDRaisedButton(
                        text="OK",
                        md_bg_color=(0.12, 0.45, 0.12, 1),
                        on_release=lambda x: self.dialog.dismiss()
                    )
                ]
            )
            self.dialog.open()
            return
            
        self.temp_edit_id = db_id
        self.selected_tipe = tipe
        
        # Fields for manual edit
        self.edit_field_name = MDTextField(
            text=str(nama_barang),
            hint_text="Nama Barang",
            mode="rectangle"
        )
        
        self.btn_select_type = MDRaisedButton(
            text=f"Tipe: {tipe}",
            md_bg_color=(0.12, 0.45, 0.12, 1),
            size_hint_x=1,
            on_release=self.open_type_dropdown
        )
        
        self.edit_field_qty = MDTextField(
            text=str(jumlah),
            hint_text="Jumlah",
            input_filter="int",
            mode="rectangle"
        )
        self.edit_field_desc = MDTextField(
            text=str(keterangan or ""),
            hint_text="Keterangan",
            mode="rectangle"
        )
        
        content = BoxLayout(orientation="vertical", size_hint_y=None, height="260dp", spacing="10dp")
        content.add_widget(self.edit_field_name)
        content.add_widget(self.btn_select_type)
        content.add_widget(self.edit_field_qty)
        content.add_widget(self.edit_field_desc)
        
        self.dialog = MDDialog(
            title="Ubah Mutasi Inventaris",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="HAPUS",
                    theme_text_color="Custom",
                    text_color=(0.8, 0.2, 0.2, 1),
                    on_release=self.delete_inventaris
                ),
                MDFlatButton(
                    text="BATAL",
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDRaisedButton(
                    text="SIMPAN",
                    md_bg_color=(0.12, 0.45, 0.12, 1),
                    on_release=self.save_edit_inventaris
                )
            ]
        )
        self.dialog.open()

    def save_edit_inventaris(self, *args):
        name = self.edit_field_name.text.strip()
        qty = self.edit_field_qty.text.strip()
        desc = self.edit_field_desc.text.strip()
        if name and qty:
            database.update_inventaris_manual(self.temp_edit_id, name, self.selected_tipe, int(qty), desc)
            self.dialog.dismiss()
            self.trigger_loading()

    def delete_inventaris(self, *args):
        database.delete_inventaris_manual(self.temp_edit_id)
        self.dialog.dismiss()
        self.trigger_loading()
