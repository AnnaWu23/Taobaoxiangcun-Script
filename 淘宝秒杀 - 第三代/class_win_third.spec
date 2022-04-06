# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['class_win_third.py'],
             pathex=['HttpPorxy.py', 'LocalDatabase.py', 'NetDataBase.py', 'D:\\CODE\\VS_CODE\\PYTHON\\Taobaoxiangcun-Script\\淘宝秒杀 - 第三代'],
             binaries=[],
             datas=[],
             hiddenimports=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='class_win_third',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='taobao.ico')
