import sys
import os
import json
import platform
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QFileDialog, QMessageBox, QRadioButton, QSlider, QProgressBar,
    QTextEdit, QGroupBox, QButtonGroup, QGridLayout, QSpacerItem, QSizePolicy,
    QDialog, QFormLayout, QCheckBox, QComboBox, QScrollArea, QFrame, QTreeWidget, 
    QTreeWidgetItem, QSplitter, QHeaderView, QListWidget, QListWidgetItem
)
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPalette, QColor, QImage, QFontDatabase
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QDir
from psd_tools import PSDImage
from PIL import Image
from bidi.algorithm import get_display
import arabic_reshaper

# ==================== تنظیمات و تم ====================
SETTINGS_FILE = "psd_extractor_settings.json"
#ICONS_DIR = "icons"#

# تعیین مسیر منابع (برای حالت exe و حالت عادی)
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

ICONS_DIR = resource_path("icons")
FONT_PATH = resource_path("fonts/vazirmatn.ttf")

DEFAULT_SETTINGS = {
    "quality": 95,
    "preview_enabled": True,
    "output_format": "png",
    "theme": "light",
    "language": "en",
    "layer_mode": "all",
    "extract_groups": True,
    "preserve_structure": True
}

THEMES = {
    "dark": {
        "bg": "#1a1a2e", "fg": "#16213e", "accent": "#0f3460", "secondary": "#e94560",
        "text": "#ffffff", "success": "#00b894", "warning": "#fdcb6e", "error": "#e84393",
        "border": "#37474f", "progress": "#00cec9", "tree_bg": "#0f0f1a"
    },
    "light": {
        "bg": "#f8f9fa", "fg": "#ffffff", "accent": "#4dabf7", "secondary": "#ff8787",
        "text": "#212529", "success": "#51cf66", "warning": "#ffd43b", "error": "#ff6b6b",
        "border": "#dee2e6", "progress": "#339af0", "tree_bg": "#e9ecef"
    }
}

TEXTS = {
    "fa": {
        "app_title": "استخراج کننده حرفه ای لایه های PSD",
        "settings": "تنظیمات",
        "about": "درباره برنامه",
        "select_psd": "انتخاب فایل PSD:",
        "select_output": "انتخاب پوشه خروجی:",
        "browse": "مرور...",
        "output_format": "فرمت خروجی:",
        "start_extraction": "شروع استخراج لایه ها",
        "start_selected_extraction": "استخراج لایه های انتخاب شده",
        "stop_extraction": "توقف استخراج",
        "ready": "آماده به کار",
        "processing": "در حال پردازش...",
        "console": "کنترل عملیات",
        "clear_console": "پاک کردن کنسول",
        "open_output": "باز کردن پوشه خروجی",
        "preview": "پیش نمایش لایه ها",
        "analyze": "تحلیل فایل",
        "layer_mode": "نوع لایه ها:",
        "visible_layers": "فقط لایه های قابل مشاهده",
        "hidden_layers": "فقط لایه های مخفی",
        "all_layers": "همه لایه ها",
        "quality": "کیفیت خروجی:",
        "preview_enabled": "فعال سازی پیش نمایش",
        "theme": "تم برنامه:",
        "dark": "تیره", "light": "روشن", "system": "سیستم",
        "language": "زبان برنامه:",
        "apply": "اعمال تنظیمات", "cancel": "انصراف", "reset": "بازنشانی",
        "preview_title": "پیش نمایش لایه ها",
        "layer_info": "اطلاعات لایه",
        "name": "نام:", "type": "نوع:", "size": "ابعاد:", "position": "موقعیت:",
        "visibility": "وضعیت:", "visible": "قابل مشاهده", "hidden": "مخفی",
        "extract": "استخراج", "success": "موفقیت", "error": "خطا",
        "warning": "هشدار", "info": "اطلاعات",
        "layers_found": "لایه پیدا شد", "layers_processed": "لایه پردازش شد",
        "extraction_complete": "استخراج با موفقیت انجام شد",
        "file_analyzed": "فایل با موفقیت تحلیل شد",
        "no_file_selected": "لطفاً یک فایل PSD انتخاب کنید",
        "no_output_selected": "لطفاً پوشه خروجی را انتخاب کنید",
        "no_layers_found": "هیچ لایه ای در فایل پیدا نشد",
        "no_layers_selected": "هیچ لایه ای انتخاب نشده است",
        "layer": "لایه", "saved": "ذخیره شد", "in": "در", "of": "از",
        "about_title": "درباره برنامه",
        "about_content": """استخراج کننده حرفه ای لایه های PSD

نسخه: ۲.۰
توسعه دهنده: امین محمدی
وبسایت: www.artika.ir

قابلیت های برنامه:
• استخراج لایه های PSD به فرمت های مختلف
• پیش نمایش حرفه ای لایه ها
• پشتیبانی از زبان فارسی و انگلیسی
• رابط کاربری مدرن و واکنش گرا
• تنظیمات پیشرفته کیفیت
• پشتیبانی از لایه های مختلف

قدرت گرفته از: Python • PyQt5 • PSD-Tools""",
        "close": "بستن",
        "settings_applied": "تنظیمات با موفقیت اعمال شد",
        "loading": "در حال بارگذاری...",
        "select_file": "انتخاب فایل",
        "select_folder": "انتخاب پوشه",
        "file_info": "اطلاعات فایل",
        "total_layers": "تعداد کل لایه ها",
        "layer_structure": "ساختار لایه ها",
        "extract_groups": "استخراج پوشه ها به عنوان لایه",
        "preserve_structure": "حفظ ساختار پوشه ها در خروجی",
        "group": "پوشه",
        "layers_in_group": "لایه ها در پوشه",
        "export_structure": "حفظ ساختار پوشه ها در خروجی",
        "selected_layers": "لایه های انتخاب شده",
        "select_all": "انتخاب همه",
        "deselect_all": "لغو انتخاب همه",
        "selected": "انتخاب شده",
        "empty_image": "تصویر خالی",
        "extraction_stopped": "استخراج متوقف شد",
        "progress": "پیشرفت",
        "preview_layer": "پیش نمایش لایه"
    },
    "en": {
        "app_title": "Professional PSD Layer Extractor",
        "settings": "Settings",
        "about": "About",
        "select_psd": "Select PSD File:",
        "select_output": "Select Output Folder:",
        "browse": "Browse...",
        "output_format": "Output Format:",
        "start_extraction": "Start Extraction",
        "start_selected_extraction": "Extract Selected Layers",
        "stop_extraction": "Stop Extraction",
        "ready": "Ready",
        "processing": "Processing...",
        "console": "Operation Console",
        "clear_console": "Clear Console",
        "open_output": "Open Output Folder",
        "preview": "Preview Layers",
        "analyze": "Analyze File",
        "layer_mode": "Layer Mode:",
        "visible_layers": "Visible Layers Only",
        "hidden_layers": "Hidden Layers Only",
        "all_layers": "All Layers",
        "quality": "Output Quality:",
        "preview_enabled": "Enable Preview",
        "theme": "Theme:",
        "dark": "Dark", "light": "Light", "system": "System",
        "language": "Language:",
        "apply": "Apply Settings", "cancel": "Cancel", "reset": "Reset",
        "preview_title": "Layer Preview",
        "layer_info": "Layer Information",
        "name": "Name:", "type": "Type:", "size": "Size:", "position": "Position:",
        "visibility": "Visibility:", "visible": "Visible", "hidden": "Hidden",
        "extract": "Extract", "success": "Success", "error": "Error",
        "warning": "Warning", "info": "Info",
        "layers_found": "layers found", "layers_processed": "layers processed",
        "extraction_complete": "Extraction completed successfully",
        "file_analyzed": "File analyzed successfully",
        "no_file_selected": "Please select a PSD file",
        "no_output_selected": "Please select output folder",
        "no_layers_found": "No layers found in file",
        "no_layers_selected": "No layers selected",
        "layer": "Layer", "saved": "saved", "in": "in", "of": "of",
        "about_title": "About Application",
        "about_content": """Professional PSD Layer Extractor

Version: 2.0
Developer: Amin Mohammadi
Website: www.artika.ir

Features:
• Extract PSD layers to various formats
• Professional layer preview
• Persian & English language support
• Modern responsive UI
• Advanced quality settings
• Support for different layer types

Powered by: Python • PyQt5 • PSD-Tools""",
        "close": "Close",
        "settings_applied": "Settings applied successfully",
        "loading": "Loading...",
        "select_file": "Select File",
        "select_folder": "Select Folder",
        "file_info": "File Information",
        "total_layers": "Total Layers",
        "layer_structure": "Layer Structure",
        "extract_groups": "Extract groups as layers",
        "preserve_structure": "Preserve folder structure in output",
        "group": "Group",
        "layers_in_group": "Layers in group",
        "export_structure": "Preserve folder structure in output",
        "selected_layers": "Selected Layers",
        "select_all": "Select All",
        "deselect_all": "Deselect All",
        "selected": "Selected",
        "empty_image": "Empty image",
        "extraction_stopped": "Extraction stopped",
        "progress": "Progress",
        "preview_layer": "Preview Layer"
    }
}

