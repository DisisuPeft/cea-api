import unicodedata

SENTINELS_EMPTY = {"null", "undefined", "none", "nan"}

def normalize_q(raw):
    q = (raw or "").strip()
    if q.lower() in SENTINELS_EMPTY:
        return ""
    return q

def strip_accents(s: str) -> str:
    # Elimina diacríticos: "Fernández" -> "Fernandez"
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if unicodedata.category(c) != "Mn")

def tokenize(q: str):
    # minúsculas, recorta, quita acentos y separa por espacios
    q_clean = strip_accents(q.lower()).strip()
    terms = [t for t in q_clean.split() if t]
    return terms