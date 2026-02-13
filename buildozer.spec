[app]
title = Ghost_Pro
package.name = ghost.pro.secure
package.domain = org.ghost.dev
source.dir = .
source.include_exts = py,png,jpg,kv,html,js,json
version = 2.0

# Добавляем 'openssl' и 'requests' в самое начало, это заставит билд весить больше
requirements = python3,kivy==2.2.1,openssl,requests,pyjnius,android,pyrebase4,urllib3,certifi,hostpython3,sqlite3

orientation = portrait
android.api = 34
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a

android.permissions = INTERNET, ACCESS_NETWORK_STATE
android.manifest.uses_cleartext_traffic = True
android.accept_sdk_license = True
android.presplash_color = #000000

[buildozer]
log_level = 2
warn_on_root = 1

