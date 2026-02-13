import os, json, certifi, pyrebase
from kivy.app import App
from kivy.utils import platform
from kivy.clock import Clock

os.environ['SSL_CERT_FILE'] = certifi.where()

firebase_config = {
    "apiKey": "AIzaSyAbiRCuR9egtHKg0FNzzBdL9dNqPqpPLNk",
    "authDomain": "ghost-pro-5aa22.firebaseapp.com",
    "projectId": "ghost-pro-5aa22",
    "storageBucket": "ghost-pro-5aa22.firebasestorage.app",
    "messagingSenderId": "332879455079",
    "appId": "1:332879455079:android:15c36642c62d13e0dd05c2",
    "databaseURL": ""
}

try:
    auth = pyrebase.initialize_app(firebase_config).auth()
except:
    auth = None

if platform == 'android':
    from android.runnable import run_on_ui_thread
    from jnius import autoclass, PythonJavaClass, java_method
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    Activity = autoclass('org.kivy.android.PythonActivity').mActivity

    class JSInterface(PythonJavaClass):
        __javainterfaces__ = ['java/lang/Object']
        def __init__(self, cb):
            super().__init__()
            self.cb = cb
        @java_method('(Ljava/lang/String;Ljava/lang/String;)V')
        def send_to_python(self, a, d): self.cb(a, d)
else:
    def run_on_ui_thread(f): return f

class GhostApp(App):
    def build(self):
        Clock.schedule_once(self.create_webview, 0.5)
        return None

    @run_on_ui_thread
    def create_webview(self, dt):
        self.wv = WebView(Activity)
        self.wv.getSettings().setJavaScriptEnabled(True)
        self.wv.getSettings().setDomStorageEnabled(True)
        self.wv.setWebViewClient(WebViewClient())
        self.interface = JSInterface(self.on_js)
        self.wv.addJavascriptInterface(self.interface, "Kivy")
        self.wv.loadUrl("file:///android_asset/index.html")
        Activity.setContentView(self.wv)

    def on_js(self, action, data_json):
        if not auth: return
        d = json.loads(data_json)
        e, p = d.get('e'), d.get('p')
        try:
            if action == 'register':
                user = auth.create_user_with_email_and_password(e, p)
                auth.send_email_verification(user['idToken'])
                self.run_js(f"log('2FA: Письмо отправлено на {e}')")
            elif action == 'login':
                user = auth.sign_in_with_email_and_password(e, p)
                if auth.get_account_info(user['idToken'])['users'][0]['emailVerified']:
                    self.run_js("log('ДОСТУП РАЗРЕШЕН', '#0f0')")
                else:
                    self.run_js("log('Сначала подтвердите почту!', '#ff0')")
        except Exception as ex:
            self.run_js(f"log('Ошибка: {str(ex)[:40]}', '#f00')")

    @run_on_ui_thread
    def run_js(self, code):
        try: self.wv.evaluateJavascript(code, None)
        except: pass

if __name__ == "__main__":
    GhostApp().run()
