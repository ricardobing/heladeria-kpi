import streamlit as st
from pathlib import Path

from data_processor import (
    load_and_clean, get_kpi_metrics, get_sales_by_month,
    get_sales_by_day, get_sales_by_hour, get_sales_by_weekday,
    get_sales_by_size, get_top_flavors
)
from visualizations import (
    revenue_trend, monthly_revenue, pie_sales_by_size,
    bar_sizes, top_flavors, sales_by_hour, sales_by_weekday,
    heatmap_hour_weekday, cumulative_revenue, scatter_rev_vs_sales,
    flavor_treemap, flavor_evolution, fmt_currency, fmt_number
)

st.set_page_config(
    page_title="Heladeria KPI Dashboard",
    page_icon="🍦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- Refined CSS ----
st.markdown("""
<style>
    .stApp {
        background: #FFF8F0;
    }
    .main-header {
        font-size: 2.4rem;
        font-weight: 800;
        color: #1E1B4B;
        text-align: center;
        padding: 0.8rem 0 0.3rem 0;
        letter-spacing: -0.5px;
    }
    .main-header span {
        background: linear-gradient(135deg, #FF6B9D, #C084FC);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .sub-header {
        text-align: center;
        color: #6B7280;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    .section-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1E1B4B;
        border-left: 5px solid #FF6B9D;
        padding-left: 0.8rem;
        margin: 1.2rem 0 0.8rem 0;
    }
    div[data-testid="stMetric"] {
        background: white;
        border-radius: 16px;
        padding: 1rem 0.8rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        border: 1px solid rgba(0,0,0,0.04);
    }
    div[data-testid="stMetric"] label {
        font-size: 0.8rem;
        color: #6B7280;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        font-size: 1.6rem;
        font-weight: 800;
        color: #1E1B4B;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFF8F0, #FEF3C7);
        border-right: 1px solid rgba(0,0,0,0.05);
    }
    .stButton>button {
        border-radius: 24px;
        font-weight: 600;
        border: none;
        background: linear-gradient(135deg, #FF6B9D, #C084FC);
        color: white;
        padding: 0.5rem 1.5rem;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(255,107,157,0.4);
    }
    section[data-testid="stSidebar"] h2 {
        font-size: 1.4rem;
        color: #1E1B4B;
        font-weight: 700;
    }
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(0,0,0,0.06);
    }
</style>
""", unsafe_allow_html=True)

# ---- Load Data ----
@st.cache_data(ttl=3600)
def load_data():
    data_path = Path(__file__).parent / "Base de datos Heladeria.xlsx"
    return load_and_clean(data_path)

df_sales, df_flavors = load_data()

with st.spinner("Procesando datos..."):
    metrics = get_kpi_metrics(df_sales)
    monthly_df = get_sales_by_month(df_sales)
    daily_df = get_sales_by_day(df_sales)
    hourly_df = get_sales_by_hour(df_sales)
    weekday_df = get_sales_by_weekday(df_sales)
    sizes_df = get_sales_by_size(df_sales)
    flavors_df = get_top_flavors(df_flavors, top_n=25)

# ---- Sidebar Filters ----
st.sidebar.markdown("## 🍦 Filtros")

min_date = df_sales["FECHA"].min().date()
max_date = df_sales["FECHA"].max().date()

date_range = st.sidebar.date_input(
    "Rango de Fechas",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    start_date, end_date = date_range
    mask = (df_sales["FECHA"].dt.date >= start_date) & (df_sales["FECHA"].dt.date <= end_date)
    df_sales_f = df_sales[mask].copy()
else:
    df_sales_f = df_sales.copy()

selected_sizes = st.sidebar.multiselect(
    "Tamanio del Producto",
    options=["1/4 KG", "1/2 KG", "1KG"],
    default=["1/4 KG", "1/2 KG", "1KG"]
)
df_sales_f = df_sales_f[df_sales_f["PRODUCTOS"].isin(selected_sizes)]

available_hours = sorted(df_sales["HORA"].dropna().unique())
selected_hours = st.sidebar.select_slider(
    "Horario",
    options=available_hours,
    value=(min(available_hours), max(available_hours))
)
df_sales_f = df_sales_f[(df_sales_f["HORA"] >= selected_hours[0]) & (df_sales_f["HORA"] <= selected_hours[1])]

st.sidebar.markdown("---")
st.sidebar.markdown(f"**{len(df_sales_f):,}** ventas filtradas  \n**${df_sales_f['REVENUE'].sum():,.0f}** ingresos")

# Recompute with filters
monthly_f = get_sales_by_month(df_sales_f)
daily_f = get_sales_by_day(df_sales_f)
hourly_f = get_sales_by_hour(df_sales_f)
weekday_f = get_sales_by_weekday(df_sales_f)
sizes_f = get_sales_by_size(df_sales_f)

# ======================== MAIN UI ========================
st.markdown(
    '<div class="main-header"><span>Heladeria KPI</span></div>'
    '<div class="sub-header">Dashboard Interactivo de Ventas & Productos</div>',
    unsafe_allow_html=True
)

# ---- KPI Cards with st.metric ----
st.markdown('<div class="section-title">Resumen Ejecutivo</div>', unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.metric("💰 Ingresos Totales", fmt_currency(metrics["total_revenue"]),
              delta=f"{metrics['unique_days']} dias", delta_color="off")
with c2:
    st.metric("📦 Ventas Totales", fmt_number(metrics["total_sales"]),
              delta=f"{len(selected_sizes)} tamanios activos", delta_color="off")
with c3:
    st.metric("💵 Ticket Promedio", fmt_currency(metrics["avg_ticket"]))
with c4:
    st.metric("🍦 Sabores Disponibles", metrics["unique_flavors"])
with c5:
    st.metric("🏆 Mejor Mes", metrics["best_month"],
              delta=fmt_currency(metrics["best_month_rev"]), delta_color="off")

# ---- Tabs ----
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Tendencias",
    "🍧 Productos & Sabores",
    "⏰ Horarios & Patrones",
    "📋 Datos"
])

with tab1:
    st.markdown('<div class="section-title">Tendencias de Ventas</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns([1.5, 1])
    with col_a:
        st.plotly_chart(revenue_trend(daily_f), width="stretch")
    with col_b:
        st.plotly_chart(pie_sales_by_size(sizes_f), width="stretch")

    st.plotly_chart(monthly_revenue(monthly_f), width="stretch")

    col_c, col_d = st.columns(2)
    with col_c:
        st.plotly_chart(cumulative_revenue(daily_f), width="stretch")
    with col_d:
        st.plotly_chart(scatter_rev_vs_sales(daily_f), width="stretch")

with tab2:
    st.markdown('<div class="section-title">Productos y Sabores</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.plotly_chart(top_flavors(flavors_df), width="stretch")
    with col_b:
        st.plotly_chart(flavor_treemap(df_flavors), width="stretch")

    st.plotly_chart(bar_sizes(sizes_f), width="stretch")

    flavor_monthly = df_flavors.groupby(["MES_NAME", "PRODUCTOS"]).size().reset_index(name="count")
    top_10_all = df_flavors.groupby("PRODUCTOS").size().nlargest(10).index.tolist()
    flavor_top = flavor_monthly[flavor_monthly["PRODUCTOS"].isin(top_10_all)]
    st.plotly_chart(flavor_evolution(flavor_top), width="stretch")

with tab3:
    st.markdown('<div class="section-title">Horarios y Patrones de Compra</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.plotly_chart(sales_by_hour(hourly_f), width="stretch")
    with col_b:
        st.plotly_chart(heatmap_hour_weekday(df_sales_f), width="stretch")

    st.plotly_chart(sales_by_weekday(weekday_f), width="stretch")

    st.markdown("### Analisis de Horas Pico")
    peak_data = hourly_f.copy()
    ph1, ph2, ph3 = st.columns(3)
    with ph1:
        hora_pico = peak_data.loc[peak_data["revenue"].idxmax()]
        st.metric("🔺 Hora Pico Maxima", f"{int(hora_pico['HORA'])}:00 hs",
                  delta=fmt_currency(hora_pico["revenue"]), delta_color="off")
    with ph2:
        hora_valle = peak_data.loc[peak_data["revenue"].idxmin()]
        st.metric("🔻 Hora Valle Minima", f"{int(hora_valle['HORA'])}:00 hs",
                  delta=fmt_currency(hora_valle["revenue"]), delta_color="off")
    with ph3:
        max_ticket_h = hourly_f.loc[hourly_f["avg_ticket"].idxmax()]
        st.metric("💎 Ticket Maximo", fmt_currency(max_ticket_h["avg_ticket"]),
                  delta=f"a las {int(max_ticket_h['HORA'])}:00 hs", delta_color="off")

with tab4:
    st.markdown('<div class="section-title">Explorar Datos de Ventas</div>', unsafe_allow_html=True)

    display_df = df_sales_f[["FECHA", "HORARIO", "PRODUCTOS", "PRECIO_CLEAN", "REVENUE", "DIA_SEMANA", "MES_NAME"]].copy()
    display_df.columns = ["Fecha", "Horario", "Producto", "Precio ($)", "Ingreso ($)", "Dia Semana", "Mes"]
    display_df = display_df.sort_values("Fecha", ascending=False)

    st.dataframe(
        display_df,
        width="stretch",
        height=400,
        column_config={
            "Fecha": st.column_config.DateColumn(format="DD/MM/YYYY"),
            "Precio ($)": st.column_config.NumberColumn(format="$%d"),
            "Ingreso ($)": st.column_config.NumberColumn(format="$%d"),
        },
        hide_index=True
    )

    csv = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Descargar Datos Filtrados (CSV)",
        data=csv,
        file_name="heladeria_ventas_filtradas.csv",
        mime="text/csv"
    )

    st.markdown("---")
    st.markdown(f"**Total de registros:** {len(df_sales_f):,}  |  "
                f"**Rango:** {df_sales_f['FECHA'].min().strftime('%d/%m/%Y')} - "
                f"{df_sales_f['FECHA'].max().strftime('%d/%m/%Y')}")

# ---- Footer ----
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#92400E;font-size:0.85rem;padding-bottom:1rem;'>"
    "🍦 Heladeria KPI Dashboard · Datos simulados de muestra · Streamlit + Plotly"
    "</div>",
    unsafe_allow_html=True
)
