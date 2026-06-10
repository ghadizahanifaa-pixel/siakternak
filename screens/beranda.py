from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
import database

try:
    import matplotlib.pyplot as plt
    import numpy as np
    from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
    matplotlib_available = True
except ImportError:
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
        matplotlib_available = True
    except ImportError:
        matplotlib_available = False

KV = '''
<BerandaScreen>:
    MDFloatLayout:
        md_bg_color: 0.95, 0.98, 0.95, 1

        # Main Scrollable Content (Hidden during loading)
        ScrollView:
            id: scroll_content
            opacity: 0
            disabled: True
            
            MDBoxLayout:
                orientation: 'vertical'
                adaptive_height: True
                padding: "16dp"
                spacing: "16dp"

                MDCard:
                    size_hint_y: None
                    height: "120dp"
                    padding: "16dp"
                    radius: 20
                    md_bg_color: 0.12, 0.45, 0.12, 1
                    elevation: 2
                    orientation: 'vertical'
                    canvas:
                        Color:
                            rgba: 0.12, 0.45, 0.12, 1
                        RoundedRectangle:
                            size: self.size
                            pos: self.pos
                            radius: [20, ]
                    
                    MDLabel:
                        text: "ESTIMASI LABA BERSIH"
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 0.7
                        bold: True
                        font_style: "Subtitle2"
                    MDLabel:
                        id: laba_label
                        text: "Rp 0"
                        halign: "center"
                        font_style: "H4"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1
                        bold: True

                # In/Out Grid
                MDGridLayout:
                    cols: 2
                    spacing: "12dp"
                    size_hint_y: None
                    height: "85dp"

                    MDCard:
                        padding: "12dp"
                        radius: 15
                        orientation: 'vertical'
                        elevation: 1
                        
                        MDLabel:
                            text: "Total Pemasukan"
                            font_style: "Caption"
                            halign: "center"
                            theme_text_color: "Secondary"
                        MDLabel:
                            id: total_in_label
                            text: "Rp 0"
                            halign: "center"
                            font_style: "Subtitle1"
                            theme_text_color: "Custom"
                            text_color: 0.12, 0.5, 0.12, 1
                            bold: True

                    MDCard:
                        padding: "12dp"
                        radius: 15
                        orientation: 'vertical'
                        elevation: 1
                        
                        MDLabel:
                            text: "Total Pengeluaran"
                            font_style: "Caption"
                            halign: "center"
                            theme_text_color: "Secondary"
                        MDLabel:
                            id: total_out_label
                            text: "Rp 0"
                            halign: "center"
                            font_style: "Subtitle1"
                            theme_text_color: "Custom"
                            text_color: 0.8, 0.2, 0.2, 1
                            bold: True

                # Chart Card (Clickable to show details)
                MDCard:
                    size_hint_y: None
                    height: "290dp"
                    padding: "8dp"
                    radius: 15
                    orientation: 'vertical'
                    elevation: 1
                    ripple_behavior: True
                    on_release: root.show_chart_details()
                    
                    MDBoxLayout:
                        size_hint_y: None
                        height: "40dp"
                        orientation: 'horizontal'
                        padding: ["8dp", "0dp", "8dp", "0dp"]
                        
                        MDLabel:
                            text: "Grafik Keuangan (6 Bulan Terakhir)"
                            font_style: "Subtitle2"
                            bold: True
                            valign: "middle"
                            
                        MDIcon:
                            icon: "information-outline"
                            theme_text_color: "Custom"
                            text_color: 0.5, 0.5, 0.5, 1
                            size_hint_x: None
                            width: "24dp"
                            pos_hint: {"center_y": 0.5}
                    
                    MDBoxLayout:
                        id: chart_container
                        orientation: 'vertical'
                        # Chart or fallback label will be added dynamically

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
                text: "Memuat Dashboard..."
                halign: "center"
                bold: True
                font_style: "Caption"
                theme_text_color: "Custom"
                text_color: 0.12, 0.45, 0.12, 1
'''

Builder.load_string(KV)

