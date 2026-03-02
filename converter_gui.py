import os
import sys
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import subprocess

class WebpConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Конвертер WEBP/HEIC в JPEG")
        self.root.geometry("550x320")
        self.root.resizable(False, False)
        
        self.config_file = os.path.join(
            os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__), 
            'converter_config.json'
        )
        
        config = self.load_config()
        self.folder_path = tk.StringVar(value=config.get('folder_path', r'D:\Сайт'))
        self.skip_confirmation = tk.BooleanVar(value=config.get('skip_confirmation', True))
        self.delete_original = tk.BooleanVar(value=config.get('delete_original', True))
        
        self.heic_support = self.check_heic_support()
        
        self.create_widgets()
        
        self.center_window()
        
    def check_heic_support(self):
        """Проверяет наличие библиотеки для HEIC"""
        try:
            import pillow_heif

            from pillow_heif import register_heif_opener
            register_heif_opener()
            return True
        except ImportError:
            return False
    
    def install_heic_support(self):
        """Устанавливает поддержку HEIC"""
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow-heif"])
            import pillow_heif
            from pillow_heif import register_heif_opener
            register_heif_opener()
            return True
        except:
            return False
    
    def load_config(self):
        """Загружает настройки из файла"""
        default_config = {
            'folder_path': r'D:\Сайт',
            'skip_confirmation': True,
            'delete_original': True
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return config
        except:
            pass
        return default_config
    
    def save_config(self):
        """Сохраняет настройки в файл"""
        try:
            config = {
                'folder_path': self.folder_path.get(),
                'skip_confirmation': self.skip_confirmation.get(),
                'delete_original': self.delete_original.get()
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
        except:
            pass
    
    def center_window(self):
        """Центрирует окно на экране"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Создает элементы интерфейса"""
        
        top_padding = ttk.Frame(self.root, height=10)
        top_padding.pack()
        
        folder_frame = ttk.Frame(self.root, padding="10")
        folder_frame.pack(fill=tk.X)
        
        ttk.Label(folder_frame, text="Папка для обработки:", font=('Arial', 10)).pack(anchor=tk.W)
        
        path_frame = ttk.Frame(folder_frame)
        path_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.path_entry = ttk.Entry(path_frame, textvariable=self.folder_path, font=('Arial', 9))
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        ttk.Button(path_frame, text="Обзор...", command=self.browse_folder).pack(side=tk.RIGHT)
        
        settings_frame = ttk.LabelFrame(self.root, text=" Настройки ", padding="10")
        settings_frame.pack(fill=tk.X, padx=10, pady=10)
        
        confirm_check = ttk.Checkbutton(
            settings_frame, 
            text="Запрашивать подтверждение перед конвертацией",
            variable=self.skip_confirmation,
            command=self.save_config
        )
        confirm_check.pack(anchor=tk.W, pady=2)
        
        delete_check = ttk.Checkbutton(
            settings_frame, 
            text="Удалять оригинальные файлы после конвертации",
            variable=self.delete_original,
            command=self.save_config
        )
        delete_check.pack(anchor=tk.W, pady=2)
        
        heic_frame = ttk.Frame(settings_frame)
        heic_frame.pack(anchor=tk.W, pady=5)
        
        if self.heic_support:
            ttk.Label(heic_frame, text="✓ HEIC поддержка: ДА", foreground='green').pack(side=tk.LEFT)
        else:
            ttk.Label(heic_frame, text="✗ HEIC поддержка: НЕТ", foreground='red').pack(side=tk.LEFT)
            ttk.Button(heic_frame, text="Установить HEIC поддержку", 
                      command=self.install_heic_support_prompt).pack(side=tk.LEFT, padx=(10, 0))
        
        button_frame = ttk.Frame(self.root)
        button_frame.pack(expand=True, fill=tk.BOTH, pady=10)
        
        self.convert_btn = tk.Button(
            button_frame,
            text="КОНВЕРТИРОВАТЬ",
            font=('Arial', 14, 'bold'),
            bg='#4CAF50',
            fg='white',
            activebackground='#45a049',
            activeforeground='white',
            relief=tk.RAISED,
            bd=3,
            padx=40,
            pady=15,
            cursor='hand2',
            command=self.convert_files
        )
        self.convert_btn.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        status_frame = ttk.Frame(self.root, relief=tk.SUNKEN, padding=(5, 2))
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = ttk.Label(status_frame, text="Готов к работе")
        self.status_label.pack(side=tk.LEFT)
        
        formats_label = ttk.Label(status_frame, text="Поддерживаемые форматы: WEBP, HEIC", foreground='gray')
        formats_label.pack(side=tk.RIGHT)
    
    def install_heic_support_prompt(self):
        """Запрашивает подтверждение и устанавливает HEIC поддержку"""
        if messagebox.askyesno("Установка HEIC поддержки", 
                              "Для поддержки HEIC формата требуется установить библиотеку pillow-heif.\n\n"
                              "Установить сейчас?"):
            self.update_status("Установка HEIC поддержки...")
            self.root.update()
            
            if self.install_heic_support():
                self.heic_support = True
                messagebox.showinfo("Успешно", "HEIC поддержка успешно установлена!\nПерезапустите программу.")
                self.update_status("HEIC поддержка установлена. Перезапустите программу.")
            else:
                messagebox.showerror("Ошибка", "Не удалось установить HEIC поддержку.\n"
                                    "Попробуйте установить вручную:\n"
                                    "pip install pillow-heif")
                self.update_status("Ошибка установки HEIC поддержки")
    
    def browse_folder(self):
        """Открывает диалог выбора папки"""
        folder = filedialog.askdirectory(
            title="Выберите папку с изображениями",
            initialdir=self.folder_path.get() if os.path.exists(self.folder_path.get()) else os.path.expanduser("~")
        )
        if folder:
            self.folder_path.set(folder)
            self.save_config()
            self.update_status(f"Выбрана папка: {os.path.basename(folder)}")
    
    def update_status(self, message, is_error=False):
        """Обновляет статус"""
        self.status_label.config(text=message)
        self.root.update()
    
    def get_image_files(self, folder):
        """Возвращает список WEBP и HEIC файлов в папке"""
        image_files = []
        for file in os.listdir(folder):
            lower_file = file.lower()
            if lower_file.endswith('.webp') or lower_file.endswith('.heic'):
                image_files.append(file)
        return image_files
    
    def convert_files(self):
        """Конвертирует файлы"""
        folder = self.folder_path.get()
        
        if not os.path.exists(folder):
            messagebox.showerror("Ошибка", f"Папка не существует:\n{folder}")
            self.update_status("Ошибка: папка не найдена")
            return
        
        image_files = self.get_image_files(folder)
        
        if not image_files:
            messagebox.showinfo("Информация", f"В папке не найдены WEBP или HEIC файлы")
            self.update_status("Файлы не найдены")
            return
        
        heic_files = [f for f in image_files if f.lower().endswith('.heic')]
        webp_files = [f for f in image_files if f.lower().endswith('.webp')]
        
        if heic_files and not self.heic_support:
            messagebox.showerror(
                "Ошибка", 
                "Найдены HEIC файлы, но не установлена поддержка HEIC.\n\n"
                "Нажмите кнопку 'Установить HEIC поддержку' в настройках."
            )
            return
        
        if self.skip_confirmation.get():
            heic_text = f"\nHEIC файлов: {len(heic_files)}" if heic_files else ""
            webp_text = f"\nWEBP файлов: {len(webp_files)}" if webp_files else ""
            
            result = messagebox.askyesno(
                "Подтверждение",
                f"Найдено файлов: {len(image_files)}\n"
                f"{webp_text}{heic_text}\n\n"
                f"Будет выполнено:\n"
                f"• Конвертация в JPEG\n"
                f"{'• Удаление оригиналов' if self.delete_original.get() else '• Оригиналы будут сохранены'}\n\n"
                f"Продолжить?"
            )
            if not result:
                self.update_status("Операция отменена")
                return
        
        self.update_status("Конвертация...")
        self.convert_btn.config(state='disabled')
        self.root.update()
        
        converted = 0
        errors = 0
        error_files = []
        
        for filename in image_files:
            input_path = os.path.join(folder, filename)
            jpeg_path = os.path.join(folder, os.path.splitext(filename)[0] + '.jpg')
            
            try:
                
                with Image.open(input_path) as img:
                    
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    img.save(jpeg_path, 'JPEG', quality=95, optimize=True)
                
                
                if os.path.exists(jpeg_path) and os.path.getsize(jpeg_path) > 0:
                    if self.delete_original.get():
                        os.remove(input_path)
                    converted += 1
                else:
                    errors += 1
                    error_files.append(filename)
                    
            except Exception as e:
                errors += 1
                error_files.append(f"{filename} (ошибка)")
        
        
        self.convert_btn.config(state='normal')
        
        delete_text = " и удалены" if self.delete_original.get() else ""
        
        if errors == 0:
            messagebox.showinfo(
                "Готово!",
                f"Конвертировано файлов: {converted}\n"
                f"Оригиналы{delete_text}."
            )
            self.update_status(f"Готово: {converted} файлов конвертировано")
        else:
            error_text = "\n".join(error_files[:5])
            if len(error_files) > 5:
                error_text += f"\n...и еще {len(error_files) - 5}"
            
            messagebox.showwarning(
                "Завершено с ошибками",
                f"Успешно: {converted}\n"
                f"Ошибок: {errors}\n\n"
                f"Проблемные файлы:\n{error_text}"
            )
            self.update_status(f"Завершено: {converted} успешно, {errors} ошибок")

def main():
    root = tk.Tk()
    app = WebpConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()