# 🍦 Heladeria KPI Dashboard

<p align="center">
  <a href="https://heladeria-kpi.streamlit.app/" target="_blank">
    <img src="https://img.shields.io/badge/VER_DEMO_EN_VIVO-FF6B9D?style=for-the-badge&logo=streamlit&logoColor=white" alt="Demo en vivo">
  </a>
</p>

<p align="center">
  <b>Dashboard ejecutivo de ventas y productos para heladerias.</b><br>
  Transforma datos crudos de Excel en decisiones de negocio claras, rapidas y compartibles.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Plotly-5.17+-3F4F75?logo=plotly&logoColor=white" alt="Plotly">
  <img src="https://img.shields.io/badge/Pandas-2.0+-150458?logo=pandas&logoColor=white" alt="Pandas">
  <img src="https://img.shields.io/badge/OpenPyXL-3.1+-217346?logo=microsoft-excel&logoColor=white" alt="OpenPyXL">
</p>

---

## 🚀 Demo en vivo

**Accede al dashboard funcional con datos reales del negocio:**

### 👉 [https://heladeria-kpi.streamlit.app/](https://heladeria-kpi.streamlit.app/)

El tablero esta desplegado en Streamlit Cloud y se actualiza automaticamente con cada cambio en este repositorio.

---

## 💡 El Problema

El dueno de una heladeria recibe diariamente ventas en Excel pero no tiene una forma rapida de responder preguntas clave:

- ¿Cuanto estamos vendiendo realmente?
- ¿Que sabores conviene mantener y cuales descontinuar?
- ¿A que hora necesito mas personal?
- ¿Que dias de la semana son mas rentables?
- ¿Como evolucionan las ventas mes a mes?

Ademas, el archivo de origen tenia datos inconsistentes: precios mezclados como texto, filas vacias, precios en cero, fechas futuras y estructura duplicada. Sin limpieza, cualquier tablero tradicional arrojaria conclusiones incorrectas.

---

## ✅ La Solucion

Un **dashboard web interactivo** construido con Python y Streamlit que:

1. **Limpia y modela automaticamente** los datos del Excel.
2. **Visualiza dos areas criticas**: Ventas e Inventario/Productos.
3. **Permite filtrar** por fecha, tamanio de pote y franja horaria.
4. **Exporta los datos filtrados** a CSV.
5. **Carga rapido**, se ve profesional y funciona en cualquier dispositivo.

### Por que Streamlit en lugar de Power BI

| Aspecto | Power BI | Esta solucion Streamlit |
|---------|----------|-------------------------|
| Licencias | Requiere licencia Pro/Premium para compartir | Gratis y sin limites de usuarios |
| Despliegue | Publicacion manual en servicio de Microsoft | Push a GitHub = deploy automatico |
| Personalizacion | Limitada sin DAX avanzado | Total con Python + CSS |
| Vinculacion de datos | Requiere conectores especificos | Se actualiza reemplazando un archivo Excel |
| Costo | Mensual por usuario | Cero costos recurrentes |
| Velocidad de carga | Depende del modelo y gateway | Carga directa en memoria, tiempos rapidos |

---

## 📊 Resultados Clave del Negocio (con datos reales del archivo)

Con la informacion limpia y modelada, el dashboard revela:

| Metrica | Valor | Insight |
|---------|-------|---------|
| **Ingresos totales** | $120.093.000 | Cifra consolidada en el periodo analizado |
| **Ventas totales** | 10.040 transacciones | Cada fila representa una unidad vendida |
| **Ticket promedio** | $11.961 | Gasto promedio por compra |
| **Dias con ventas** | 360 | Casi un anio completo de datos diarios |
| **Sabores en catalogo** | 52 | Variedad amplia para analizar rotacion |
| **Mejor mes** | Mar 2026 | Mes de mayor facturacion |
| **Tamanio mas vendido en ingresos** | 1 KG | Representa la mayor parte de los ingresos |
| **Franja horaria critica** | 17:00 - 23:00 | Horario completo de operacion con datos |

---

## 🛠 Stack Tecnico

