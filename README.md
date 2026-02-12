# ⚖️ Anayasa RAG Chatbot  
### PDF → Retrieval → Kaynaklı Cevap (Grounded Answers)

Yerel (local) çalışan, yüklenen Anayasa PDF’inden **yalnızca metne dayanarak** cevap üreten ve kullanılan kaynakları açıkça gösteren bir Retrieval-Augmented Generation (RAG) uygulamasıdır.

---

##  Proje Özeti

Bu uygulama:

- PDF yükler
- Metni madde bazlı parçalara ayırır
- BM25 ile en alakalı bölümleri getirir
- LLM kullanarak yalnızca bu kaynaklara dayanarak cevap üretir
- Kullanılan kaynakları şeffaf biçimde gösterir

> ⚠️ Uyarı: Bu proje yalnızca eğitim ve demo amaçlıdır. Hukuki danışmanlık niteliği taşımaz.

---

##  Özellikler

-  PDF yükleme (örn: Türkiye Cumhuriyeti Anayasası)
-  “Madde …” bazlı metin parçalama
-  BM25 ile Top-K retrieval
-  Kaynak kontrollü cevap üretimi
-  Kaynak gösterimi (retrieved passages)
-  Hallucination azaltılmış katı prompt politikası

---

## 🖼 Demo

### PDF Yükleme ve İndeksleme
<img width="1919" height="876" alt="demo1" src="https://github.com/user-attachments/assets/a899e9cf-89c2-4bc2-8a20-98c39983836b" />

### Kaynaklı Cevap Üretimi
<img width="1294" height="716" alt="demo3" src="https://github.com/user-attachments/assets/42b688b0-c2b5-4e80-b576-8f63f6dd7470" />
<img width="1511" height="695" alt="demo4" src="https://github.com/user-attachments/assets/0079cbea-3948-4880-87c3-3fba44814a85" />

### Retrieval (Top-K)
<img width="287" height="124" alt="demo2" src="https://github.com/user-attachments/assets/d5142d5d-90a2-4616-a488-fd006f8dbc32" />

### Kaynak Gösterimi
<img width="1505" height="686" alt="demo5" src="https://github.com/user-attachments/assets/1f3d3503-bf05-442a-b5cf-bb776ed40515" />
<img width="723" height="110" alt="image" src="https://github.com/user-attachments/assets/431f0cbc-54c9-4dab-bd08-c1d62720c6c1" />


---

## 🧩 Kullanılan Teknolojiler

- Python 3.10+
- Streamlit
- pypdf
- rank-bm25
- Ollama (local LLM – `llama3.1:8b`)

---

## 🏗 Mimari Akış
PDF
↓
Metni çıkar
↓
Madde bazlı parçalama
↓
BM25 Retrieval (Top-K)
↓
LLM (Sadece kaynaklardan cevap)
↓
Cevap + Kaynak Gösterimi


---

##  Kurulum

### 1- Ollama Kur

=> https://ollama.com

Modeli indir:

```bash
ollama pull llama3.1:8b
ollama run llama3.1:8b

```
Python ortamı oluştur ve bağımlılıkları yükle (Windows):
```bash
.venv\Scripts\activate
pip install -r requirements.txt
```
Uygulamayı başlat:
```bash
streamlit run app.py
```

