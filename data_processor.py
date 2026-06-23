import pandas as pd
import re
from pathlib import Path

HELADERIA_COLORS = {
    "primary": "#E8A0BF",
    "secondary": "#BA90C6",
    "accent": "#C0DBEA",
    "chocolate": "#8B5E3C",
    "mint": "#7EC8A6",
    "strawberry": "#FF8BA7",
    "vanilla": "#FFF5E1",
    "dark": "#4A3B42",
    "bg": "#FFF8F0",
    "chart_colors": [
        "#E8A0BF", "#BA90C6", "#C0DBEA", "#8B5E3C", "#7EC8A6",
        "#FF8BA7", "#F4A261", "#A8DADC", "#E5989B", "#B5838D",
        "#6D6875", "#FFB4A2", "#9D8189", "#457B9D", "#2A9D8F",
        "#E76F51", "#F4A261", "#E9C46A", "#264653", "#A8DADC",
        "#FFB4A2", "#9D8189", "#457B9D", "#2A9D8F", "#E76F51",
        "#F4A261", "#E9C46A", "#6D6875", "#B5838D", "#E5989B",
        "#FF8BA7", "#A8DADC", "#8B5E3C", "#BA90C6", "#E8A0BF",
        "#7EC8A6", "#C0DBEA", "#264653", "#FFB4A2", "#E5989B"
    ]
}


def load_and_clean(filepath):
    """
    Load the Excel file, clean and transform the data.
    Returns: df_sales (size rows with prices), df_flavors (flavor rows), df_full (all valid)
    """
    df = pd.read_excel(filepath, sheet_name="Hoja 1")
    df = df.dropna(how="all").copy()
    df = df.dropna(subset=["FECHA"]).copy()

    # Clean PRECIO DE VENTA
    df["PRECIO_CLEAN"] = df["PRECIO DE VENTA"].apply(_clean_price)
    df["Cantidad vendida"] = df["Cantidad vendida"].fillna(1).astype(int)

    # Classify row type
    SIZE_KEYWORDS = ["1/4 KG", "1/2 KG", "1KG"]
    df["IS_SALE"] = df["PRODUCTOS"].isin(SIZE_KEYWORDS)

    # Sales df: rows with actual prices
    df_sales = df[df["IS_SALE"]].copy()
    df_sales["REVENUE"] = df_sales["PRECIO_CLEAN"] * df_sales["Cantidad vendida"]
    df_sales["PRICE_LABEL"] = df_sales["PRODUCTOS"].map({
        "1/4 KG": "1/4 KG ($6,000)",
        "1/2 KG": "1/2 KG ($11,000)",
        "1 KG": "1 KG ($19,000)"
    })

    # Flavor df: flavor tracking rows (no price)
    df_flavors = df[~df["IS_SALE"]].copy()
    df_flavors = df_flavors.dropna(subset=["PRODUCTOS"])

    # Date features for both
    for d in [df_sales, df_flavors]:
        d["FECHA"] = pd.to_datetime(d["FECHA"])
        d["MES"] = d["FECHA"].dt.to_period("M").astype(str)
        d["MES_NAME"] = d["FECHA"].dt.strftime("%b %Y")
        _dias = {0: "Lunes", 1: "Martes", 2: "Miercoles", 3: "Jueves", 4: "Viernes", 5: "Sabado", 6: "Domingo"}
        d["DIA_SEMANA"] = d["FECHA"].dt.dayofweek.map(_dias)
        d["DIA_SEMANA_NUM"] = d["FECHA"].dt.dayofweek
        d["HORA"] = d["HORARIO"].apply(lambda x: x.hour if pd.notna(x) else None)
        d["DIA"] = d["FECHA"].dt.date

    return df_sales, df_flavors


def _clean_price(x):
    if isinstance(x, str):
        return float(re.sub(r"[^\d.]", "", x))
    return float(x)


def get_kpi_metrics(df_sales):
    total_revenue = df_sales["REVENUE"].sum()
    total_sales = len(df_sales)
    avg_daily_rev = df_sales.groupby("DIA")["REVENUE"].sum().mean()
    unique_days = df_sales["DIA"].nunique()
    avg_ticket = total_revenue / total_sales
    best_month = df_sales.groupby("MES_NAME")["REVENUE"].sum().idxmax()
    best_month_rev = df_sales.groupby("MES_NAME")["REVENUE"].sum().max()

    return {
        "total_revenue": total_revenue,
        "total_sales": total_sales,
        "avg_daily_revenue": avg_daily_rev,
        "unique_days": unique_days,
        "avg_ticket": avg_ticket,
        "best_month": best_month,
        "best_month_rev": best_month_rev,
        "unique_flavors": 52
    }


def get_sales_by_month(df_sales):
    monthly = df_sales.groupby("MES_NAME").agg(
        revenue=("REVENUE", "sum"),
        sales=("REVENUE", "count"),
        avg_ticket=("REVENUE", "mean")
    ).reset_index()
    monthly = monthly.sort_values("MES_NAME")
    monthly["cumulative_revenue"] = monthly["revenue"].cumsum()
    return monthly


def get_sales_by_day(df_sales):
    daily = df_sales.groupby("DIA").agg(
        revenue=("REVENUE", "sum"),
        sales=("REVENUE", "count")
    ).reset_index()
    daily["DIA"] = pd.to_datetime(daily["DIA"])
    return daily.sort_values("DIA")


def get_sales_by_hour(df_sales):
    hourly = df_sales.groupby("HORA").agg(
        revenue=("REVENUE", "sum"),
        sales=("REVENUE", "count"),
        avg_ticket=("REVENUE", "mean")
    ).reset_index()
    return hourly.sort_values("HORA")


def get_sales_by_weekday(df_sales):
    weekday_order = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
    wd = df_sales.groupby(["DIA_SEMANA", "DIA_SEMANA_NUM"]).agg(
        revenue=("REVENUE", "sum"),
        sales=("REVENUE", "count")
    ).reset_index()
    wd["DIA_SEMANA"] = pd.Categorical(wd["DIA_SEMANA"], categories=weekday_order, ordered=True)
    return wd.sort_values("DIA_SEMANA")


def get_sales_by_size(df_sales):
    sizes = df_sales.groupby("PRICE_LABEL").agg(
        revenue=("REVENUE", "sum"),
        sales=("REVENUE", "count"),
        pct=("REVENUE", lambda x: x.sum() / df_sales["REVENUE"].sum() * 100)
    ).reset_index()
    return sizes


def get_top_flavors(df_flavors, top_n=25):
    flavors = df_flavors.groupby("PRODUCTOS").size().reset_index(name="count")
    flavors = flavors.sort_values("count", ascending=True).tail(top_n)
    return flavors


def get_flavor_seasonality(df_flavors):
    flavors = df_flavors.groupby(["MES_NAME", "PRODUCTOS"]).size().reset_index(name="count")
    return flavors
