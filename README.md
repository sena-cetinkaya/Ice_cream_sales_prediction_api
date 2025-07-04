# 🍦 Dondurma Karlılığı Tahmin Uygulaması (FastAPI + Makine Öğrenmesi)

Bu proje, **FastAPI tabanlı bir web uygulamasıdır** ve aşağıdaki özellikleri sunar:
- JWT destekli **kullanıcı kayıt/giriş sistemi**
- Sıcaklık verisine dayalı **dondurma satış tahmini**
- Jinja2 ile şablonlu **web arayüzü**
- PostgreSQL ile veri saklama (SQLModel ORM üzerinden)

---

## 🧠 Özellikler

- 🔐 Kullanıcı kayıt, giriş, silme, güncelleme
- 🔄 Access ve refresh token desteği (JWT)
- ♻️ `/refresh` ile token yenileme
- 📈 Sıcaklığa göre dondurma kar tahmini
- 🎨 Web arayüzü üzerinden tahmin sonucu gösterimi
- 🧠 Hazır eğitilmiş Lineer Regresyon modeli (`linear_regression_model.pkl`)

---

## 🧾 Kullanılan Teknolojiler

- Python 3.10+
- FastAPI
- SQLModel (ORM)
- PostgreSQL
- scikit-learn (ML için)
- passlib + jose (şifreleme ve token)
- Jinja2 (HTML şablonları için)

---

## 📁 Proje Yapısı

├── main.py # Uygulama giriş noktası

├── routes.py # API endpoint'leri

├── models.py # DB modelleri ve validasyon sınıfları

├── auth.py # JWT ve şifre işlemleri

├── model_trainer.py # ML modeli eğiten dosya

├── linear_regression_model.pkl # Eğitilmiş model (çıkış)

├── templates/

│ └── index.html # Tahmin formu (Jinja2 HTML)

├── static/ # Statik dosyalar (CSS, JS)

│ └── style.css

└── README.md

---

## ⚙️ Kurulum ve Başlatma

### 1️⃣ Gerekli Kütüphaneleri Yükle

```bash
pip install fastapi uvicorn[standard] sqlmodel psycopg2-binary passlib[bcrypt] python-jose scikit-learn jinja2
```

2️⃣ PostgreSQL Kurulumu
PostgreSQL kur

fastapi_db adında bir veritabanı oluştur

models.py içindeki bağlantı ayarları şu şekildedir:

```python
postgresql://postgres:postgres@localhost:5432/fastapi_db
```

Gerekirse kullanıcı adı, şifre ya da portu kendi ortamına göre düzenle.

3️⃣ Veritabanı Tablolarını Oluştur
Uygulamayı bir kere çalıştırman yeterli: create_db() fonksiyonu main.py içinde çağrılıyor.

Alternatif olarak manuel çalıştırabilirsin:

```python
from models import create_db
create_db()
```

4️⃣ ML Modelini Eğit
```bash
python model_trainer.py
```

Bu işlem:

CSV dosyasını okur (Ice Cream Sales - temperatures.csv)

Lineer Regresyon modeli oluşturur

linear_regression_model.pkl olarak kaydeder

⚠️ model_trainer.py içindeki CSV dosya yolunun doğru olduğundan emin ol.

▶️ Uygulamayı Çalıştır
```bash
uvicorn main:app --reload
```

Tarayıcıdan şu adrese git: http://localhost:8000

Swagger arayüzü için: http://localhost:8000/docs

🔌 API Endpoint'leri

📍 POST /register

Yeni kullanıcı kaydı oluşturur.

```json
{
  "email": "test@example.com",
  "password": "12345"
}
```

📍 POST /login

Giriş yapar, access ve refresh token döner.

📍 POST /refresh

Refresh token ile access token'ı yeniler.

```json
{
  "refresh_token": "<refresh_token>"
}
```

📍 GET /secret

Sadece geçerli access token ile erişilebilen korumalı sayfa.

📍 PUT /update

Kullanıcı email veya şifresini günceller.

📍 DELETE /delete

Hesabı siler (token ile doğrulama gerekir).

📍 POST /estimated_profit

Form üzerinden sıcaklık değeri alır, tahmini sonucu ana sayfada gösterir.

Form alanı:
```
temperature=30
```

🎨 Web Arayüzü

Anasayfa (/) üzerinden form sunulur

Sıcaklık girilerek kâr tahmini yapılır

Sonuç aynı sayfada görünür

🤖 Makine Öğrenmesi Modeli

Algoritma: Lineer Regresyon

Girdi: Temperature

Hedef: Ice Cream Profits

Kaydedilen model dosyası: linear_regression_model.pkl

Kullanım: Uygulama açıldığında model belleğe yüklenir

⚠️ Önemli Notlar

Şifreler bcrypt ile hash’lenir

JWT HS256 algoritması ile imzalanır

Token süresi dolduğunda /refresh kullanılır

Refresh token 7 gün geçerlidir

🪪 Geliştirici
Sena Çetinkaya

📧 E-posta: cetinkayasena96@gmail.com

🌐 GitHub: [https://github.com/sena-cetinkaya](https://github.com/sena-cetinkaya)

📄 Lisans

Bu proje MIT Lisansı ile lisanslanmıştır.
