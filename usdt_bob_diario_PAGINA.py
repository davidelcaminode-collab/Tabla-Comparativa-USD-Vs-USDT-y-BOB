#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import csv
import json
import os
import statistics
import urllib.request
from datetime import date

#  PARÁMETROS CONFIGURABLES
ARCHIVO_CSV   = "historial_usdt_bob.csv"
ARCHIVO_PNG   = "grafico_usdt_bob.png"
N_ANUNCIOS    = 10            # anuncios que promedié
TC_OFICIAL    = 6.96          # tipo de cambio oficial fijo (BOB por USD)
HEADERS       = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}


#  FUENTE 1: Binance P2P, que es la más usada en Bolivia
def precio_binance_p2p(trade_type="SELL"):

    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    payload = json.dumps({
        "asset": "USDT",
        "fiat": "BOB",
        "tradeType": trade_type,
        "page": 1,
        "rows": N_ANUNCIOS,
        "payTypes": [],
        "publisherType": None,
    }).encode("utf-8")

    req = urllib.request.Request(url, data=payload, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.load(resp)

    precios = [float(item["adv"]["price"]) for item in data.get("data", [])]
    return precios


#  FUENTE 2 (respaldo): CriptoYa, porque agrega varias plataformas P2P, y se usa de manera más fiable para el resultado
def precio_criptoya():
    url = "https://criptoya.com/api/USDT/BOB/1"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.load(resp)

    precios = []
    for plataforma, valores in data.items():
        if isinstance(valores, dict):
            # cada plataforma trae 'ask' (venta) y 'bid' (compra)
            if "ask" in valores and valores["ask"]:
                precios.append(float(valores["ask"]))
    return precios


#  OBTENER EL PROMEDIO DE HOY (con respaldo entre fuentes)
def obtener_promedio_hoy():

    # Intento 1: Binance P2P
    try:
        precios = precio_binance_p2p("SELL")
        if precios:
            return round(statistics.mean(precios), 4), "Binance P2P"
    except Exception as e:
        print(f"  [aviso] Binance P2P no respondió: {e}")

    # Intento 2: CriptoYa
    try:
        precios = precio_criptoya()
        if precios:
            return round(statistics.mean(precios), 4), "CriptoYa (varias P2P)"
    except Exception as e:
        print(f"  [aviso] CriptoYa no respondió: {e}")

    raise RuntimeError("Ninguna fuente de datos respondió. Revisá tu conexión.")

#  GUARDAR EN CSV (sin duplicar la fecha de hoy)
def guardar_en_csv(fecha, promedio, fuente):
    filas = []
    existe = os.path.exists(ARCHIVO_CSV)

    if existe:
        with open(ARCHIVO_CSV, newline="", encoding="utf-8") as f:
            filas = list(csv.DictReader(f))

    # quitar fila de hoy si ya existía (para reemplazarla)
    filas = [fila for fila in filas if fila["fecha"] != fecha]

    # calcular tipo de cambio implícito y comparación
    sobreprecio_pct = round((promedio / TC_OFICIAL - 1) * 100, 2)

    filas.append({
        "fecha": fecha,
        "promedio_usdt_bob": promedio,
        "tc_oficial": TC_OFICIAL,
        "sobreprecio_vs_oficial_%": sobreprecio_pct,
        "fuente": fuente,
    })

    filas.sort(key=lambda x: x["fecha"])

    with open(ARCHIVO_CSV, "w", newline="", encoding="utf-8") as f:
        campos = ["fecha", "promedio_usdt_bob", "tc_oficial",
                  "sobreprecio_vs_oficial_%", "fuente"]
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(filas)

    return filas


#  GRÁFICO DE EVOLUCIÓN
def graficar(filas):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("  [aviso] matplotlib no está instalado. Saltando gráfico.")
        print("          Instalalo con:  pip install matplotlib")
        return

    fechas    = [f["fecha"] for f in filas]
    promedios = [float(f["promedio_usdt_bob"]) for f in filas]
    oficial   = [float(f["tc_oficial"]) for f in filas]

    plt.figure(figsize=(10, 5))
    plt.plot(fechas, promedios, marker="o", label="USDT/BOB P2P (promedio diario)")
    plt.plot(fechas, oficial, linestyle="--", label="Tipo de cambio oficial")
    plt.title("Evolución del USDT en bolivianos (P2P) vs. tipo de cambio oficial")
    plt.xlabel("Fecha")
    plt.ylabel("Bolivianos por 1 USDT")
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(ARCHIVO_PNG, dpi=120)
    print(f"  Gráfico guardado en: {ARCHIVO_PNG}")


#  PROGRAMA PRINCIPAL
def main():
    hoy = date.today().isoformat()
    print("=" * 60)
    print(f"  Calculando promedio USDT/BOB para el {hoy}")
    print("=" * 60)

    promedio, fuente = obtener_promedio_hoy()
    sobreprecio = round((promedio / TC_OFICIAL - 1) * 100, 2)

    print(f"  Fuente usada .............. {fuente}")
    print(f"  Promedio USDT/BOB hoy ..... {promedio} Bs")
    print(f"  Tipo de cambio oficial .... {TC_OFICIAL} Bs")
    print(f"  Sobreprecio vs. oficial ... {sobreprecio} %")
    print("-" * 60)

    filas = guardar_en_csv(hoy, promedio, fuente)
    print(f"  Datos guardados en: {ARCHIVO_CSV}  ({len(filas)} días registrados)")

    graficar(filas)
    print("=" * 60)
    print("  Listo. Ejecute este script una vez por día para ir")
    print("  acumulando el historial automáticamente.")
    print("=" * 60)


if __name__ == "__main__":
    main()
