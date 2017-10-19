import os
from datetime import datetime

import pymongo

from scraper import (
    normalize_value, normalize_label, normalize_path, normalize_last_updated
)

client = pymongo.MongoClient(os.getenv('MONGODB_URI'))
db = client.get_default_database()

objects = [
 {
   "Type": "AEE",
   "path": "aee",
   "Fecha Actualizado": "9/26/2017",
   "Status": "5.00%",
   "Fecha Obtenido": "9/26/2017"
 },
 {
   "Type": "Antenas Celular",
   "path": "antenna",
   "Fecha Actualizado": "9/26/2017",
   "Status": "8.00%",
   "Fecha Obtenido": "9/26/2017"
 },
 {
   "Type": "Gasolineras",
   "path": "gas",
   "Fecha Actualizado": "9/26/2017",
   "Status": "40.91%",
   "Fecha Obtenido": "9/26/2017"
 },
 {
   "Type": "Puertos Abiertos",
   "path": "port",
   "Fecha Actualizado": "9/26/2017",
   "Status": "32.00%",
   "Fecha Obtenido": "9/26/2017"
 },
 {
   "Type": "AEE",
   "path": "aee",
   "Fecha Actualizado": "9/27/2017",
   "Status": "5.00%",
   "Fecha Obtenido": "9/27/2017"
 },
 {
   "Type": "Antenas Celular",
   "path": "antenna",
   "Fecha Actualizado": "9/27/2017",
   "Status": "9.00%",
   "Fecha Obtenido": "9/27/2017"
 },
 {
   "Type": "ATMs",
   "path": "atms",
   "Fecha Actualizado": "9/27/2017",
   "Status": "150",
   "Fecha Obtenido": "9/27/2017"
 },
 {
   "Type": "Correos",
   "path": "goverment.mail",
   "Fecha Actualizado": "9/27/2017",
   "Status": "5",
   "Fecha Obtenido": "9/27/2017"
 },
 {
   "Type": "Gasolineras",
   "path": "gas",
   "Fecha Actualizado": "9/27/2017",
   "Status": "48.45%",
   "Fecha Obtenido": "9/27/2017"
 },
 {
   "Type": "Hospitales Asistidos",
   "path": "hospital",
   "Fecha Actualizado": "9/27/2017",
   "Status": "29",
   "Fecha Obtenido": "9/27/2017"
 },
 {
   "Type": "Puertos Abiertos",
   "path": "port",
   "Fecha Actualizado": "9/27/2017",
   "Status": "44.00%",
   "Fecha Obtenido": "9/27/2017"
 },
 {
   "Type": "Refugiados",
   "path": "refugee",
   "Fecha Actualizado": "9/27/2017",
   "Status": "10,389",
   "Fecha Obtenido": "9/27/2017"
 },
 {
   "Type": "Refugios",
   "path": "shelter",
   "Fecha Actualizado": "9/27/2017",
   "Status": "182",
   "Fecha Obtenido": "9/27/2017"
 },
 {
   "Type": "Supermercados",
   "path": "supermarket",
   "Fecha Actualizado": "9/27/2017",
   "Status": "202.00",
   "Fecha Obtenido": "9/27/2017"
 },
 {
   "Type": "AEE",
   "path": "aee",
   "Fecha Actualizado": "9/28/2017",
   "Status": "5.00%",
   "Fecha Obtenido": "9/28/2017"
 },
 {
   "Type": "Antenas Celular",
   "path": "antenna",
   "Fecha Actualizado": "9/28/2017",
   "Status": "9.00%",
   "Fecha Obtenido": "9/28/2017"
 },
 {
   "Type": "Correos",
   "path": "goverment.mail",
   "Fecha Actualizado": "9/28/2017",
   "Status": "28",
   "Fecha Obtenido": "9/28/2017"
 },
 {
   "Type": "Diesel (abastos en barriles)",
   "path": "barrel.diesel",
   "Fecha Actualizado": "9/28/2017",
   "Status": "574,158",
   "Fecha Obtenido": "9/28/2017"
 },
 {
   "Type": "Gasolina (abastos en barriles)",
   "path": "barrel.gas",
   "Fecha Actualizado": "9/28/2017",
   "Status": "402,781",
   "Fecha Obtenido": "9/28/2017"
 },
 {
   "Type": "Gasolineras",
   "path": "gas",
   "Fecha Actualizado": "9/28/2017",
   "Status": "62.64%",
   "Fecha Obtenido": "9/28/2017"
 },
 {
   "Type": "Hospitales Asistidos",
   "path": "hospital",
   "Fecha Actualizado": "9/28/2017",
   "Status": "33",
   "Fecha Obtenido": "9/28/2017"
 },
 {
   "Type": "Puertos Abiertos",
   "path": "port",
   "Fecha Actualizado": "9/28/2017",
   "Status": "50.00%",
   "Fecha Obtenido": "9/28/2017"
 },
 {
   "Type": "Supermercados",
   "path": "supermarket",
   "Fecha Actualizado": "9/28/2017",
   "Status": "224.00",
   "Fecha Obtenido": "9/28/2017"
 },
 {
   "Type": "Telecomunicaciones",
   "path": "telecomunication",
   "Fecha Actualizado": "9/28/2017",
   "Status": "28.00%",
   "Fecha Obtenido": "9/28/2017"
 },
 {
   "Type": "Torres celular",
   "path": "tower",
   "Fecha Actualizado": "9/28/2017",
   "Status": "28.00",
   "Fecha Obtenido": "9/28/2017"
 },
 {
   "Type": "AAA Este",
   "Fecha Actualizado": "9/29/2017",
   "Status": "30.00%",
   "Fecha Obtenido": "9/29/2017"
 },
 {
   "Type": "AAA Metro",
   "Fecha Actualizado": "9/29/2017",
   "Status": "49.00%",
   "Fecha Obtenido": "9/29/2017"
 },
 {
   "Type": "AAA Norte",
   "Fecha Actualizado": "9/29/2017",
   "Status": "26.00%",
   "Fecha Obtenido": "9/29/2017"
 },
 {
   "Type": "AAA Oeste",
   "Fecha Actualizado": "9/29/2017",
   "Status": "58.00%",
   "Fecha Obtenido": "9/29/2017"
 },
 {
   "Type": "AAA Sur",
   "Fecha Actualizado": "9/29/2017",
   "Status": "39.00%",
   "Fecha Obtenido": "9/29/2017"
 },
 {
   "Type": "AEE",
   "path": "aee",
   "Fecha Actualizado": "9/29/2017",
   "Status": "5.00%",
   "Fecha Obtenido": "9/29/2017"
 },
 {
   "Type": "Antenas Celular",
   "path": "antenna",
   "Fecha Actualizado": "9/29/2017",
   "Status": "10.00%",
   "Fecha Obtenido": "9/29/2017"
 },
 {
   "Type": "ATMs",
   "path": "atms",
   "Fecha Actualizado": "9/29/2017",
   "Status": "230",
   "Fecha Obtenido": "9/29/2017"
 },
 {
   "Type": "Cooperativas",
   "path": "cooperatives",
   "Fecha Actualizado": "9/29/2017",
   "Status": "63",
   "Fecha Obtenido": "9/29/2017"
 },
 {
   "Type": "Correos",
   "path": "goverment.mail",
   "Fecha Actualizado": "9/29/2017",
   "Status": "56",
   "Fecha Obtenido": "9/29/2017"
 },
 {
   "Type": "Diesel (abastos en barriles)",
   "path": "barrel.diesel",
   "Fecha Actualizado": "9/29/2017",
   "Status": "562,935",
   "Fecha Obtenido": "9/29/2017"
 },
 {
   "Type": "Diesel (abastos en barriles)",
   "path": "barrel.diesel",
   "Fecha Actualizado": "9/29/2017",
   "Status": "467,766",
   "Fecha Obtenido": "9/29/2017"
 },
 {
   "Type": "Farmacias",
   "path": "pharmacy",
   "Fecha Actualizado": "9/29/2017",
   "Status": "311",
   "Fecha Obtenido": "9/29/2017"
 },
 {
   "Type": "Gasolineras",
   "path": "gas",
   "Fecha Actualizado": "9/29/2017",
   "Status": "61.36%",
   "Fecha Obtenido": "9/29/2017"
 },
 {
   "Type": "Hospitales Asistidos",
   "path": "hospital",
   "Fecha Actualizado": "9/29/2017",
   "Status": "33",
   "Fecha Obtenido": "9/29/2017"
 },
 {
   "Type": "Mascotas Refugiadas",
   "path": "pet",
   "Fecha Actualizado": "9/29/2017",
   "Status": "193",
   "Fecha Obtenido": "9/29/2017"
 },
 {
   "Type": "Puertos Abiertos",
   "path": "port",
   "Fecha Actualizado": "9/29/2017",
   "Status": "54.00%",
   "Fecha Obtenido": "9/29/2017"
 },
 {
   "Type": "Refugiados",
   "path": "refugee",
   "Fecha Actualizado": "9/29/2017",
   "Status": "10201",
   "Fecha Obtenido": "9/29/2017"
 },
 {
   "Type": "Refugios",
   "path": "shelter",
   "Fecha Actualizado": "9/29/2017",
   "Status": "161",
   "Fecha Obtenido": "9/29/2017"
 },
 {
   "Type": "Telecomunicaciones",
   "path": "telecomunication",
   "Fecha Actualizado": "9/29/2017",
   "Status": "30.00%",
   "Fecha Obtenido": "9/29/2017"
 },
 {
   "Type": "Torres celular",
   "path": "tower",
   "Fecha Actualizado": "9/29/2017",
   "Status": "96.00",
   "Fecha Obtenido": "9/29/2017"
 },
 {
   "Type": "AAA Este",
   "Fecha Actualizado": "9/30/2017",
   "Status": "46.00%",
   "Fecha Obtenido": "9/30/2017"
 },
 {
   "Type": "AAA Metro",
   "Fecha Actualizado": "9/30/2017",
   "Status": "55.00%",
   "Fecha Obtenido": "9/30/2017"
 },
 {
   "Type": "AAA Norte",
   "Fecha Actualizado": "9/30/2017",
   "Status": "29.00%",
   "Fecha Obtenido": "9/30/2017"
 },
 {
   "Type": "AAA Oeste",
   "Fecha Actualizado": "9/30/2017",
   "Status": "19.00%",
   "Fecha Obtenido": "9/30/2017"
 },
 {
   "Type": "AAA Sur",
   "Fecha Actualizado": "9/30/2017",
   "Status": "72.00%",
   "Fecha Obtenido": "9/30/2017"
 },
 {
   "Type": "AEE",
   "path": "aee",
   "Fecha Actualizado": "9/29/2017",
   "Status": "5.00%",
   "Fecha Obtenido": "9/30/2017"
 },
 {
   "Type": "Centros de Dialisis Asistidos",
   "path": "dialysis",
   "Fecha Actualizado": "9/30/2017",
   "Status": "46",
   "Fecha Obtenido": "9/30/2017"
 },
 {
   "Type": "Farmacias",
   "path": "pharmacy",
   "Fecha Actualizado": "9/28/2017",
   "Status": "337",
   "Fecha Obtenido": "9/30/2017"
 },
 {
   "Type": "Gasolineras",
   "path": "gas",
   "Fecha Actualizado": "9/30/2017",
   "Status": "64.91%",
   "Fecha Obtenido": "9/30/2017"
 },
 {
   "Type": "Hospitales Asistidos",
   "path": "hospital",
   "Fecha Actualizado": "9/30/2017",
   "Status": "51",
   "Fecha Obtenido": "9/30/2017"
 },
 {
   "Type": "Mascotas Refugiadas",
   "path": "pet",
   "Fecha Actualizado": "9/30/2017",
   "Status": "234",
   "Fecha Obtenido": "9/30/2017"
 },
 {
   "Type": "Puertos (capacidad operacional diaria)",
   "Fecha Actualizado": "9/30/2017",
   "Status": "62.92%",
   "Fecha Obtenido": "9/30/2017"
 },
 {
   "Type": "Puertos Abiertos",
   "path": "port",
   "Fecha Actualizado": "9/29/2017",
   "Status": "75.00%",
   "Fecha Obtenido": "9/30/2017"
 },
 {
   "Type": "Refugiados",
   "path": "refugee",
   "Fecha Actualizado": "9/30/2017",
   "Status": "10,201",
   "Fecha Obtenido": "9/30/2017"
 },
 {
   "Type": "Refugios",
   "path": "shelter",
   "Fecha Actualizado": "9/30/2017",
   "Status": "150",
   "Fecha Obtenido": "9/30/2017"
 },
 {
   "Type": "Supermercados",
   "path": "supermarket",
   "Fecha Actualizado": "9/28/2017",
   "Status": "49.12%",
   "Fecha Obtenido": "9/30/2017"
 },
 {
   "Type": "Telecomunicaciones",
   "path": "telecomunication",
   "Fecha Actualizado": "9/30/2017",
   "Status": "30.50%",
   "Fecha Obtenido": "9/30/2017"
 },
 {
   "Type": "Torres celular",
   "path": "tower",
   "Fecha Actualizado": "9/30/2017",
   "Status": "10.70%",
   "Fecha Obtenido": "9/30/2017"
 },
 {
   "Type": "AAA Este",
   "Fecha Actualizado": "9/30/2017",
   "Status": "46.00%",
   "Fecha Obtenido": "10/1/2017"
 },
 {
   "Type": "AAA Metro",
   "Fecha Actualizado": "9/30/2017",
   "Status": "55.00%",
   "Fecha Obtenido": "10/1/2017"
 },
 {
   "Type": "AAA Norte",
   "Fecha Actualizado": "9/30/2017",
   "Status": "29.00%",
   "Fecha Obtenido": "10/1/2017"
 },
 {
   "Type": "AAA Oeste",
   "Fecha Actualizado": "9/30/2017",
   "Status": "19.00%",
   "Fecha Obtenido": "10/1/2017"
 },
 {
   "Type": "AAA Sur",
   "Fecha Actualizado": "9/30/2017",
   "Status": "72.00%",
   "Fecha Obtenido": "10/1/2017"
 },
 {
   "Type": "AEE",
   "path": "aee",
   "Fecha Actualizado": "9/29/2017",
   "Status": "5.00%",
   "Fecha Obtenido": "10/1/2017"
 },
 {
   "Type": "Centros de Dialisis Asistidos",
   "path": "dialysis",
   "Fecha Actualizado": "9/30/2017",
   "Status": "46",
   "Fecha Obtenido": "10/1/2017"
 },
 {
   "Type": "Farmacias",
   "path": "pharmacy",
   "Fecha Actualizado": "9/28/2017",
   "Status": "337",
   "Fecha Obtenido": "10/1/2017"
 },
 {
   "Type": "Gasolineras",
   "path": "gas",
   "Fecha Actualizado": "10/1/2017",
   "Status": "65.55%",
   "Fecha Obtenido": "10/1/2017"
 },
 {
   "Type": "Hospitales Asistidos",
   "path": "hospital",
   "Fecha Actualizado": "9/30/2017",
   "Status": "51",
   "Fecha Obtenido": "10/1/2017"
 },
 {
   "Type": "Mascotas Refugiadas",
   "path": "pet",
   "Fecha Actualizado": "9/30/2017",
   "Status": "234",
   "Fecha Obtenido": "10/1/2017"
 },
 {
   "Type": "Puertos (capacidad operacional diaria)",
   "Fecha Actualizado": "9/30/2017",
   "Status": "62.92%",
   "Fecha Obtenido": "10/1/2017"
 },
 {
   "Type": "Puertos Abiertos",
   "path": "port",
   "Fecha Actualizado": "9/29/2017",
   "Status": "75.00%",
   "Fecha Obtenido": "10/1/2017"
 },
 {
   "Type": "Refugiados",
   "path": "refugee",
   "Fecha Actualizado": "9/30/2017",
   "Status": "8,800",
   "Fecha Obtenido": "10/1/2017"
 },
 {
   "Type": "Refugios",
   "path": "shelter",
   "Fecha Actualizado": "9/30/2017",
   "Status": "139",
   "Fecha Obtenido": "10/1/2017"
 },
 {
   "Type": "Supermercados",
   "path": "supermarket",
   "Fecha Actualizado": "9/28/2017",
   "Status": "49.12%",
   "Fecha Obtenido": "10/1/2017"
 },
 {
   "Type": "Telecomunicaciones",
   "path": "telecomunication",
   "Fecha Actualizado": "9/30/2017",
   "Status": "30.80%",
   "Fecha Obtenido": "10/1/2017"
 },
 {
   "Type": "Torres celular",
   "path": "tower",
   "Fecha Actualizado": "9/30/2017",
   "Status": "11.30%",
   "Fecha Obtenido": "10/1/2017"
 },
 {
   "Type": "AAA Este",
   "Fecha Actualizado": "9/30/2017",
   "Status": "46.00%",
   "Fecha Obtenido": "10/2/2017"
 },
 {
   "Type": "AAA Metro",
   "Fecha Actualizado": "9/30/2017",
   "Status": "55.00%",
   "Fecha Obtenido": "10/2/2017"
 },
 {
   "Type": "AAA Norte",
   "Fecha Actualizado": "9/30/2017",
   "Status": "29.00%",
   "Fecha Obtenido": "10/2/2017"
 },
 {
   "Type": "AAA Oeste",
   "Fecha Actualizado": "9/30/2017",
   "Status": "19.00%",
   "Fecha Obtenido": "10/2/2017"
 },
 {
   "Type": "AAA Sur",
   "Fecha Actualizado": "9/30/2017",
   "Status": "72.00%",
   "Fecha Obtenido": "10/2/2017"
 },
 {
   "Type": "AEE",
   "path": "aee",
   "Fecha Actualizado": "10/1/2017",
   "Status": "5.00%",
   "Fecha Obtenido": "10/2/2017"
 },
 {
   "Type": "Centros de Dialisis Asistidos",
   "path": "dialysis",
   "Fecha Actualizado": "9/30/2017",
   "Status": "46",
   "Fecha Obtenido": "10/2/2017"
 },
 {
   "Type": "Farmacias",
   "path": "pharmacy",
   "Fecha Actualizado": "9/28/2017",
   "Status": "337",
   "Fecha Obtenido": "10/2/2017"
 },
 {
   "Type": "Gasolineras",
   "path": "gas",
   "Fecha Actualizado": "10/1/2017",
   "Status": "65.55%",
   "Fecha Obtenido": "10/2/2017"
 },
 {
   "Type": "Hospitales Asistidos",
   "path": "hospital",
   "Fecha Actualizado": "9/30/2017",
   "Status": "51",
   "Fecha Obtenido": "10/2/2017"
 },
 {
   "Type": "Mascotas Refugiadas",
   "path": "pet",
   "Fecha Actualizado": "10/1/2017",
   "Status": "234",
   "Fecha Obtenido": "10/2/2017"
 },
 {
   "Type": "Puertos (capacidad operacional diaria)",
   "Fecha Actualizado": "9/30/2017",
   "Status": "62.92%",
   "Fecha Obtenido": "10/2/2017"
 },
 {
   "Type": "Puertos Abiertos",
   "path": "port",
   "Fecha Actualizado": "9/29/2017",
   "Status": "75.00%",
   "Fecha Obtenido": "10/2/2017"
 },
 {
   "Type": "Refugiados",
   "path": "refugee",
   "Fecha Actualizado": "10/1/2017",
   "Status": "8,867",
   "Fecha Obtenido": "10/2/2017"
 },
 {
   "Type": "Refugios",
   "path": "shelter",
   "Fecha Actualizado": "10/1/2017",
   "Status": "139",
   "Fecha Obtenido": "10/2/2017"
 },
 {
   "Type": "Supermercados",
   "path": "supermarket",
   "Fecha Actualizado": "9/30/2017",
   "Status": "64.69%",
   "Fecha Obtenido": "10/2/2017"
 },
 {
   "Type": "Telecomunicaciones",
   "path": "telecomunication",
   "Fecha Actualizado": "10/1/2017",
   "Status": "35.80%",
   "Fecha Obtenido": "10/2/2017"
 },
 {
   "Type": "Torres celular",
   "path": "tower",
   "Fecha Actualizado": "10/1/2017",
   "Status": "14.21%",
   "Fecha Obtenido": "10/2/2017"
 },
 {
   "Type": "AAA",
   "Fecha Actualizado": "10/3/2017",
   "Status": "45.00%",
   "Fecha Obtenido": "10/3/2017"
 },
 {
   "Type": "AAA Este",
   "Fecha Actualizado": "10/3/2017",
   "Status": "45.00%",
   "Fecha Obtenido": "10/3/2017"
 },
 {
   "Type": "AAA Metro",
   "Fecha Actualizado": "10/3/2017",
   "Status": "57.00%",
   "Fecha Obtenido": "10/3/2017"
 },
 {
   "Type": "AAA Norte",
   "Fecha Actualizado": "10/3/2017",
   "Status": "13.00%",
   "Fecha Obtenido": "10/3/2017"
 },
 {
   "Type": "AAA Oeste",
   "Fecha Actualizado": "10/3/2017",
   "Status": "25.00%",
   "Fecha Obtenido": "10/3/2017"
 },
 {
   "Type": "AAA Sur",
   "Fecha Actualizado": "10/3/2017",
   "Status": "73.00%",
   "Fecha Obtenido": "10/3/2017"
 },
 {
   "Type": "AEE",
   "path": "aee",
   "Fecha Actualizado": "10/3/2017",
   "Status": "6.89%",
   "Fecha Obtenido": "10/3/2017"
 },
 {
   "Type": "Antenas Celular",
   "path": "antenna",
   "Fecha Actualizado": "10/2/2017",
   "Status": "11.68%",
   "Fecha Obtenido": "10/3/2017"
 },
 {
   "Type": "ATMs",
   "path": "atms",
   "Fecha Actualizado": "10/1/2017",
   "Status": "315",
   "Fecha Obtenido": "10/3/2017"
 },
 {
   "Type": "Centros de Dialisis Asistidos",
   "path": "dialysis",
   "Fecha Actualizado": "10/3/2017",
   "Status": "46",
   "Fecha Obtenido": "10/3/2017"
 },
 {
   "Type": "Cooperativas",
   "path": "cooperatives",
   "Fecha Actualizado": "10/3/2017",
   "Status": "85",
   "Fecha Obtenido": "10/3/2017"
 },
 {
   "Type": "Diesel (abastos en barriles)",
   "path": "barrel.diesel",
   "Fecha Actualizado": "10/1/2017",
   "Status": "539,715",
   "Fecha Obtenido": "10/3/2017"
 },
 {
   "Type": "Farmacias",
   "path": "pharmacy",
   "Fecha Actualizado": "10/2/2017",
   "Status": "606",
   "Fecha Obtenido": "10/3/2017"
 },
 {
   "Type": "Gasolina (abastos en barriles)",
   "path": "barrel.gas",
   "Fecha Actualizado": "10/1/2017",
   "Status": "467,766",
   "Fecha Obtenido": "10/3/2017"
 },
 {
   "Type": "Gasolineras",
   "path": "gas",
   "Fecha Actualizado": "10/3/2017",
   "Status": "74.00%",
   "Fecha Obtenido": "10/3/2017"
 },
 {
   "Type": "Hospitales Asistidos",
   "path": "hospital",
   "Fecha Actualizado": "10/2/2017",
   "Status": "51",
   "Fecha Obtenido": "10/3/2017"
 },
 {
   "Type": "Mascotas Refugiadas",
   "path": "pet",
   "Fecha Actualizado": "10/2/2017",
   "Status": "232",
   "Fecha Obtenido": "10/3/2017"
 },
 {
   "Type": "Puertos (capacidad operacional diaria)",
   "Fecha Actualizado": "10/3/2017",
   "Status": "61.07%",
   "Fecha Obtenido": "10/3/2017"
 },
 {
   "Type": "Puertos Abiertos",
   "path": "port",
   "Fecha Actualizado": "10/3/2017",
   "Status": "75.00%",
   "Fecha Obtenido": "10/3/2017"
 },
 {
   "Type": "Refugiados",
   "path": "refugee",
   "Fecha Actualizado": "10/2/2017",
   "Status": "8,867",
   "Fecha Obtenido": "10/3/2017"
 },
 {
   "Type": "Refugios",
   "path": "shelter",
   "Fecha Actualizado": "10/2/2017",
   "Status": "149",
   "Fecha Obtenido": "10/3/2017"
 },
 {
   "Type": "Sucursales Bancarias",
   "path": "bank",
   "Fecha Actualizado": "10/3/2017",
   "Status": "153",
   "Fecha Obtenido": "10/3/2017"
 },
 {
   "Type": "Supermercados",
   "path": "supermarket",
   "Fecha Actualizado": "10/3/2017",
   "Status": "64.69%",
   "Fecha Obtenido": "10/3/2017"
 },
 {
   "Type": "Telecomunicaciones",
   "path": "telecomunication",
   "Fecha Actualizado": "10/3/2017",
   "Status": "40.00%",
   "Fecha Obtenido": "10/3/2017"
 },
 {
   "Type": "Torres celular",
   "path": "tower",
   "Fecha Actualizado": "10/2/2017",
   "Status": "22.54%",
   "Fecha Obtenido": "10/3/2017"
 },
 {
   "Type": "Vuelos Comerciales",
   "path": "flight",
   "Fecha Actualizado": "10/2/2017",
   "Status": "26.00%",
   "Fecha Obtenido": "10/3/2017"
 },
 {
   "Type": "Vuelos Comerciales (Capacidad Diaria)",
   "Fecha Actualizado": "10/2/2017",
   "Status": "25.63%",
   "Fecha Obtenido": "10/3/2017"
 },
 {
   "Type": "Vuelos Comerciales (Domesticos)",
   "Fecha Actualizado": "10/2/2017",
   "Status": "38",
   "Fecha Obtenido": "10/3/2017"
 },
 {
   "Type": "Vuelos Comerciales (Internacionales)",
   "Fecha Actualizado": "10/2/2017",
   "Status": "3",
   "Fecha Obtenido": "10/3/2017"
 },
 {
   "Type": "AAA",
   "Fecha Actualizado": "10/4/2017",
   "Status": "48.20%",
   "Fecha Obtenido": "10/4/2017"
 },
 {
   "Type": "AAA Este",
   "Fecha Actualizado": "10/4/2017",
   "Status": "45.20%",
   "Fecha Obtenido": "10/4/2017"
 },
 {
   "Type": "AAA Metro",
   "Fecha Actualizado": "10/4/2017",
   "Status": "63.33%",
   "Fecha Obtenido": "10/4/2017"
 },
 {
   "Type": "AAA Norte",
   "Fecha Actualizado": "10/4/2017",
   "Status": "14.67%",
   "Fecha Obtenido": "10/4/2017"
 },
 {
   "Type": "AAA Oeste",
   "Fecha Actualizado": "10/4/2017",
   "Status": "30.31%",
   "Fecha Obtenido": "10/4/2017"
 },
 {
   "Type": "AAA Sur",
   "Fecha Actualizado": "10/4/2017",
   "Status": "77.68%",
   "Fecha Obtenido": "10/4/2017"
 },
 {
   "Type": "AEE",
   "path": "aee",
   "Fecha Actualizado": "10/4/2017",
   "Status": "8.60%",
   "Fecha Obtenido": "10/4/2017"
 },
 {
   "Type": "Antenas Celular",
   "path": "antenna",
   "Fecha Actualizado": "10/2/2017",
   "Status": "11.68%",
   "Fecha Obtenido": "10/4/2017"
 },
 {
   "Type": "ATMs",
   "path": "atms",
   "Fecha Actualizado": "10/4/2017",
   "Status": "430",
   "Fecha Obtenido": "10/4/2017"
 },
 {
   "Type": "Centros de Dialisis Asistidos",
   "path": "dialysis",
   "Fecha Actualizado": "10/3/2017",
   "Status": "46",
   "Fecha Obtenido": "10/4/2017"
 },
 {
   "Type": "Comercios procesando PAN",
   "path": "comercios.procesando.pan",
   "Fecha Actualizado": "10/3/2017",
   "Status": "510",
   "Fecha Obtenido": "10/4/2017"
 },
 {
   "Type": "Contenedores",
   "path": "container",
   "Fecha Actualizado": "10/4/2017",
   "Status": "64.29%",
   "Fecha Obtenido": "10/4/2017"
 },
 {
   "Type": "Cooperativas",
   "path": "cooperatives",
   "Fecha Actualizado": "10/4/2017",
   "Status": "100",
   "Fecha Obtenido": "10/4/2017"
 },
 {
   "Type": "Diesel (abastos en barriles)",
   "path": "barrel.diesel",
   "Fecha Actualizado": "10/4/2017",
   "Status": "443,593",
   "Fecha Obtenido": "10/4/2017"
 },
 {
   "Type": "Farmacias",
   "path": "pharmacy",
   "Fecha Actualizado": "10/3/2017",
   "Status": "462",
   "Fecha Obtenido": "10/4/2017"
 },
 {
   "Type": "Gasolina (abastos en barriles)",
   "path": "barrel.gas",
   "Fecha Actualizado": "10/4/2017",
   "Status": "402,781",
   "Fecha Obtenido": "10/4/2017"
 },
 {
   "Type": "Gasolineras",
   "path": "gas",
   "Fecha Actualizado": "10/4/2017",
   "Status": "76.09%",
   "Fecha Obtenido": "10/4/2017"
 },
 {
   "Type": "Hospitales Asistidos",
   "path": "hospital",
   "Fecha Actualizado": "10/3/2017",
   "Status": "51",
   "Fecha Obtenido": "10/4/2017"
 },
 {
   "Type": "Mascotas Refugiadas",
   "path": "pet",
   "Fecha Actualizado": "10/4/2017",
   "Status": "193",
   "Fecha Obtenido": "10/4/2017"
 },
 {
   "Type": "Puertos (capacidad operacional diaria)",
   "Fecha Actualizado": "10/3/2017",
   "Status": "",
   "Fecha Obtenido": "10/4/2017"
 },
 {
   "Type": "Puertos Abiertos",
   "path": "port",
   "Fecha Actualizado": "10/3/2017",
   "Status": "75.00%",
   "Fecha Obtenido": "10/4/2017"
 },
 {
   "Type": "Refugiados",
   "path": "refugee",
   "Fecha Actualizado": "10/4/2017",
   "Status": "8,802",
   "Fecha Obtenido": "10/4/2017"
 },
 {
   "Type": "Refugios",
   "path": "shelter",
   "Fecha Actualizado": "10/4/2017",
   "Status": "135",
   "Fecha Obtenido": "10/4/2017"
 },
 {
   "Type": "Rutas AMA",
   "path": "ama",
   "Fecha Actualizado": "10/4/2017",
   "Status": "75.00%",
   "Fecha Obtenido": "10/4/2017"
 },
 {
   "Type": "Sucursales Bancarias",
   "path": "bank",
   "Fecha Actualizado": "10/3/2017",
   "Status": "153",
   "Fecha Obtenido": "10/4/2017"
 },
 {
   "Type": "Supermercados",
   "path": "supermarket",
   "Fecha Actualizado": "10/3/2017",
   "Status": "69.74%",
   "Fecha Obtenido": "10/4/2017"
 },
 {
   "Type": "Telecomunicaciones",
   "path": "telecomunication",
   "Fecha Actualizado": "10/4/2017",
   "Status": "43.32%",
   "Fecha Obtenido": "10/4/2017"
 },
 {
   "Type": "Torres celular",
   "path": "tower",
   "Fecha Actualizado": "10/3/2017",
   "Status": "22.54%",
   "Fecha Obtenido": "10/4/2017"
 },
 {
   "Type": "Vuelos Comerciales",
   "path": "flight",
   "Fecha Actualizado": "10/2/2017",
   "Status": "100.00%",
   "Fecha Obtenido": "10/4/2017"
 },
 {
   "Type": "Vuelos Comerciales (Capacidad Diaria)",
   "Fecha Actualizado": "10/2/2017",
   "Status": "100.00%",
   "Fecha Obtenido": "10/4/2017"
 },
 {
   "Type": "Vuelos Comerciales (Domesticos)",
   "Fecha Actualizado": "10/2/2017",
   "Status": "",
   "Fecha Obtenido": "10/4/2017"
 },
 {
   "Type": "Vuelos Comerciales (Internacionales)",
   "Fecha Actualizado": "10/2/2017",
   "Status": "",
   "Fecha Obtenido": "10/4/2017"
 },
 {
   "Type": "AAA",
   "Fecha Actualizado": "10/5/2017",
   "Status": "54.20%",
   "Fecha Obtenido": "10/5/2017"
 },
 {
   "Type": "AAA Este",
   "Fecha Actualizado": "10/5/2017",
   "Status": "62.73%",
   "Fecha Obtenido": "10/5/2017"
 },
 {
   "Type": "AAA Metro",
   "Fecha Actualizado": "10/5/2017",
   "Status": "63.87%",
   "Fecha Obtenido": "10/5/2017"
 },
 {
   "Type": "AAA Norte",
   "Fecha Actualizado": "10/5/2017",
   "Status": "19.93%",
   "Fecha Obtenido": "10/5/2017"
 },
 {
   "Type": "AAA Oeste",
   "Fecha Actualizado": "10/5/2017",
   "Status": "39.85%",
   "Fecha Obtenido": "10/5/2017"
 },
 {
   "Type": "AAA Sur",
   "Fecha Actualizado": "10/5/2017",
   "Status": "77.23%",
   "Fecha Obtenido": "10/5/2017"
 },
 {
   "Type": "AEE",
   "path": "aee",
   "Fecha Actualizado": "10/5/2017",
   "Status": "9.20%",
   "Fecha Obtenido": "10/5/2017"
 },
 {
   "Type": "Antenas Celular",
   "path": "antenna",
   "Fecha Actualizado": "10/5/2017",
   "Status": "13.55%",
   "Fecha Obtenido": "10/5/2017"
 },
 {
   "Type": "ATMs",
   "path": "atms",
   "Fecha Actualizado": "10/5/2017",
   "Status": "409",
   "Fecha Obtenido": "10/5/2017"
 },
 {
   "Type": "Centros de Dialisis Asistidos",
   "path": "dialysis",
   "Fecha Actualizado": "10/3/2017",
   "Status": "46",
   "Fecha Obtenido": "10/5/2017"
 },
 {
   "Type": "Comercios procesando PAN",
   "path": "comercios.procesando.pan",
   "Fecha Actualizado": "10/5/2017",
   "Status": "683",
   "Fecha Obtenido": "10/5/2017"
 },
 {
   "Type": "Contenedores",
   "path": "container",
   "Fecha Actualizado": "10/5/2017",
   "Status": "71.71%",
   "Fecha Obtenido": "10/5/2017"
 },
 {
   "Type": "Cooperativas",
   "path": "cooperatives",
   "Fecha Actualizado": "10/4/2017",
   "Status": "100",
   "Fecha Obtenido": "10/5/2017"
 },
 {
   "Type": "Correos",
   "path": "goverment.mail",
   "Fecha Actualizado": "10/5/2017",
   "Status": "90.37%",
   "Fecha Obtenido": "10/5/2017"
 },
 {
   "Type": "Diesel (abastos en barriles)",
   "path": "barrel.diesel",
   "Fecha Actualizado": "10/5/2017",
   "Status": "538,624",
   "Fecha Obtenido": "10/5/2017"
 },
 {
   "Type": "Farmacias",
   "path": "pharmacy",
   "Fecha Actualizado": "10/4/2017",
   "Status": "514",
   "Fecha Obtenido": "10/5/2017"
 },
 {
   "Type": "Gasolina (abastos en barriles)",
   "path": "barrel.gas",
   "Fecha Actualizado": "10/5/2017",
   "Status": "447,041",
   "Fecha Obtenido": "10/5/2017"
 },
 {
   "Type": "Gasolineras",
   "path": "gas",
   "Fecha Actualizado": "10/5/2017",
   "Status": "77.91%",
   "Fecha Obtenido": "10/5/2017"
 },
 {
   "Type": "Hospitales Asistidos",
   "path": "hospital",
   "Fecha Actualizado": "10/5/2017",
   "Status": "64",
   "Fecha Obtenido": "10/5/2017"
 },
 {
   "Type": "Mascotas Refugiadas",
   "path": "pet",
   "Fecha Actualizado": "10/5/2017",
   "Status": "196",
   "Fecha Obtenido": "10/5/2017"
 },
 {
   "Type": "Puertos (capacidad operacional diaria)",
   "Fecha Actualizado": "10/3/2017",
   "Status": "",
   "Fecha Obtenido": "10/5/2017"
 },
 {
   "Type": "Puertos Abiertos",
   "path": "port",
   "Fecha Actualizado": "10/3/2017",
   "Status": "75.00%",
   "Fecha Obtenido": "10/5/2017"
 },
 {
   "Type": "Refugiados",
   "path": "refugee",
   "Fecha Actualizado": "10/5/2017",
   "Status": "8,585",
   "Fecha Obtenido": "10/5/2017"
 },
 {
   "Type": "Refugios",
   "path": "shelter",
   "Fecha Actualizado": "10/5/2017",
   "Status": "132",
   "Fecha Obtenido": "10/5/2017"
 },
 {
   "Type": "Rutas AMA",
   "path": "ama",
   "Fecha Actualizado": "10/4/2017",
   "Status": "75.00%",
   "Fecha Obtenido": "10/5/2017"
 },
 {
   "Type": "Sucursales Bancarias",
   "path": "bank",
   "Fecha Actualizado": "10/5/2017",
   "Status": "55.27%",
   "Fecha Obtenido": "10/5/2017"
 },
 {
   "Type": "Supermercados",
   "path": "supermarket",
   "Fecha Actualizado": "10/5/2017",
   "Status": "79.17%",
   "Fecha Obtenido": "10/5/2017"
 },
 {
   "Type": "Telecomunicaciones",
   "path": "telecomunication",
   "Fecha Actualizado": "10/5/2017",
   "Status": "45.00%",
   "Fecha Obtenido": "10/5/2017"
 },
 {
   "Type": "Torres celular",
   "path": "tower",
   "Fecha Actualizado": "10/5/2017",
   "Status": "26.13%",
   "Fecha Obtenido": "10/5/2017"
 },
 {
   "Type": "Vuelos Comerciales",
   "path": "flight",
   "Fecha Actualizado": "10/5/2017",
   "Status": "100.00%",
   "Fecha Obtenido": "10/5/2017"
 },
 {
   "Type": "Vuelos Comerciales (Capacidad Diaria)",
   "Fecha Actualizado": "10/2/2017",
   "Status": "",
   "Fecha Obtenido": "10/5/2017"
 },
 {
   "Type": "Vuelos Comerciales (Domesticos)",
   "Fecha Actualizado": "10/2/2017",
   "Status": "",
   "Fecha Obtenido": "10/5/2017"
 },
 {
   "Type": "Vuelos Comerciales (Internacionales)",
   "Fecha Actualizado": "10/2/2017",
   "Status": "",
   "Fecha Obtenido": "10/5/2017"
 },
 {
   "Type": "AAA",
   "Fecha Actualizado": "10/6/2017",
   "Status": "55.50%",
   "Fecha Obtenido": "10/6/2017"
 },
 {
   "Type": "AAA Este",
   "Fecha Actualizado": "10/6/2017",
   "Status": "63.00%",
   "Fecha Obtenido": "10/6/2017"
 },
 {
   "Type": "AAA Metro",
   "Fecha Actualizado": "10/6/2017",
   "Status": "64.00%",
   "Fecha Obtenido": "10/6/2017"
 },
 {
   "Type": "AAA Norte",
   "Fecha Actualizado": "10/6/2017",
   "Status": "28.00%",
   "Fecha Obtenido": "10/6/2017"
 },
 {
   "Type": "AAA Oeste",
   "Fecha Actualizado": "10/6/2017",
   "Status": "69.00%",
   "Fecha Obtenido": "10/6/2017"
 },
 {
   "Type": "AAA Sur",
   "Fecha Actualizado": "10/6/2017",
   "Status": "69.00%",
   "Fecha Obtenido": "10/6/2017"
 },
 {
   "Type": "AEE",
   "path": "aee",
   "Fecha Actualizado": "10/6/2017",
   "Status": "10.70%",
   "Fecha Obtenido": "10/6/2017"
 },
 {
   "Type": "Antenas Celular",
   "path": "antenna",
   "Fecha Actualizado": "10/6/2017",
   "Status": "15.20%",
   "Fecha Obtenido": "10/6/2017"
 },
 {
   "Type": "ATMs",
   "path": "atms",
   "Fecha Actualizado": "10/6/2017",
   "Status": "481",
   "Fecha Obtenido": "10/6/2017"
 },
 {
   "Type": "Centros de Dialisis Asistidos",
   "path": "dialysis",
   "Fecha Actualizado": "10/6/2017",
   "Status": "46",
   "Fecha Obtenido": "10/6/2017"
 },
 {
   "Type": "Comercios procesando PAN",
   "path": "comercios.procesando.pan",
   "Fecha Actualizado": "10/6/2017",
   "Status": "490",
   "Fecha Obtenido": "10/6/2017"
 },
 {
   "Type": "Contenedores",
   "path": "container",
   "Fecha Actualizado": "10/6/2017",
   "Status": "81.64%",
   "Fecha Obtenido": "10/6/2017"
 },
 {
   "Type": "Cooperativas",
   "path": "cooperatives",
   "Fecha Actualizado": "10/6/2017",
   "Status": "116",
   "Fecha Obtenido": "10/6/2017"
 },
 {
   "Type": "Correos",
   "path": "goverment.mail",
   "Fecha Actualizado": "10/6/2017",
   "Status": "92.42%",
   "Fecha Obtenido": "10/6/2017"
 },
 {
   "Type": "Diesel (abastos en barriles)",
   "path": "barrel.diesel",
   "Fecha Actualizado": "10/6/2017",
   "Status": "513,892",
   "Fecha Obtenido": "10/6/2017"
 },
 {
   "Type": "Farmacias",
   "path": "pharmacy",
   "Fecha Actualizado": "10/6/2017",
   "Status": "558",
   "Fecha Obtenido": "10/6/2017"
 },
 {
   "Type": "Gasolina (abastos en barriles)",
   "path": "barrel.gas",
   "Fecha Actualizado": "10/6/2017",
   "Status": "512,426",
   "Fecha Obtenido": "10/6/2017"
 },
 {
   "Type": "Gasolineras",
   "path": "gas",
   "Fecha Actualizado": "10/6/2017",
   "Status": "78.18%",
   "Fecha Obtenido": "10/6/2017"
 },
 {
   "Type": "Hospitales Asistidos",
   "path": "hospital",
   "Fecha Actualizado": "10/6/2017",
   "Status": "68",
   "Fecha Obtenido": "10/6/2017"
 },
 {
   "Type": "Mascotas Refugiadas",
   "path": "pet",
   "Fecha Actualizado": "10/6/2017",
   "Status": "216",
   "Fecha Obtenido": "10/6/2017"
 },
 {
   "Type": "Puertos (capacidad operacional diaria)",
   "Fecha Actualizado": "10/6/2017",
   "Status": "",
   "Fecha Obtenido": "10/6/2017"
 },
 {
   "Type": "Puertos Abiertos",
   "path": "port",
   "Fecha Actualizado": "10/6/2017",
   "Status": "75.00%",
   "Fecha Obtenido": "10/6/2017"
 },
 {
   "Type": "Refugiados",
   "path": "refugee",
   "Fecha Actualizado": "10/6/2017",
   "Status": "8,349",
   "Fecha Obtenido": "10/6/2017"
 },
 {
   "Type": "Refugios",
   "path": "shelter",
   "Fecha Actualizado": "10/6/2017",
   "Status": "68",
   "Fecha Obtenido": "10/6/2017"
 },
 {
   "Type": "Rutas AMA",
   "path": "ama",
   "Fecha Actualizado": "10/6/2017",
   "Status": "75.00%",
   "Fecha Obtenido": "10/6/2017"
 },
 {
   "Type": "Sucursales Bancarias",
   "path": "bank",
   "Fecha Actualizado": "10/6/2017",
   "Status": "55.59%",
   "Fecha Obtenido": "10/6/2017"
 },
 {
   "Type": "Supermercados",
   "path": "supermarket",
   "Fecha Actualizado": "10/6/2017",
   "Status": "73.03%",
   "Fecha Obtenido": "10/6/2017"
 },
 {
   "Type": "Telecomunicaciones",
   "path": "telecomunication",
   "Fecha Actualizado": "10/6/2017",
   "Status": "42.00%",
   "Fecha Obtenido": "10/6/2017"
 },
 {
   "Type": "Torres celular",
   "path": "tower",
   "Fecha Actualizado": "10/6/2017",
   "Status": "24.09%",
   "Fecha Obtenido": "10/6/2017"
 },
 {
   "Type": "Vuelos Comerciales",
   "path": "flight",
   "Fecha Actualizado": "10/6/2017",
   "Status": "100.00%",
   "Fecha Obtenido": "10/6/2017"
 },
 {
   "Type": "AAA",
   "Fecha Actualizado": "10/7/2017",
   "Status": "56.24%",
   "Fecha Obtenido": "10/7/2017"
 },
 {
   "Type": "AAA Este",
   "Fecha Actualizado": "10/8/2017",
   "Status": "64.00%",
   "Fecha Obtenido": "10/7/2017"
 },
 {
   "Type": "AAA Metro",
   "Fecha Actualizado": "10/9/2017",
   "Status": "65.00%",
   "Fecha Obtenido": "10/7/2017"
 },
 {
   "Type": "AAA Norte",
   "Fecha Actualizado": "10/10/2017",
   "Status": "20.00%",
   "Fecha Obtenido": "10/7/2017"
 },
 {
   "Type": "AAA Oeste",
   "Fecha Actualizado": "10/11/2017",
   "Status": "48.00%",
   "Fecha Obtenido": "10/7/2017"
 },
 {
   "Type": "AAA Sur",
   "Fecha Actualizado": "10/12/2017",
   "Status": "78.00%",
   "Fecha Obtenido": "10/7/2017"
 },
 {
   "Type": "AEE",
   "path": "aee",
   "Fecha Actualizado": "10/13/2017",
   "Status": "11.70%",
   "Fecha Obtenido": "10/7/2017"
 },
 {
   "Type": "Antenas Celular",
   "path": "antenna",
   "Fecha Actualizado": "10/14/2017",
   "Status": "15.80%",
   "Fecha Obtenido": "10/7/2017"
 },
 {
   "Type": "ATMs",
   "path": "atms",
   "Fecha Actualizado": "10/15/2017",
   "Status": "612",
   "Fecha Obtenido": "10/7/2017"
 },
 {
   "Type": "Centros de Dialisis Asistidos",
   "path": "dialysis",
   "Fecha Actualizado": "10/16/2017",
   "Status": "46",
   "Fecha Obtenido": "10/7/2017"
 },
 {
   "Type": "Comercios procesando PAN",
   "path": "comercios.procesando.pan",
   "Fecha Actualizado": "10/17/2017",
   "Status": "490",
   "Fecha Obtenido": "10/7/2017"
 },
 {
   "Type": "Contenedores",
   "path": "container",
   "Fecha Actualizado": "10/18/2017",
   "Status": "88.07%",
   "Fecha Obtenido": "10/7/2017"
 },
 {
   "Type": "Cooperativas",
   "path": "cooperatives",
   "Fecha Actualizado": "10/19/2017",
   "Status": "145",
   "Fecha Obtenido": "10/7/2017"
 },
 {
   "Type": "Correos",
   "path": "goverment.mail",
   "Fecha Actualizado": "10/20/2017",
   "Status": "92.42%",
   "Fecha Obtenido": "10/7/2017"
 },
 {
   "Type": "Diesel (abastos en barriles)",
   "path": "barrel.diesel",
   "Fecha Actualizado": "10/21/2017",
   "Status": "521,354",
   "Fecha Obtenido": "10/7/2017"
 },
 {
   "Type": "Farmacias",
   "path": "pharmacy",
   "Fecha Actualizado": "10/22/2017",
   "Status": "558",
   "Fecha Obtenido": "10/7/2017"
 },
 {
   "Type": "Gasolina (abastos en barriles)",
   "path": "barrel.gas",
   "Fecha Actualizado": "10/23/2017",
   "Status": "545,935",
   "Fecha Obtenido": "10/7/2017"
 },
 {
   "Type": "Gasolineras",
   "path": "gas",
   "Fecha Actualizado": "10/24/2017",
   "Status": "78.18%",
   "Fecha Obtenido": "10/7/2017"
 },
 {
   "Type": "Hospitales Asistidos",
   "path": "hospital",
   "Fecha Actualizado": "10/25/2017",
   "Status": "66",
   "Fecha Obtenido": "10/7/2017"
 },
 {
   "Type": "Mascotas Refugiadas",
   "path": "pet",
   "Fecha Actualizado": "10/26/2017",
   "Status": "154",
   "Fecha Obtenido": "10/7/2017"
 },
 {
   "Type": "Puertos Abiertos",
   "path": "port",
   "Fecha Actualizado": "10/27/2017",
   "Status": "75.00%",
   "Fecha Obtenido": "10/7/2017"
 },
 {
   "Type": "Refugiados",
   "path": "refugee",
   "Fecha Actualizado": "10/28/2017",
   "Status": "7,442",
   "Fecha Obtenido": "10/7/2017"
 },
 {
   "Type": "Refugios",
   "path": "shelter",
   "Fecha Actualizado": "10/29/2017",
   "Status": "116",
   "Fecha Obtenido": "10/7/2017"
 },
 {
   "Type": "Rutas AMA",
   "path": "ama",
   "Fecha Actualizado": "10/30/2017",
   "Status": "75.00%",
   "Fecha Obtenido": "10/7/2017"
 },
 {
   "Type": "Sucursales Bancarias",
   "path": "bank",
   "Fecha Actualizado": "10/31/2017",
   "Status": "57.19%",
   "Fecha Obtenido": "10/7/2017"
 },
 {
   "Type": "Supermercados",
   "path": "supermarket",
   "Fecha Actualizado": "11/1/2017",
   "Status": "77.41%",
   "Fecha Obtenido": "10/7/2017"
 },
 {
   "Type": "Telecomunicaciones",
   "path": "telecomunication",
   "Fecha Actualizado": "11/2/2017",
   "Status": "44.00%",
   "Fecha Obtenido": "10/7/2017"
 },
 {
   "Type": "Torres celular",
   "path": "tower",
   "Fecha Actualizado": "11/3/2017",
   "Status": "24.09%",
   "Fecha Obtenido": "10/7/2017"
 },
 {
   "Type": "Vuelos Comerciales",
   "path": "flight",
   "Fecha Actualizado": "11/4/2017",
   "Status": "100.00%",
   "Fecha Obtenido": "10/7/2017"
 }
]

for obj in objects:
    if obj.get('path'):
        doc = {
            'label': normalize_label(obj['Type']),
            'path': obj['path'],
            'value': normalize_value(obj['Status']),
            'last_updated_at': normalize_last_updated(obj['Fecha Actualizado']),
            'imported_at': datetime.utcnow(),
            'created_at': datetime.strptime(obj['Fecha Obtenido'], '%m/%d/%Y')
        }

        print(doc)

        db.stats.insert_one(doc)
