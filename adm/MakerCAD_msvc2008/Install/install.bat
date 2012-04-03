@REM Usage: install.bat solution_dir

del %~2\script\*.* /s /q
xcopy ..\..\..\MakerCAD\script %~2\script /s /e /y
xcopy ..\%~2\MakerCAD.exe %~2\ /y