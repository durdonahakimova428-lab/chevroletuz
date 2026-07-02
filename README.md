# ChevroletUz — Django sayti

chevrolet.uz uslubidagi avtomobil saytining to'liq Django loyihasi.

## Tarkibi

- **Backend**: Python, Django
- **Frontend**: HTML, CSS (Bootstrap'siz, maxsus dizayn — qora navbar, oltin rang aksent)
- **Admin panel**: Avtomobillar (Product), Bannerlar, Yangiliklar (News), Dilerlar, So'rovlar
- **Profil**: Foydalanuvchi nomi va rasmi (avatar)
- **Autentifikatsiya**: Ro'yxatdan o'tish, Kirish, Chiqish

## Loyiha tuzilishi

```
chevroletuz/
├── chevroletuz/        # asosiy sozlamalar (settings.py, urls.py)
├── main/                # asosiy ilova
│   ├── models.py        # Banner, Category, Car, CarImage, News, Dealer, TestDriveRequest, Profile
│   ├── admin.py         # admin panel sozlamalari (rasm ko'rinishi bilan)
│   ├── views.py         # barcha sahifalar logikasi
│   ├── forms.py         # ro'yxatdan o'tish, profil, test-drayv formalari
│   ├── urls.py
│   └── templates/main/  # barcha HTML shablonlar
├── static/
│   ├── css/style.css    # asosiy dizayn
│   ├── js/main.js       # slayder logikasi
│   └── img/             # auth fon rasmi
├── media/                # yuklangan rasmlar (avtomobillar, bannerlar)
├── requirements.txt
└── manage.py
```

## O'rnatish (lokal kompyuterda)

```bash
# 1. Virtual muhit yaratish
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Kutubxonalarni o'rnatish
pip install -r requirements.txt

# 3. Ma'lumotlar bazasini tayyorlash
python manage.py migrate

# 4. Admin foydalanuvchi yaratish
python manage.py createsuperuser

# 5. Serverni ishga tushirish
python manage.py runserver
```

Brauzerda ochish: `http://127.0.0.1:8000/`
Admin panel: `http://127.0.0.1:8000/admin/`

> **Eslatma**: Loyihada tayyor demo ma'lumotlar (3 ta avtomobil, 1 banner, 1 yangilik) va
> `admin` / `admin12345` superuser allaqachon `db.sqlite3` faylida mavjud. Ishlab chiqarish
> uchun bu parolni darhol o'zgartiring (`python manage.py changepassword admin`).

## Admin panelda nima qila olasiz

1. **Avtomobillar (Car)** — yangi model qo'shish: rasm, narx, eski narx (chegirma uchun),
   texnik xususiyatlar, "Bosh sahifada ko'rsatish", "Yangi model", "Chegirmada" belgilari.
   Har bir avtomobilga **galereya rasmlari** (CarImage) qo'shish mumkin.
2. **Bannerlar** — bosh sahifadagi katta slayderni boshqarish (sarlavha, rasm, tartib).
3. **Yangiliklar (News)** — maxsus takliflar va yangiliklar bo'limi.
4. **Dilerlar** — filiallar ro'yxati.
5. **So'rovlar (TestDriveRequest)** — mijozlardan kelgan test-drayv so'rovlari.

## Suratlarni almashtirish

`chevrolet.uz`dagi kabi haqiqiy avtomobil suratlarini admin panel orqali yuklang:
`Avtomobillar → [model tanlang] → Asosiy rasm` maydoniga o'z suratingizni yuklang.
Galereya rasmlarini pastdagi "Galereya rasmi" bo'limidan qo'sha olasiz.

## Serverga (production) joylashtirish

Har qanday VPS (Ubuntu) serverga joylashtirish uchun:

```bash
# Serverga ulanib:
sudo apt update && sudo apt install python3-venv python3-pip nginx -y

# Loyihani yuklash (zip orqali yoki git orqali)
cd /var/www/
unzip chevroletuz.zip
cd chevroletuz

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# settings.py da:
#   DEBUG = False
#   ALLOWED_HOSTS = ['your-domain.uz', 'server-ip']
#   SECRET_KEY ni yangi qiymatga almashtiring

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser

# Gunicorn bilan ishga tushirish:
gunicorn chevroletuz.wsgi:application --bind 0.0.0.0:8000
```

Keyin Nginx orqali 8000-portni 80/443-portga proksi qilib, domeningizga ulaysiz
(yoki `systemd` xizmati sifatida sozlab, doimiy ishlaydigan qilasiz).

## Muhim xavfsizlik eslatmasi

Production muhitida albatta:
- `DEBUG = False` qiling
- `SECRET_KEY` ni maxfiy va yangi qiymatga o'zgartiring
- `ALLOWED_HOSTS` ga faqat o'z domeningizni yozing
- Demo `admin` parolini o'zgartiring

Savollar bo'lsa — Claude bilan davom etamiz! 🚗
