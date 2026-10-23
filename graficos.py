import matplotlib.pyplot as plt
from analisis import agrupar_por_producto, calcular_ventas, contar_registros
from conexion_sheets import obtener_datos

datos = obtener_datos()
resumen = agrupar_por_producto(datos)
total_reg = contar_registros(datos)
total_ven = calcular_ventas(datos)

productos = list(resumen.keys())
cantidades = list(resumen.values())
colores = ["#3B82F6", "#10B981", "#F59E0B", "#8B5CF6"]

# 1. PRIMER GRÁFICO: BARRAS
plt.figure(figsize=(7, 4))
plt.bar(
    productos, cantidades, color=colores[: len(productos)], edgecolor="black"
)

plt.title("1. Unidades Vendidas por Producto", fontsize=14, fontweight="bold")
plt.xlabel("Producto")
plt.ylabel("Unidades Vendidas")
plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.show()

# 2. SEGUNDO GRÁFICO: DONA
plt.figure(figsize=(6, 6))
plt.pie(
    cantidades,
    labels=productos,
    autopct="%1.1f%%",
    startangle=140,
    colors=colores[: len(productos)],
)

circulo_centro = plt.Circle((0, 0), 0.60, fc="white")
fig = plt.gcf()
fig.gca().add_artist(circulo_centro)

plt.title("2. Distribución Porcentual (%)", fontsize=14, fontweight="bold")

plt.tight_layout()
plt.show()

# 3. TERCER GRÁFICO: TARJETA DE MÉTRICAS (KPIs)
plt.figure(figsize=(5, 4))
plt.axis("off")

texto_kpi = (
    "MÉTRICAS CLAVE\n\n"
    f"• Total Registros: {total_reg}\n\n"
    f"• Total Unidades: {sum(cantidades)}\n\n"
    f"• Ventas Totales: S/ {total_ven:,.2f}"
)

plt.text(
    0.1,
    0.5,
    texto_kpi,
    fontsize=13,
    verticalalignment="center",
    bbox=dict(
        boxstyle="round,pad=1.2", facecolor="#EBF3F9", edgecolor="#3B82F6"
    ),
)

plt.title("3. Resumen General", fontsize=14, fontweight="bold")

plt.tight_layout()
plt.show()