import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# Paleta heladeria refinada
C = {
    "pink": "#FF6B9D",
    "purple": "#C084FC",
    "sky": "#67C7E3",
    "mint": "#34D399",
    "chocolate": "#92400E",
    "caramel": "#D97706",
    "cream": "#FFF5E1",
    "dark": "#1E1B4B",
    "rose": "#FB7185",
    "lilac": "#A78BFA",
    "aqua": "#38BDF8",
    "lime": "#A3E635",
    "warm": "#F97316",
    "berry": "#E11D48",
}

FONT = "Segoe UI, system-ui, sans-serif"
PAPER = "rgba(0,0,0,0)"
PLOT_BG = "rgba(255,248,240,0.4)"


def _base_layout(fig, title, subtitle=None, height=420, x_title=None, y_title=None):
    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(size=18, color=C["dark"], family=FONT),
            x=0, xanchor="left"
        ),
        plot_bgcolor=PLOT_BG,
        paper_bgcolor=PAPER,
        font=dict(color=C["dark"], family=FONT, size=12),
        margin=dict(l=10, r=10, t=50, b=10),
        height=height,
        hoverlabel=dict(bgcolor="#1E1B4B", font_size=13, font_family=FONT, font_color="white",
                        bordercolor="rgba(0,0,0,0)"),
        legend=dict(font=dict(size=11, family=FONT), orientation="h", yanchor="top", y=-0.15,
                    xanchor="center", x=0.5, bgcolor="rgba(0,0,0,0)"),
        dragmode=False,
    )
    if x_title:
        fig.update_xaxes(title=x_title, title_font=dict(size=12, color="#6B7280"))
    if y_title:
        fig.update_yaxes(title=y_title, title_font=dict(size=12, color="#6B7280"))
    fig.update_xaxes(showgrid=False, zeroline=False, color="#9CA3AF")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(0,0,0,0.06)", zeroline=False, color="#9CA3AF")
    return fig


def _gradient_bars(fig, color, n):
    """Apply gradient effect to bar traces."""
    if n == 1:
        fig.update_traces(marker=dict(color=color, line=dict(width=0)))
    else:
        steps = []
        for i in range(n):
            alpha = 0.5 + (0.5 * i / max(n - 1, 1))
            steps.append(f"rgba({_hex_to_rgb(color)}, {alpha:.2f})")
        fig.update_traces(marker=dict(color=steps, line=dict(width=0)))


def _hex_to_rgb(hex_color):
    h = hex_color.lstrip("#")
    return f"{int(h[0:2],16)}, {int(h[2:4],16)}, {int(h[4:6],16)}"


# ============================================================
# REVENUE TREND
# ============================================================
def revenue_trend(daily_df):
    daily_df = daily_df.sort_values("DIA")
    fig = go.Figure()
    # Area fill
    fig.add_trace(go.Scatter(
        x=daily_df["DIA"], y=daily_df["revenue"],
        mode="lines",
        line=dict(width=0),
        fill="tozeroy",
        fillcolor=f"rgba({_hex_to_rgb(C['pink'])}, 0.12)",
        showlegend=False,
        hoverinfo="skip"
    ))
    # Main line
    fig.add_trace(go.Scatter(
        x=daily_df["DIA"], y=daily_df["revenue"],
        mode="lines",
        line=dict(color=C["pink"], width=2.8, shape="spline", smoothing=0.5),
        name="Ingreso diario",
        hovertemplate="<b>%{x|%d %b %Y}</b><br>💰 $%{y:,.0f}<extra></extra>"
    ))
    # Rolling average
    roll = daily_df["revenue"].rolling(7, center=True).mean()
    fig.add_trace(go.Scatter(
        x=daily_df["DIA"], y=roll,
        mode="lines",
        line=dict(color=C["dark"], width=2, dash="dot"),
        name="Tendencia 7 dias",
        hovertemplate="Promedio 7d: $%{y:,.0f}<extra></extra>"
    ))
    return _base_layout(fig, "Ingresos Diarios", y_title="Ingresos ($)", height=430)


# ============================================================
# MONTHLY REVENUE BAR + LINE
# ============================================================
def monthly_revenue(monthly_df):
    monthly_df = monthly_df.sort_values("MES_NAME")
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    colors = [C["lilac"]] * len(monthly_df)
    colors[-1] = C["purple"]

    fig.add_trace(go.Bar(
        x=monthly_df["MES_NAME"], y=monthly_df["revenue"],
        name="Ingresos",
        marker=dict(color=colors, line=dict(width=0), opacity=0.85),
        hovertemplate="<b>%{x}</b><br>💰 $%{y:,.0f}<extra></extra>",
        text=[f"${v/1e6:.1f}M" for v in monthly_df["revenue"]],
        textposition="outside", textfont=dict(size=10, family=FONT, color="#6B7280"),
    ))
    fig.add_trace(go.Scatter(
        x=monthly_df["MES_NAME"], y=monthly_df["sales"],
        mode="lines+markers",
        name="Cant. Ventas",
        yaxis="y2",
        line=dict(color=C["rose"], width=2.5),
        marker=dict(size=8, color=C["rose"], line=dict(width=2, color="white")),
        hovertemplate="<b>%{x}</b><br>📦 %{y} ventas<extra></extra>"
    ), secondary_y=True)

    fig.update_yaxes(title_text="Ingresos ($)", secondary_y=False, title_font=dict(color=C["purple"]))
    fig.update_yaxes(title_text="Cantidad de Ventas", secondary_y=True, title_font=dict(color=C["rose"]))
    return _base_layout(fig, "Ingresos y Ventas Mensuales", height=430)


