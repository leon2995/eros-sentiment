import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from pysentimiento import create_analyzer

# Mapeo POS/NEU/NEG del modelo -> etiquetas de EROS
ETIQUETAS = {"POS": "positivo", "NEU": "neutral", "NEG": "negativo"}

# Opcional: si defines la variable de entorno API_KEY, se exige en cada request
API_KEY = os.getenv("API_KEY")

_analyzer = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _analyzer
    _analyzer = create_analyzer(task="sentiment", lang="es")
    yield
    _analyzer = None


app = FastAPI(title="EROS · Sentiment API", version="1.0.0", lifespan=lifespan)


class EntradaTexto(BaseModel):
    texto: str


class EntradaLote(BaseModel):
    textos: list[str]


def _verificar_key(x_api_key):
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API key invalida")


def _formatear(pred):
    probas = {ETIQUETAS.get(k, k): round(float(v), 4) for k, v in pred.probas.items()}
    return {
        "sentimiento": ETIQUETAS.get(pred.output, pred.output),
        "confianza": round(float(pred.probas[pred.output]), 4),
        "scores": probas,
    }


@app.get("/")
def raiz():
    return {
        "servicio": "EROS Sentiment API",
        "modelo": "pysentimiento/robertuito-sentiment-analysis",
        "idioma": "es",
    }


@app.get("/health")
def health():
    return {"status": "ok", "modelo_cargado": _analyzer is not None}


@app.post("/analizar")
def analizar(payload: EntradaTexto, x_api_key: str = Header(default=None)):
    _verificar_key(x_api_key)
    texto = payload.texto.strip()
    if not texto:
        raise HTTPException(status_code=422, detail="El campo 'texto' esta vacio")
    return _formatear(_analyzer.predict(texto))


@app.post("/analizar-lote")
def analizar_lote(payload: EntradaLote, x_api_key: str = Header(default=None)):
    _verificar_key(x_api_key)
    if not payload.textos:
        raise HTTPException(status_code=422, detail="La lista 'textos' esta vacia")
    preds = _analyzer.predict(payload.textos)
    return {"resultados": [_formatear(p) for p in preds]}
