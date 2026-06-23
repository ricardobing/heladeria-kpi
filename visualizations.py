import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# Paleta optima: alta contrastividad, profesional y atractiva
C = {
    "text": "#1f2937",       # gray-800, texto principal
    "muted": "#6b7280",      # gray-500, texto secundario
    "light": "#f3f4f6",      # gray-100
    "white": "#ffffff",
    "cream": "#fffbf5",
    "grid": "#e5e7eb",       # gray-200
    "primary": "#be123c",    # rose-700, fresa principal
    "secondary": "#0369a1",  # sky-700, arandano/menta
    "tertiary": "#047857",   # emerald-700, pistacho
    "quaternary": "#b45309", # amber-700, caramelo
    "accent": "#7c3aed",     # violet-600, acento adicional
    "danger": "#dc2626",
    "success": "#16a34a",
}

# Paleta para graficos categoricos de alto contraste
CATEGORICAL = ["#be123c", "#0369a1", "#047857", "#b45309", "#7c3aed", "#db2777", "#0891b2", "#65a30d", "#ea580c", "#9333ea"]

FONT = "Inter, Segoe UI, system-ui, sans-serif"
PAPER = "rgba(0,0,0,0)"
PLOT_BG = "rgba(243,244,246,0.45)"


def _hex_to_rgb(hex_color):
    h = hex_color.lstrip("#")
    return f"{int(h[0:2],16)}, {int(h[2:4],16)}, {int(h[4:6],16)}"


def _base_layout(fig, title, height=420, x_title=None, y_title=None):
    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(size=17, color=C["text"], family=FONT),
            x=0, xanchor="left"
        ),
        plot_bgcolor=PLOT_BG,
        paper_bgcolor=PAPER,
        font=dict(color=C["text"], family=FONT, size=12),
        margin=dict(l=15, r=15, t=55, b=15),
        height=height,
        hoverlabel=dict(
            bgcolor=C["text"], font_size=13, font_family=FONT, font_color=C["white"],
            bordercolor=C["text"]
        ),
        legend=dict(
            font=dict(size=12, family=FONT, color=C["text"]),
            orientation="h", yanchor="top", y=-0.18,
            xanchor="center", x=0.5, bgcolor="rgba(0,0,0,0)"
        ),
        dragmode=False,
    )
    fig.update_xaxes(
        showgrid=False, zeroline=False, color=C["muted"],
        title=dict(text=x_title, font=dict(size=12, color=C["muted"]))
    )
    fig.update_yaxes(
        showgrid=True, gridcolor="rgba(0,0,0,0.07)", zeroline=False, color=C["muted"],
        title=dict(text=y_title, font=dict(size=12, color=C["muted"]))
    )
    return fig


def _interpolate_colors(start, end, n):
    """Generate n colors between start and end hex colors."""
    s = tuple(int(start[i:i+2], 16) for i in (1, 3, 5))
    e = tuple(int(end[i:i+2], 16) for i in (1, 3, 5))
    colors = []
    for i in range(n):
        t = i / max(n - 1, 1)
        c = tuple(int(s[j] + (e[j] - s[j]) * t) for j in range(3))
        colors.append(f"rgb({c[0]}, {c[1]}, {c[2]})")
    return colors


# ============================================================
# REVENUE TREND
# ============================================================
def revenue_trend(daily_df):
    daily_df = daily_df.sort_values("DIA")
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=daily_df["DIA"], y=daily_df["revenue"],
        mode="lines",
        line=dict(width=0),
        fill="tozeroy",
        fillcolor=f"rgba({_hex_to_rgb(C['primary'])}, 0.10)",
        showlegend=False,
        hoverinfo="skip"
    ))
    fig.add_trace(go.Scatter(
        x=daily_df["DIA"], y=daily_df["revenue"],
        mode="lines",
        line=dict(color=C["primary"], width=2.6, shape="spline", smoothing=0.5),
        name="Ingreso diario",
        hovertemplate="<b>%{x|%d %b %Y}</b><br>Ingreso: $%{y:,.0f}<extra></extra>"
    ))
    roll = daily_df["revenue"].rolling(7, center=True).mean()
    fig.add_trace(go.Scatter(
        x=daily_df["DIA"], y=roll,
        mode="lines",
        line=dict(color=C["text"], width=2, dash="dot"),
        name="Tendencia 7 dias",
        hovertemplate="Tendencia 7d: $%{y:,.0f}<extra></extra>"
    ))
    return _base_layout(fig, "Evolucion Diaria de Ingresos", y_title="Ingresos ($)", height=440)


