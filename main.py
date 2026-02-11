from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDFillRoundFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from cryptography.fernet import Fernet
import requests

# Твой уникальный ключ шифрования (должен быть у обоих)
KEY = b'uV0pZH1c-5wz76NTxs90U5IF-ri8GYQ_example_key='
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
            text_color_focus: 1, 1, 1, 1

        MDTextField:
            id: user_uid
            hint_text: "Придумайте ваш уникальный ЮЗ"
            mode: "rectangle"
            helper_text: "Этот ID нельзя будет изменить"
            helper_text_mode: "on_focus"

        MDFillRoundFlatButton:
            text: "ВОЙТИ В СЕТЬ"
            pos_hint: {"center_x": .5}
            size_hint_x: 1
            on_release: app.login()

<ChatScreen>:
    name: "chat"
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.05, 0.05, 0.05, 1

        MDTopAppBar:
            title: "Ghost Messenger"
            elevation: 4
            md_bg_color: 0.1, 0.1, 0.1, 1
            specific_text_color: 1, 1, 1, 1

        ScrollView:
            MDList:
                id: chat_list
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
                fill_color: 0.15, 0.15, 0.15, 1

            MDIconButton:
                icon: "send"
                theme_text_color: "Custom"
                text_color: 0.2, 0.6, 1, 1
                on_release: app.send_message()
'''

class GhostChatApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)

    def login(self):
        uid = self.root.get_screen("login").ids.user_uid.text
        email = self.root.get_screen("login").ids.email.text
        
        if uid and email:
            # Здесь можно добавить проверку на уникальность через Firebase или твой сервер
            # Пока просто пропускаем в чат
            self.root.current = "chat"

    def send_message(self):
        msg = self.root.get_screen("chat").ids.msg_input.text
        if msg:
            # Шифруем перед отправкой (имитация)
            encrypted = cipher.encrypt(msg.encode()).decode()
            
            # Добавляем в визуал чата
            label = MDLabel(
                text=f"[ВЫ]: {msg}", 
                theme_text_color="Custom",
                text_color=(0.8, 0.8, 0.8, 1),
                size_hint_y=None,
                height="40dp"
            )
            self.root.get_screen("chat").ids.chat_list.add_widget(label)
            self.root.get_screen("chat").ids.msg_input.text = ""

if __name__ == "__main__":
    GhostChatApp().run()


