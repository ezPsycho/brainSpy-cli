# -*- mode: python -*-

import os
import sys
sys.path.append('./src')

welcome = '''
 _ __                   __,            
( /  )         o       (               
 /--< _   __, ,  _ _    `.   ,_   __  ,
/___// (_(_/(_(_/ / /_(___)_/|_)_/ (_/_
                            /|      /  
Packaging Script           (/      '   

==========================================

Prepareing for packaging your files, please wait...

'''

print(welcome)

from PyInstaller.utils.hooks import collect_submodules

hiddenimports = []

for _ in ['producers', 'readers', 'parsers']:
    hiddenimports = hiddenimports + collect_submodules(_)

block_cipher = None


a = Analysis(['src\\brainSpy.py'],
             pathex=[os.path.abspath(SPECPATH)],
             binaries=[],
             datas=[],
             hiddenimports=hiddenimports,
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='brainSpy',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True , icon='etc\\assets\\brainSpy_win32.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='brainSpy')
