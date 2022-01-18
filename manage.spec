# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['manage.py'],
             pathex=['E:\\PythonCode\\survivalmodel'],
             binaries=[],
             datas=[(r'E:\PythonCode\survivalmodel\generateapp\templates', r'.\generateapp\templates'),
             (r'E:\PythonCode\survivalmodel\static\static_root', r'.\static\static_root'),
             (r'E:\PythonCode\survivalmodel\generateapp\data', r'./generateapp\data')],
             hiddenimports=['scipy.special.cython_special','tensorflow.contrib','generateapp.urls'],
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
          name='manage',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='manage')
