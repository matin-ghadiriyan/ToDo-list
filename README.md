# ✅ تسک‌یار (TaskFlow)

یک اپلیکیشن وب مدرن، ماژولار و متن‌باز برای مدیریت کارهای روزانه، ساخته‌شده با **Flask** و **SQLite**.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-blue?logo=python" alt="Python" />
  <img src="https://img.shields.io/badge/Flask-3.x-black?logo=flask" alt="Flask" />
  <img src="https://img.shields.io/badge/SQLite-3-blue?logo=sqlite" alt="SQLite" />
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License" />
</p>

## ✨ امکانات

- 📊 **داشبورد آماری** با نمودار پیشرفت، تعداد کارها، عقب‌افتاده‌ها و کارهای امروز
- 🗂️ **صفحه همه کارها** با جستجو و فیلتر بر اساس وضعیت و اولویت
- 📅 **صفحه کارهای امروز** با نمای تایم‌لاین
- ➕ **افزودن و ویرایش کار** با فرم‌های اعتبارسنجی‌شده (WTForms)
- 🎯 **اولویت‌بندی** (کم / معمولی / زیاد) و **تاریخ سررسید**
- 🔌 **API JSON** برای تعاملات سمت کلاینت
- 🎨 **رابط کاربری حرفه‌ای**، فارسی (RTL) و کاملاً ریسپانسیو
- ⌨️ میان‌بر کیبورد (`N` برای کار جدید)

## 🛠️ تکنولوژی‌ها

| بخش | تکنولوژی |
|-----|----------|
| بک‌اند | Python, Flask, Blueprints |
| دیتابیس | SQLite + Flask-SQLAlchemy |
| فرم‌ها | Flask-WTF, WTForms |
| مهاجرت | Flask-Migrate |
| فرانت‌اند | HTML5, CSS3, JavaScript (Vanilla) |

## 📁 ساختار پروژه

```
flask-ToDoList/
├── app/
│   ├── __init__.py          # Application Factory
│   ├── extensions.py        # نمونه‌های db و migrate
│   ├── models.py            # مدل Task
│   ├── forms.py             # فرم‌های WTForms
│   ├── routes/
│   │   ├── main.py          # داشبورد و درباره
│   │   ├── tasks.py         # CRUD کارها
│   │   └── api.py           # نقاط پایانی JSON
│   ├── templates/
│   │   ├── base.html        # قالب پایه
│   │   ├── dashboard.html   # داشبورد
│   │   ├── about.html       # درباره
│   │   └── tasks/
│   │       ├── list.html    # همه کارها
│   │       ├── today.html   # کارهای امروز
│   │       └── form.html    # فرم افزودن/ویرایش
│   └── static/
│       ├── css/style.css    # طراحی حرفه‌ای
│       └── js/app.js        # تعاملات کلاینت
├── config.py                # تنظیمات
├── run.py                   # نقطه ورود توسعه
├── wsgi.py                  # نقطه ورود پروداکشن
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE
├── CONTRIBUTING.md
└── README.md
```

## 🚀 نصب و اجرا

### ۱. کلون کردن

```bash
git clone https://github.com/USERNAME/flask-ToDoList.git
cd flask-ToDoList
```

### ۲. محیط مجازی

**ویندوز:**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**لینوکس / مک:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### ۳. نصب وابستگی‌ها

```bash
pip install -r requirements.txt
```

### ۴. تنظیمات محیطی (اختیاری)

```bash
copy .env.example .env   # ویندوز
cp .env.example .env     # لینوکس/مک
```

### ۵. اجرا

```bash
python run.py
```

سپس مرورگر را باز کنید: **http://127.0.0.1:5000**

> دیتابیس به‌صورت خودکار در پوشه `instance/todo.db` ساخته می‌شود.

## 🔌 مسیرها (Routes)

### صفحات

| متد | مسیر | توضیح |
|-----|------|-------|
| GET | `/` | داشبورد |
| GET | `/about` | درباره |
| GET | `/tasks/` | همه کارها (با فیلتر و جستجو) |
| GET | `/tasks/today` | کارهای امروز |
| GET/POST | `/tasks/new` | افزودن کار |
| GET/POST | `/tasks/<id>/edit` | ویرایش کار |
| POST | `/tasks/<id>/toggle` | تغییر وضعیت |
| POST | `/tasks/<id>/delete` | حذف کار |

### API

| متد | مسیر | توضیح |
|-----|------|-------|
| GET | `/api/tasks` | لیست همه کارها (JSON) |
| PATCH | `/api/tasks/<id>` | به‌روزرسانی جزئی |

## 🤝 مشارکت

لطفاً فایل [CONTRIBUTING.md](CONTRIBUTING.md) را مطالعه کنید.

## 📄 مجوز

این پروژه تحت مجوز **MIT** منتشر شده است — جزئیات در [LICENSE](LICENSE).
