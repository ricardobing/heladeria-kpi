import streamlit as st
from pathlib import Path

from data_processor import (
    load_and_clean, get_kpi_metrics, get_sales_by_month,
    get_sales_by_day, get_sales_by_hour, get_sales_by_weekday,
    get_sales_by_size, get_top_flavors, HELADERIA_COLORS
)
from visualizations import (
    make_kpi_cards, revenue_trend, monthly_revenue, pie_sales_by_size,
    bar_sizes, top_flavors, sales_by_hour, sales_by_weekday,
    heatmap_hour_weekday, cumulative_revenue, scatter_rev_vs_sales,
    flavor_treemap, make_data_table
)

st.set_page_config(
    page_title="Heladeria KPI Dashboard",
    page_icon="🍦",
    layout="wide",
    initial_sidebar_state="expanded"
)

C = HELADERIA_COLORS

# ---- Custom CSS ----
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@400;600;700&display=swap');
    .stApp {{ background: linear-gradient(135deg, #FFF8F0 0%, #FFF0F5 100%); }}
    .main-header {{
        font-family: 'Fredoka One', cursive;
        font-size: 2.8rem;
        color: {C['dark']};
        text-align: center;
        padding: 1rem 0 0.5rem 0;
        text-shadow: 2px 2px 0px rgba(232,160,191,0.3);
    }}
    .sub-header {{
        text-align: center;
        color: {C['chocolate']};
        font-family: 'Nunito', sans-serif;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
    }}
    .section-title {{
        font-family: 'Fredoka One', cursive;
        font-size: 1.6rem;
        color: {C['dark']};
        border-left: 5px solid {C['strawberry']};
        padding-left: 1rem;
        margin: 1.5rem 0 1rem 0;
    }}
    div[data-testid="stMetricValue"] {{ font-family: 'Nunito', sans-serif; font-weight: 700; }}
    .stPlotlyChart {{ border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); }}
    .stDataFrame {{ border-radius: 12px; overflow: hidden; }}
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #FFF8F0 0%, #FFF0F5 100%);
    }}
    .stButton>button {{
        border-radius: 20px; font-family: 'Nunito', sans-serif;
        font-weight: 600; border: none;
        background: {C['strawberry']}; color: white;
    }}
    .stButton>button:hover {{ background: {C['chocolate']}; }}
