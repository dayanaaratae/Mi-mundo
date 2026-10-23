from datetime import datetime
from conexion_sheets import obtener_datos

# Cargar datos desde Google Sheets
datos = obtener_datos()

# ==========================================
#           DATOS DE SHEETS
# ==========================================


def parsear_fecha(fecha_str):
    """Auxiliar para convertir texto a objeto datetime probando distintos formatos."""
    if not fecha_str:
        return None
    formatos = ["%d/%m/%Y %H:%M:%S", "%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"]
    for fmt in formatos:
        try:
            return datetime.strptime(str(fecha_str).strip(), fmt)
        except ValueError:
            pass
    return None


def calcular_dias_solicitud(fila):
    """Calcula la cantidad total de días restando Fecha final menos Fecha inicio."""
    f_inicio_str = fila.get("Fecha inicio - 1ra Alternativa")
    f_fin_str = fila.get("Fecha final - 1ra Alternativa")

    fecha_inicio = parsear_fecha(f_inicio_str)
    fecha_fin = parsear_fecha(f_fin_str)

    if fecha_inicio and fecha_fin:
        # Sumamos 1 día para incluir el día de inicio completo
        dias = (fecha_fin - fecha_inicio).days + 1
        return max(dias, 0)

    return 0


def obtener_estado(fila):
    """Obtiene el estado de la solicitud o asigna 'Aprobado' por defecto."""
    estado = (
        fila.get("Estado")
        or fila.get("Estado de la solicitud")
        or fila.get("Columna 1")
    )
    if not estado or str(estado).strip() == "":
        return "Aprobado"
    return str(estado).strip()


# ==========================================
# PATRICK G.
# ==========================================


def obtener_top_empleados_mas_dias(datos, top_n=5):
    """Identifica a los N empleados con mayor cantidad total de días de vacaciones solicitados."""
    acumulado = {}
    for fila in datos:
        # Intenta armar el nombre con las columnas de Sheets o encabezados genéricos
        nombres = (fila.get("NOMBRES") or "").strip()
        paterno = (fila.get("APELLIDO PATERNO") or "").strip()
        materno = (fila.get("APELLIDO MATERNO") or "").strip()

        nombre_completo = f"{nombres} {paterno} {materno}".strip()

        empleado = (
            nombre_completo
            or fila.get("Nombre")
            or fila.get("Empleado")
            or fila.get("Nombre completo")
            or "Desconocido"
        )
        dias = calcular_dias_solicitud(fila)
        if empleado and empleado != "Desconocido":
            acumulado[empleado] = acumulado.get(empleado, 0) + dias

    # Ordena de mayor a menor según la cantidad de días
    empleados_ordenados = sorted(
        acumulado.items(), key=lambda item: item[1], reverse=True
    )
    return dict(empleados_ordenados[:top_n])


def promedio_dias_por_departamento(datos):
    """Calcula la cantidad promedio de días por solicitud en cada área/departamento."""
    conteo = {}
    suma_dias = {}

    for fila in datos:
        area = fila.get("Área", "Sin Área")
        dias = calcular_dias_solicitud(fila)
        if area:
            suma_dias[area] = suma_dias.get(area, 0) + dias
            conteo[area] = conteo.get(area, 0) + 1

    promedios = {}
    for area, total in suma_dias.items():
        promedios[area] = round(total / conteo[area], 2)

    return promedios


# ==========================================
# FERNANDO R.
# ==========================================


def contar_solicitudes_por_departamento(datos):
    """Cuenta cuántas solicitudes de vacaciones en total se han enviado agrupadas por área/departamento."""
    resultado = {}
    for fila in datos:
        area = fila.get("Área", "Sin Área")
        if area:
            resultado[area] = resultado.get(area, 0) + 1
    return resultado


def promedio_dias_por_estado(datos, estado="Aprobado"):
    """Calcula el promedio de días pedidos según el estado de la solicitud."""
    dias_filtrados = [
        calcular_dias_solicitud(fila)
        for fila in datos
        if obtener_estado(fila).lower() == str(estado).lower()
    ]
    if not dias_filtrados:
        return 0.0
    return sum(dias_filtrados) / len(dias_filtrados)


# ==========================================
# DAYANA A.
# ==========================================


def porcentaje_vacaciones_prolongadas(datos, dias_limite=10):
    """Calcula el porcentaje de solicitudes donde el empleado pide periodos iguales o mayores a 10 días."""
    if not datos:
        return 0.0

    prolongadas = sum(
        1 for fila in datos if calcular_dias_solicitud(fila) >= dias_limite
    )
    return (prolongadas / len(datos)) * 100


def porcentaje_solicitudes_por_estado(datos):
    """Genera un cálculo porcentual de las solicitudes según cada estado dentro de la base de datos."""
    if not datos:
        return {}

    total = len(datos)
    conteo = {}
    for fila in datos:
        est = obtener_estado(fila)
        conteo[est] = conteo.get(est, 0) + 1

    # Cálculo porcentual
    return {
        estado: round((cantidad / total) * 100, 2)
        for estado, cantidad in conteo.items()
    }


# ==========================================
# MOSTRAR RESULTADOS EN CONSOLA
# ==========================================
if __name__ == "__main__":
    print("==========================================")
    print("        PATRICK G.          ")
    print("==========================================")
    print("Top empleados con más días:", obtener_top_empleados_mas_dias(datos))
    print("Promedio días por departamento:", promedio_dias_por_departamento(datos))

    print("\n==========================================")
    print("          FERNANDO R.         ")
    print("==========================================")
    print(
        "Solicitudes por departamento:",
        contar_solicitudes_por_departamento(datos),
    )
    print(
        "Promedio de días (Aprobado):",
        round(promedio_dias_por_estado(datos, "Aprobado"), 2),
    )

    print("\n==========================================")
    print("             DAYANA A.          ")
    print("==========================================")
    print(
        "Porcentaje vacaciones prolongadas (>=10 días):",
        f"{round(porcentaje_vacaciones_prolongadas(datos), 2)}%",
    )
    print(
        "Porcentaje solicitudes por estado:",
        porcentaje_solicitudes_por_estado(datos),
    )