# ============================================================
# MONTHLY REVENUE
# ============================================================
def monthly_revenue(monthly_df):
    monthly_df = monthly_df.sort_values("MES")
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    n = len(monthly_df)
    colors = [C["secondary"]] * n
    colors[-1] = C["accent"]

    fig.add_trace(go.Bar(
        x=monthly_df["MES_NAME"], y=monthly_df["revenue"],
        name="Ingresos",
        marker=dict(color=colors, line=dict(width=0), opacity=0.88),
        hovertemplate="<b>%{x}</b><br>Ingresos: $%{y:,.0f}<extra></extra>",
        text=[f"${v/1e6:.1f}M" for v in monthly_df["revenue"]],
        textposition="outside", textfont=dict(size=10, family=FONT, color=C["text"]),
    ))
    fig.add_trace(go.Scatter(
        x=monthly_df["MES_NAME"], y=monthly_df["sales"],
        mode="lines+markers",
        name="Cantidad de Ventas",
        yaxis="y2",
        line=dict(color=C["primary"], width=2.5),
        marker=dict(size=8, color=C["primary"], line=dict(width=2, color=C["white"])),
        hovertemplate="<b>%{x}</b><br>Ventas: %{y}<extra></extra>"
    ), secondary_y=True)

    fig.update_yaxes(title_text="Ingresos ($)", secondary_y=False, tickprefix="$")
    fig.update_yaxes(title_text="Ventas", secondary_y=True)
    return _base_layout(fig, "Ingresos y Ventas Mensuales", height=430)


# ============================================================
# PIE DONUT - SIZE DISTRIBUTION
# ============================================================
def pie_sales_by_size(sizes_df):
    colors = [C["primary"], C["secondary"], C["tertiary"]]
    total = sizes_df["revenue"].sum()
    fig = go.Figure(go.Pie(
        labels=sizes_df["PRICE_LABEL"],
        values=sizes_df["revenue"],
        hole=0.55,
        marker=dict(colors=colors, line=dict(color=C["white"], width=3)),
        textinfo="label+percent",
        textfont=dict(size=13, family=FONT, color=C["text"]),
        textposition="outside",
        hovertemplate="<b>%{label}</b><br>Ingresos: $%{value:,.0f}<br>Porcentaje: %{percent}<extra></extra>",
        sort=False,
        direction="clockwise",
        rotation=90,
        pull=[0, 0.02, 0],
    ))
    fig.add_annotation(
        text=f"<b style='font-size:24px'>{fmt_currency(total)}</b><br><span style='font-size:12px;color:{C['muted']}'>ingresos</span>",
        x=0.5, y=0.5, showarrow=False, font=dict(family=FONT)
    )
    return _base_layout(fig, "Distribucion por Tamanio", height=420)


# ============================================================
# BAR: UNITS BY SIZE
# ============================================================
def bar_sizes(sizes_df):
    order = ["1/4 KG ($6,000)", "1/2 KG ($11,000)", "1 KG ($19,000)"]
    sizes_df = sizes_df.copy()
    sizes_df["_sort"] = sizes_df["PRICE_LABEL"].apply(lambda x: order.index(x) if x in order else 99)
    sizes_df = sizes_df.sort_values("_sort")

    fig = go.Figure(go.Bar(
        x=sizes_df["PRICE_LABEL"], y=sizes_df["sales"],
        marker=dict(
            color=[C["primary"], C["secondary"], C["tertiary"]],
            line=dict(width=0),
            opacity=0.9
        ),
        text=sizes_df["sales"].astype(str),
        textposition="outside", textfont=dict(size=14, family=FONT, color=C["text"]),
        hovertemplate="<b>%{x}</b><br>Unidades vendidas: %{y}<extra></extra>"
    ))
    return _base_layout(fig, "Unidades Vendidas por Tamanio", y_title="Unidades", height=360)


