[app]

# (str) Title of your application
# METS ICI LE NOM DE TON APPLICATION
title = Poker Mind Coach

# (str) Package name
# METS ICI UN NOM TECHNIQUE COURT, MINUSCULES, SANS ESPACES
package.name = pokermindcoach

# (str) Package domain (needed for android/ios packaging)
# METS ICI QUELQUE CHOSE D'UNIQUE (ex: com.tonpseudo.app)
package.domain = com.AlmenakZ

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
# IMPORTANT : S'assurer que 'py' et 'ttf' sont inclus
source.include_exts = py,png,jpg,kv,atlas,ttf

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin, venv

# (list) List of exclusions using pattern matching
# Do not prefix with './'
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 0.1

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# On spécifie la version de Kivy
requirements = python3,kivy==2.3.1

# (str) Custom source folders for requirements
# requirements.source.kivy = ../../kivy

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (list) Supported orientations
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
# On met juste INTERNET pour l'instant
android.permissions = INTERNET

# (list) features (adds uses-feature -tags to manifest)
#android.features = android.hardware.usb.host

# (int) Target Android API, should be as high as possible.
# Laisser commenté pour que Buildozer choisisse par défaut (souvent 33 ou 34)
#android.api = 33

# (int) Minimum API your APK / AAB will support.
# Laisser commenté pour que Buildozer choisisse par défaut (souvent 21)
#android.minapi = 21

# (int) Android SDK version to use (LAISSER COMMENTÉ, Buildozer gère)
#android.sdk = 27

# (str) Android NDK version to use
# On spécifie la version 25b qui est stable
android.ndk = 25b

# (str) Android build tools version to use
# On spécifie la version 33.0.2 qui est stable
android.build_tools_version = 33.0.2

# (int) Android NDK API to use.
# Laisser commenté pour que Buildozer choisisse (doit correspondre à minapi)
#android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
# android.private_storage = True # Défaut est True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_path =

# (bool) If True, then skip trying to update the Android sdk
# android.skip_update = False # Laisser Buildozer mettre à jour si besoin

# (bool) If True, then automatically accept SDK license
# !!! IMPORTANT pour GitHub Actions !!!
android.accept_sdk_license = True

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.kivy.android.PythonActivity

# (str) Android app theme, default is ok for Kivy-based app
# android.apptheme = "@android:style/Theme.NoTitleBar"

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# On inclut 64 et 32 bits pour une meilleure compatibilité
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) The format used to package the app for release mode (aab or apk or aar).
# android.release_artifact = aab # aab est le format préféré pour le Play Store

# (str) The format used to package the app for debug mode (apk or aar).
# android.debug_artifact = apk # apk pour les tests directs

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
# Mettre 2 pour avoir un maximum d'infos en cas d'erreur
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
# bin_dir = ./bin