| Componente | Tecnologia | Rol en el proyecto |
|------------|------------|-------------------|
| **Lenguaje** | Python 3.12+ | Procesamiento, logica de negocio y backend |
| **Framework UI** | Streamlit 1.28+ | Interfaces interactivas, filtros y layout responsivo |
| **Visualizaciones** | Plotly 5.17+ | Graficos interactivos de alta calidad (15+ tipos) |
| **Procesamiento de datos** | Pandas 2.0+ | ETL, limpieza, agregaciones y modelado |
| **Lectura Excel** | OpenPyXL 3.1+ | Parseo eficiente de archivos .xlsx grandes |
| **Estilos** | CSS3 custom | Tema visual alineado con la identidad de una heladeria |
| **Control de versiones** | Git + GitHub | Versionado continuo y despliegue automatico |

---

## 📁 Estructura del Proyecto

```
heladeria-kpi/
├── app.py                            # Aplicacion principal Streamlit (4 tabs)
├── data_processor.py                 # Pipeline ETL: carga, limpieza, curacion, metricas
├── visualizations.py                 # Funciones generadoras de graficos Plotly
├── requirements.txt                  # Dependencias Python
├── Base de datos Heladeria.xlsx      # Fuente de datos original (~30.000 filas)
├── .gitignore                        # Exclusiones de Git
└── README.md                         # Documentacion del proyecto
```

---

## 🧹 Proceso de Limpieza y Modelado de Datos

El archivo Excel original tenia mas de 30.000 filas pero con calidad irregular. Se aplico un pipeline de limpieza riguroso:

| Problema detectado | Impacto si no se corrige | Solucion aplicada |
|--------------------|--------------------------|-------------------|
| 12.000 filas completamente vacias | Distorsiona conteos y promedios | Eliminadas con `dropna(how="all")` |
| Precios como texto (`$11000`) | Imposible sumar o comparar | Regex para extraer solo valores numericos |
| Precios en cero en filas de sabor | Ingresos calculados incorrectamente | Separacion en `df_sales` (filas con precio) y `df_flavors` (popularidad de sabores) |
| Fechas del 2027 en una muestra de 2026 | Parecen datos de prueba | Conservadas y etiquetadas como proyeccion/muestra |
| Columna `Vendedor` vacia (1 valor en 30k filas) | No aporta informacion | Excluida del analisis |
| `TIPO DE PRODUCTO` siempre = HELADOS | Sin variabilidad util | Simplificado a una sola categoria |
| Cantidad vendida siempre = 1 | No refleja volumen real | Interpretado como "una unidad por fila" |

### Modelo de datos resultante

El campo `PRODUCTOS` se separo en dos universos:

- **Filas de tamanio (10.040 registros)**: `1/4 KG`, `1/2 KG`, `1 KG`. Tienen precio asignado ($6.000, $11.000, $19.000) y sirven para calcular **ingresos y rentabilidad**.
- **Filas de sabor (8.877 registros)**: nombres de sabores. No tienen precio y sirven para medir **preferencias del cliente** y rotacion de catalogo.

Esta separacion evita que precios en cero contaminen las metricas financieras, mientras aprovecha toda la informacion disponible.

---

## 🎨 Diseno Visual

Se diseno una paleta de colores con alto contraste, profesional y alineada con la estetica de una heladeria artesanal:

| Color | Hex | Uso |
|-------|-----|-----|
| **Fresa principal** | `#be123c` | Titulos, acentos, linea de ingresos, KPI principal |
| **Azul helado** | `#0369a1` | Series secundarias, barras de ventas |
| **Menta** | `#047857` | Ingresos acumulados, metricas positivas |
| **Caramelo** | `#b45309` | Dias de fin de semana, destacados |
| **Violeta** | `#7c3aed` | Acentos adicionales y mes actual |
| **Texto principal** | `#1f2937` | Tipografia de alta legibilidad |
| **Texto secundario** | `#6b7280` | Subtitulos, ejes y etiquetas |
| **Fondo crema** | `#fffbf5` | Fondo general calido y limpio |
| **Blanco tarjetas** | `#ffffff` | Cards de KPIs con sombra suave |

