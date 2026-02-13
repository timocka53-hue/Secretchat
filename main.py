import os, json, certifi, pyrebase
from kivy.app import App
from kivy.utils import platform
from kivy.clock import Clock

os.environ['SSL_CERT_FILE'] = certifi.where()

# Данные из твоего google-services.json
firebase_config = {
    "apiKey": "AIzaSyAbiRCuR9egtHKg0FNzzBdL9dNqPqpPLNk",
    "authDomain": "ghost-pro-5aa22.firebaseapp.com",
    "projectId": "ghost-pro-5aa22",
    "storageBucket": "ghost-pro-5aa22.firebasestorage.app",
    "messagingSenderId": "332879455079",
    "appId": "1:332879455079:android:15c36642c62d13e0dd05c2",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

if platform == 'android':
    from android.runnable import run_on_ui_thread
    from jnius import autoclass, PythonJavaClass, java_method
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    Activity = autoclass('org.kivy.android.PythonActivity').mActivity

    class JSInterface(PythonJavaClass):
        __javainterfaces__ = ['java/lang/Object']
        def __init__(self, callback):
            super().__init__()
            self.callback = callback
        @java_method('(Ljava/lang/String;Ljava/lang/String;)V')
        def send_to_python(self, action, data):
            self.callback(action, data)
else:
    def run_on_ui_thread(f): return f

class GhostApp(App):
    def build(self):
        Clock.schedule_once(self.create_webview, 0.5)
        return None

    @run_on_ui_thread
    def create_webview(self, dt):
        self.webview = WebView(Activity)
        s = self.webview.getSettings()
        s.setJavaScriptEnabled(True)
        s.setDomStorageEnabled(True)
        s.setAllowFileAccess(True)
        self.webview.setWebViewClient(WebViewClient())
        self.interface = JSInterface(self.on_js_call)
        self.webview.addJavascriptInterface(self.interface, "Kivy")
        self.webview.loadUrl("file:///android_asset/index.html")
        Activity.setContentView(self.webview)

    def on_js_call(self, action, data_json):
        data = json.loads(data_json)
        e, p = data.get('e'), data.get('p')

        if action == 'register':
            try:
                user = auth.create_user_with_email_and_password(e, p)
                auth.send_email_verification(user['idToken'])
                self.run_js(f"log('2FA: Письмо отправлено на {e}')")
            except Exception as ex:
                self.run_js(f"log('Ошибка: {str(ex)}', '#f00')")

        elif action == 'login':
            try:
                user = auth.sign_in_with_email_and_password(e, p)
                info = auth.get_account_info(user['idToken'])
                if info['users'][0]['emailVerified']:
                    self.run_js("log('ДОСТУП РАЗРЕШЕН. Ghost онлайн.', '#0f0')")
                else:
                    self.run_js("log('Подтвердите Email для входа!', '#ff0')")
            except Exception as ex:
                self.run_js(f"log('Вход запрещен: {str(ex)}', '#f00')")

    @run_on_ui_thread
    def run_js(self, code):
        self.webview.evaluateJavascript(code, None)

if __name__ == "__main__":
    GhostApp().run()
