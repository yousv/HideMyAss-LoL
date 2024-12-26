import PyInstaller.__main__
import os

icon_path = os.path.abspath("app.ico")

PyInstaller.__main__.run([
    'hma-lol.py',
    '--onefile',
    '--noconsole',
    '--uac-admin',
    '--manifest', 'admin_manifest.xml',
    '--name', 'HideMyAss LoL',
    '--icon', icon_path,
    '--add-data', f'{icon_path};.'
])
