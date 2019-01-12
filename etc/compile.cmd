cd ..
rmdir "dist\brainSpy" /S /Q 
pyinstaller ./brainSpy.spec
mkdir "dist\brainSpy\data"
xcopy ".\src\data" ".\dist\brainSpy\data" /S /Y
cd "dist\brainSpy"
del "VCRUNTIME140.dll" /Q
cd ../..