import os
import subprocess
import sys
import shutil

def build_exe():
    # نام فایل اصلی برنامه
    script_name = "psd_extractor.py"
    
    # نام فایل آیکن
    icon_name = "app_icon.ico"
    
    # ایجاد پوشه های مورد نیاز
    os.makedirs("dist", exist_ok=True)
    os.makedirs("fonts", exist_ok=True)
    
    # کپی فونت به پوشه fonts (اگر در ریشه پروژه وجود دارد)
    if os.path.exists("vazirmatn.ttf") and not os.path.exists("fonts/vazirmatn.ttf"):
        shutil.copy2("vazirmatn.ttf", "fonts/vazirmatn.ttf")
    
    # بررسی وجود فونت
    if not os.path.exists("fonts/vazirmatn.ttf"):
        print("هشدار: فونت vazirmatn.ttf در پوشه fonts یافت نشد!")
        print("لطفاً فونت را در پوشه fonts قرار دهید.")
        return
    
    # دستور PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        f"--icon={icon_name}",
        "--name=PSD Layer Extractor",
        "--add-data=icons;icons",
        "--add-data=fonts;fonts", 
        f"--add-data={icon_name};.",
        "--hidden-import=PyQt5.QtCore",
        "--hidden-import=PyQt5.QtGui",
        "--hidden-import=PyQt5.QtWidgets",
        "--hidden-import=psd_tools",
        "--hidden-import=PIL",
        "--hidden-import=arabic_reshaper",
        "--hidden-import=bidi",
        "--hidden-import=PIL._imaging",
        "--hidden-import=PIL.Image",
        "--hidden-import=PIL.ImageFile",
        "--hidden-import=PIL.ImageOps",
        "--clean",
        script_name
    ]
    
    try:
        print("شروع ساخت فایل اجرایی...")
        subprocess.run(cmd, check=True)
        
        # کپی فایل تنظیمات به پوشه dist
        if os.path.exists("psd_extractor_settings.json"):
            shutil.copy2("psd_extractor_settings.json", "dist/psd_extractor_settings.json")
        
        print("ساخت فایل اجرایی با موفقیت انجام شد!")
        print("فایل اجرایی در پوشه 'dist' قرار دارد.")
        
        # حذف فایل های موقت
        if os.path.exists("build"):
            shutil.rmtree("build")
        if os.path.exists("PSD Layer Extractor.spec"):
            os.remove("PSD Layer Extractor.spec")
            
    except subprocess.CalledProcessError as e:
        print(f"خطا در ساخت فایل اجرایی: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"خطای غیرمنتظره: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_exe()