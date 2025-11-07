<div align="center">

# PSD Layer Extractor

[![Version](https://img.shields.io/badge/version-2.0-brightgreen.svg)](https://github.com/irpbz/psd-layer-extractor)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Downloads](https://img.shields.io/github/downloads/irpbz/psd-layer-extractor/total?color=orange)](https://github.com/irpbz/psd-layer-extractor/releases)
[![Stars](https://img.shields.io/github/stars/irpbz/psd-layer-extractor?style=social)](https://github.com/irpbz/psd-layer-extractor)

**The Ultimate Free PSD Layer Extractor** – Extract layers from PSD files **without Photoshop**! Supports **PSB** (large files), full **layer group structure**, **selective extraction**, and **high-quality exports** up to 2025 PSD formats.

</div>

## 🌟 Why This Tool is the Best in 2025

| Feature                  | PSD Layer Extractor | Photoshop Export | Aspose PSD Extractor | ImageMagick | psd-tools CLI |
|--------------------------|--------------------|------------------|----------------------|-------------|---------------|
| **Full Layer Group Support** | ✅ **Perfect**      | ✅               | ❌ Partial           | ❌ No        | ❌ No          |
| **Selective Layer Extraction** | ✅ **Advanced**    | ✅               | ❌ No                | ❌ No        | ❌ No          |
| **PSB (Large Files > 2GB)**  | ✅ **Yes**          | ✅               | ✅                  | ❌ No        | ✅             |
| **Preserve Folder Structure**| ✅ **Yes**          | ❌ No             | ❌ No                | ❌ No        | ❌ No          |
| **Modern UI (Dark/Light)**   | ✅ **Beautiful**    | ❌ Basic          | ✅ Web               | ❌ CLI       | ❌ CLI         |
| **Batch Quality (95%)**      | ✅ **Best**         | ❌ 72% default    | ✅                  | ❌ Variable  | ❌ Variable    |
| **Free & Open Source**       | ✅ **100%**         | ❌ $20/month      | ❌ Limited free      | ✅           | ✅             |
| **Updated Oct 2025**          | ✅ **Latest**       | -                | -                   | -           | -             |

**Tested with latest psd-tools 1.10.13 (Oct 2, 2025)** – handles all modern Photoshop 2025 features!

**No installation needed** – just run!

### Source Code
```bash
git clone https://github.com/irpbz/psd-layer-extractor.git
cd psd-layer-extractor
pip install -r requirements.txt
python main.py






```
<div align="right" dir="rtl">

# استخراج کننده لایه های PSD

[![نسخه](https://img.shields.io/badge/version-۲.۰-green.svg)](https://github.com/irpbz/psd-layer-extractor/releases/latest)
[![لایسنس](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![دانلودها](https://img.shields.io/github/downloads/irpbz/psd-layer-extractor/total?color=orange)](https://github.com/irpbz/psd-layer-extractor/releases)

**بهترین ابزار **رایگان** استخراج لایه های PSD** – بدون نیاز به فتوشاپ! پشتیبانی کامل از **PSB** (فایل های بزرگ)، **ساختار گروه ها**، **انتخابی** و **کیفیت بالا** تا سال ۱۴۰۴/۲۰۲۵.

</div>
### کد منبع
```bash
git clone https://github.com/irpbz/psd-layer-extractor.git
cd psd-layer-extractor
pip install -r requirements.txt
python main.py



```

## Overview

PSD Layer Extractor is a professional desktop application built with Python and PyQt5 for extracting layers from Adobe Photoshop PSD files. It provides a modern, responsive user interface with support for Persian (Farsi) and English languages, dark/light themes, and advanced features like layer preview, selective extraction, and structure preservation. This tool is ideal for designers, developers, and anyone working with PSD files who needs to export individual layers to formats like PNG, JPEG, TIFF, or WebP.

Powered by the psd-tools library, it handles complex PSD structures including groups and nested layers. The app is cross-platform (Windows, macOS, Linux) and can be packaged as a standalone executable using PyInstaller.
Features

    Layer Extraction: Export all layers, visible/hidden layers only, or selected layers to PNG, JPEG, TIFF, or WebP formats.
    Layer Preview: Interactive preview dialog with navigation for all layers, showing images, dimensions, positions, and visibility status.
    Structure Preservation: Optionally extract groups as folders and maintain the original PSD hierarchy in the output directory.
    Advanced Settings: Adjustable output quality (for JPEG/WebP), theme switching (dark/light/system), and language selection.
    Layer Tree View: Hierarchical tree widget to browse and select layers/groups, with tooltips for detailed info.
    Progress Tracking: Real-time console logging, progress bar, and status updates during extraction.
    Multi-Language Support: Full RTL (Right-to-Left) support for Persian, with automatic text reshaping.
    Custom Fonts: Integrated Vazirmatn font for Persian text rendering.

## Usage

    Select Files: Choose a PSD file and output folder via the browse buttons.
    Configure Settings: Select output format, quality, layer mode (all/visible/hidden), and options like group extraction.
    Analyze & Preview: Click "Analyze File" to load the layer tree. Use "Preview Layers" to view layers interactively.
    Extract Layers:
        "Start Extraction" for all layers.
        Select specific layers in the tree and use "Extract Selected Layers".
    Monitor Progress: Watch the console for logs and progress bar.
    Open Output: Automatically open the output folder after extraction.

## Supported Formats

    Input: PSD files (via psd-tools).
    Output: PNG (default), JPEG (with quality slider), TIFF, WebP.

## Limitations

    Does not support editing PSD files (read-only extraction).
    Some complex PSD effects (e.g., advanced blending) may not render perfectly.
    Requires Pillow for image processing; ensure it's installed for full functionality.

## Contributing

Contributions are welcome! Please:

    Fork the repository.
    Create a feature branch (git checkout -b feature/AmazingFeature).
    Commit changes (git commit -m 'Add some AmazingFeature').
    Push to the branch (git push origin feature/AmazingFeature).
    Open a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgments

    Built with PyQt5 for the GUI.
    PSD parsing via psd-tools.
    Persian text support: arabic-reshaper and python-bidi.
    Font: Vazirmatn.

For issues or feedback, open a GitHub issue. Developed by Amin Mohammadi (www.artika.ir).


## بررسی اجمالی

استخراج‌کننده لایه‌های PSD یک برنامه دسکتاپ حرفه‌ای است که با پایتون و PyQt5 ساخته شده و برای استخراج لایه‌ها از فایل‌های PSD ادوبی فتوشاپ طراحی شده است. این برنامه دارای رابط کاربری مدرن و واکنش‌گرا با پشتیبانی از زبان‌های فارسی و انگلیسی، تم‌های تیره/روشن، و ویژگی‌های پیشرفته مانند پیش‌نمایش لایه‌ها، استخراج انتخابی، و حفظ ساختار است. این ابزار برای طراحان، توسعه‌دهندگان و هر کسی که با فایل‌های PSD کار می‌کند و نیاز به خروجی لایه‌های جداگانه به فرمت‌هایی مانند PNG، JPEG، TIFF یا WebP دارد، ایده‌آل است.

این برنامه بر پایه کتابخانه psd-tools ساخته شده و ساختارهای پیچیده PSD از جمله گروه‌ها و لایه‌های تو در تو را مدیریت می‌کند. برنامه کراس‌پلتفرم (ویندوز، مک‌اواس، لینوکس) است و می‌تواند به عنوان فایل اجرایی مستقل با PyInstaller بسته‌بندی شود.
ویژگی‌ها

    استخراج لایه‌ها: خروجی تمام لایه‌ها، فقط لایه‌های قابل مشاهده/مخفی، یا لایه‌های انتخاب‌شده به فرمت‌های PNG، JPEG، TIFF یا WebP.
    پیش‌نمایش لایه‌ها: دیالوگ تعاملی پیش‌نمایش با ناوبری برای تمام لایه‌ها، نمایش تصاویر، ابعاد، موقعیت‌ها و وضعیت visibility.
    حفظ ساختار: اختیاری استخراج گروه‌ها به عنوان پوشه‌ها و حفظ سلسله‌مراتب اصلی PSD در دایرکتوری خروجی.
    تنظیمات پیشرفته: تنظیم کیفیت خروجی (برای JPEG/WebP)، تغییر تم (تیره/روشن/سیستمی)، و انتخاب زبان.
    نمایش درختی لایه‌ها: ویجت درخت سلسله‌مراتبی برای مرور و انتخاب لایه‌ها/گروه‌ها، با tooltipهای جزئیات.
    پیگیری پیشرفت: لاگینگ کنسول زمان واقعی، نوار پیشرفت، و به‌روزرسانی وضعیت در حین استخراج.
    پشتیبانی چندزبانه: پشتیبانی کامل RTL (راست به چپ) برای فارسی، با reshape خودکار متن.
    فونت‌های سفارشی: فونت یکپارچه Vazirmatn برای رندرینگ متن فارسی.


## استفاده

    انتخاب فایل‌ها: فایل PSD و پوشه خروجی را با دکمه‌های مرور انتخاب کنید.
    پیکربندی تنظیمات: فرمت خروجی، کیفیت، حالت لایه (همه/قابل مشاهده/مخفی)، و گزینه‌هایی مانند استخراج گروه‌ها را انتخاب کنید.
    تحلیل و پیش‌نمایش: روی "تحلیل فایل" کلیک کنید تا درخت لایه بارگذاری شود. از "پیش‌نمایش لایه‌ها" برای مشاهده تعاملی استفاده کنید.
    استخراج لایه‌ها:
        "شروع استخراج" برای تمام لایه‌ها.
        لایه‌های خاص را در درخت انتخاب کنید و از "استخراج لایه‌های انتخاب‌شده" استفاده کنید.
    نظارت بر پیشرفت: لاگ‌های کنسول و نوار پیشرفت را تماشا کنید.
    باز کردن خروجی: پوشه خروجی را پس از استخراج به طور خودکار باز کنید.

## فرمت‌های پشتیبانی‌شده

    ورودی: فایل‌های PSD (از طریق psd-tools).
    خروجی: PNG (پیش‌فرض)، JPEG (با اسلایدر کیفیت)، TIFF، WebP.

## محدودیت‌ها

    پشتیبانی از ویرایش فایل‌های PSD ندارد (فقط خواندنی و استخراج).
    برخی افکت‌های پیچیده PSD (مانند blending پیشرفته) ممکن است کامل رندر نشوند.
    برای پردازش تصویر، Pillow لازم است؛ اطمینان حاصل کنید که نصب شده باشد.

## مشارکت

مشارکت خوشامد است! لطفاً:

    مخزن را فورک کنید.
    شاخه ویژگی ایجاد کنید (git checkout -b feature/AmazingFeature).
    تغییرات را کامیت کنید (git commit -m 'Add some AmazingFeature').
    به شاخه push کنید (git push origin feature/AmazingFeature).
    یک Pull Request باز کنید.

## لایسنس

این پروژه تحت لایسنس MIT منتشر شده - فایل LICENSE را برای جزئیات ببینید.

## قدرت گرفته

    ساخته‌شده با PyQt5 برای GUI.
    تجزیه PSD از طریق psd-tools.
    پشتیبانی متن فارسی: arabic-reshaper و python-bidi.
    فونت: Vazirmatn.

برای مسائل یا بازخورد، یک issue در GitHub باز کنید. توسعه‌یافته توسط امین محمدی (www.artika.ir).