# ============================================================
# PIE DONUT - SIZE DISTRIBUTION
# ============================================================
def pie_sales_by_size(sizes_df):
    pie_colors = [C["pink"], C["purple"], C["sky"]]
    fig = go.Figure(go.Pie(
        labels=sizes_df["PRICE_LABEL"],
        values=sizes_df["revenue"],
        hole=0.5,
        marker=dict(colors=pie_colors, line=dict(color="white", width=3)),
        textinfo="label+percent",
        textfont=dict(size=13, family=FONT, color=C["dark"]),
        hovertemplate="<b>%{label}</b><br>💰 $%{value:,.0f}<br>📊 %{percent}<extra></extra>",
        sort=False,
        direction="clockwise",
        rotation=90,
    ))
    total = sizes_df["revenue"].sum()
    fig.add_annotation(
        text=f"<b style='font-size:22px'>${total/1e6:.1f}M</b><br><span style='font-size:12px;color:#6B7280'>total</span>",
        x=0.5, y=0.5, showarrow=False, font=dict(family=FONT)
    )
    return _base_layout(fig, "Mix de Tamanios", height=400)


# ============================================================
# BAR: UNITS BY SIZE
# ============================================================
def bar_sizes(sizes_df):
    colors = [C["pink"], C["purple"], C["sky"]]
    fig = go.Figure(go.Bar(
        x=sizes_df["PRICE_LABEL"], y=sizes_df["sales"],
        marker=dict(color=colors, line=dict(width=0)),
        text=sizes_df["sales"].astype(str),
        textposition="outside", textfont=dict(size=13, family=FONT),
        hovertemplate="<b>%{x}</b><br>📦 %{y} unidades<extra></extra>"
    ))
    return _base_layout(fig, "Unidades por Tamanio", y_title="Unidades", height=350)


# ============================================================
# TOP FLAVORS - HORIZONTAL BAR
# ============================================================
def top_flavors(flavors_df):
    n = len(flavors_df)
    grad = px.colors.sample_colorscale(
        [(0, C["mint"]), (0.5, C["sky"]), (1, C["pink"])],
        samplepoints=n, colortype="rgb"
    )
    fig = go.Figure(go.Bar(
        y=flavors_df["PRODUCTOS"], x=flavors_df["count"],
        orientation="h",
        marker=dict(color=grad, line=dict(width=0)),
        text=flavors_df["count"].astype(str),
        textposition="outside", textfont=dict(size=11, family=FONT),
        hovertemplate="<b>%{y}</b><br>🍦 %{x} registros<extra></extra>"
    ))
    fig.update_layout(yaxis=dict(autorange="reversed", tickfont=dict(size=11)))
    return _base_layout(fig, "Top Sabores Mas Populares", x_title="Veces Registrado", height=580)


# ============================================================
# SALES BY HOUR
# ============================================================
def sales_by_hour(hourly_df):
    hourly_df = hourly_df.sort_values("HORA")
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(
        x=hourly_df["HORA"], y=hourly_df["revenue"],
        mode="lines+markers",
        name="Ingresos",
        line=dict(color=C["pink"], width=3, shape="spline", smoothing=0.6),
        marker=dict(size=10, color=C["pink"], line=dict(width=2, color="white")),
        fill="tozeroy",
        fillcolor=f"rgba({_hex_to_rgb(C['pink'])}, 0.15)",
        hovertemplate="<b>%{x}:00 hs</b><br>💰 $%{y:,.0f}<extra></extra>"
    ))
    fig.add_trace(go.Bar(
        x=hourly_df["HORA"], y=hourly_df["sales"],
        name="Ventas",
        yaxis="y2",
        marker=dict(color=C["sky"], opacity=0.4, line=dict(width=0)),
        hovertemplate="<b>%{x}:00 hs</b><br>📦 %{y} ventas<extra></extra>"
    ), secondary_y=True)
    fig.update_xaxes(tickmode="linear", dtick=1)
    fig.update_yaxes(title_text="Ingresos ($)", secondary_y=False, title_font=dict(color=C["pink"]))
    fig.update_yaxes(title_text="Cant. Ventas", secondary_y=True, title_font=dict(color=C["sky"]))
    return _base_layout(fig, "Actividad por Hora del Dia", x_title="Hora", height=380)


