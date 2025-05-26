from setuptools import setup
import os

APP = ['main.py']
DATA_FILES = [('', ['assets'])] if os.path.exists('assets') else []
OPTIONS = {
    'argv_emulation': False,
    'packages': ['pygame'],
    'includes': ['pygame'],
    'excludes': ['tkinter'],
    'iconfile': 'icon.png' if os.path.exists('icon.png') else None,
    'plist': {
        'CFBundleIdentifier': 'com.yourdomain.platformer',
        'CFBundleName': 'Platformer',
        'CFBundleShortVersionString': '1.0.0',
        'LSMinimumSystemVersion': '10.13.0',
        'NSHighResolutionCapable': True,
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    name="Platformer",
)
