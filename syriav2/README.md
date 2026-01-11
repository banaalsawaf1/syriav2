نظام سوريا V2.0 - نظام إدارة إعادة الإعمار

نظرة عامة:
سوريا V2.0 هو نظام إلكتروني متكامل لإدارة وتنسيق عملية إعادة إعمار سوريا بعد سنوات الحرب. تم تصميم النظام ليكون منصة شاملة تجمع بين المواطنين والمنظمات والمتعهدين والإداريين لتحقيق إدارة فعالة وشفافة لمشاريع إعادة الإعمار.


المتطلبات التقنية:
بيئة التطوير
Python 3.8 

pip (مدير حزم Python)

Git (للتحكم بالإصدارات)

المكتبات الرئيسية:
Django 6.0: إطار العمل الرئيسي

Pillow 12.0.0: معالجة الصور

django-crispy-forms 2.3: نماذج متطورة

folium 0.15.1: خرائط تفاعلية

plotly 5.24.1: رسومات بيانية

قواعد البيانات

MySql 


متطلبات التشغيل:

البرامج المطلوبة:
- Python 3.8 أو أعلى
- Git

حزم Python المطلوبة:
- Django 6.0
- crispy-bootstrap5
- folium
- Pillow

خطوات التثبيت والتشغيل:

1. تنزيل المشروع
```bash
git clone https://github.com/اسم-المستخدم/اسم-المشروع.git
cd اسم-المشروع
```

2. إنشاء وتفعيل البيئة الافتراضية
```bash
python -m venv venv
venv\Scripts\activate
```

3. تثبيت المتطلبات
```bash
pip install -r requirements.txt
```

4. إعداد قاعدة البيانات
```bash
python manage.py makemigrations
python manage.py migrate
```


6. جمع الملفات الثابتة
```bash
python manage.py collectstatic
```

7. تشغيل الخادم
```bash
python manage.py runserver
```

8. الوصول للموقع
- الموقع الرئيسي: [http://localhost:8000](http://localhost:8000)
- لوحة الإدارة: [http://localhost:8000/admin](http://localhost:8000/admin)

---


استكشاف الأخطاء وإصلاحها

مشكلة: ModuleNotFoundError
```bash
pip install django
pip install crispy-bootstrap5
```

مشكلة: No such table
```bash
python manage.py migrate
```

مشكلة: Static files not loading
```bash
python manage.py collectstatic
```




```bash
# 1. تنزيل المشروع
git clone https://github.com/banaalsawaf1/syriav2.git
cd syriav2

# 2. تثبيت المتطلبات
pip install django crispy-bootstrap5

# 3. تشغيل
python manage.py migrate
python manage.py runserver
```

زيارة: [http://localhost:8000](http://localhost:8000)
