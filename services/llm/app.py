"""
FastAPI LLM Normalizer: rule-based (default) with optional HF small model.
"""
import os
import re
from fastapi import FastAPI
from pydantic import BaseModel

USE_HF = os.environ.get("USE_HF_MODEL", "0") == "1"
hf_model = None
tokenizer = None

app = FastAPI(title="LLM Normalizer", version="1.0.0")

def simple_normalize(text: str) -> str:
    # Lowercase, strip, collapse whitespace, normalize dates dd/mm/yyyy -> yyyy-mm-dd (naive)
    t = text.strip().lower()
    t = re.sub(r"\s+", " ", t)
    # Convert common date forms to ISO
    t = re.sub(r"(\b\d{1,2})/(\d{1,2})/(\d{4})",
               lambda m: f"{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}", t)
    t = re.sub(r"(\b\d{4})-(\d{1,2})-(\d{1,2})",
               lambda m: f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}", t)
    return t

def hf_normalize(text: str) -> str:
    # Toy use of a small model; returns rule-based normalization to remain deterministic.
    global hf_model, tokenizer
    try:
        from transformers import AutoModelForCausalLM, AutoTokenizer
        if hf_model is None or tokenizer is None:
            name = "distilgpt2"
            tokenizer = AutoTokenizer.from_pretrained(name)
            hf_model = AutoModelForCausalLM.from_pretrained(name)
        # No actual generation; just return rule-based normalization.
        return simple_normalize(text)
    except Exception:
        return simple_normalize(text)

class NormIn(BaseModel):
    text: str

class NormOut(BaseModel):
    normalized: str

@app.post("/normalize", response_model=NormOut)
def normalize(inp: NormIn):
    if USE_HF:
        norm = hf_normalize(inp.text)
    else:
        norm = simple_normalize(inp.text)
    return {"normalized": norm}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)