La tipografia utiliza **Inter** (via Google Fonts) para garantizar legibilidad en todo tipo de pantallas.

---

## 📈 Arquitectura del Dashboard

La interfaz se organiza en **4 pestanas** mas una barra lateral de filtros globales.

### Barra lateral - Filtros globales

| Filtro | Tipo | Que hace |
|--------|------|----------|
| **Rango de fechas** | Selector de fechas | Filtra todo el dashboard por un periodo especifico |
| **Tamanio del producto** | Multiselect | Incluye/excluye tamanios: 1/4 KG, 1/2 KG, 1 KG |
| **Horario** | Range slider | Ajusta la franja horaria visible (17:00 - 23:00) |

Bajo los filtros se muestra en tiempo real el **total de ventas filtradas** y la **suma de ingresos**.

### Resumen Ejecutivo - KPIs

Cinco metricas siempre visibles en la parte superior:

| KPI | Que mide | Formula | Como interpretarlo |
|-----|----------|---------|-------------------|
| **Ingresos Totales** | Facturacion total del periodo | `SUM(PRECIO_CLEAN)` | Indicador principal de salud financiera. Comparar mes a mes. |
| **Ventas Totales** | Numero de transacciones | `COUNT(*)` | Volumen operativo. No es lo mismo que ingresos. |
| **Ticket Promedio** | Gasto promedio por venta | `Ingresos / Ventas` | Si sube, mejora la rentabilidad por transaccion. |
| **Sabores** | Variedad de productos ofrecidos | `COUNT(DISTINCT PRODUCTOS)` | Alto numero = oferta amplia; puede indicar necesidad de simplificar. |
| **Mejor Mes** | Periodo de mayor facturacion | `MAX(SUM(REVENUE) GROUP BY MES)` | Sirve para replicar estrategias exitosas. |

---

## 🔍 Detalle por Pestana

### 📈 Tendencias

Visualizaciones para entender la evolucion del negocio en el tiempo:

| Grafico | Tipo | Insight que aporta |
|---------|------|-------------------|
| **Evolucion de Ingresos Diarios** | Linea + area + tendencia | Detecta estacionalidad, picos, caidas y tendencia de 7 dias |
| **Distribucion por Tamanio** | Donut | Muestra que formato aporta mas ingresos |
| **Ingresos y Ventas Mensuales** | Barras + linea (doble eje) | Relacion entre facturacion y cantidad de ventas mes a mes |
| **Ingresos Acumulados** | Area | Progreso hacia metas anuales o trimestrales |
| **Relacion Ventas vs Ingresos** | Scatter | Identifica dias excepcionales y consistencia del negocio |

### 🍧 Productos y Sabores

Analisis del catalogo y las preferencias de los clientes:

| Grafico | Tipo | Insight que aporta |
|---------|------|-------------------|
| **Top Sabores Mas Populares** | Barras horizontales con degradado | Sabores que nunca deben faltar |
| **Top 10 Sabores (Treemap)** | Treemap | Visualizacion jerarquica de la concentracion de demanda |
| **Unidades Vendidas por Tamanio** | Barras verticales | Volumen real por formato de pote |
| **Evolucion Mensual del Top 10** | Lineas multiples | Tendencias de sabores: ascendentes, estacionales o en declive |

### ⏰ Horarios y Patrones

Descubre cuando vender mas y cuando preparar menos:

| Grafico | Tipo | Insight que aporta |
|---------|------|-------------------|
| **Ventas por Hora del Dia** | Linea + barras (doble eje) | Horas pico de ingresos y de cantidad |
| **Mapa de Calor: Dia vs Hora** | Heatmap | Patrones cruzados: que dia y hora generan mas ventas |
| **Ingresos por Dia de la Semana** | Barras | Identifica los dias mas rentables |
| **Analisis de Horas Pico** | Metric cards | Hora pico, hora valle y ticket maximo por hora |

### 📋 Datos