class BerandaScreen(MDScreen):
    
    def on_enter(self):
        self.trigger_loading()
        
    def trigger_loading(self):
        # 1. Reset views to loading state
        self.ids.scroll_content.opacity = 0
        self.ids.scroll_content.disabled = True
        self.ids.loading_layout.opacity = 1
        self.ids.loading_layout.disabled = False
        
        # 2. Delay loading database and chart to simulate client-side rendering (SPA)
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self.load_data(), 0.5)
        
    def load_data(self):
        # 1. Fetch data summary from database
        summary = database.get_summary()
        self.ids.total_in_label.text = f"Rp {summary['total_in']:,}"
        self.ids.total_out_label.text = f"Rp {summary['total_out']:,}"
        self.ids.laba_label.text = f"Rp {summary['laba']:,}"
        
        # 2. Update Matplotlib chart
        self.update_chart()
        
        # 3. Fade in content and disable loader
        self.ids.scroll_content.opacity = 1
        self.ids.scroll_content.disabled = False
        self.ids.loading_layout.opacity = 0
        self.ids.loading_layout.disabled = True

    def update_chart(self):
        container = self.ids.chart_container
        container.clear_widgets()
        
        if not matplotlib_available:
            from kivymd.uix.label import MDLabel
            container.add_widget(MDLabel(
                text="Matplotlib belum terinstal atau tidak didukung.",
                halign="center",
                font_style="Caption"
            ))
            return
            
        try:
            # Clear previous plots
            plt.clf()
            
            labels, in_vals, out_vals = database.get_monthly_summary()
            
            # Setup Plot styling
            fig, ax = plt.subplots(figsize=(6, 3.2))
            fig.patch.set_facecolor('#F5F9F5')  # Sleek green tint match layout
            ax.set_facecolor('#FFFFFF')
            
            x = np.arange(len(labels))
            width = 0.35
            
            # Plot double bar
            rects1 = ax.bar(x - width/2, in_vals, width, label='Masuk', color='#2E7D32')
            rects2 = ax.bar(x + width/2, out_vals, width, label='Keluar', color='#C62828')
            
            ax.set_xticks(x)
            ax.set_xticklabels(labels, fontsize=8)
            ax.legend(fontsize=8, loc='upper left')
            
            # Format labels as brief Rp values if large
            def format_rp(y, pos):
                if y >= 1_000_000:
                    return f'Rp {y/1_000_000:.1f}jt'
                elif y >= 1_000:
                    return f'Rp {y/1_000:.0f}rb'
                return f'Rp {y:.0f}'
                
            from matplotlib.ticker import FuncFormatter
            ax.yaxis.set_major_formatter(FuncFormatter(format_rp))
            ax.tick_params(axis='y', labelsize=8)
            
            # Clean spines
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#CCCCCC')
            ax.spines['bottom'].set_color('#CCCCCC')
            ax.yaxis.grid(True, linestyle='--', alpha=0.4, color='#888888')
            
            fig.tight_layout()
            
            # Render to Kivy widget
            canvas = FigureCanvasKivyAgg(plt.gcf())
            container.add_widget(canvas)
        except Exception as e:
            from kivymd.uix.label import MDLabel
            container.add_widget(MDLabel(
                text=f"Error rendering chart: {str(e)}",
                halign="center",
                font_style="Caption"
            ))

    def show_chart_details(self):
        labels, in_vals, out_vals = database.get_monthly_summary()
        
        content_text = ""
        for i in range(len(labels)):
            month = labels[i]
            pemasukan = in_vals[i]
            pengeluaran = out_vals[i]
            laba = pemasukan - pengeluaran
            content_text += (
                f"[b]{month}[/b]\n"
                f"  • Pemasukan: Rp {pemasukan:,}\n"
                f"  • Pengeluaran: Rp {pengeluaran:,}\n"
                f"  • Laba Bersih: [color=1B5E20]Rp {laba:,}[/color]\n\n"
            )
            
        dialog = MDDialog(
            title="Rincian Laba Rugi Bulanan",
            text=content_text.strip(),
            buttons=[
                MDRaisedButton(
                    text="TUTUP",
                    md_bg_color=(0.12, 0.45, 0.12, 1),
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
