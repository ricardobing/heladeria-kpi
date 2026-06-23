import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from data_processor import HELADERIA_COLORS

C = HELADERIA_COLORS
CHART_COLORS = C["chart_colors"]
PLOT_BG = "rgba(255,248,240,0.3)"
PAPER_BG = "rgba(0,0,0,0)"
FONT_COLOR = "#4A3B42"
TITLE_FONT_SIZE = 18


def _common_layout(fig, title, x_title=None, y_title=None, height=400):
    fig.update_layout(
        title=dict(text=title, font=dict(size=TITLE_FONT_SIZE, color=FONT_COLOR, family="Segoe UI"), x=0.05),
        plot_bgcolor=PLOT_BG,
        paper_bgcolor=PAPER_BG,
        font=dict(color=FONT_COLOR, family="Segoe UI"),
        margin=dict(l=20, r=20, t=50, b=20),
        height=height,
        hoverlabel=dict(bgcolor="white", font_size=13, font_family="Segoe UI"),
        legend=dict(font=dict(size=12)),
    )
    if x_title:
        fig.update_xaxes(title=x_title)
    if y_title:
        fig.update_yaxes(title=y_title)
    return fig


# ---- KPI CARDS ----
def make_kpi_cards(metrics):
    figs = []
    cards = [
        ("💰 Ingresos Totales", f"${metrics['total_revenue']:,.0f}", C["strawberry"]),
        ("📦 Ventas Totales", f"{metrics['total_sales']:,}", C["secondary"]),
        ("📅 Ticket Promedio", f"${metrics['avg_ticket']:,.0f}", C["mint"]),
        ("🍦 Sabores", f"{metrics['unique_flavors']}", C["accent"]),
        ("📊 Dias con Ventas", f"{metrics['unique_days']}", C["chocolate"]),
        ("🏆 Mejor Mes", f"{metrics['best_month']}", C["primary"]),
    ]
    for title, value, color in cards:
        fig = go.Figure()
        fig.add_annotation(
            text=f"<b style='font-size:28px; color:{color}'>{value}</b><br>"
                 f"<span style='font-size:13px; color:#6D6875'>{title}</span>",
            x=0.5, y=0.5, showarrow=False, font=dict(family="Segoe UI")
        )
        fig.update_layout(
            height=110, margin=dict(l=5, r=5, t=5, b=5),
            paper_bgcolor=PAPER_BG, plot_bgcolor=PAPER_BG,
            xaxis=dict(visible=False), yaxis=dict(visible=False)
        )
        figs.append(fig)
    return figs


# ---- REVENUE TREND (LINE) ----
def revenue_trend(daily_df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily_df["DIA"], y=daily_df["revenue"],
        mode="lines",
        line=dict(color=C["strawberry"], width=2.5),
        fill="tozeroy",
        fillcolor="rgba(255,139,167,0.15)",
        name="Ingreso Diario",
        hovertemplate="%{x|%d %b %Y}<br>$%{y:,.0f}<extra></extra>"
    ))
    rolling = daily_df["revenue"].rolling(7, center=True).mean()
    fig.add_trace(go.Scatter(
        x=daily_df["DIA"], y=rolling,
        mode="lines",
        line=dict(color=C["chocolate"], width=2, dash="dot"),
        name="Tendencia (7d)",
        hovertemplate="Promedio 7d: $%{y:,.0f}<extra></extra>"
    ))
    return _common_layout(fig, "Evolucion de Ingresos Diarios", y_title="Ingresos ($)", height=400)


# ---- MONTHLY REVENUE (BAR + LINE COMBO) ----
def monthly_revenue(monthly_df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        x=monthly_df["MES_NAME"], y=monthly_df["revenue"],
        name="Ingresos", marker=dict(color=C["secondary"], opacity=0.8),
        text=monthly_df["revenue"].apply(lambda x: f"${x/1e6:.1f}M"),
        textposition="outside", textfont=dict(size=11),
        hovertemplate="%{x}<br>$%{y:,.0f}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=monthly_df["MES_NAME"], y=monthly_df["sales"],
        mode="lines+markers",
        name="Ventas", yaxis="y2",
        line=dict(color=C["strawberry"], width=2.5),
        marker=dict(size=8),
        hovertemplate="%{x}<br>%{y} ventas<extra></extra>"
    ), secondary_y=True)
    fig.update_yaxes(title_text="Ingresos ($)", secondary_y=False)
    fig.update_yaxes(title_text="Cantidad de Ventas", secondary_y=True)
    return _common_layout(fig, "Ingresos y Ventas por Mes", height=420)