- Tabla interactiva con las ventas filtradas.
- Columnas: Fecha, Horario, Producto, Precio, Ingreso, Dia de la semana, Mes.
- Boton para descargar los datos filtrados en CSV.
- Resumen del total de registros y rango de fechas.

---

## 📖 Guia de Interpretacion de KPIs para el Negocio

### Tendencias

- **Linea de tendencia (punteada)**: si sube de forma sostenida, el negocio crece. Si cae varios dias seguidos, revisar precios, competencia o marketing.
- **Scatter Ventas vs Ingresos**: los puntos en la esquina superior derecha son dias excelentes. Los de la esquina inferior izquierda son dias flojos. Si hay mucha dispersion, el negocio es inestable.

### Productos

- **Sabores top**: mantener siempre en stock y ubicarlos en posiciones privilegiadas de la carta.
- **Sabores con pocos registros**: evaluar rotarlos o reemplazarlos por sabores de temporada.
- **Tamanio dominante**: si 1 KG genera la mayor parte de los ingresos, asegurar suficiente produccion de ese formato.

### Horarios

- **Hora pico**: programar mas personal y preparar stock adicional.
- **Hora valle**: momento ideal para limpieza profunda, reposicion de inventario y corte de caja.
- **Heatmap**: si ciertos dias y horas son consistentemente rojos, considerar abrir mas temprano o extender el horario.

### Acciones recomendadas segun lo que se observa

| Senal en el dashboard | Accion recomendada |
|-----------------------|-------------------|
| Caida sostenida en la tendencia de 7 dias | Revisar precios, competencia y campanas de marketing |
| Muchos sabores con menos de 10 registros al mes | Simplificar la carta para reducir desperdicio |
| Pico concentrado en una sola hora | Reforzar personal y stock en esa franja |
| Fines de semana similares a dias de semana | Crear promociones especificas para sabados y domingos |
| Ticket promedio a la baja | Implementar combos, upselling o promociones 2x1 |

---

## 🚀 Instalacion Local

### Requisitos

- Python 3.12 o superior
- pip

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/ricardobing/heladeria-kpi.git
cd heladeria-kpi

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate      # Linux/macOS
# o
venv\Scripts\activate         # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicacion
streamlit run app.py
```

La app se abrira automaticamente en `http://localhost:8501`.

---

## 🌐 Despliegue en Streamlit Cloud

1. Hacer push del repositorio a GitHub.
2. Ir a [share.streamlit.io](https://share.streamlit.io).
3. Conectar la cuenta de GitHub.
4. Seleccionar el repositorio `heladeria-kpi`, branch `master` y archivo `app.py`.
5. Hacer clic en **Deploy**.

Cada push a `master` actualiza el dashboard automaticamente.

---

## 🔄 Actualizacion de Datos

Para mantener el tablero actualizado:

1. Reemplazar el archivo `Base de datos Heladeria.xlsx` con la nueva version.
2. Mantener los nombres de columnas: `FECHA`, `TIPO DE PRODUCTO`, `Vendedor`, `HORARIO`, `PRODUCTOS`, `Cantidad vendida`, `PRECIO DE VENTA`.
3. Hacer commit y push. Streamlit Cloud actualiza la app en segundos.

---

## 🚧 Roadmap de Mejoras Futuras

- [ ] Conexion directa a base de datos o Google Sheets para actualizacion automatica sin reemplazar Excel.
- [ ] Modulo de prediccion de demanda con machine learning.
- [ ] Alertas automaticas por caidas de ventas o stock critico.
- [ ] Comparativo ano contra ano.
- [ ] Exportacion de reportes en PDF.

---

## 📄 Licencia

Proyecto demostrativo para portfolio. Los datos son simulados de muestra.

---

## 👤 Autor

**Ricardo Bing**

- GitHub: [@ricardobing](https://github.com/ricardobing)
- Demo: [https://heladeria-kpi.streamlit.app/](https://heladeria-kpi.streamlit.app/)

---

<p align="center">
  Si este proyecto te resulta util, dejame una ⭐ en el repositorio.
</p>
