import requests

OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.1:8b"

SYSTEM = """Sen bir hukuk asistanısın.
Sadece verilen KAYNAKLAR'a dayanarak cevap ver.

Kurallar:
- Metin dışı bilgi kullanma.
- Kaynaklardaki açık hükümlere dayanarak zorunlu mantıksal sonuç çıkarabilirsin.
  (Örn: 'yetki devredilemez' → 'Cumhurbaşkanı devralamaz')
- Kaynaklarda dayanak yoksa aynen şunu yaz:
  "Bu metinde açıkça belirtilmemiştir."
- Cevap kısa ve net olsun (2-5 cümle).
- En sonda: Kaynak: SOURCE X (gerekirse birden fazla) yaz.
- Kaynak dışı konulara sapma (ör. başka maddelerden alakasız açıklama) yapma.
"""


def ask_llm(question: str, sources: list[str]) -> str:
    src_block = "\n\n".join([f"[SOURCE {i+1}]\n{src}" for i, src in enumerate(sources)])

    user_prompt = f"""SORU:
{question}

KAYNAKLAR:
{src_block}

Talimat:
- Cevap sadece KAYNAKLAR'dan gelmeli.
- Eğer bulunamazsa "Bu metinde açıkça belirtilmemiştir." yaz.
- Sonuna 'Kaynak: SOURCE 1' gibi ekle.
"""

    payload = {
        "model": MODEL,
        "stream": False,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user_prompt},
        ],
        "options": {"temperature": 0.0}

    }

    r = requests.post(OLLAMA_CHAT_URL, json=payload, timeout=180)
    r.raise_for_status()

    data = r.json()
    # Ollama chat response: {"message": {"role":"assistant","content":"..."}}
    return (data.get("message", {}).get("content") or "").strip()
