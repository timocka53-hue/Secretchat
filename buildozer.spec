[app]
title = Ghost
package.name = ghost.dev.core.final
package.domain = org.ghost
source.dir = .
source.include_exts = py,png,jpg,kv,html,js,json
version = 1.3

# Добавил системные утилиты Python для веса
requirements = python3,kivy==2.2.1,pyjnius,android,requests,pyrebase4,urllib3,certifi,openssl,hostpython3,sqlite3,setuptools,six,pbr

orientation = portrait
android.api = 34
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

android.permissions = INTERNET, ACCESS_NETWORK_STATE, POST_NOTIFICATIONS
android.manifest.uses_cleartext_traffic = True
android.accept_sdk_license = True
android.presplash_color = #000000
presplash.filename = 
icon.filename = icon.png

[buildozer]
log_level = 2
warn_on_root = 1
