import json
import random
import unicodedata

# Cargar base de conocimiento
with open('intents.json', encoding='utf-8') as archivo:
    datos = json.load(archivo)

def normalizar(texto):
    """Elimina acentos y convierte a minúsculas."""
    texto = texto.lower()
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    return texto

def obtener_respuesta(mensaje_usuario):
    mensaje_normalizado = normalizar(mensaje_usuario)

    for intent in datos['intents']:
        for patron in intent['patterns']:
            # Busca cada palabra clave del patrón dentro del mensaje
            palabras = normalizar(patron).split()
            if any(palabra in mensaje_normalizado for palabra in palabras):
                return random.choice(intent['responses'])

    return 'Lo siento, no entiendo tu pregunta. ¿Puedes intentar con otras palabras?'