# ============================================================
# WEEKDAY BAR
# ============================================================
def sales_by_weekday(wd_df):
    day_colors = [C["pink"], C["pink"], C["purple"], C["purple"], C["sky"], C["mint"], C["mint"]]
    fig = go.Figure(go.Bar(
        x=wd_df["DIA_SEMANA"], y=wd_df["revenue"],
        marker=dict(color=day_colors, line=dict(width=0)),
        text=[f"${v/1e6:.1f}M" for v in wd_df["revenue"]],
        textposition="outside", textfont=dict(size=11, family=FONT),
        hovertemplate="<b>%{x}</b><br>💰 $%{y:,.0f}<extra></extra>"
    ))
    return _base_layout(fig, "Ingresos por Dia de la Semana", y_title="Ingresos ($)", height=350)


# ============================================================
# HEATMAP HOUR x WEEKDAY
# ============================================================
def heatmap_hour_weekday(df_sales):
    pivot = df_sales.pivot_table(
        values="REVENUE", index="DIA_SEMANA", columns="HORA", aggfunc="sum", fill_value=0
    )
    weekday_order = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
    pivot = pivot.reindex(weekday_order)

    fig = go.Figure(go.Heatmap(
        z=pivot.values,
        x=pivot.columns.astype(str),
        y=pivot.index,
        colorscale=[(0, "#FEF3C7"), (0.5, C["pink"]), (1, C["dark"])],
        hovertemplate="<b>%{y} %{x}:00 hs</b><br>💰 $%{z:,.0f}<extra></extra>",
        colorbar=dict(
            title="Ingresos ($)", tickprefix="$",
            title_font=dict(size=11, family=FONT),
            tickfont=dict(size=10),
            thickness=15, len=0.7
        ),
        xgap=2, ygap=2
    ))
    fig.update_xaxes(side="bottom")
    return _base_layout(fig, "Mapa de Calor: Dia x Hora", x_title="Hora", y_title="Dia", height=400)


# ============================================================
# CUMULATIVE REVENUE
# ============================================================
def cumulative_revenue(daily_df):
    daily_df = daily_df.sort_values("DIA")
    daily_df["cumsum"] = daily_df["revenue"].cumsum()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily_df["DIA"], y=daily_df["cumsum"],
        mode="lines",
        line=dict(color=C["mint"], width=3),
        fill="tozeroy",
        fillcolor=f"rgba({_hex_to_rgb(C['mint'])}, 0.15)",
        name="Acumulado",
        hovertemplate="<b>%{x|%d %b %Y}</b><br>💰 $%{y:,.0f} acum.<extra></extra>"
    ))
    return _base_layout(fig, "Ingresos Acumulados", y_title="Acumulado ($)", height=380)


# ============================================================
# SCATTER: REVENUE VS SALES
# ============================================================
def scatter_rev_vs_sales(daily_df):
    daily_df = daily_df.copy()
    daily_df["day_name"] = pd.to_datetime(daily_df["DIA"]).dt.day_name()
    fig = go.Figure(go.Scatter(
        x=daily_df["sales"], y=daily_df["revenue"],
        mode="markers",
        marker=dict(
            size=12, color=C["pink"], opacity=0.6,
            line=dict(color="white", width=1.5)
        ),
        hovertemplate="<b>%{x} ventas</b><br>💰 $%{y:,.0f}<extra></extra>",
        name="Dias"
    ))
    return _base_layout(fig, "Relacion: Ventas vs Ingresos",
                        x_title="Cantidad de Ventas", y_title="Ingresos ($)", height=380)


# ============================================================
# FLAVOR TREEMAP
# ============================================================
def flavor_treemap(df_flavors):
    top = df_flavors.groupby("PRODUCTOS").size().reset_index(name="count")
    top = top.sort_values("count", ascending=False).head(10)
    fig = go.Figure(go.Treemap(
        labels=top["PRODUCTOS"],
        values=top["count"],
        parents=[""] * len(top),
        marker=dict(
            colors=top["count"],
            colorscale=[(0, C["mint"]), (0.5, C["sky"]), (1, C["pink"])],
            showscale=False
        ),
        textinfo="label+value",
        textfont=dict(size=14, family=FONT),
        hovertemplate="<b>%{label}</b><br>🍦 %{value} registros<extra></extra>",
        branchvalues="total",
    ))
    return _base_layout(fig, "Top 10 Sabores (Treemap)", height=400)


# ============================================================
# FLAVOR EVOLUTION LINE CHART
# ============================================================
def flavor_evolution(flavor_monthly):
    import plotly.express as px
    fig = px.line(
        flavor_monthly, x="MES_NAME", y="count", color="PRODUCTOS",
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.update_traces(line=dict(width=2.5), marker=dict(size=6))
    return _base_layout(fig, "Evolucion Mensual del Top 10 Sabores",
                        x_title="Mes", y_title="Registros", height=420)


# ============================================================
# METRIC VALUE FORMATTER
# ============================================================
def fmt_currency(v):
    """Format currency with K/M suffix."""
    if abs(v) >= 1e6:
        return f"${v/1e6:,.1f}M"
    elif abs(v) >= 1e3:
        return f"${v/1e3:,.0f}K"
    return f"${v:,.0f}"


def fmt_number(v):
    if abs(v) >= 1e6:
        return f"{v/1e6:,.1f}M"
    elif abs(v) >= 1e3:
        return f"{v:,.0f}"
    return str(v)