# ---- PIE: SALES BY SIZE ----
def pie_sales_by_size(sizes_df):
    fig = go.Figure(go.Pie(
        labels=sizes_df["PRICE_LABEL"],
        values=sizes_df["revenue"],
        hole=0.45,
        marker=dict(colors=[C["strawberry"], C["secondary"], C["accent"]],
                    line=dict(color="white", width=2)),
        textinfo="label+percent",
        textfont=dict(size=13, family="Segoe UI"),
        hovertemplate="%{label}<br>$%{value:,.0f} (%{percent})<extra></extra>"
    ))
    fig.add_annotation(text=f"<b>Total</b><br>${sizes_df['revenue'].sum():,.0f}",
                       x=0.5, y=0.5, showarrow=False, font=dict(size=14, color=FONT_COLOR))
    return _common_layout(fig, "Distribucion de Ingresos por Tamanio", height=380)


# ---- BAR: PROPORTION BY SIZE ----
def bar_sizes(sizes_df):
    fig = go.Figure(go.Bar(
        x=sizes_df["PRICE_LABEL"], y=sizes_df["sales"],
        marker=dict(color=[C["strawberry"], C["secondary"], C["accent"]], opacity=0.85),
        text=sizes_df["sales"],
        textposition="outside", textfont=dict(size=13),
        hovertemplate="%{x}<br>%{y} unidades<extra></extra>"
    ))
    return _common_layout(fig, "Unidades Vendidas por Tamanio", y_title="Unidades", height=350)


# ---- HORIZONTAL BAR: TOP FLAVORS ----
def top_flavors(flavors_df):
    fig = go.Figure(go.Bar(
        y=flavors_df["PRODUCTOS"], x=flavors_df["count"],
        orientation="h",
        marker=dict(
            color=flavors_df["count"],
            colorscale=[C["accent"], C["strawberry"]],
            showscale=False
        ),
        text=flavors_df["count"],
        textposition="outside", textfont=dict(size=12),
        hovertemplate="%{y}<br>%{x} registros<extra></extra>"
    ))
    return _common_layout(fig, "Top 25 Sabores Mas Populares", x_title="Veces Registrado", height=600)


# ---- LINE: SALES BY HOUR ----
def sales_by_hour(hourly_df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hourly_df["HORA"], y=hourly_df["revenue"],
        mode="lines+markers",
        line=dict(color=C["strawberry"], width=3, shape="spline"),
        marker=dict(size=10, color=C["strawberry"]),
        fill="tozeroy",
        fillcolor="rgba(255,139,167,0.2)",
        name="Ingresos",
        hovertemplate="%{x}:00 hs<br>$%{y:,.0f}<extra></extra>"
    ))
    fig.add_trace(go.Bar(
        x=hourly_df["HORA"], y=hourly_df["sales"],
        name="Ventas",
        marker=dict(color=C["accent"], opacity=0.5),
        yaxis="y2",
        hovertemplate="%{x}:00 hs<br>%{y} ventas<extra></extra>"
    ))
    fig.update_layout(
        xaxis=dict(tickmode="linear", dtick=1),
        yaxis=dict(title="Ingresos ($)"),
        yaxis2=dict(title="Ventas", overlaying="y", side="right")
    )
    return _common_layout(fig, "Ventas por Hora del Dia", x_title="Hora", height=380)


