from fastapi import FastAPI , Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import joblib
import pandas as pd
import numpy as np
import uvicorn

app = FastAPI()

templates = Jinja2Templates(directory="templates")

model  = joblib.load("model/model.pkl")
scaler = joblib.load("model/scaler.pkl")

sinif_adlari = {
    0: "Normal",
    1: "DDoS",
    2: "Brute Force",
    3: "Malware",
    4: "Ransomware",
    5: "SQL Injection"
}

protokol_map = {"HTTP": 0, "HTTPS": 1, "TCP": 2, "UDP": 3}
cihaz_map    = {"Android": 0, "Linux": 1, "MacOS": 2, "Windows": 3, "iOS": 4}
sebeke_map   = {"Ethernet": 0, "Mobile": 1, "VPN": 2, "WiFi": 3}
seher_map    = {"Bakı": 0, "Gəncə": 1, "Lənkəran": 2, "Mingəçevir": 3, "Sumqayıt": 4}

@app.get("/" , response_class=HTMLResponse)
async def index(request:Request):
    return templates.TemplateResponse("index.html" , {"request": request})

@app.post("/predict")
async def predict(request: Request):
    data = await request.json()
    df = pd.DataFrame([{
        "Paket_Ölçüsü"    : float(data["paket_olcusu"]),
        "Paket_Sayı"      : float(data["paket_sayi"]),
        "Bağlantı_Müddəti": float(data["baglanti_muddeti"]),
        "Port_Nömrəsi"    : float(data["port_nomresi"]),
        "Xəta_Sayı"       : float(data["xeta_sayi"]),
        "Giriş_Cəhdi"     : float(data["giris_cehdi"]),
        "CPU_İstifadəsi"  : float(data["cpu"]),
        "RAM_İstifadəsi"  : float(data["ram"]),
        "Şəbəkə_Sürəti"   : float(data["sebeke_sureti"]),
        "Aktiv_Sessiya"   : float(data["aktiv_sessiya"]),
        "Protokol"        : protokol_map[data["protokol"]],
        "Cihaz_Növü"      : cihaz_map[data["cihaz"]],
        "Şəbəkə_Növü"     : sebeke_map[data["sebeke"]],
        "Şəhər"           : seher_map[data["seher"]],
    }])
    scaled  = scaler.transform(df)
    proqnoz = model.predict(scaled)[0]
    ehtimal = model.predict_proba(scaled)[0].max() * 100

    return {
        "proqnoz" : sinif_adlari[proqnoz],
        "ehtimal" : round(ehtimal, 2),
        "sinif_id": int(proqnoz)
    }

if __name__ == "__main__":
    uvicorn.run("app:app" , host="0.0.0.0", port=8000 , reload=True)