# ==================== کلاس فونت ====================
class FontManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FontManager, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance
    
    def __init__(self):
        if not self.initialized:
            self.font_family = "Vazirmatn"
            self.initialized = True
    
    def setup_fonts(self):
        """این متد باید بعد از ایجاد QApplication فراخوانی شود"""
        try:
            # اضافه کردن فونت به سیستم
            font_id = QFontDatabase.addApplicationFont(FONT_PATH)
            
            if font_id != -1:
                font_families = QFontDatabase.applicationFontFamilies(font_id)
                if font_families:
                    self.font_family = font_families[0]
                    print(f"فونت {self.font_family} با موفقیت بارگذاری شد")
                    return True
                else:
                    print("خطا در بارگذاری فونت Vazirmatn: فونت خانواده یافت نشد")
                    return False
            else:
                print("خطا در افزودن فونت Vazirmatn به برنامه")
                return False
        except Exception as e:
            print(f"خطا در راه اندازی فونت: {e}")
            return False
    
    def get_font(self, size=10, weight=QFont.Normal):
        """دریافت فونت با سایز و وزن مشخص"""
        try:
            font = QFont(self.font_family, size, weight)
            font.setStyleStrategy(QFont.PreferAntialias)
            return font
        except:
            # اگر فونت بارگذاری نشد، از فونت پیشفرض سیستم استفاده کن
            return QFont("Tahoma", size, weight)

# ایجاد نمونه فونت منیجر (اما setup_fonts بعداً فراخوانی می شود)
font_manager = FontManager()


# ==================== کلاس های کمکی ====================
class RTLLabel(QLabel):
    def __init__(self, text="", lang="fa", font_size=10):
        super().__init__(text)
        self.lang = lang
        self.setAlignment(Qt.AlignRight | Qt.AlignVCenter if lang == "fa" else Qt.AlignLeft | Qt.AlignVCenter)
        
        # تنظیم فونت
        font = font_manager.get_font(font_size)
        self.setFont(font)
        
        self.setText(text)

    def setText(self, text):
        if self.lang == "fa":
            try:
                reshaped = arabic_reshaper.reshape(text)
                super().setText(get_display(reshaped))
            except Exception as e:
                print(f"خطا در reshape متن: {e}")
                super().setText(text)
        else:
            super().setText(text)

class RTLText:
    @staticmethod
    def reshape(text):
        if any('\u0600' <= c <= '\u06FF' for c in text):
            try:
                return get_display(arabic_reshaper.reshape(text))
            except:
                return text
        return text

class LayerTreeWidget(QTreeWidget):
    def __init__(self, lang="fa"):
        super().__init__()
        self.lang = lang
        self.setHeaderLabels([TEXTS[lang]["layer_structure"]])
        self.setColumnCount(1)
        self.setFont(font_manager.get_font(9))
        self.setStyleSheet(f"""
            QTreeWidget {{
                background-color: {THEMES["dark"]["tree_bg"]};
                color: white;
                border: 1px solid {THEMES["dark"]["border"]};
                border-radius: 8px;
            }}
            QTreeWidget::item {{
                padding: 5px;
                border-bottom: 1px solid {THEMES["dark"]["bg"]};
            }}
            QTreeWidget::item:selected {{
                background-color: {THEMES["dark"]["accent"]};
            }}
        """)