# ---- BAR: SALES BY WEEKDAY ----
def sales_by_weekday(wd_df):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=wd_df["DIA_SEMANA"], y=wd_df["revenue"],
        name="Ingresos",
        marker=dict(color=C["secondary"], opacity=0.8),
        text=wd_df["revenue"].apply(lambda x: f"${x/1e6:.1f}M"),
        textposition="outside", textfont=dict(size=11),
        hovertemplate="%{x}<br>$%{y:,.0f}<extra></extra>"
    ))
    return _common_layout(fig, "Ingresos por Dia de la Semana", y_title="Ingresos ($)", height=350)


# ---- HEATMAP: SALES BY HOUR x WEEKDAY ----
def heatmap_hour_weekday(df_sales):
    pivot = df_sales.pivot_table(
        values="REVENUE", index="DIA_SEMANA", columns="HORA", aggfunc="sum"
    )
    weekday_order = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
    pivot = pivot.reindex(weekday_order)
    fig = go.Figure(go.Heatmap(
        z=pivot.values,
        x=pivot.columns.astype(str),
        y=pivot.index,
        colorscale=[[0, "#FFF5E1"], [0.5, "#FF8BA7"], [1, "#8B5E3C"]],
        hovertemplate="%{y} %{x}:00<br>$%{z:,.0f}<extra></extra>",
        colorbar=dict(title="Ingresos ($)", tickprefix="$")
    ))
    return _common_layout(fig, "Mapa de Calor: Ventas por Dia y Hora", x_title="Hora", y_title="Dia", height=400)


# ---- AREA CHART: CUMULATIVE REVENUE ----
def cumulative_revenue(daily_df):
    daily_df = daily_df.copy()
    daily_df["cumsum"] = daily_df["revenue"].cumsum()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily_df["DIA"], y=daily_df["cumsum"],
        mode="lines",
        line=dict(color=C["mint"], width=3),
        fill="tozeroy",
        fillcolor="rgba(126,200,166,0.2)",
        name="Acumulado",
        hovertemplate="%{x|%d %b %Y}<br>$%{y:,.0f}<extra></extra>"
    ))
    return _common_layout(fig, "Ingresos Acumulados Anuales", y_title="Ingresos Acumulados ($)", height=380)


# ---- SCATTER: REVENUE VS SALES PER DAY ----
def scatter_rev_vs_sales(daily_df):
    fig = go.Figure(go.Scatter(
        x=daily_df["sales"], y=daily_df["revenue"],
        mode="markers",
        marker=dict(
            size=10, color=C["strawberry"], opacity=0.7,
            line=dict(color="white", width=1)
        ),
        hovertemplate="%{x} ventas<br>$%{y:,.0f}<extra></extra>",
        name="Dias"
    ))
    return _common_layout(fig, "Relacion: Ventas vs Ingresos Diarios",
                          x_title="Cantidad de Ventas", y_title="Ingresos ($)", height=380)


# ---- PIE: FLAVORS BY MONTH (small multiples concept) ----
def flavor_treemap(flavors_df):
    top_10 = flavors_df.groupby("PRODUCTOS").size().reset_index(name="count")
    top_10 = top_10.sort_values("count", ascending=False).head(10)
    fig = go.Figure(go.Treemap(
        labels=top_10["PRODUCTOS"],
        values=top_10["count"],
        parents=[""] * len(top_10),
        marker=dict(
            colors=top_10["count"],
            colorscale=[C["accent"], C["strawberry"]],
            showscale=False
        ),
        textinfo="label+value",
        hovertemplate="%{label}<br>%{value} registros<extra></extra>"
    ))
    return _common_layout(fig, "Top 10 Sabores (Treemap)", height=400)


# ---- TABLE: RAW DATA PREVIEW ----
def make_data_table(df, max_rows=100):
    display = df.head(max_rows).copy()
    cols = {
        "FECHA": "Fecha",
        "HORARIO": "Horario",
        "PRODUCTOS": "Producto",
        "PRECIO_CLEAN": "Precio ($)",
        "REVENUE": "Ingreso ($)",
        "PRICE_LABEL": "Tamanio"
    }
    available = {k: v for k, v in cols.items() if k in display.columns}
    display = display[list(available.keys())].rename(columns=available)
    return display
