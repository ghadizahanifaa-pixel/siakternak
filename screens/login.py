from kivy.lang import Builder
from kivymd.uix.screen import MDScreen

KV = '''
<LoginScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        padding: "40dp"
        spacing: "20dp"
        md_bg_color: 0.95, 0.98, 0.95, 1  # Sleek pastel light green

        MDBoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.35
            spacing: "12dp"
            pos_hint: {"center_x": 0.5}

            MDIcon:
                icon: "cow"
                halign: "center"
                font_size: "90sp"
                theme_text_color: "Custom"
                text_color: 0.12, 0.45, 0.12, 1

            MDLabel:
                text: "SIAKTERNAK PRO"
                halign: "center"
                font_style: "H4"
                theme_text_color: "Custom"
                text_color: 0.12, 0.45, 0.12, 1
                bold: True

            MDLabel:
                text: "Sistem Informasi Akuntansi Peternakan"
                halign: "center"
                font_style: "Caption"
                theme_text_color: "Custom"
                text_color: 0.3, 0.5, 0.3, 1

        MDBoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.45
            spacing: "16dp"
            padding: ["20dp", "10dp", "20dp", "10dp"]

            MDTextField:
                id: username_input
                hint_text: "Username"
                icon_right: "account"
                mode: "rectangle"
                size_hint_x: 0.85
                pos_hint: {"center_x": 0.5}
                line_color_focus: 0.12, 0.45, 0.12, 1
                hint_text_color_focus: 0.12, 0.45, 0.12, 1

            MDTextField:
                id: password_input
                hint_text: "Password"
                icon_right: "key-variant"
                password: True
                mode: "rectangle"
                size_hint_x: 0.85
                pos_hint: {"center_x": 0.5}
                line_color_focus: 0.12, 0.45, 0.12, 1
                hint_text_color_focus: 0.12, 0.45, 0.12, 1
                on_text_validate: app.verify_login()

            MDRaisedButton:
                text: "MASUK APLIKASI"
                md_bg_color: 0.12, 0.45, 0.12, 1
                size_hint: 0.85, None
                height: "50dp"
                pos_hint: {"center_x": 0.5}
                elevation: 2
                on_release: app.verify_login()

            MDFlatButton:
                text: "KEMBALI KE PORTAL UTAMA"
                theme_text_color: "Custom"
                text_color: 0.12, 0.45, 0.12, 1
                pos_hint: {"center_x": 0.5}
                on_release: app.back_to_landing()

            MDLabel:
                id: error_label
                text: ""
                halign: "center"
                theme_text_color: "Error"
                font_style: "Caption"
                bold: True

        MDBoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.2
            justify_content: 'center'

            MDLabel:
                text: "© 2026 SIAKTERNAK Management System"
                halign: "center"
                font_style: "Caption"
                theme_text_color: "Custom"
                text_color: 0.5, 0.5, 0.5, 1
'''

Builder.load_string(KV)

class LoginScreen(MDScreen):
    pass