</style>
""", unsafe_allow_html=True)

# ---- Load Data ----
@st.cache_data(ttl=3600)
def load_data():
    data_path = Path(__file__).parent / "Base de datos Heladeria.xlsx"
    return load_and_clean(data_path)

df_sales, df_flavors = load_data()

# Derived data
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
st.sidebar.markdown(f"**{len(df_sales_f):,}** ventas filtradas")
st.sidebar.markdown(f"**${df_sales_f['REVENUE'].sum():,.0f}** ingresos")

# Recompute derived data with filters
monthly_f = get_sales_by_month(df_sales_f)
daily_f = get_sales_by_day(df_sales_f)
hourly_f = get_sales_by_hour(df_sales_f)
weekday_f = get_sales_by_weekday(df_sales_f)
sizes_f = get_sales_by_size(df_sales_f)

# ============= MAIN UI =============
st.markdown(f'<div class="main-header">🍦 Heladeria KPI</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-header">Dashboard Interactivo de Ventas y Productos</div>', unsafe_allow_html=True)

# ---- KPI Cards Row ----
st.markdown(f'<div class="section-title">Resumen Ejecutivo</div>', unsafe_allow_html=True)
kpi_figs = make_kpi_cards(metrics)
cols = st.columns(6)
for i, fig in enumerate(kpi_figs):
    with cols[i]:
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

# ---- TAB SYSTEM ----
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Tendencias",
    "🍧 Productos y Sabores",
    "⏰ Horarios y Patrones",
    "📋 Datos"
])

with tab1:
    st.markdown(f'<div class="section-title">Tendencias de Ventas</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.plotly_chart(revenue_trend(daily_f), width="stretch")
    with col2:
        st.plotly_chart(pie_sales_by_size(sizes_f), width="stretch")

    st.plotly_chart(monthly_revenue(monthly_f), width="stretch")

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(cumulative_revenue(daily_f), width="stretch")
    with col4:
        st.plotly_chart(scatter_rev_vs_sales(daily_f), width="stretch")

with tab2:
    st.markdown(f'<div class="section-title">Productos y Sabores</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(top_flavors(flavors_df), width="stretch")
    with col2:
        st.plotly_chart(flavor_treemap(df_flavors), width="stretch")

    st.plotly_chart(bar_sizes(sizes_f), width="stretch")

    st.markdown("### Top 10 Sabores por Mes")
    flavor_monthly = df_flavors.groupby(["MES_NAME", "PRODUCTOS"]).size().reset_index(name="count")
    top_10_all = df_flavors.groupby("PRODUCTOS").size().nlargest(10).index.tolist()
    flavor_top = flavor_monthly[flavor_monthly["PRODUCTOS"].isin(top_10_all)]
    import plotly.express as px
    fig_fm = px.line(
        flavor_top, x="MES_NAME", y="count", color="PRODUCTOS",
        markers=True,
        color_discrete_sequence=C["chart_colors"],
        title="Evolucion Mensual de Top 10 Sabores"
    )
    fig_fm.update_layout(
        plot_bgcolor="rgba(255,248,240,0.3)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=C["dark"], family="Segoe UI"),
        height=400, legend=dict(font=dict(size=11)),
        xaxis_title="Mes", yaxis_title="Registros",
        hoverlabel=dict(bgcolor="white", font_size=13)
    )
    st.plotly_chart(fig_fm, width="stretch")

with tab3:
    st.markdown(f'<div class="section-title">Horarios y Patrones de Compra</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(sales_by_hour(hourly_f), width="stretch")
    with col2:
        st.plotly_chart(heatmap_hour_weekday(df_sales_f), width="stretch")

    st.plotly_chart(sales_by_weekday(weekday_f), width="stretch")

    # Peak hours analysis
    st.markdown("### Analisis de Horas Pico")
    peak_data = hourly_f.copy()
    peak_data["es_pico"] = peak_data["revenue"] > peak_data["revenue"].median()
    ph1, ph2, ph3 = st.columns(3)
    with ph1:
        hora_pico = peak_data.loc[peak_data["revenue"].idxmax()]
        st.metric("Hora Pico Maxima", f"{int(hora_pico['HORA'])}:00 hs",
                  f"${hora_pico['revenue']:,.0f}")
    with ph2:
        hora_valle = peak_data.loc[peak_data["revenue"].idxmin()]
        st.metric("Hora Valle Minima", f"{int(hora_valle['HORA'])}:00 hs",
                  f"${hora_valle['revenue']:,.0f}")
    with ph3:
        ticket_pico = hourly_f.groupby("HORA")["avg_ticket"].mean()
        st.metric("Ticket Prom. Hora Pico", f"${ticket_pico.max():,.0f}",
                  f"Hora {int(hourly_f.loc[hourly_f['avg_ticket'].idxmax(), 'HORA'])}:00")

with tab4:
    st.markdown(f'<div class="section-title">Explorar Datos de Ventas</div>', unsafe_allow_html=True)

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
    st.markdown(f"**Total de registros:** {len(df_sales_f):,} | **Rango:** {df_sales_f['FECHA'].min().strftime('%d/%m/%Y')} - {df_sales_f['FECHA'].max().strftime('%d/%m/%Y')}")

# ---- Footer ----
st.markdown("---")
st.markdown(
    f"<div style='text-align:center; color:{C['chocolate']}; font-size:0.85rem;'>"
    "🍦 Heladeria KPI Dashboard · Datos simulados de muestra · Creado con Streamlit & Plotly"
    "</div>",
    unsafe_allow_html=True
)
