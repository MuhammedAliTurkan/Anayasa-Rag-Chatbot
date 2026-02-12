import re
from rank_bm25 import BM25Okapi


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_by_madde(text: str) -> list[dict]:
    """
    'Madde 161 – ...' gibi blokları yakalar.
    """
    text = normalize_text(text)

    pattern = r"(Madde\s+(\d+)\s*[–-]\s*.*?)(?=(\nMadde\s+\d+\s*[–-])|\Z)"
    matches = re.findall(pattern, text, flags=re.DOTALL)

    items = []

    for full_block, madde_no, _ in matches:
        block = full_block.strip()
        first_line = block.split("\n", 1)[0].strip()

        items.append({
            "id": f"madde_{madde_no}",
            "title": first_line,
            "text": block
        })

    if not items:
        items = fallback_chunk(text)

    return items


def fallback_chunk(text: str, chunk_size_words: int = 220, overlap_words: int = 60) -> list[dict]:
    words = text.split()
    chunks = []
    start = 0
    idx = 0

    while start < len(words):
        end = min(start + chunk_size_words, len(words))
        chunk = " ".join(words[start:end]).strip()

        if chunk:
            chunks.append({
                "id": f"chunk_{idx}",
                "title": f"Chunk {idx}",
                "text": chunk
            })
            idx += 1

        if end == len(words):
            break

        start = max(0, end - overlap_words)

    return chunks


def _tokenize(s: str) -> list[str]:
    s = s.lower()
    s = re.sub(r"[^\w\sçğıöşü]", " ", s)
    return [t for t in s.split() if t]


def build_bm25(items: list[dict]) -> BM25Okapi:
    tokenized = [_tokenize(it["text"]) for it in items]
    return BM25Okapi(tokenized)


def retrieve(items: list[dict], bm25: BM25Okapi, query: str, k: int = 3) -> list[dict]:
    if not isinstance(items, list):
        raise TypeError(f"items must be a list, got {type(items)}")

    scores = bm25.get_scores(_tokenize(query))
    idxs = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]

    results = []

    for i in idxs:
        it = dict(items[i])
        it["score"] = float(scores[i])
        results.append(it)

    return results
