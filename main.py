from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import math

app = FastAPI()

# Permitir solicitudes desde cualquier origen (necesario para App Inventor)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar los desfibriladores reducidos en memoria al iniciar la API
with open("dea_catalunya_lite.json", "r", encoding="utf-8") as f:
    DEAS = json.load(f)

def calcular_distancia_metros(lat1: float, lon1: float, lat2: float, lon2: float) -> int:
    """Calcula la distancia en metros entre dos coordenadas usando la fórmula de Haversine."""
    R = 6371000  # Radio de la Tierra en metros
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return round(R * c)

@app.get("/")
def inicio():
    return {"mensaje": "API de Desfibriladores activa"}

@app.get("/cercanos")
def obtener_tres_mas_cercanos(lat: float, lng: float):
    lista_con_distancias = []

    for dea in DEAS:
        distancia = calcular_distancia_metros(lat, lng, dea["lat"], dea["lng"])
        
        # Hacemos una copia del desfibrilador y le añadimos la distancia en metros
        dea_info = dea.copy()
        dea_info["dist_m"] = distancia
        lista_con_distancias.append(dea_info)

    # Ordenamos la lista por la distancia de menor a mayor
    lista_ordenada = sorted(lista_con_distancias, key=lambda x: x["dist_m"])

    # Devolvemos SOLO los 3 primeros
    return lista_ordenada[:3]
