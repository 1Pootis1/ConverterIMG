@echo off
chcp 65001 >nul
title Сборка EXE

echo ========================================
echo     СБОРКА EXE ФАЙЛА
echo ========================================
echo.


python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не установлен!
    pause
    exit /b
)


echo Установка PyInstaller...
python -m pip install --upgrade pip
python -m pip install pyinstaller


echo Установка поддержки HEIC...
python -m pip install pillow-heif


echo.
echo Создание EXE файла...
echo.

python -m PyInstaller --onefile ^
                     --noconsole ^
                     --name "Image_Converter" ^
                     --hidden-import PIL ^
                     --hidden-import PIL._webp ^
                     --hidden-import PIL.Image ^
                     --hidden-import PIL.ImageFile ^
                     --hidden-import pillow_heif ^
                     --hidden-import pillow_heif._plugin ^
                     converter_gui.py


if exist dist\Image_Converter.exe (
    echo.
    echo ✅ EXE файл успешно создан!
    copy dist\Image_Converter.exe .\
    echo ✅ EXE скопирован в текущую папку
    
    
    rmdir /s /q build 2>nul
    rmdir /s /q dist 2>nul
    del *.spec 2>nul
    
    echo.
    echo Файл готов: Image_Converter.exe
) else (
    echo.
    echo ❌ Ошибка при создании EXE
)

echo.
echo ========================================
pause