# ============================================================
# TOP FLAVORS - HORIZONTAL BAR
# ============================================================
def top_flavors(flavors_df):
    n = len(flavors_df)
    colors = _interpolate_colors("#0369a1", "#be123c", n)

    fig = go.Figure(go.Bar(
        y=flavors_df["PRODUCTOS"], x=flavors_df["count"],
        orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=flavors_df["count"].astype(str),
        textposition="outside", textfont=dict(size=11, family=FONT, color=C["text"]),
        hovertemplate="<b>%{y}</b><br>Registros: %{x}<extra></extra>"
    ))
    fig.update_layout(yaxis=dict(autorange="reversed", tickfont=dict(size=11, color=C["text"])))
    return _base_layout(fig, "Sabores Mas Populares", x_title="Cantidad de registros", height=600)


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
        line=dict(color=C["primary"], width=3, shape="spline", smoothing=0.6),
        marker=dict(size=9, color=C["primary"], line=dict(width=2, color=C["white"])),
        fill="tozeroy",
        fillcolor=f"rgba({_hex_to_rgb(C['primary'])}, 0.12)",
        hovertemplate="<b>%{x}:00 hs</b><br>Ingresos: $%{y:,.0f}<extra></extra>"
    ))
    fig.add_trace(go.Bar(
        x=hourly_df["HORA"], y=hourly_df["sales"],
        name="Ventas",
        yaxis="y2",
        marker=dict(color=C["secondary"], opacity=0.35, line=dict(width=0)),
        hovertemplate="<b>%{x}:00 hs</b><br>Ventas: %{y}<extra></extra>"
    ), secondary_y=True)
    fig.update_xaxes(tickmode="linear", dtick=1)
    fig.update_yaxes(title_text="Ingresos ($)", secondary_y=False, tickprefix="$")
    fig.update_yaxes(title_text="Cantidad de Ventas", secondary_y=True)
    return _base_layout(fig, "Ventas por Hora del Dia", x_title="Hora", height=400)


# ============================================================
# WEEKDAY BAR
# ============================================================
def sales_by_weekday(wd_df):
    colors = [C["primary"], C["primary"], C["secondary"], C["secondary"], C["tertiary"], C["quaternary"], C["quaternary"]]
    fig = go.Figure(go.Bar(
        x=wd_df["DIA_SEMANA"], y=wd_df["revenue"],
        marker=dict(color=colors, line=dict(width=0), opacity=0.9),
        text=[f"${v/1e6:.1f}M" for v in wd_df["revenue"]],
        textposition="outside", textfont=dict(size=11, family=FONT, color=C["text"]),
        hovertemplate="<b>%{x}</b><br>Ingresos: $%{y:,.0f}<extra></extra>"
    ))
    return _base_layout(fig, "Ingresos por Dia de la Semana", y_title="Ingresos ($)", height=360)


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
        colorscale=[(0, "#f3f4f6"), (0.35, "#fecdd3"), (0.7, C["primary"]), (1, "#4c0519")],
        hovertemplate="<b>%{y} %{x}:00 hs</b><br>Ingresos: $%{z:,.0f}<extra></extra>",
        colorbar=dict(
            title="Ingresos", tickprefix="$",
            title_font=dict(size=11, family=FONT),
            tickfont=dict(size=10),
            thickness=15, len=0.7
        ),
        xgap=2, ygap=2
    ))
    return _base_layout(fig, "Mapa de Calor: Dia vs Hora", x_title="Hora", y_title="Dia", height=420)


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
        line=dict(color=C["tertiary"], width=3),
        fill="tozeroy",
        fillcolor=f"rgba({_hex_to_rgb(C['tertiary'])}, 0.12)",
        name="Acumulado",
        hovertemplate="<b>%{x|%d %b %Y}</b><br>Acumulado: $%{y:,.0f}<extra></extra>"
    ))
    return _base_layout(fig, "Ingresos Acumulados", y_title="Acumulado ($)", height=400)


