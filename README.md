# EROS · Sentiment API

Microservicio de deteccion de sentimiento en español para Proyecto Onion.
Corre en CPU con el modelo `pysentimiento/robertuito-sentiment-analysis` y
expone una API REST. Sin dependencia de proveedores externos (no manda las
transcripciones a Google ni a nadie fuera de tu Railway).

## Deploy en un clic

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/new/template?template=https://github.com/leon2995/eros-sentiment)

Reemplaza `TU_USUARIO/eros-sentiment` en el enlace de arriba por tu repo real.
Al hacer clic, Railway clona el repo, detecta el Dockerfile y despliega solo.

## Paso a paso (primera vez)

1. Sube esta carpeta a un repo publico de GitHub:
```bash
cd eros-sentiment
git init
git add .
git commit -m "EROS sentiment API"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/eros-sentiment.git
git push -u origin main
```

2. Opcion A (boton): edita la URL del boton de arriba con tu repo y dale clic.
   Opcion B (dashboard): en Railway, New Project, Deploy from GitHub,
   selecciona el repo. Railway detecta el Dockerfile y construye solo.

3. El primer build tarda unos minutos porque descarga y cachea el modelo
   dentro de la imagen.

4. Genera el dominio publico en Settings, Networking, Generate Domain.

### Alternativa por CLI
```bash
npm i -g @railway/cli
railway login
railway init
railway up
```

## Variables de entorno (opcionales)
- `API_KEY`: si la defines, cada request debe mandar el header
  `x-api-key: <valor>`. Recomendado porque el dominio de Railway es publico.

## Endpoints

`GET /health` → estado del servicio.

`POST /analizar`
```json
{ "texto": "no me vuelvan a llamar, ya pague ayer" }
```
Respuesta:
```json
{
  "sentimiento": "negativo",
  "confianza": 0.9123,
  "scores": { "negativo": 0.9123, "neutral": 0.07, "positivo": 0.017 }
}
```

`POST /analizar-lote`
```json
{ "textos": ["gracias, muy amable", "esto es un abuso"] }
```

### Ejemplo curl
```bash
curl -X POST https://TU-APP.up.railway.app/analizar \
  -H "Content-Type: application/json" \
  -H "x-api-key: TU_LLAVE" \
  -d '{"texto":"que buena atencion, gracias"}'
```

## Costo aproximado (plan Pro)
El proceso consume ~0.8-1.2 GB de RAM encendido 24/7. A $0.014/GB-hora eso
son ~$8-12 USD de uso al mes, que se absorben dentro de los $20 de credito
incluido del plan Pro si tienes margen. CPU casi en cero salvo picos por
request. Sin cargos por request en Railway.

## Integracion con EROS
Reemplaza la llamada a Gemini por un `POST /analizar` con la transcripcion.
Para procesar lotes de una campaña usa `/analizar-lote`. El campo
`sentimiento` ya viene en el formato positivo/neutral/negativo.

FINCOMUN · MEJORA CONTINUA