class ExtractionThread(QThread):
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    log = pyqtSignal(str, str)
    finished = pyqtSignal()
    stopped = pyqtSignal()

    def __init__(self, psd_path, output_dir, settings, texts, selected_layers=None):
        super().__init__()
        self.psd_path = psd_path
        self.output_dir = output_dir
        self.settings = settings
        self.texts = texts
        self.selected_layers = selected_layers  # لیست لایه های انتخاب شده
        self._is_running = True

    def stop(self):
        self._is_running = False

    def extract_layer_with_structure(self, layer, base_path, counter, parent_path="", depth=0):
        """تابع بازگشتی برای استخراج لایه ها با حفظ ساختار پوشه ها"""
        if not self._is_running:
            return counter

        try:
            if layer.is_group():
                # اگر پوشه است و گزینه extract_groups فعال باشد
                if self.settings.get("extract_groups", True):
                    # ایجاد پوشه متناظر
                    group_name = "".join(c for c in layer.name if c.isalnum() or c in (' ', '-', '_')).strip()
                    if not group_name:
                        group_name = f"group_{depth}"
                    
                    # ایجاد مسیر کامل پوشه
                    if self.settings.get("preserve_structure", True):
                        group_path = os.path.join(base_path, parent_path, group_name)
                        new_parent_path = os.path.join(parent_path, group_name)
                    else:
                        group_path = base_path
                        new_parent_path = parent_path
                    
                    os.makedirs(group_path, exist_ok=True)
                    
                    # استخراج لایه های داخل پوشه
                    sub_counter = counter
                    for child in layer:
                        if not self._is_running:
                            return sub_counter
                        sub_counter = self.extract_layer_with_structure(child, base_path, sub_counter, new_parent_path, depth + 1)
                    return sub_counter
                else:
                    # اگر استخراج پوشه غیرفعال است، فقط لایه های داخل آن را استخراج کن
                    sub_counter = counter
                    for child in layer:
                        if not self._is_running:
                            return sub_counter
                        sub_counter = self.extract_layer_with_structure(child, base_path, sub_counter, parent_path, depth + 1)
                    return sub_counter
            else:
                # اگر لایه معمولی است
                mode = self.settings["layer_mode"]
                if (mode == "visible" and not layer.is_visible()) or \
                   (mode == "hidden" and layer.is_visible()):
                    return counter

                img = layer.topil()
                if img is None:
                    return counter

                safe_name = "".join(c for c in layer.name if c.isalnum() or c in (' ', '-', '_')).strip()
                if not safe_name:
                    safe_name = f"layer_{counter:03d}"

                fmt = self.settings["output_format"]
                filename = f"{counter:03d}_{safe_name}.{fmt}"
                
                # ایجاد مسیر کامل با در نظر گرفتن ساختار پوشه ها
                if self.settings.get("preserve_structure", True) and parent_path:
                    full_path = os.path.join(base_path, parent_path, filename)
                    # ایجاد پوشه والد اگر وجود ندارد
                    os.makedirs(os.path.dirname(full_path), exist_ok=True)
                else:
                    full_path = os.path.join(base_path, filename)

                save_kwargs = {}
                if fmt == "jpg":
                    # تبدیل RGBA به RGB برای فرمت JPG
                    if img.mode == 'RGBA':
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[-1])
                        img = background
                    save_kwargs["quality"] = self.settings["quality"]
                    save_kwargs["optimize"] = True
                elif fmt == "webp":
                    save_kwargs["quality"] = self.settings["quality"]

                img.save(full_path, **save_kwargs)
                visibility = self.texts["visible"] if layer.is_visible() else self.texts["hidden"]
                
                if self.settings.get("preserve_structure", True) and parent_path:
                    location = f" ({self.texts['in']} {parent_path})"
                else:
                    location = ""
                
                self.log.emit(f"{self.texts['layer']} {counter}: {layer.name} ({visibility}){location} {self.texts['saved']}", "success")
                return counter + 1

        except Exception as e:
            self.log.emit(f"{self.texts['error']} {self.texts['in']} {self.texts['layer']} {counter}: {e}", "error")
            return counter

    def extract_selected_layers_with_structure(self, layers, base_path):
        """استخراج لایه های انتخاب شده با حفظ ساختار"""
        counter = 1
        total = len(layers)
        for i, layer_info in enumerate(layers):
            if not self._is_running:
                break
                
            # محاسبه درصد پیشرفت
            progress = int((i / total) * 100) if total > 0 else 0
            self.progress.emit(progress)
                
            layer = layer_info["layer"]
            parent_path = layer_info.get("parent_path", "")
            
            if layer.is_group():
                continue  # از استخراج پوشه ها صرف نظر می کنیم
            
            mode = self.settings["layer_mode"]
            if (mode == "visible" and not layer.is_visible()) or \
               (mode == "hidden" and layer.is_visible()):
                continue

            try:
                img = layer.topil()
                if img is None:
                    self.log.emit(f"{self.texts['layer']} {counter}: {layer.name} — {self.texts['empty_image']}", "warning")
                    continue

                safe_name = "".join(c for c in layer.name if c.isalnum() or c in (' ', '-', '_')).strip()
                if not safe_name:
                    safe_name = f"layer_{counter:03d}"

                fmt = self.settings["output_format"]
                filename = f"{counter:03d}_{safe_name}.{fmt}"
                
                # ایجاد مسیر کامل با در نظر گرفتن ساختار پوشه ها
                if self.settings.get("preserve_structure", True) and parent_path:
                    full_path = os.path.join(base_path, parent_path, filename)
                    # ایجاد پوشه والد اگر وجود ندارد
                    os.makedirs(os.path.dirname(full_path), exist_ok=True)
                else:
                    full_path = os.path.join(base_path, filename)

                save_kwargs = {}
                if fmt == "jpg":
                    # تبدیل RGBA به RGB برای فرمت JPG
                    if img.mode == 'RGBA':
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[-1])
                        img = background
                    save_kwargs["quality"] = self.settings["quality"]
                    save_kwargs["optimize"] = True
                elif fmt == "webp":
                    save_kwargs["quality"] = self.settings["quality"]

                img.save(full_path, **save_kwargs)
                visibility = self.texts["visible"] if layer.is_visible() else self.texts["hidden"]
                
                if self.settings.get("preserve_structure", True) and parent_path:
                    location = f" ({self.texts['in']} {parent_path})"
                else:
                    location = ""
                
                self.log.emit(f"{self.texts['layer']} {counter}: {layer.name} ({visibility}){location} {self.texts['saved']}", "success")
                counter += 1
                
            except Exception as e:
                self.log.emit(f"{self.texts['error']} {self.texts['in']} {self.texts['layer']} {counter}: {e}", "error")
        
        return counter - 1

    def count_extractable_layers(self, root):
        """شمارش لایه های قابل استخراج با در نظر گرفتن تنظیمات"""
        count = 0
        mode = self.settings["layer_mode"]
        
        for layer in root.descendants():
            if layer.is_group():
                continue
            if (mode == "visible" and not layer.is_visible()) or \
               (mode == "hidden" and layer.is_visible()):
                continue
            count += 1
        return count

    def run(self):
        try:
            self.log.emit(self.texts["processing"] + "...", "info")
            psd = PSDImage.open(self.psd_path)
            fmt = self.settings["output_format"]

            os.makedirs(self.output_dir, exist_ok=True)

            if self.selected_layers:
                # استخراج لایه های انتخاب شده
                total = len(self.selected_layers)
                if total == 0:
                    self.log.emit(self.texts["no_layers_selected"], "warning")
                    return
                
                extracted_count = self.extract_selected_layers_with_structure(self.selected_layers, self.output_dir)
                if self._is_running:
                    self.progress.emit(100)
                    self.log.emit(f"{self.texts['extraction_complete']} - {extracted_count} {self.texts['layers_processed']}", "success")
                else:
                    self.log.emit(f"{self.texts['extraction_stopped']} - {extracted_count} {self.texts['layers_processed']}", "warning")
            else:
                # استخراج تمام لایه ها (حالت عادی)
                all_layers = list(psd.descendants())
                total_layers = self.count_extractable_layers(psd)
                if total_layers == 0:
                    self.log.emit(self.texts["no_layers_found"], "warning")
                    return

                extracted_count = 1
                processed = 0
                for layer in psd:
                    if not self._is_running:
                        break
                    extracted_count = self.extract_layer_with_structure(layer, self.output_dir, extracted_count)
                    processed += 1
                    
                    # محاسبه درصد پیشرفت
                    progress = int((processed / len(list(psd.descendants()))) * 100)
                    self.progress.emit(progress)

                if self._is_running:
                    self.progress.emit(100)
                    self.log.emit(self.texts["extraction_complete"], "success")
                else:
                    self.log.emit(f"{self.texts['extraction_stopped']} - {extracted_count-1} {self.texts['layers_processed']}", "warning")
                    
        except Exception as e:
            self.log.emit(f"{self.texts['error']}: {e}", "error")
        finally:
            if not self._is_running:
                self.stopped.emit()
            self.finished.emit()

# ==================== پنجره های فرعی ====================
class AboutDialog(QDialog):
    def __init__(self, lang, theme, parent=None):
        super().__init__(parent)
        self.lang = lang
        self.theme = theme
        self.setWindowTitle(TEXTS[lang]["about_title"])
        self.setFixedSize(600, 500)
        self.setStyleSheet(f"background-color: {theme['bg']}; color: {theme['text']};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        title = RTLLabel(TEXTS[lang]["about_title"], lang)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        content = QTextEdit()
        content.setReadOnly(True)
        content.setStyleSheet(f"background-color: {theme['fg']}; border: none; padding: 10px;")
        content.setText(RTLText.reshape(TEXTS[lang]["about_content"]) if lang == "fa" else TEXTS[lang]["about_content"])
        layout.addWidget(content)

        close_btn = QPushButton(TEXTS[lang]["close"])
        close_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "about.svg")))
        close_btn.setStyleSheet(f"background-color: {theme['secondary']}; color: white; padding: 10px; border-radius: 12px; font-weight: bold;")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignCenter)

