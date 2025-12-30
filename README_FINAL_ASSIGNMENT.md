# Smart Garbage Segregation System - Final Assignment

## 📋 Proje Açıklaması

Bu proje, derin öğrenme kullanarak atık türlerini sınıflandıran ve servo motor davranışını yazılımsal olarak simüle eden bir web tabanlı uygulamadır.

## 🎯 Proje Amacı

Bir görüntüden atık türünü tahmin eden ve tahmine göre hangi çöp kutusuna gideceğini belirleyen (servo motor davranışı yazılımsal olarak simüle edilen) bir web tabanlı sistem oluşturmak.

## ⚙️ Teknolojiler

- **Backend**: FastAPI
- **Frontend**: HTML + CSS + JavaScript
- **Model**: TensorFlow/Keras (CNN)
- **Python**: 3.10+

## 📁 Proje Yapısı

```
.
├── main.py                 # FastAPI backend
├── utils.py                # Model ve preprocessing fonksiyonları
├── requirements.txt        # Python bağımlılıkları
├── static/
│   ├── index.html         # Ana HTML sayfası
│   ├── style.css          # CSS stilleri
│   └── script.js          # JavaScript kodları
└── weights/
    └── modelnew.h5        # Eğitilmiş model dosyası
```

## 🚀 Kurulum ve Çalıştırma

### 1. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 2. Uygulamayı Başlatın

```bash
uvicorn main:app --reload
```

### 3. Tarayıcıda Açın

Uygulama başladıktan sonra tarayıcınızda şu adresi açın:
```
http://localhost:8000
```

## 📊 Model Bilgileri

- **Model Dosyası**: `weights/modelnew.h5`
- **Model Tipi**: CNN (Convolutional Neural Network)
- **Giriş Boyutu**: 300x300x3 (RGB)
- **Çıkış Sınıfları**: 6 sınıf

### Sınıflar

```python
{
  0: "cardboard",
  1: "glass",
  2: "metal",
  3: "paper",
  4: "plastic",
  5: "trash"
}
```

## 🔄 Sınıf → Kutu (Servo) Kararı

- **Recyclable** (Geri Dönüştürülebilir):
  - cardboard, glass, metal, paper, plastic
  - Servo Açısı: 90°
  
- **Other** (Diğer):
  - trash
  - Servo Açısı: 0°

## 🎮 Kullanım

### 1. Fotoğraf Yükleme
- "Upload Image" bölümünden bir görüntü dosyası seçin
- Veya dosyayı sürükleyip bırakın

### 2. Kameradan Fotoğraf Çekme
- "Take Photo with Camera" bölümünden "Start Camera" butonuna tıklayın
- Kameraya izin verin
- "Capture Photo" ile fotoğraf çekin

### 3. Tahmin Yapma
- Görüntü seçildikten sonra "🔍 Predict" butonuna tıklayın
- Sonuçlar otomatik olarak gösterilecektir:
  - Tahmin edilen sınıf
  - Güven skoru (confidence)
  - Kutu tipi (Recyclable/Other)
  - Servo motor simülasyonu

## 📡 API Endpoint

### POST /predict

Görüntü dosyası yükleyerek tahmin yapma.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: `file` (image file)

**Response:**
```json
{
  "predicted_class": "plastic",
  "confidence": 0.81,
  "bin": "Recyclable",
  "servo_angle": 90
}
```

## 🔧 Önemli Notlar

- Model eğitimi yapılmaz, sadece eğitilmiş model kullanılır
- Dataset (Data/Train, Data/Test) kullanılmaz
- Etiketler hardcode edilmiştir
- Fiziksel servo motor yoktur, sadece simülasyon vardır
- Model uygulama başında bir kez yüklenir

## 📝 Kod Yapısı

### Backend (main.py)
- FastAPI uygulaması
- Model yükleme (startup event)
- `/predict` endpoint
- CORS desteği
- Static dosya servisi

### Utils (utils.py)
- Model mimarisi tanımı
- Görüntü ön işleme
- Model yükleme fonksiyonu
- Recyclable/Other sınıflandırması

### Frontend
- **index.html**: Ana sayfa yapısı
- **style.css**: Modern ve temiz tasarım
- **script.js**: API çağrıları ve servo simülasyonu

## 🎓 Akademik Amaç

Bu proje bir üniversite ödevidir. Amaç, donanım gerektirmeden "kamera/görüntü → yapay zekâ kararı → servo yönlendirme" mantığını uçtan uca yazılımsal olarak göstermektir.

## 📄 Lisans

Bu proje akademik amaçlı geliştirilmiştir.



