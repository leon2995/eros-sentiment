from pysentimiento import create_analyzer

# Descarga los pesos y los deja cacheados dentro de la imagen,
# asi el contenedor arranca sin descargar nada (sin cold-start).
create_analyzer(task="sentiment", lang="es")
print("Modelo de sentimiento (es) descargado y cacheado.")
