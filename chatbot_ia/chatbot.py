import json
import random
import unicodedata

# Cargar base de conocimiento
with open('intents.json', encoding='utf-8') as archivo:
    datos = json.load(archivo)

# Palabras vacías que no deben usarse para hacer coincidir intents
PALABRAS_VACIAS = {
    'a', 'al', 'con', 'como', 'cual', 'de', 'del', 'el', 'en', 'es',
    'eso', 'esta', 'este', 'hay', 'la', 'las', 'le', 'les', 'lo', 'los',
    'me', 'mi', 'no', 'o', 'para', 'por', 'que', 'se', 'si', 'su',
    'sus', 'te', 'tu', 'tus', 'un', 'una', 'y', 'yo'
}

def normalizar(texto):
    """Elimina acentos y convierte a minúsculas."""
    texto = texto.lower()
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    return texto

def palabras_clave(texto):
    """Extrae palabras significativas (sin palabras vacías)."""
    return [p for p in normalizar(texto).split() if p not in PALABRAS_VACIAS and len(p) > 2]

def obtener_respuesta(mensaje_usuario):
    palabras_usuario = palabras_clave(mensaje_usuario)

    if not palabras_usuario:
        return 'Lo siento, no entiendo tu pregunta. ¿Puedes intentar con otras palabras?'

    mejor_intent = None
    mejor_puntaje = 0

    for intent in datos['intents']:
        for patron in intent['patterns']:
            palabras_patron = palabras_clave(patron)
            if not palabras_patron:
                continue

            # Contar cuántas palabras clave del patrón están en el mensaje
            coincidencias = sum(1 for p in palabras_patron if p in palabras_usuario)
            # Puntaje: proporción de palabras del patrón que coinciden
            puntaje = coincidencias / len(palabras_patron)

            if puntaje > mejor_puntaje:
                mejor_puntaje = puntaje
                mejor_intent = intent

    # Solo responder si hay una coincidencia razonablemente buena
    if mejor_intent and mejor_puntaje >= 0.5:
        return random.choice(mejor_intent['responses'])

    return 'Lo siento, no entiendo tu pregunta. ¿Puedes intentar con otras palabras?'
