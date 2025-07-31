import re
import spacy
from typing import List, Dict

_nlp = spacy.load("en_core_web_sm")

_patterns = [
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),  # SSN
    re.compile(r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b"),  # card
]

def detect(text: str) -> List[Dict]:
    ents = []
    doc = _nlp(text)
    for ent in doc.ents:
        ents.append(dict(text=ent.text, label=ent.label_, start=ent.start_char, end=ent.end_char))
    for pat in _patterns:
        for m in pat.finditer(text):
            ents.append(dict(text=m.group(), label="CUSTOM", start=m.start(), end=m.end()))
    return ents