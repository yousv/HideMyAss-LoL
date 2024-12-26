import PyInstaller.__main__
import os

# Add the icon path
icon_path = os.path.abspath("app.ico")

PyInstaller.__main__.run([
    'status_manager.py',
    '--onefile',
    '--noconsole',
    '--uac-admin',
    '--manifest', 'admin_manifest.xml',
    '--name', 'LoLStatusManager',
    '--icon', icon_path,
    '--add-data', f'{icon_path};.'
])
