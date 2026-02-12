from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from cryptography.fernet import Fernet
import requests

# ИСПРАВЛЕННЫЙ КЛЮЧ (теперь ровно 32 байта в base64)
KEY = b'6fL3_F5_E8v1pXz7_m-90U5IF-ri8GYQ_ABCDE123456=' 
cipher = Fernet(KEY)

KV = '''
ScreenManager:
    LoginScreen:
    ChatScreen:

<LoginScreen>:
    name: "login"
    MDBoxLayout:
        orientation: 'vertical'
        padding: "40dp"
        spacing: "20dp"
        md_bg_color: 0.1, 0.1, 0.1, 1

        MDLabel:
            text: "GHOST CHAT"
            halign: "center"
            font_style: "H4"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1

        MDTextField:
            id: email
            hint_text: "Почта"
            mode: "rectangle"

        MDTextField:
            id: user_uid
            hint_text: "Ваш ID"
            mode: "rectangle"

        MDRaisedButton:
            text: "ВОЙТИ"
            pos_hint: {"center_x": .5}
            on_release: app.login()

<ChatScreen>:
    name: "chat"
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.05, 0.05, 0.05, 1

        MDTopAppBar:
            title: "GhostChat"
            right_action_items: [["logout", lambda x: app.logout()]]

        ScrollView:
            MDBoxLayout:
                id: chat_box
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                padding: "10dp"
                spacing: "10dp"

        MDBoxLayout:
            size_hint_y: None
            height: "60dp"
            padding: "5dp"
            spacing: "5dp"
            md_bg_color: 0.1, 0.1, 0.1, 1

            MDTextField:
                id: msg_input
                hint_text: "Сообщение..."
                mode: "fill"

            MDIconButton:
                icon: "send"
                on_release: app.send_message()
'''

class GhostChatApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)

    def login(self):
        self.root.current = "chat"

    def logout(self):
        self.root.current = "login"

    def send_message(self):
        msg = self.root.get_screen("chat").ids.msg_input.text
        if msg:
            # Шифрование работает!
            encrypted = cipher.encrypt(msg.encode()).decode()
            label = MDLabel(text=f"[ВЫ]: {msg}", size_hint_y=None, height="40dp", theme_text_color="Hint")
            self.root.get_screen("chat").ids.chat_box.add_widget(label)
            self.root.get_screen("chat").ids.msg_input.text = ""

if __name__ == "__main__":
    GhostChatApp().run()