# ============================================================
# SCATTER: REVENUE VS SALES
# ============================================================
def scatter_rev_vs_sales(daily_df):
    fig = go.Figure(go.Scatter(
        x=daily_df["sales"], y=daily_df["revenue"],
        mode="markers",
        marker=dict(
            size=10, color=C["primary"], opacity=0.55,
            line=dict(color=C["white"], width=1.5)
        ),
        hovertemplate="<b>%{x} ventas</b><br>Ingresos: $%{y:,.0f}<extra></extra>",
        name="Dias"
    ))
    fig.add_hline(y=daily_df["revenue"].mean(), line_dash="dash", line_color=C["muted"], opacity=0.6,
                  annotation_text="Promedio", annotation_position="right")
    fig.add_vline(x=daily_df["sales"].mean(), line_dash="dash", line_color=C["muted"], opacity=0.6)
    return _base_layout(fig, "Relacion: Ventas vs Ingresos Diarios",
                        x_title="Cantidad de Ventas", y_title="Ingresos ($)", height=400)


# ============================================================
# FLAVOR TREEMAP
# ============================================================
def flavor_treemap(df_flavors):
    top = df_flavors.groupby("PRODUCTOS").size().reset_index(name="count")
    top = top.sort_values("count", ascending=False).head(10)
    colors = _interpolate_colors("#047857", "#be123c", len(top))
    fig = go.Figure(go.Treemap(
        labels=top["PRODUCTOS"],
        values=top["count"],
        parents=[""] * len(top),
        marker=dict(colors=colors, line=dict(color=C["white"], width=2)),
        textinfo="label+value",
        textfont=dict(size=13, family=FONT, color=C["white"]),
        hovertemplate="<b>%{label}</b><br>Registros: %{value}<extra></extra>",
        branchvalues="total",
    ))
    return _base_layout(fig, "Top 10 Sabores", height=420)


# ============================================================
# FLAVOR EVOLUTION LINE CHART
# ============================================================
def flavor_evolution(flavor_monthly):
    flavor_monthly = flavor_monthly.sort_values("MES_NAME")
    fig = go.Figure()
    products = flavor_monthly["PRODUCTOS"].unique()
    for idx, product in enumerate(products):
        sub = flavor_monthly[flavor_monthly["PRODUCTOS"] == product]
        color = CATEGORICAL[idx % len(CATEGORICAL)]
        fig.add_trace(go.Scatter(
            x=sub["MES_NAME"], y=sub["count"],
            mode="lines+markers",
            name=product,
            line=dict(color=color, width=2.5),
            marker=dict(size=6, color=color, line=dict(width=1, color=C["white"])),
            hovertemplate=f"<b>{product}</b><br>%{{x}}: %{{y}} registros<extra></extra>"
        ))
    return _base_layout(fig, "Evolucion Mensual del Top 10 Sabores",
                        x_title="Mes", y_title="Registros", height=440)


# ============================================================
# METRIC VALUE FORMATTERS
# ============================================================
def fmt_currency(v):
    """Format currency with K/M suffix, robust to locale."""
    if abs(v) >= 1e6:
        return f"${v/1e6:,.1f}M".replace(",", "X").replace(".", ",").replace("X", ".")
    elif abs(v) >= 1e5:
        return f"${v/1e3:,.0f}K".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"${v:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_number(v):
    if abs(v) >= 1e6:
        return f"{v/1e6:,.1f}M".replace(",", "X").replace(".", ",").replace("X", ".")
    # Show full number with thousands separator (Spanish) for counts < 100k
    return f"{v:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
