import base64
from io import BytesIO

from flask import Flask, render_template
import matplotlib

matplotlib.use("Agg")  # Evita que se abran ventanas emergentes de Matplotlib
import matplotlib.pyplot as plt

# Importar las funciones reales de tu archivo analisis.py
from analisis import (
    agrupar_dias_por_departamento,
    agrupar_solicitudes_por_estado,
    contar_solicitudes_por_departamento,
    contar_solicitudes_por_estado,
    contar_vacaciones_prolongadas,
    datos,
    promedio_dias_por_estado,
)

app = Flask(__name__)


def fig_to_base64(fig):
    """Convierte la figura de Matplotlib a una imagen en Base64 para HTML."""
    img = BytesIO()
    fig.savefig(img, format="png", bbox_inches="tight")
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode("utf-8")


@app.route("/")
def dashboard():
    # 1. Obtener métricas para tarjetas (KPIs)
    aprobados = contar_solicitudes_por_estado(datos, "Aprobado")
    prolongadas = contar_vacaciones_prolongadas(datos, 10)
    promedio_dias = round(promedio_dias_por_estado(datos, "Aprobado"), 1)

    # 2. GRÁFICO 1: Días de vacaciones solicitados por Área (Barras)
    dias_area = agrupar_dias_por_departamento(datos)
    areas = list(dias_area.keys())
    dias = list(dias_area.values())

    fig1, ax1 = plt.subplots(figsize=(6, 4))
    colores_barras = ["#3B82F6", "#10B981", "#F59E0B", "#8B5CF6", "#EC4899"]
    ax1.bar(
        areas,
        dias,
        color=colores_barras[: len(areas)],
        edgecolor="#1E293B",
        linewidth=0.8,
    )
    ax1.set_title(
        "Días Solicitados por Área", fontsize=13, fontweight="bold", pad=12
    )
    ax1.set_xlabel("Área / Departamento", fontsize=10)
    ax1.set_ylabel("Total Días", fontsize=10)
    ax1.grid(axis="y", linestyle="--", alpha=0.4)
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    grafico_barras = fig_to_base64(fig1)
    plt.close(fig1)

    # 3. GRÁFICO 2: Distribución por Estado de Solicitud (Dona)
    estados_dict = agrupar_solicitudes_por_estado(datos)
    estados = list(estados_dict.keys())
    cantidades = list(estados_dict.values())

    fig2, ax2 = plt.subplots(figsize=(5, 5))
    colores_dona = ["#10B981", "#F59E0B", "#EF4444", "#6B7280"]
    ax2.pie(
        cantidades,
        labels=estados,
        autopct="%1.1f%%",
        startangle=140,
        colors=colores_dona[: len(estados)],
        wedgeprops=dict(width=0.4, edgecolor="w"),
    )
    ax2.set_title(
        "Distribución por Estado", fontsize=13, fontweight="bold", pad=12
    )
    plt.tight_layout()
    grafico_dona = fig_to_base64(fig2)
    plt.close(fig2)

    return render_template(
        "dashboard.html",
        aprobados=aprobados,
        prolongadas=prolongadas,
        promedio_dias=promedio_dias,
        grafico_barras=grafico_barras,
        grafico_dona=grafico_dona,
    )


if __name__ == "__main__":
    app.run(debug=True)