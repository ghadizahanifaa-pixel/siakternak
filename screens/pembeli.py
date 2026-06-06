from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
import database

KV_PEMBELI = '''
<PembeliScreen>:
    MDFloatLayout:
        md_bg_color: 0.95, 0.98, 0.95, 1

        # Main Content Layout (Hidden during loading)
        MDBoxLayout:
            id: main_content
            opacity: 0
            disabled: True
            orientation: 'vertical'
            padding: ["16dp", "16dp", "16dp", "75dp"]  # Bottom padding to avoid navigation overlaps
            spacing: "12dp"

            # Header Area
            MDBoxLayout:
                size_hint_y: None
                height: "50dp"
                orientation: 'horizontal'
                
                MDLabel:
                    text: "DATA PEMESANAN SAPI"
                    bold: True
                    font_style: "H6"
                    theme_text_color: "Custom"
                    text_color: 0.12, 0.45, 0.12, 1
                    
            MDLabel:
                text: "Daftar pemesanan sapi. Status yang sudah di-Acc/Tolak bersifat permanen dan tidak dapat diubah kembali."
                font_style: "Caption"
                theme_text_color: "Secondary"
                size_hint_y: None
                height: "25dp"

            ScrollView:
                MDBoxLayout:
                    id: list_container
                    orientation: 'vertical'
                    adaptive_height: True
                    spacing: "12dp"
                    padding: ["2dp", "2dp", "2dp", "2dp"]

        # Simulated Loading overlay
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
                text: "Memuat Data Pembeli..."
                halign: "center"
                bold: True
                font_style: "Caption"
                theme_text_color: "Custom"
                text_color: 0.12, 0.45, 0.12, 1
'''

Builder.load_string(KV_PEMBELI)

class PembeliScreen(MDScreen):
    def on_enter(self):
        self.trigger_loading()

    def trigger_loading(self):
        self.ids.main_content.opacity = 0
        self.ids.main_content.disabled = True
        self.ids.loading_layout.opacity = 1
        self.ids.loading_layout.disabled = False
        
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self.load_data(), 0.5)

    def load_data(self):
        container = self.ids.list_container
        container.clear_widgets()
        
        orders = database.get_all_pesanan()
        
        if not orders:
            empty_lbl = MDLabel(
                text="Belum ada data pemesanan sapi.",
                halign="center",
                font_style="Subtitle1",
                theme_text_color="Secondary",
                size_hint_y=None,
                height=dp(100)
            )
            container.add_widget(empty_lbl)
        else:
            for o in orders:
                # o = (id, nama, wa, jenis_sapi, jumlah_sapi, keterangan, status, tanggal)
                card = self.create_order_card(o)
                container.add_widget(card)
        
        # Fade in main content
        self.ids.main_content.opacity = 1
        self.ids.main_content.disabled = False
        self.ids.loading_layout.opacity = 0
        self.ids.loading_layout.disabled = True

    def create_order_card(self, order):
        order_id, nama, wa, jenis_sapi, jumlah_sapi, keterangan, status, tanggal = order
        
        is_pending = (status == 'Pending')
        card_height = dp(180) if is_pending else dp(135)
        
        card = MDCard(
            size_hint_y=None,
            height=card_height,
            radius=[12, 12, 12, 12],
            padding=dp(16),
            spacing=dp(6),
            orientation='vertical',
            elevation=1,
            md_bg_color=(1, 1, 1, 1)
        )
        
        # Row 1: Name & Date
        row1 = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(25))
        lbl_name = MDLabel(text=f"[b]{nama}[/b]", markup=True, font_style="Subtitle1", theme_text_color="Custom", text_color=(0.12, 0.45, 0.12, 1))
        lbl_date = MDLabel(text=tanggal, halign="right", font_style="Caption", theme_text_color="Secondary")
        row1.add_widget(lbl_name)
        row1.add_widget(lbl_date)
        card.add_widget(row1)
        
        # Row 2: Breed & Qty
        row2 = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(20))
        lbl_details = MDLabel(text=f"Sapi {jenis_sapi}  •  {jumlah_sapi} Ekor  •  WA: {wa}", font_style="Body2", theme_text_color="Primary")
        row2.add_widget(lbl_details)
        card.add_widget(row2)
        
        # Row 3: Notes
        row3 = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(20))
        lbl_notes = MDLabel(text=f"Catatan: {keterangan or '-'}", font_style="Caption", theme_text_color="Secondary")
        row3.add_widget(lbl_notes)
        card.add_widget(row3)
        
        # Row 4: Status / Actions
        row4 = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(36), spacing=dp(10))
        
        if is_pending:
            btn_acc = MDRaisedButton(
                text="ACC (SETUJU)",
                md_bg_color=(0.12, 0.5, 0.12, 1),
                size_hint_x=0.5,
                on_release=lambda x, oid=order_id: self.update_order_status(oid, 'Iya')
            )
            btn_reject = MDRaisedButton(
                text="TOLAK",
                md_bg_color=(0.8, 0.2, 0.2, 1),
                size_hint_x=0.5,
                on_release=lambda x, oid=order_id: self.update_order_status(oid, 'Tidak')
            )
            row4.add_widget(btn_acc)
            row4.add_widget(btn_reject)
        else:
            if status == 'Iya':
                badge_text = "✓ DISETUJUI (ACC)"
                badge_color = (0.12, 0.5, 0.12, 1)
            else:
                badge_text = "✗ DITOLAK"
                badge_color = (0.8, 0.2, 0.2, 1)
                
            lbl_badge = MDLabel(
                text=badge_text,
                bold=True,
                font_style="Subtitle2",
                theme_text_color="Custom",
                text_color=badge_color,
                halign="left"
            )
            row4.add_widget(lbl_badge)
            
        card.add_widget(row4)
        return card

    def update_order_status(self, order_id, new_status):
        database.update_status_pesanan(order_id, new_status)
        self.trigger_loading()
