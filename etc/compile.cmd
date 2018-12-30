cd ..
rmdir "dist/brainSpy" /S /Q
pyinstaller ./brainSpy.py --icon=etc/assets/brainSpy_win32.ico
cd modules/brainSpy
cd ..
rmdir "__pycache__" /S /Q
cd ..
md "dist/brainSpy/modules/brainspy"
xcopy "modules/brainspy" "dist/brainSpy/modules/brainspy" /Y /S
cd "dist/brainSpy"
del "VCRUNTIME140.dll"
cd "modules/brainSpy/data"
del "*.zip"
cd ../../../../