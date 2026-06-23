# 🍦 Heladeria KPI Dashboard

Dashboard interactivo para monitoreo de ventas y productos de una heladeria, construido con **Python**, **Streamlit** y **Plotly**. Transforma datos crudos de un Excel en visualizaciones profesionales listas para toma de decisiones.

[![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?logo=streamlit)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-5.17+-blueviolet?logo=plotly)](https://plotly.com)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-darkgreen?logo=pandas)](https://pandas.pydata.org)

---

## 📊 Demo en vivo

La app esta desplegada en Streamlit Cloud:

```
streamlit run app.py
```

---

## 🎯 Objetivo del Proyecto

Proveer un **dashboard unificado** que permita al dueno de una heladeria:

1. **Monitorear ingresos** diarios, mensuales y acumulados en tiempo real
2. **Identificar patrones** de venta por horario, dia de la semana y temporada
3. **Analizar la popularidad** de sabores y tamanios de producto
4. **Exportar datos** filtrados para uso externo
5. **Tomar decisiones informadas** sobre inventario, personal y precios

---

## 🛠 Stack Tecnologico

| Componente         | Tecnologia          | Proposito                                    |
|--------------------|---------------------|----------------------------------------------|
| **Lenguaje**       | Python 3.12+        | Logica de procesamiento y backend            |
| **Framework Web**  | Streamlit 1.28+     | UI interactiva, filtros, layout responsivo   |
| **Visualizaciones**| Plotly 5.17+        | Graficos interactivos (15+ tipos)            |
| **Datos**          | Pandas 2.0+         | ETL, limpieza, agregaciones, transformaciones|
| **Lectura Excel**  | OpenPyXL 3.1+       | Parseo de archivo .xlsx de 3MB+              |
| **Estilos**        | CSS3 custom         | Tema heladeria, tipografias Google Fonts     |

---

## 📁 Estructura del Proyecto

```
heladeria-kpi/
├── app.py                            # Aplicacion principal Streamlit (4 tabs)
├── data_processor.py                 # ETL: carga, limpieza, curacion, metricas
├── visualizations.py                 # Funciones generadoras de graficos Plotly
├── requirements.txt                  # Dependencias Python
├── Base de datos Heladeria.xlsx      # Fuente de datos original (~30k filas)
├── .gitignore                        # Exclusiones Git
└── README.md                         # Este documento
```

---

## 🧹 Proceso de Limpieza y Curacion de Datos

El archivo Excel original presentaba multiples problemas que fueron resueltos:

### Problemas detectados y soluciones

| Problema                              | Solucion aplicada                                      |
|---------------------------------------|--------------------------------------------------------|
| 12,000 filas completamente vacias     | `dropna(how="all")` - eliminadas al cargar            |
| Precios en formato string (`$11000`)  | Regex `[^\d.]` para extraer valor numerico limpio     |
| Precios = 0 en filas de sabor         | Clasificacion en dos datasets: `df_sales` (con precio > 0) y `df_flavors` (seguimiento de popularidad) |
| Fechas futuras (2027)                 | Conservadas como datos de proyeccion / muestra        |
| Columna Vendedor sin datos utiles     | Ignorada (solo 1 valor en 30k filas)                  |
| Todos los TIPO DE PRODUCTO = HELADOS  | Simplificado: categoria unica                         |
| Cantidad vendida siempre = 1          | Interpretado como "cada fila = 1 unidad vendida"      |

### Clasificacion de filas

El campo `PRODUCTOS` contiene dos tipos de datos:

- **Filas de tamanio** (10,040 registros): `1/4 KG`, `1/2 KG`, `1KG` -- representan ventas con precio asignado
- **Filas de sabor** (8,877 registros): nombres de sabores -- representan la popularidad de cada sabor, sin precio

Esta separacion permite analizar:
- **Ingresos y rentabilidad** a traves de las filas de tamanio
- **Preferencias del cliente** a traves de las filas de sabor

---

## 📈 Arquitectura del Dashboard

La aplicacion esta organizada en **4 pestanias** principales con filtros globales en la barra lateral.

### Sidebar - Filtros Globales

| Filtro          | Tipo          | Efecto                                               |
|-----------------|---------------|------------------------------------------------------|
| Rango de Fechas | Date picker   | Filtra todas las visualizaciones por periodo         |
| Tamanio         | Multiselect   | Selecciona que tamanios incluir (1/4 KG, 1/2 KG, 1KG)|
| Horario         | Range slider  | Filtra por franja horaria (17:00 - 23:00)            |

Muestra en tiempo real: **total de ventas filtradas** y **suma de ingresos**.

### KPI Cards (Resumen Ejecutivo)

Siempre visibles en la parte superior del dashboard:

| KPI                  | Descripcion                                          | Formula                         |
|----------------------|------------------------------------------------------|---------------------------------|
| 💰 Ingresos Totales  | Suma de todos los ingresos en el periodo              | `SUM(PRECIO_CLEAN)`             |
| 📦 Ventas Totales    | Cantidad de transacciones registradas                 | `COUNT(*)`                      |
| 📅 Ticket Promedio   | Gasto promedio por venta                              | `Ingresos / Ventas`             |
| 🍦 Sabores           | Cantidad de sabores unicos en catalogo                | `COUNT(DISTINCT PRODUCTOS)`     |
| 📊 Dias con Ventas   | Cantidad de dias con al menos 1 venta                 | `COUNT(DISTINCT FECHA)`         |
| 🏆 Mejor Mes         | Mes con mayor ingreso en el periodo                   | `MAX(SUM(REVENUE) GROUP BY MES)`|

---

### Tab 1: 📈 Tendencias

Visualizaciones enfocadas en la evolucion temporal de los ingresos.

| Grafico                              | Tipo             | Que muestra                                           |
|--------------------------------------|------------------|-------------------------------------------------------|
| **Evolucion de Ingresos Diarios**    | Linea + area     | Ingreso diario con media movil de 7 dias (suavizado)  |
| **Distribucion por Tamanio**         | Donut/Pie        | Proporcion de ingresos: 1/4 KG ($6k) vs 1/2 KG ($11k) vs 1 KG ($19k) |
| **Ingresos y Ventas por Mes**        | Barras + Linea   | Doble eje: barras = ingresos mensuales, linea = cantidad de ventas |
| **Ingresos Acumulados Anuales**      | Area             | Running total de ingresos a lo largo del anio         |
| **Relacion Ventas vs Ingresos**      | Scatter          | Cada punto = un dia. Correlacion entre nro de ventas e ingreso |

---

### Tab 2: 🍧 Productos y Sabores

Analisis de catalogo, preferencias del cliente y mix de productos.

| Grafico                              | Tipo             | Que muestra                                           |
|--------------------------------------|------------------|-------------------------------------------------------|
| **Top 25 Sabores Mas Populares**     | Barras horiz.    | Ranking de sabores por cantidad de registros, con gradiente de color |
| **Top 10 Sabores (Treemap)**         | Treemap          | Visualizacion jerarquica de los 10 sabores mas frecuentes |
| **Unidades Vendidas por Tamanio**     | Barras verticales| Cuantas unidades se vendieron de cada tamanio         |
| **Evolucion Mensual de Top 10**      | Lineas multiples | Como varia la popularidad de cada sabor mes a mes     |

---

### Tab 3: ⏰ Horarios y Patrones

Identificacion de horas pico, valles y patrones semanales.

| Grafico                              | Tipo             | Que muestra                                           |
|--------------------------------------|------------------|-------------------------------------------------------|
| **Ventas por Hora del Dia**          | Linea + Barras   | Ingresos (linea) y cantidad (barras) por cada hora del dia |
| **Mapa de Calor: Dia x Hora**        | Heatmap          | Intensidad de ingresos en matriz dia de la semana vs hora |
| **Ingresos por Dia de la Semana**    | Barras           | Que dias generan mas ingresos (Lunes a Domingo)      |
| **Metricas de Horas Pico**           | Metric cards     | Hora de maximo ingreso, hora valle, ticket promedio maximo |

---

### Tab 4: 📋 Datos

Exploracion de datos crudos y exportacion.

| Funcion                              | Descripcion                                           |
|--------------------------------------|-------------------------------------------------------|
| **Tabla interactiva**                | Datos filtrados con columnas: Fecha, Horario, Producto, Precio, Ingreso, Dia, Mes |
| **Descarga CSV**                     | Boton para exportar los datos filtrados               |
| **Resumen inferior**                 | Total de registros y rango de fechas activo           |

---

## 🎨 Diseno y Estetica

### Paleta de colores tematica

| Color          | Hex       | Uso                                       |
|----------------|-----------|-------------------------------------------|
| Rosa fresa     | `#FF8BA7` | KPIs, lineas de tendencia, acentos        |
| Lavanda        | `#BA90C6` | Barras mensuales, weekday                 |
| Celeste        | `#C0DBEA` | Treemap, barras secundarias               |
| Chocolate      | `#8B5E3C` | Detalles, hover, textos descriptivos      |
| Menta          | `#7EC8A6` | Revenue acumulado, metricas positivas     |
| Fondo          | `#FFF8F0` | Background general (crema pastelera)      |

### Tipografia

- **Fredoka One**: Titulos principales (personalidad de heladeria)
- **Nunito**: Cuerpo, KPI values, labels (legibilidad moderna)

---

## 🚀 Instalacion y Uso

### Requisitos previos

- Python 3.12 o superior
- pip (gestor de paquetes)

### Instalacion local

```bash
# 1. Clonar el repositorio
git clone https://github.com/ricardobing/heladeria-kpi.git
cd heladeria-kpi

# 2. Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate    # Linux/macOS
# o
venv\Scripts\activate       # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicacion
streamlit run app.py
```

La aplicacion se abrira automaticamente en `http://localhost:8501`.

### Despliegue en Streamlit Cloud

1. Hacer push del repositorio a GitHub
2. Ir a [share.streamlit.io](https://share.streamlit.io)
3. Conectar la cuenta de GitHub
4. Seleccionar repo `heladeria-kpi`, branch `master`, archivo `app.py`
5. Click en **Deploy**

---

## 📋 Interpretacion de KPIs - Guia para el Negocio

### Como leer las tendencias

- **Linea de tendencia diaria**: Si la media movil (linea punteada marron) sube consistentemente, las ventas estan mejorando. Bajadas pronunciadas sin recuperacion indican problemas.
- **Scatter ventas vs ingresos**: Dias en la esquina superior derecha = dias excelentes (muchas ventas + ticket alto). Dias abajo-izquierda = dias flojos. La dispersion indica que tan consistente es el negocio.

### Como usar los horarios

- **Hora pico**: Programar mas personal en esa franja. Preparar stock extra.
- **Hora valle**: Ideal para limpieza, reposicion de inventario, corte de caja.
- **Heatmap**: Si los sabados a las 19hs son rojos intensos = maxima demanda. Refuerzo de personal y stock ahi.

### Como interpretar productos

- **Sabores top**: Mantener SIEMPRE en stock. Ubicarlos en posicion preferencial de la carta/vitrina.
- **Sabores de cola baja**: Evaluar si conviene mantenerlos o rotarlos por sabores de temporada.
- **Distribucion de tamanios**: Si 1KG genera el 53% de ingresos, asegurar produccion suficiente de ese formato. Analizar margen por tamanio.

### Acciones basadas en datos

| Si ves...                                    | Accion recomendada                       |
|----------------------------------------------|------------------------------------------|
| Caida sostenida en media movil 7d            | Revisar precios, competencia, marketing  |
| Muchos sabores con <10 registros/mes          | Simplificar carta, rotar sabores         |
| Pico muy marcado en 1 sola hora              | Evaluar abrir mas temprano / cerrar mas tarde |
| Sabados y Domingos igual que Martes           | Campanias especificas de fin de semana   |
| Ticket promedio bajando                      | Upselling, combos, promociones 2x1       |

---

## 🔄 Actualizacion de Datos

Para actualizar el dashboard con nuevos datos:

1. Reemplazar `Base de datos Heladeria.xlsx` con el nuevo archivo
2. Mantener el mismo nombre de columnas y estructura
3. Hacer commit y push. Si esta en Streamlit Cloud, se actualiza automaticamente.

---

## 📄 Licencia

Proyecto demostrativo para portfolio. Datos simulados de muestra.

---

## 👤 Autor

**Ricardo Bing** - [GitHub](https://github.com/ricardobing)

---

*Dashboard creado como propuesta para competencia en Freelancer. Si te gusta, dejame una estrella ⭐ en el repo.*