class SettingsDialog(QDialog):
    def __init__(self, settings, apply_callback, lang, theme, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.apply_callback = apply_callback
        self.lang = lang
        self.theme = theme
        self.setWindowTitle(TEXTS[lang]["settings"])
        self.setFixedSize(500, 600)
        self.setStyleSheet(f"background-color: {theme['bg']}; color: {theme['text']};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        preview_cb = QCheckBox(TEXTS[lang]["preview_enabled"])
        preview_cb.setChecked(settings.get("preview_enabled", True))
        layout.addWidget(preview_cb)
        self.preview_cb = preview_cb

        extract_groups_cb = QCheckBox(TEXTS[lang]["extract_groups"])
        extract_groups_cb.setChecked(settings.get("extract_groups", True))
        layout.addWidget(extract_groups_cb)
        self.extract_groups_cb = extract_groups_cb

        preserve_structure_cb = QCheckBox(TEXTS[lang]["preserve_structure"])
        preserve_structure_cb.setChecked(settings.get("preserve_structure", True))
        layout.addWidget(preserve_structure_cb)
        self.preserve_structure_cb = preserve_structure_cb

        theme_group = QGroupBox(TEXTS[lang]["theme"])
        theme_layout = QHBoxLayout()
        themes = [("dark", TEXTS[lang]["dark"]), ("light", TEXTS[lang]["light"]), ("system", TEXTS[lang]["system"])]
        self.theme_group = QButtonGroup()
        for val, text in themes:
            rb = QRadioButton(text)
            rb.setChecked(settings.get("theme", "dark") == val)
            theme_layout.addWidget(rb)
            self.theme_group.addButton(rb)
            rb.value = val
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)

        lang_group = QGroupBox(TEXTS[lang]["language"])
        lang_layout = QHBoxLayout()
        langs = [("fa", "فارسی"), ("en", "English")]
        self.lang_group = QButtonGroup()
        for val, text in langs:
            rb = QRadioButton(text)
            rb.setChecked(settings.get("language", "fa") == val)
            lang_layout.addWidget(rb)
            self.lang_group.addButton(rb)
            rb.value = val
        lang_group.setLayout(lang_layout)
        layout.addWidget(lang_group)

        btn_layout = QHBoxLayout()
        apply_btn = QPushButton(TEXTS[lang]["apply"])
        apply_btn.clicked.connect(self.apply)
        cancel_btn = QPushButton(TEXTS[lang]["cancel"])
        cancel_btn.clicked.connect(self.reject)
        reset_btn = QPushButton(TEXTS[lang]["reset"])
        reset_btn.clicked.connect(self.reset)

        for btn in (apply_btn, cancel_btn, reset_btn):
            btn.setStyleSheet(f"padding: 8px 16px; border-radius: 12px; font-weight: bold;")
            btn_layout.addWidget(btn)

        layout.addLayout(btn_layout)

    def apply(self):
        new_settings = {
            "preview_enabled": self.preview_cb.isChecked(),
            "extract_groups": self.extract_groups_cb.isChecked(),
            "preserve_structure": self.preserve_structure_cb.isChecked(),
            "theme": next(b.value for b in self.theme_group.buttons() if b.isChecked()),
            "language": next(b.value for b in self.lang_group.buttons() if b.isChecked())
        }
        self.apply_callback(new_settings)
        self.accept()

    def reset(self):
        self.preview_cb.setChecked(True)
        self.extract_groups_cb.setChecked(True)
        self.preserve_structure_cb.setChecked(True)
        for btn in self.theme_group.buttons():
            btn.setChecked(btn.value == "dark")
        for btn in self.lang_group.buttons():
            btn.setChecked(btn.value == "fa")

class PreviewDialog(QDialog):
    def __init__(self, layer_data, lang, theme, parent=None):
        super().__init__(parent)
        self.lang = lang
        self.theme = theme
        self.setWindowTitle(TEXTS[lang]["preview_layer"])
        self.setFixedSize(500, 600)
        self.setStyleSheet(f"background-color: {theme['bg']}; color: {theme['text']};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        layer = layer_data["layer"]
        parent_path = layer_data["parent_path"]

        # نام لایه
        display_name = layer.name
        if parent_path:
            display_name = f"{parent_path} / {layer.name}"
            
        name_label = RTLLabel(display_name, lang)
        name_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #e94560;")
        layout.addWidget(name_label, alignment=Qt.AlignCenter)

        # تصویر لایه
        image_label = QLabel()
        image_label.setFixedSize(400, 300)
        image_label.setStyleSheet(f"background-color: {theme['fg']}; border: 2px dashed {theme['border']};")
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label, alignment=Qt.AlignCenter)

        # اطلاعات لایه
        info = QTextEdit()
        info.setFixedHeight(150)
        info.setReadOnly(True)
        info.setStyleSheet(f"background-color: {theme['fg']}; border: 1px solid {theme['border']}; padding: 8px;")
        layout.addWidget(info)

        # دکمه بستن
        close_btn = QPushButton(TEXTS[lang]["close"])
        close_btn.setStyleSheet(f"background-color: {theme['secondary']}; color: white; padding: 10px; border-radius: 12px; font-weight: bold;")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignCenter)

        # نمایش تصویر و اطلاعات
        try:
            img = layer.topil()
            if img is not None:
                w, h = img.size
                ratio = min(400 / w, 300 / h)
                new_size = (int(w * ratio), int(h * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)

                data = img.convert("RGBA").tobytes("raw", "RGBA")
                qimg = QImage(data, img.size[0], img.size[1], QImage.Format_RGBA8888)
                image_label.setPixmap(QPixmap.fromImage(qimg))
            else:
                image_label.setText(TEXTS[lang]["empty_image"])
        except Exception as e:
            image_label.setText(f"{TEXTS[lang]['error']}: {str(e)}")

        # اطلاعات لایه
        visibility = TEXTS[lang]["visible"] if layer.is_visible() else TEXTS[lang]["hidden"]
        info_text = f"{TEXTS[lang]['name']} {layer.name}\n"
        info_text += f"{TEXTS[lang]['type']} {layer.kind}\n"
        info_text += f"{TEXTS[lang]['size']} {layer.width} × {layer.height}\n"
        info_text += f"{TEXTS[lang]['position']} ({layer.left}, {layer.top})\n"
        info_text += f"{TEXTS[lang]['visibility']} {visibility}"
        
        if parent_path:
            info_text += f"\n{TEXTS[lang]['group']}: {parent_path}"
            
        info.setText(RTLText.reshape(info_text) if lang == "fa" else info_text)

class AllLayersPreviewDialog(QDialog):
    def __init__(self, all_layers_data, lang, theme, parent=None):
        super().__init__(parent)
        self.lang = lang
        self.theme = theme
        self.idx = 0
        self.setWindowTitle(TEXTS[lang]["preview_title"])
        self.setFixedSize(620, 720)
        self.setStyleSheet(f"background-color: {theme['bg']}; color: {theme['text']};")

        # all_layers_data یک لیست از دیکشنری ها است
        self.layers_data = all_layers_data
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        nav = QHBoxLayout()
        self.prev_btn = QPushButton("Previous")
        self.next_btn = QPushButton("Next")
        self.prev_btn.setFixedSize(80, 40)
        self.next_btn.setFixedSize(80, 40)
        self.counter = QLabel("0/0")
        self.counter.setStyleSheet("font-weight: bold; font-size: 14px;")
        nav.addWidget(self.prev_btn)
        nav.addStretch()
        nav.addWidget(self.counter)
        nav.addStretch()
        nav.addWidget(self.next_btn)
        layout.addLayout(nav)

        self.name_label = RTLLabel("", lang)
        self.name_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #e94560;")
        layout.addWidget(self.name_label, alignment=Qt.AlignCenter)

        self.image_label = QLabel()
        self.image_label.setFixedSize(500, 350)
        self.image_label.setStyleSheet(f"background-color: {theme['fg']}; border: 2px dashed {theme['border']};")
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label, alignment=Qt.AlignCenter)

        info = QTextEdit()
        info.setFixedHeight(130)
        info.setReadOnly(True)
        info.setStyleSheet(f"background-color: {theme['fg']}; border: 1px solid {theme['border']}; padding: 8px;")
        layout.addWidget(info)
        self.info = info

        self.prev_btn.clicked.connect(self.prev)
        self.next_btn.clicked.connect(self.next)

        if self.layers_data:
            self.show_layer()
        else:
            self.image_label.setText(TEXTS[lang]["no_layers_found"])

    def show_layer(self):
        if not self.layers_data:
            return
        
        layer_data = self.layers_data[self.idx]
        layer = layer_data["layer"]  # اینجا لایه واقعی است
        parent_path = layer_data["parent_path"]
        
        self.counter.setText(f"{self.idx + 1}/{len(self.layers_data)}")
        visibility = TEXTS[self.lang]["visible"] if layer.is_visible() else TEXTS[self.lang]["hidden"]
        
        display_name = layer.name
        if parent_path:
            display_name = f"{parent_path} / {layer.name}"
            
        self.name_label.setText(f"{display_name} ({visibility})")

        try:
            img = layer.topil()
            if img is None:
                self.image_label.setText("تصویر خالی")
                return

            w, h = img.size
            ratio = min(500 / w, 350 / h)
            new_size = (int(w * ratio), int(h * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)

            data = img.convert("RGBA").tobytes("raw", "RGBA")
            qimg = QImage(data, img.size[0], img.size[1], QImage.Format_RGBA8888)
            self.image_label.setPixmap(QPixmap.fromImage(qimg))

            info = f"{TEXTS[self.lang]['name']} {layer.name}\n"
            info += f"{TEXTS[self.lang]['type']} {layer.kind}\n"
            info += f"{TEXTS[self.lang]['size']} {layer.width} × {layer.height}\n"
            info += f"{TEXTS[self.lang]['position']} ({layer.left}, {layer.top})\n"
            info += f"{TEXTS[self.lang]['visibility']} {visibility}"
            
            if parent_path:
                info += f"\n{TEXTS[self.lang]['group']}: {parent_path}"
                
            self.info.setText(RTLText.reshape(info) if self.lang == "fa" else info)

        except Exception as e:
            self.image_label.setText(f"خطا: {str(e)}")

    def prev(self):
        if self.idx > 0:
            self.idx -= 1
            self.show_layer()

    def next(self):
        if self.idx < len(self.layers_data) - 1:
            self.idx += 1
            self.show_layer()

# ==================== برنامه اصلی ====================
class PSDExtractorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # راه اندازی فونت Manager بعد از ایجاد QApplication
        font_manager.setup_fonts()
        
        self.settings = self.load_settings()
        self.lang = self.settings.get("language", "fa")
        self.theme_name = self.settings.get("theme", "dark")
        self.theme = THEMES[self.theme_name]
        self.texts = TEXTS[self.lang]
        self.layers = []
        self.layer_tree = None
        self.selected_layers = []
        self.all_layers_data = []
        self.extraction_thread = None

        self.setWindowTitle(self.texts["app_title"])
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1200, 800)
        
        # اضافه کردن آیکن به برنامه
        try:
            app_icon_path = resource_path("app_icon.ico")
            if os.path.exists(app_icon_path):
                self.setWindowIcon(QIcon(app_icon_path))
            else:
                # اگر آیکن پیدا نشد، از آیکن های موجود در icons استفاده کن
                icon_path = resource_path(os.path.join("icons", "about.svg"))
                if os.path.exists(icon_path):
                    self.setWindowIcon(QIcon(icon_path))
        except Exception as e:
            print(f"خطا در بارگذاری آیکن: {e}")

        self.init_ui()
        self.apply_theme()
        self.apply_font_to_all_widgets()

    def apply_font_to_all_widgets(self):
        """اعمال فونت به تمام ویجت های موجود"""
        def set_font(widget):
            if hasattr(widget, 'setFont'):
                current_font = widget.font()
                if self.lang == "fa":
                    widget.setFont(font_manager.get_font(current_font.pointSize(), current_font.weight()))
                else:
                    # برای انگلیسی از فونت پیشفرض سیستم استفاده کنید
                    english_font = QFont("Tahoma", current_font.pointSize(), current_font.weight())
                    widget.setFont(english_font)
        
        def apply_to_children(parent):
            for child in parent.findChildren(QWidget):
                set_font(child)
                apply_to_children(child)
        
        apply_to_children(self)

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        
        # استفاده از Splitter برای تقسیم پنجره
        splitter = QSplitter(Qt.Horizontal)
        
        # پنل سمت چپ - ساختار لایه ها
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        left_header = QHBoxLayout()
        structure_title = RTLLabel(self.texts["layer_structure"], self.lang)
        structure_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        left_header.addWidget(structure_title)
        left_header.addStretch()
        
        refresh_btn = QPushButton()
        refresh_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "refresh.svg")))
        refresh_btn.setToolTip("بروزرسانی ساختار")
        refresh_btn.clicked.connect(self.analyze_file)
        left_header.addWidget(refresh_btn)
        
        left_layout.addLayout(left_header)
        
        self.layer_tree_widget = LayerTreeWidget(self.lang)
        self.layer_tree_widget.setSelectionMode(QTreeWidget.MultiSelection)
        self.layer_tree_widget.itemSelectionChanged.connect(self.on_layer_selected)
        self.layer_tree_widget.itemDoubleClicked.connect(self.on_layer_double_clicked)
        left_layout.addWidget(self.layer_tree_widget)
        
        # دکمه های انتخاب
        selection_btns = QHBoxLayout()
        select_all_btn = QPushButton(self.texts["select_all"])
        select_all_btn.clicked.connect(self.select_all_layers)
        deselect_all_btn = QPushButton(self.texts["deselect_all"])
        deselect_all_btn.clicked.connect(self.deselect_all_layers)
        
        selection_btns.addWidget(select_all_btn)
        selection_btns.addWidget(deselect_all_btn)
        left_layout.addLayout(selection_btns)
        
        tree_info = QLabel(self.texts["no_file_selected"])
        tree_info.setStyleSheet("color: #888; padding: 10px;")
        left_layout.addWidget(tree_info)
        self.tree_info = tree_info
        
        splitter.addWidget(left_panel)
        
        # پنل سمت راست - کنترل های اصلی
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(15)

        # Header
        header = QHBoxLayout()
        title = RTLLabel(self.texts["app_title"], self.lang)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        header.addWidget(title, 1)

        about_btn = QPushButton()
        about_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "about.svg")))
        about_btn.clicked.connect(self.show_about)
        settings_btn = QPushButton()
        settings_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "settings.svg")))
        settings_btn.clicked.connect(self.show_settings)

        header.addWidget(settings_btn)
        header.addWidget(about_btn)
        right_layout.addLayout(header)

        # File Selection
        file_frame = QGroupBox()
        file_layout = QGridLayout()
        file_layout.addWidget(RTLLabel(self.texts["select_psd"], self.lang), 0, 0)
        self.psd_path = QLineEdit()
        self.psd_path.setPlaceholderText(self.texts["select_file"])
        psd_btn = QPushButton(self.texts["browse"])
        psd_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "folder.svg")))
        psd_btn.clicked.connect(self.browse_psd)
        file_layout.addWidget(self.psd_path, 0, 1)
        file_layout.addWidget(psd_btn, 0, 2)

        file_layout.addWidget(RTLLabel(self.texts["select_output"], self.lang), 1, 0)
        self.output_dir = QLineEdit()
        self.output_dir.setPlaceholderText(self.texts["select_folder"])
        out_btn = QPushButton(self.texts["browse"])
        out_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "folder.svg")))
        out_btn.clicked.connect(self.browse_output)
        file_layout.addWidget(self.output_dir, 1, 1)
        file_layout.addWidget(out_btn, 1, 2)

        file_frame.setLayout(file_layout)
        right_layout.addWidget(file_frame)

        # Settings
        settings_frame = QGroupBox()
        settings_layout = QHBoxLayout()
        left_settings = QVBoxLayout()
        right_settings = QVBoxLayout()

        fmt_group = QGroupBox(self.texts["output_format"])
        fmt_layout = QVBoxLayout()
        self.format_group = QButtonGroup()
        # تغییر فرمت ها به PNG, JPEG, TIFF, WebP
        for fmt, label in [("png", "PNG"), ("jpg", "JPEG"), ("tiff", "TIFF"), ("webp", "WebP")]:
            rb = QRadioButton(label)
            rb.setChecked(self.settings.get("output_format", "png") == fmt)
            fmt_layout.addWidget(rb)
            self.format_group.addButton(rb)
            rb.value = fmt
        fmt_group.setLayout(fmt_layout)
        left_settings.addWidget(fmt_group)

        self.quality_frame = QGroupBox(self.texts["quality"])
        q_layout = QVBoxLayout()
        self.quality_slider = QSlider(Qt.Horizontal)
        self.quality_slider.setRange(1, 100)
        self.quality_slider.setValue(self.settings.get("quality", 95))
        self.quality_label = QLabel(f"{self.quality_slider.value()}%")
        q_layout.addWidget(self.quality_slider)
        q_layout.addWidget(self.quality_label)
        self.quality_frame.setLayout(q_layout)
        left_settings.addWidget(self.quality_frame)

        mode_group = QGroupBox(self.texts["layer_mode"])
        mode_layout = QVBoxLayout()
        self.mode_group = QButtonGroup()
        modes = [("all", self.texts["all_layers"]), ("visible", self.texts["visible_layers"]), ("hidden", self.texts["hidden_layers"])]
        for val, label in modes:
            rb = QRadioButton(label)
            rb.setChecked(self.settings.get("layer_mode", "all") == val)
            mode_layout.addWidget(rb)
            self.mode_group.addButton(rb)
            rb.value = val
        mode_group.setLayout(mode_layout)
        right_settings.addWidget(mode_group)

        extract_groups_cb = QCheckBox(self.texts["extract_groups"])
        extract_groups_cb.setChecked(self.settings.get("extract_groups", True))
        right_settings.addWidget(extract_groups_cb)
        self.extract_groups_cb = extract_groups_cb

        preserve_structure_cb = QCheckBox(self.texts["preserve_structure"])
        preserve_structure_cb.setChecked(self.settings.get("preserve_structure", True))
        right_settings.addWidget(preserve_structure_cb)
        self.preserve_structure_cb = preserve_structure_cb

        settings_layout.addLayout(left_settings)
        settings_layout.addLayout(right_settings)
        settings_frame.setLayout(settings_layout)
        right_layout.addWidget(settings_frame)

        # Preview & Analyze
        preview_frame = QHBoxLayout()
        self.preview_btn = QPushButton(self.texts["preview"])
        self.preview_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "preview.svg")))
        self.preview_btn.clicked.connect(self.show_preview)
        self.analyze_btn = QPushButton(self.texts["analyze"])
        self.analyze_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "analyze.svg")))
        self.analyze_btn.clicked.connect(self.analyze_file)
        self.info_label = RTLLabel(self.texts["no_file_selected"], self.lang)
        preview_frame.addWidget(self.preview_btn)
        preview_frame.addWidget(self.analyze_btn)
        preview_frame.addWidget(self.info_label, 1)
        right_layout.addLayout(preview_frame)

        # Extract Buttons
        extract_buttons_layout = QHBoxLayout()
        self.extract_btn = QPushButton(self.texts["start_extraction"])
        self.extract_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "play.svg")))
        self.extract_btn.clicked.connect(self.start_extraction)
        
        self.extract_selected_btn = QPushButton(self.texts["start_selected_extraction"])
        self.extract_selected_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "play_selected.svg")))
        self.extract_selected_btn.clicked.connect(self.start_selected_extraction)
        self.extract_selected_btn.setEnabled(False)  # ابتدا غیرفعال
        
        self.stop_extract_btn = QPushButton(self.texts["stop_extraction"])
        self.stop_extract_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "stop.svg")))
        self.stop_extract_btn.clicked.connect(self.stop_extraction)
        self.stop_extract_btn.setEnabled(False)  # ابتدا غیرفعال
        
        extract_buttons_layout.addWidget(self.extract_btn)
        extract_buttons_layout.addWidget(self.extract_selected_btn)
        extract_buttons_layout.addWidget(self.stop_extract_btn)
        right_layout.addLayout(extract_buttons_layout)

        # Progress
        progress_frame = QHBoxLayout()
        progress_label = RTLLabel(self.texts["progress"], self.lang)
        progress_label.setStyleSheet("font-weight: bold;")
        progress_frame.addWidget(progress_label)
        
        self.progress = QProgressBar()
        progress_frame.addWidget(self.progress, 1)
        
        self.progress_percent = QLabel("0%")
        self.progress_percent.setStyleSheet("font-weight: bold; min-width: 40px;")
        progress_frame.addWidget(self.progress_percent)
        
        right_layout.addLayout(progress_frame)

        self.status = QLabel(self.texts["ready"])
        right_layout.addWidget(self.status)

        # Console
        console_frame = QGroupBox(self.texts["console"])
        console_layout = QVBoxLayout()
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        console_layout.addWidget(self.console)

        btns = QHBoxLayout()
        clear_btn = QPushButton(self.texts["clear_console"])
        clear_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "clear.svg")))
        clear_btn.clicked.connect(self.console.clear)
        open_btn = QPushButton(self.texts["open_output"])
        open_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "open_folder.svg")))
        open_btn.clicked.connect(self.open_output)
        btns.addWidget(clear_btn)
        btns.addWidget(open_btn)
        console_layout.addLayout(btns)

        console_frame.setLayout(console_layout)
        right_layout.addWidget(console_frame)
        
        splitter.addWidget(right_panel)
        splitter.setSizes([400, 800])
        
        main_layout = QHBoxLayout(central)
        main_layout.addWidget(splitter)

        self.format_group.buttonClicked.connect(self.update_quality_visibility)
        self.quality_slider.valueChanged.connect(self.update_quality_display)
        self.update_quality_visibility()

    def update_quality_display(self):
        value = self.quality_slider.value()
        self.quality_label.setText(f"{value}%")

    def apply_theme(self):
        app = QApplication.instance()
        if self.theme_name == "system":
            app.setStyleSheet("")
        else:
            # برای فونت فارسی از Vazirmatn و برای انگلیسی از Tahoma استفاده می کنیم
            font_family = font_manager.font_family if self.lang == "fa" else "Tahoma"
            
            qss = f"""
                * {{
                    font-family: "{font_family}";
                }}
                QWidget {{ 
                    background-color: {self.theme['bg']}; 
                    color: {self.theme['text']}; 
                }}
                QGroupBox {{ 
                    border: 2px solid {self.theme['border']}; 
                    border-radius: 12px; 
                    padding: 10px; 
                    margin-top: 10px; 
                }}
                QGroupBox::title {{ 
                    subcontrol-origin: margin; 
                    left: 10px; 
                    padding: 0 5px; 
                }}
                QPushButton {{ 
                    background-color: {self.theme['fg']}; 
                    border: 2px solid {self.theme['border']}; 
                    border-radius: 12px; 
                    padding: 8px; 
                }}
                QPushButton:hover {{ 
                    background-color: {self.theme['accent']}; 
                }}
                QLineEdit {{ 
                    background-color: {self.theme['fg']}; 
                    border: 1px solid {self.theme['border']}; 
                    border-radius: 8px; 
                    padding: 5px; 
                }}
                QProgressBar {{ 
                    background-color: {self.theme['fg']}; 
                    border: 1px solid {self.theme['border']}; 
                    border-radius: 10px; 
                    text-align: center; 
                }}
                QProgressBar::chunk {{ 
                    background-color: {self.theme['progress']}; 
                }}
                QTreeWidget {{ 
                    background-color: {self.theme['tree_bg']}; 
                    color: {self.theme['text']}; 
                    border: 1px solid {self.theme['border']}; 
                    border-radius: 8px; 
                }}
                QTreeWidget::item {{ 
                    padding: 5px; 
                    border-bottom: 1px solid {self.theme['bg']}; 
                }}
                QTreeWidget::item:selected {{ 
                    background-color: {self.theme['accent']}; 
                }}
            """
            app.setStyleSheet(qss)

        if self.lang == "fa":
            QApplication.setLayoutDirection(Qt.RightToLeft)
        else:
            QApplication.setLayoutDirection(Qt.LeftToRight)


    def load_settings(self):
        try:
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    return {**DEFAULT_SETTINGS, **json.load(f)}
        except:
            pass
        return DEFAULT_SETTINGS.copy()

    def save_settings(self):
        try:
            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
        except:
            pass

    def log(self, msg, type="info"):
        icons = {"success": "success.svg", "error": "error.svg", "warning": "warning.svg", "info": "info.svg"}
        icon_path = os.path.join(ICONS_DIR, icons.get(type, "info.svg"))
        timestamp = datetime.now().strftime("%H:%M:%S")
        text = f"[{timestamp}] {msg}"
        self.console.append(f'<img src="{icon_path}" width="16" height="16"> {RTLText.reshape(text) if self.lang == "fa" else text}')

    def browse_psd(self):
        path, _ = QFileDialog.getOpenFileName(self, self.texts["select_psd"], "", "PSD Files (*.psd)")
        if path:
            self.psd_path.setText(path)
            self.analyze_file()

    def browse_output(self):
        dir = QFileDialog.getExistingDirectory(self, self.texts["select_output"])
        if dir:
            self.output_dir.setText(dir)

    def build_layer_tree(self, parent_item, layer, parent_path=""):
        """تابع بازگشتی برای ساختن ساختار درختی لایه ها"""
        if layer.is_group():
            # ایجاد آیتم برای پوشه
            layer_text = f"📁 {layer.name}"
            if self.lang == "fa":
                layer_text = RTLText.reshape(layer_text)
            item = QTreeWidgetItem(parent_item, [layer_text])
            
            # اضافه کردن اطلاعات به tooltip
            tooltip = f"{self.texts['group']}: {layer.name}\n"
            tooltip += f"{self.texts['visibility']}: {self.texts['visible'] if layer.is_visible() else self.texts['hidden']}"
            item.setToolTip(0, tooltip)
            item.setData(0, Qt.UserRole, {"layer": layer, "parent_path": parent_path})
            
            # اضافه کردن لایه های داخل پوشه
            child_count = 0
            new_path = f"{parent_path}/{layer.name}" if parent_path else layer.name
            for child in layer:
                child_count += self.build_layer_tree(item, child, new_path)
            
            # نمایش تعداد لایه های داخل پوشه
            if child_count > 0:
                count_text = f" ({child_count} {self.texts['layers_in_group']})"
                if self.lang == "fa":
                    count_text = RTLText.reshape(count_text)
                item.setText(0, item.text(0) + count_text)
            
            return child_count
        else:
            # ایجاد آیتم برای لایه معمولی
            visibility_icon = "●" if layer.is_visible() else "○"
            layer_text = f"{visibility_icon} {layer.name}"
            if self.lang == "fa":
                layer_text = RTLText.reshape(layer_text)
            item = QTreeWidgetItem(parent_item, [layer_text])
            
            # اضافه کردن اطلاعات به tooltip
            tooltip = f"{self.texts['name']}: {layer.name}\n"
            tooltip += f"{self.texts['type']}: {layer.kind}\n"
            tooltip += f"{self.texts['size']}: {layer.width} × {layer.height}\n"
            tooltip += f"{self.texts['visibility']}: {self.texts['visible'] if layer.is_visible() else self.texts['hidden']}"
            if parent_path:
                tooltip += f"\n{self.texts['group']}: {parent_path}"
            item.setToolTip(0, tooltip)
            item.setData(0, Qt.UserRole, {"layer": layer, "parent_path": parent_path})
            
            return 1

    def analyze_file(self):
        if not self.psd_path.text():
            QMessageBox.warning(self, self.texts["warning"], self.texts["no_file_selected"])
            return
        try:
            self.status.setText(self.texts["loading"])
            psd = PSDImage.open(self.psd_path.text())
            
            # پاک کردن درخت موجود
            self.layer_tree_widget.clear()
            
            # ساختن ساختار درختی
            root_item = self.layer_tree_widget.invisibleRootItem()
            total_layers = 0
            
            for layer in psd:
                total_layers += self.build_layer_tree(root_item, layer)
            
            # گسترش دادن تمام آیتم ها
            self.layer_tree_widget.expandAll()
            
            # جمع آوری تمام لایه های غیر گروهی برای پیشنمایش
            self.all_layers_data = []
            self.collect_all_layers(psd)
            
            # به روزرسانی اطلاعات
            visible = len([l for l in self.all_layers_data if l["layer"].is_visible()])
            hidden = len(self.all_layers_data) - visible
            
            info = f"{len(self.all_layers_data)} {self.texts['total_layers']} • {visible} {self.texts['visible']} • {hidden} {self.texts['hidden']}"
            self.info_label.setText(info)
            self.tree_info.setText(f"{total_layers} {self.texts['layers_found']} ({len(self.all_layers_data)} {self.texts['layer']})")
            
            self.log(f"{self.texts['file_analyzed']}: {len(self.all_layers_data)} {self.texts['layers_found']}", "success")
        except Exception as e:
            self.log(f"{self.texts['error']}: {e}", "error")
            self.info_label.setText(self.texts["error"])
            self.tree_info.setText(self.texts["error"])
        finally:
            self.status.setText(self.texts["ready"])

    def collect_all_layers(self, layers, parent_path=""):
        """جمع آوری تمام لایه های غیر گروهی به صورت بازگشتی"""
        for layer in layers:
            if layer.is_group():
                # اگر پوشه است، لایه های داخل آن را بررسی کن
                new_path = f"{parent_path}/{layer.name}" if parent_path else layer.name
                self.collect_all_layers(layer, new_path)
            else:
                # اگر لایه معمولی است، اضافه کن
                self.all_layers_data.append({
                    "layer": layer,
                    "parent_path": parent_path
                })

    def on_layer_selected(self):
        """هنگام انتخاب لایه ها در درخت"""
        selected_items = self.layer_tree_widget.selectedItems()
        self.selected_layers = []
        
        for item in selected_items:
            layer_data = item.data(0, Qt.UserRole)
            if layer_data and not layer_data["layer"].is_group():
                self.selected_layers.append(layer_data)
        
        # فعال/غیرفعال کردن دکمه استخراج لایه های انتخاب شده
        self.extract_selected_btn.setEnabled(len(self.selected_layers) > 0)
        
        # به روزرسانی اطلاعات
        if self.selected_layers:
            self.tree_info.setText(f"{len(self.selected_layers)} {self.texts['selected_layers']}")
        else:
            self.tree_info.setText(self.texts["no_layers_selected"])

    def on_layer_double_clicked(self, item, column):
        """هنگام دوبار کلیک روی لایه در درخت"""
        layer_data = item.data(0, Qt.UserRole)
        if layer_data and not layer_data["layer"].is_group():
            PreviewDialog(layer_data, self.lang, self.theme, self).exec_()

    def select_all_layers(self):
        """انتخاب تمام لایه ها در درخت"""
        self.layer_tree_widget.selectAll()
        self.on_layer_selected()

    def deselect_all_layers(self):
        """لغو انتخاب تمام لایه ها در درخت"""
        self.layer_tree_widget.clearSelection()
        self.on_layer_selected()

    def show_preview(self):
        if not self.psd_path.text():
            QMessageBox.warning(self, self.texts["warning"], self.texts["no_file_selected"])
            return
        if not hasattr(self, 'all_layers_data') or not self.all_layers_data:
            self.analyze_file()
        if hasattr(self, 'all_layers_data') and self.all_layers_data:
            AllLayersPreviewDialog(self.all_layers_data, self.lang, self.theme, self).exec_()

    def update_quality_visibility(self):
        selected_format = [b.value for b in self.format_group.buttons() if b.isChecked()][0]
        self.quality_frame.setVisible(selected_format in ["jpg", "webp"])

    def start_extraction(self):
        if not self.psd_path.text() or not self.output_dir.text():
            QMessageBox.critical(self, self.texts["error"], self.texts["no_file_selected"] if not self.psd_path.text() else self.texts["no_output_selected"])
            return

        # ریست کردن نوار پیشرفت
        self.progress.setValue(0)
        self.progress_percent.setText("0%")

        self.settings.update({
            "output_format": [b.value for b in self.format_group.buttons() if b.isChecked()][0],
            "quality": self.quality_slider.value(),
            "layer_mode": [b.value for b in self.mode_group.buttons() if b.isChecked()][0],
            "extract_groups": self.extract_groups_cb.isChecked(),
            "preserve_structure": self.preserve_structure_cb.isChecked()
        })

        # غیرفعال کردن دکمه های استخراج و فعال کردن دکمه توقف
        self.extract_btn.setEnabled(False)
        self.extract_selected_btn.setEnabled(False)
        self.stop_extract_btn.setEnabled(True)

        self.extraction_thread = ExtractionThread(self.psd_path.text(), self.output_dir.text(), self.settings, self.texts)
        self.extraction_thread.progress.connect(self.progress.setValue)
        self.extraction_thread.progress.connect(lambda v: self.progress_percent.setText(f"{v}%"))
        self.extraction_thread.status.connect(self.status.setText)
        self.extraction_thread.log.connect(self.log)
        self.extraction_thread.finished.connect(self.extraction_finished)
        self.extraction_thread.stopped.connect(self.extraction_stopped)
        self.extraction_thread.start()

    def start_selected_extraction(self):
        if not self.psd_path.text() or not self.output_dir.text():
            QMessageBox.critical(self, self.texts["error"], self.texts["no_file_selected"] if not self.psd_path.text() else self.texts["no_output_selected"])
            return
        
        if not self.selected_layers:
            QMessageBox.warning(self, self.texts["warning"], self.texts["no_layers_selected"])
            return

        # ریست کردن نوار پیشرفت
        self.progress.setValue(0)
        self.progress_percent.setText("0%")

        self.settings.update({
            "output_format": [b.value for b in self.format_group.buttons() if b.isChecked()][0],
            "quality": self.quality_slider.value(),
            "layer_mode": [b.value for b in self.mode_group.buttons() if b.isChecked()][0],
            "extract_groups": self.extract_groups_cb.isChecked(),
            "preserve_structure": self.preserve_structure_cb.isChecked()
        })

        # غیرفعال کردن دکمه های استخراج و فعال کردن دکمه توقف
        self.extract_btn.setEnabled(False)
        self.extract_selected_btn.setEnabled(False)
        self.stop_extract_btn.setEnabled(True)

        self.extraction_thread = ExtractionThread(self.psd_path.text(), self.output_dir.text(), self.settings, self.texts, self.selected_layers)
        self.extraction_thread.progress.connect(self.progress.setValue)
        self.extraction_thread.progress.connect(lambda v: self.progress_percent.setText(f"{v}%"))
        self.extraction_thread.status.connect(self.status.setText)
        self.extraction_thread.log.connect(self.log)
        self.extraction_thread.finished.connect(self.extraction_finished)
        self.extraction_thread.stopped.connect(self.extraction_stopped)
        self.extraction_thread.start()

    def stop_extraction(self):
        if self.extraction_thread and self.extraction_thread.isRunning():
            self.extraction_thread.stop()
            self.stop_extract_btn.setEnabled(False)
            self.status.setText(self.texts["extraction_stopped"])

    def extraction_finished(self):
        self.extract_btn.setEnabled(True)
        self.extract_selected_btn.setEnabled(len(self.selected_layers) > 0)
        self.stop_extract_btn.setEnabled(False)
        self.status.setText(self.texts["ready"])

    def extraction_stopped(self):
        self.extract_btn.setEnabled(True)
        self.extract_selected_btn.setEnabled(len(self.selected_layers) > 0)
        self.stop_extract_btn.setEnabled(False)
        self.status.setText(self.texts["extraction_stopped"])

    def open_output(self):
        path = self.output_dir.text()
        if path and os.path.exists(path):
            if platform.system() == "Windows":
                os.startfile(path)
            elif platform.system() == "Darwin":
                os.system(f'open "{path}"')
            else:
                os.system(f'xdg-open "{path}"')

    def show_about(self):
        AboutDialog(self.lang, self.theme, self).exec_()

    def show_settings(self):
        dlg = SettingsDialog(self.settings, self.apply_settings, self.lang, self.theme, self)
        dlg.exec_()

    def apply_settings(self, new_settings):
        lang_changed = self.lang != new_settings.get("language")
        theme_changed = self.theme_name != new_settings.get("theme")

        self.settings.update(new_settings)
        self.save_settings()

        if theme_changed:
            self.theme_name = new_settings["theme"]
            self.theme = THEMES[self.theme_name]
            self.apply_theme()

        if lang_changed:
            self.lang = new_settings["language"]
            self.texts = TEXTS[self.lang]
            self.init_ui()
            self.apply_theme()

        self.log(self.texts["settings_applied"], "success")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # راه اندازی فونت منیجر
    if not font_manager.setup_fonts():
        print("هشدار: فونت Vazirmatn بارگذاری نشد. از فونت پیشفرض استفاده می شود.")
    
    # تنظیم فونت پیشفرض برای برنامه
    default_font = font_manager.get_font(10)
    app.setFont(default_font)
    
    window = PSDExtractorApp()
    window.show()
    sys.exit(app.exec_())