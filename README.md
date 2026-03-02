# ConverterIMG
Converting .webp &amp; .heic to jpeg

# Image Converter

Конвертер WEBP/HEIC в JPEG с простым GUI.

## 🚀 Быстрый старт

### Вариант 1: Готовый EXE
1. Скачайте `Image_Converter.exe` из [Releases](https://github.com/yourusername/image-converter/releases)
2. Запустите!

### Вариант 2: Сборка из исходников
```bash
# Установка
pip install Pillow pillow-heif pyinstaller

# Сборка
pyinstaller --onefile --noconsole --name "Image_Converter" converter_gui.py

# Или просто запустите build_gui.bat
```

## ✨ Возможности

- ✅ **WEBP → JPEG** - базовая конвертация
- ✅ **HEIC → JPEG** - поддержка Apple формата
- ✅ **Автоудаление** оригиналов (опционально)
- ✅ **Запоминает** последнюю папку
- ✅ **Пакетная обработка**
- ✅ **Простой интерфейс**

## 📦 Зависимости

- Python 3.7+
- Pillow
- pillow-heif (для HEIC)
- tkinter (встроен)

## 📁 Файлы

- `converter_gui.py` - программа
- `build.bat` - скрипт сборки
- `converter_config.json` - настройки

---
MIT License
