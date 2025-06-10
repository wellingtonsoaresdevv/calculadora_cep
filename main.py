import requests
import re
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
# Não precisa de Optional nem typing aqui
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time

app = FastAPI(title="API de Cálculo de Distância para Locação")

geolocator = Nominatim(user_agent="locacao_distance_api")

# *** ESTA LINHA É CRÍTICA! A VARIÁVEL DE AMBIENTE DEVE SER "Maps_API_KEY" ***
Maps_API_KEY = os.getenv("Maps_API_KEY", "SUA_CHAVE_AQUI")

class DistanceResponse(BaseModel):
    cep_origem: str
    cep_destino: str
    distancia_km: float
    # Removido: duracao_min e metodo_calculo para simplificar a resposta

def validar_cep(cep: str) -> bool:
    cep = cep.strip().upper()
    pattern = r'^\d{5}-?\d{3}$'
    return bool(re.match(pattern, cep))

def normalizar_cep(cep: str) -> str:
    return re.sub(r'[^0-9]', '', cep)

def obter_endereco_viacep(cep: str):
    try:
        cep_normalizado = normalizar_cep(cep)
        response = requests.get(f"https://viacep.com.br/ws/{cep_normalizado}/json/", timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "erro" in data:
            return None
        return data
    except requests.exceptions.RequestException:
        return None

def obter_coordenadas(endereco_data):
    try:
        endereco_completo = f"{endereco_data.get('logradouro', '')}, {endereco_data.get('bairro', '')}, {endereco_data.get('localidade', '')}, {endereco_data.get('uf', '')}, Brasil"
        time.sleep(0.5) 
        location = geolocator.geocode(endereco_completo, timeout=10)
        if location:
            return location.latitude, location.longitude
        return None
    except (GeocoderTimedOut, GeocoderServiceError):
        return None

def calcular_distancia_haversine(lat1, lon1, lat2, lon2):
    import math
    
    R = 6371
    
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return distance

async def calcular_distancia_Maps(origem_str: str, destino_str: str):
    # Verifica se a chave está configurada corretamente
    if not Maps_API_KEY or Maps_API_KEY == "SUA_CHAVE_AQUI":
        print("AVISO: Chave de API do Google Maps não configurada ou inválida. Usando fallback.")
        return None # Retorna None para a distância se a chave não estiver OK.

    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    
    params = {
        "origins": origem_str,
        "destinations": destino_str,
        "key": Maps_API_KEY, # Usa a chave da variável global
        "mode": "driving",
        "language": "pt-BR",
        "units": "metric"
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data["status"] == "OK" and data["rows"] and data["rows"][0]["elements"]:
            element = data["rows"][0]["elements"][0]
            
            if element["status"] == "OK":
                distancia_metros = element["distance"]["value"]
                distancia_km = distancia_metros / 1000
                return distancia_km
            else:
                print(f"ERRO Google Maps Element Status: {element['status']}")
        else:
            print(f"ERRO Google Maps Response Status: {data.get('status', 'Status desconhecido')}")
            if "error_message" in data:
                print(f"Mensagem de erro: {data['error_message']}")
            
    except requests.exceptions.RequestException as e:
        print(f"ERRO de Requisição Google Maps API: {e}")
    except KeyError as e:
        print(f"ERRO ao Parsear Resposta Google Maps API (chave JSON ausente): {e}")
    except Exception as e:
        print(f"ERRO Inesperado Google Maps API: {e}")
        
    return None # Retorna None em caso de qualquer falha

@app.get("/calcular_distancia", response_model=DistanceResponse)
async def calcular_distancia(cep_origem: str, cep_destino: str):
    
    if not validar_cep(cep_origem):
        raise HTTPException(
            status_code=400, 
            detail={"erro": "CEP de origem inválido. Use o formato XXXXX-XXX ou XXXXXXXX."}
        )
    
    if not validar_cep(cep_destino):
        raise HTTPException(
            status_code=400, 
            detail={"erro": "CEP de destino inválido. Use o formato XXXXX-XXX ou XXXXXXXX."}
        )
    
    endereco_origem_data = obter_endereco_viacep(cep_origem)
    endereco_destino_data = obter_endereco_viacep(cep_destino)
    
    if not endereco_origem_data:
        raise HTTPException(
            status_code=400,
            detail={"erro": "CEP de origem não encontrado. Verifique se o CEP está correto."}
        )
    
    if not endereco_destino_data:
        raise HTTPException(
            status_code=400,
            detail={"erro": "CEP de destino não encontrado. Verifique se o CEP está correto."}
        )
    
    origem_str = f"{endereco_origem_data.get('logradouro', '')}, {endereco_origem_data.get('bairro', '')}, {endereco_origem_data.get('localidade', '')}, {endereco_origem_data.get('uf', '')}, Brasil"
    destino_str = f"{endereco_destino_data.get('logradouro', '')}, {endereco_destino_data.get('bairro', '')}, {endereco_destino_data.get('localidade', '')}, {endereco_destino_data.get('uf', '')}, Brasil"
    
    distancia_km = None

    # Tenta usar a Google Maps API primeiro
    # A função calcular_distancia_Maps agora só retorna a distância_km ou None
    distancia_km = await calcular_distancia_Maps(origem_str, destino_str)
    
    # Se a distância do Google Maps é None (falhou), usa Haversine
    if distancia_km is None:
        print("Usando Haversine (linha reta) como fallback.")
        coords_origem = obter_coordenadas(endereco_origem_data)
        coords_destino = obter_coordenadas(endereco_destino_data)
        
        if not coords_origem:
            raise HTTPException(
                status_code=500,
                detail={"erro": "Não foi possível obter as coordenadas do CEP de origem para cálculo Haversine."}
            )
        
        if not coords_destino:
            raise HTTPException(
                status_code=500,
                detail={"erro": "Não foi possível obter as coordenadas do CEP de destino para cálculo Haversine."}
            )
        
        lat1, lon1 = coords_origem
        lat2, lon2 = coords_destino
        distancia_km = calcular_distancia_haversine(lat1, lon1, lat2, lon2)
        
    if distancia_km is None: # Se ainda for None, algo deu muito errado
         raise HTTPException(
            status_code=500,
            detail={"erro": "Não foi possível calcular a distância por nenhum método disponível."}
        )

    return DistanceResponse(
        cep_origem=cep_origem,
        cep_destino=cep_destino,
        distancia_km=round(distancia_km, 2)
    )

@app.get("/")
async def root():
    return {
        "message": "API de Cálculo de Distância para Locação",
        "endpoint": "/calcular_distancia?cep_origem=XXXXX-XXX&cep_destino=XXXXX-XXX",
        "exemplo": "/calcular_distancia?cep_origem=24220-031&cep_destino=01001-000",
        "descricao": "Calcula a distância em quilômetros entre dois CEPs brasileiros"
    }
