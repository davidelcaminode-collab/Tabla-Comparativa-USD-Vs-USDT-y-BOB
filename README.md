# 📊 Promedio diario del USDT en bolivianos (P2P)

Automatización en Python que calcula el **promedio diario del precio del USDT
(Tether) en bolivianos (BOB)** en el mercado P2P, y lo compara con el tipo de
cambio oficial de Bolivia.

> Proyecto desarrollado para la asignatura **Fundamentos de Ciencia de Datos**.

---

## 🎯 ¿Qué problema resuelve?

En Bolivia, el acceso a dólares físicos está restringido y el tipo de cambio
**oficial es casi fijo** (~6.96 BOB por dólar). Sin embargo, en el mercado real
el dólar se consigue mucho más caro.

El **USDT (Tether)** es una *stablecoin*: un token digital que intenta valer
1 dólar. Como en Bolivia se compra y vende masivamente en plataformas P2P
(persona a persona), **su precio en bolivianos refleja el tipo de cambio
paralelo real** — un termómetro mucho más preciso del valor verdadero del
boliviano frente al dólar.

Este proyecto captura ese precio cada día, calcula un promedio representativo
y mide la **brecha entre el dólar oficial y el dólar real (P2P)**.

> ⚠️ **Aclaración conceptual:** el USDT *no* es el dólar (USD). El dólar es una
> moneda emitida por un gobierno; el USDT es un token privado que intenta
> mantener una paridad de 1:1 con el dólar.

---

## ⚙️ ¿Qué hace el programa?

1. Consulta el precio del USDT/BOB en el mercado P2P (Binance P2P, con CriptoYa
   como fuente de respaldo).
2. Promedia varios anuncios del día para obtener un valor representativo
   (no depende de un único precio puntual).
3. Guarda el resultado en `historial_usdt_bob.csv`, **agregando una fila nueva
   por cada día** (construyendo así una serie histórica propia).
4. Calcula el **sobreprecio (%)** del precio P2P respecto al tipo de cambio
   oficial.
5. Genera un gráfico de evolución en `grafico_usdt_bob.png`.

---

## 🚀 Cómo usarlo

### Requisitos
- Python 3.8 o superior
- La librería `matplotlib` (para el gráfico)

### Instalación
```bash
pip install matplotlib
```

### Ejecución
```bash
python usdt_bob_diario.py
```

Cada vez que lo ejecutás, registra el promedio del día actual. Para construir
el historial, ejecutalo **una vez por día**.

---

## 📁 Archivos del proyecto

| Archivo                   | Descripción                                          |
|---------------------------|------------------------------------------------------|
| `usdt_bob_diario.py`      | Programa principal (la automatización).              |
| `historial_usdt_bob.csv`  | Historial de promedios diarios (se genera solo).     |
| `grafico_usdt_bob.png`    | Gráfico de evolución (se genera solo).               |
| `index.html`              | Página de presentación (opcional, para GitHub Pages).|
| `README.md`               | Este archivo.                                        |

---

## 📈 Ejemplo de resultado

| fecha      | promedio_usdt_bob | tc_oficial | sobreprecio_vs_oficial_% |
|------------|-------------------|------------|--------------------------|
| 2026-06-14 | 9.82              | 6.96       | 41.09                    |
| 2026-06-15 | 9.87              | 6.96       | 41.81                    |
| 2026-06-16 | 9.88              | 6.96       | 41.98                    |

Esto muestra que, en la práctica, conseguir un dólar (vía USDT) cuesta alrededor
de un **40% más** que el valor oficial.

---

## 🔮 Posibles mejoras

- Ejecución automática diaria con GitHub Actions (sin necesidad de tener la PC
  encendida).
- Agregar el dólar paralelo de otra fuente para comparar tres líneas en el
  gráfico (oficial, paralelo y P2P).
- Cálculo de promedios semanales y mensuales.

---

## 👤 Autor

Proyecto académico — Fundamentos de Ciencia de Datos.
