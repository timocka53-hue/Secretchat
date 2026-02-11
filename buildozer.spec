[app]
title = GhostChat
package.name = ghost.messenger.secure
package.domain = org.ghost
source.dir = .
source.include_exts = py,png,jpg,kv
version = 1.0

# ВАЖНО: Добавлены все нужные библиотеки для красоты и защиты
requirements = python3,kivy==2.2.1,kivymd,requests,cryptography,urllib3,certifi

orientation = portrait
android.api = 33
android.minapi = 21
icon.filename = icon.png

# Права только на интернет
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE


