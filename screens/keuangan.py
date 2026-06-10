from kivy.lang import Builder
from kivymd.uix.screen import MDScreen

KV = '''
<KeuanganScreen>:
    MDFloatLayout:
        md_bg_color: 0.95, 0.98, 0.95, 1

        # Main Layout (Hidden during loading)
        MDBoxLayout:
            id: main_content
            opacity: 0
            disabled: True
            orientation: 'vertical'
            padding: "16dp"
            spacing: "16dp"

            # Header
            MDLabel:
                text: "MODUL KEUANGAN & AKUNTANSI"
                bold: True
                font_style: "H6"
                theme_text_color: "Custom"
                text_color: 0.12, 0.45, 0.12, 1
                size_hint_y: None
                height: "40dp"
                halign: "center"
                
            ScrollView:
                MDBoxLayout:
                    orientation: 'vertical'
                    adaptive_height: True
                    spacing: "16dp"
                    
                    # Info Card
                    MDCard:
                        size_hint_y: None
                        height: "80dp"
                        padding: "12dp"
                        radius: 15
                        md_bg_color: 0.12, 0.45, 0.12, 0.08
                        elevation: 0
                        orientation: 'horizontal'
                        spacing: "12dp"
                        
                        MDIcon:
                            icon: "information-outline"
                            font_size: "24sp"
                            theme_text_color: "Custom"
                            text_color: 0.12, 0.45, 0.12, 1
                            size_hint_x: None
                            width: "24dp"
                            pos_hint: {"center_y": 0.5}
                            
                        MDLabel:
                            text: "Modul akuntansi SAK ETAP aktif. Silakan pilih laporan keuangan peternakan Anda di bawah."
                            font_style: "Caption"
                            theme_text_color: "Custom"
                            text_color: 0.12, 0.45, 0.12, 1
                            valign: "middle"
                    
                    # 1. COA Card (Full width at top)
                    MDCard:
                        size_hint_y: None
                        height: "80dp"
                        padding: "16dp"
                        radius: 16
                        elevation: 1
                        orientation: 'horizontal'
                        ripple_behavior: True
                        on_release: app.switch_accounting_screen("coa")
                        md_bg_color: 1, 1, 1, 1
                        
                        MDIcon:
                            icon: "card-account-details-outline"
                            size_hint: None, None
                            size: dp(30), dp(30)
                            pos_hint: {"center_y": 0.5}
                            theme_text_color: "Custom"
                            text_color: 0.12, 0.45, 0.12, 1
                            font_size: "30sp"
                        MDBoxLayout:
                            orientation: 'vertical'
                            padding: ["12dp", "0dp", "0dp", "0dp"]
                            pos_hint: {"center_y": 0.5}
                            size_hint_y: None
                            height: self.minimum_height
                            MDLabel:
                                text: "Daftar Akun (COA)"
                                bold: True
                                font_style: "Subtitle1"
                                size_hint_y: None
                                height: self.texture_size[1]
                            MDLabel:
                                text: "Bagan akun & penggolongan aset, beban, pendapatan"
                                font_style: "Caption"
                                theme_text_color: "Secondary"
                                size_hint_y: None
                                height: self.texture_size[1]
                        MDIcon:
                            icon: "chevron-right"
                            size_hint: None, None
                            size: dp(24), dp(24)
                            pos_hint: {"center_y": 0.5}
                            theme_text_color: "Secondary"
                            font_size: "24sp"
                    
                    # 2. 2-Column Grid Layout for the other 4 cards
                    MDGridLayout:
                        cols: 2
                        spacing: "12dp"
                        size_hint_y: None
                        height: "240dp"  # Two rows of 110dp cards + 20dp spacing
                        
                        # Jurnal Umum Card
                        MDCard:
                            orientation: 'vertical'
                            padding: "16dp"
                            spacing: "4dp"
                            radius: 16
                            elevation: 1
                            ripple_behavior: True
                            on_release: app.switch_accounting_screen("jurnal")
                            md_bg_color: 1, 1, 1, 1
                            
                            MDIcon:
                                icon: "book-open-variant"
                                size_hint: None, None
                                size: dp(30), dp(30)
                                theme_text_color: "Custom"
                                text_color: 0.12, 0.45, 0.12, 1
                                font_size: "26sp"
                            MDLabel:
                                text: "Jurnal Umum"
                                bold: True
                                font_style: "Subtitle2"
                                size_hint_y: None
                                height: self.texture_size[1]
                            MDLabel:
                                text: "Double-entry kronologis"
                                font_style: "Caption"
                                theme_text_color: "Secondary"
                                size_hint_y: None
                                height: self.texture_size[1]
                                
                        # Buku Besar Card
                        MDCard:
                            orientation: 'vertical'
                            padding: "16dp"
                            spacing: "4dp"
                            radius: 16
                            elevation: 1
                            ripple_behavior: True
                            on_release: app.switch_accounting_screen("buku_besar")
                            md_bg_color: 1, 1, 1, 1
                            
                            MDIcon:
                                icon: "notebook-outline"
                                size_hint: None, None
                                size: dp(30), dp(30)
                                theme_text_color: "Custom"
                                text_color: 0.12, 0.45, 0.12, 1
                                font_size: "26sp"
                            MDLabel:
                                text: "Buku Besar"
                                bold: True
                                font_style: "Subtitle2"
                                size_hint_y: None
                                height: self.texture_size[1]
                            MDLabel:
                                text: "Mutasi saldo per akun"
                                font_style: "Caption"
                                theme_text_color: "Secondary"
                                size_hint_y: None
                                height: self.texture_size[1]
                                
                        # Neraca Saldo Card
                        MDCard:
                            orientation: 'vertical'
                            padding: "16dp"
                            spacing: "4dp"
                            radius: 16
                            elevation: 1
                            ripple_behavior: True
                            on_release: app.switch_accounting_screen("neraca")
                            md_bg_color: 1, 1, 1, 1
                            
                            MDIcon:
                                icon: "scale-balance"
                                size_hint: None, None
                                size: dp(30), dp(30)
                                theme_text_color: "Custom"
                                text_color: 0.12, 0.45, 0.12, 1
                                font_size: "26sp"
                            MDLabel:
                                text: "Neraca Saldo"
                                bold: True
                                font_style: "Subtitle2"
                                size_hint_y: None
                                height: self.texture_size[1]
                            MDLabel:
                                text: "Uji keseimbangan D/K"
                                font_style: "Caption"
                                theme_text_color: "Secondary"
                                size_hint_y: None
                                height: self.texture_size[1]
                                
                        # Laba Rugi Card
                        MDCard:
                            orientation: 'vertical'
                            padding: "16dp"
                            spacing: "4dp"
                            radius: 16
                            elevation: 1
                            ripple_behavior: True
                            on_release: app.switch_accounting_screen("laba_rugi")
                            md_bg_color: 1, 1, 1, 1
                            
                            MDIcon:
                                icon: "finance"
                                size_hint: None, None
                                size: dp(30), dp(30)
                                theme_text_color: "Custom"
                                text_color: 0.12, 0.45, 0.12, 1
                                font_size: "26sp"
                            MDLabel:
                                text: "Laba Rugi"
                                bold: True
                                font_style: "Subtitle2"
                                size_hint_y: None
                                height: self.texture_size[1]
                            MDLabel:
                                text: "Ikhtisar hasil laba bersih"
                                font_style: "Caption"
                                theme_text_color: "Secondary"
                                size_hint_y: None
                                height: self.texture_size[1]

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
                text: "Memuat Menu Keuangan..."
                halign: "center"
                bold: True
                font_style: "Caption"
                theme_text_color: "Custom"
                text_color: 0.12, 0.45, 0.12, 1
'''

Builder.load_string(KV)

class KeuanganScreen(MDScreen):
    
    def on_enter(self):
        self.trigger_loading()
        
    def trigger_loading(self):
        # 1. Reset views to loading state
        self.ids.main_content.opacity = 0
        self.ids.main_content.disabled = True
        self.ids.loading_layout.opacity = 1
        self.ids.loading_layout.disabled = False
        
        # 2. Delay loading visual grid to simulate SPA client-side rendering
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self.finish_loading(), 0.4)
        
    def finish_loading(self):
        # Reveal actual content
        self.ids.main_content.opacity = 1
        self.ids.main_content.disabled = False
        self.ids.loading_layout.opacity = 0
        self.ids.loading_layout.disabled = True
