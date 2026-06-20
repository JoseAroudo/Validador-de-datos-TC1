from logger import Logger

from .validar_campos import (
    validar_niu, validar_cod_conexion, validar_tipo_c,
    validar_nivel_tension, validar_nivel_tension_prim, validar_porc_propiedad,
    validar_conex_red, validar_id_cx, validar_id_mercado, validar_grupo_calidad,
    validar_cod_frontera, validar_cod_circuito, validar_cod_trafo,
    validar_cod_dane, validar_ubicacion, validar_direccion, validar_cond_especiales,
    validar_tipo_area_esp, validar_cod_area_esp, validar_estrato, validar_altitud,
    validar_longitud, validar_latitud, validar_autogenerador, validar_exporta_energia,
    validar_capacidad_auto, validar_tipo_generacion, validar_cod_frontera_aut,
    validar_fecha_operacion, validar_contrato_respaldo, validar_capacidad_respaldo,
    validar_consistencias_multicampo
)

def validar_registro(campos: list[str], num_fila: int) -> tuple[str, int, int, dict[str, dict[str, int]]]:
    """Valida un registro completo y reporta errores.
    
    Retorna: (estado, num_errores, num_advertencias)
    """
    resumen_campos = {
        "Estructura de Fila": {"errores": 0, "advertencias": 0},
        "NIU": {"errores": 0, "advertencias": 0},
        "Cod Conexión": {"errores": 0, "advertencias": 0},
        "Tipo de C": {"errores": 0, "advertencias": 0},
        "Nivel de Tension": {"errores": 0, "advertencias": 0},
        "Nivel de Tension Primario": {"errores": 0, "advertencias": 0},
        "% propiedad": {"errores": 0, "advertencias": 0},
        "Conex de Red": {"errores": 0, "advertencias": 0},
        "ID CX": {"errores": 0, "advertencias": 0},
        "ID MERCADO": {"errores": 0, "advertencias": 0},
        "Grupo de Calidad": {"errores": 0, "advertencias": 0},
        "Cod frontera": {"errores": 0, "advertencias": 0},
        "Cod Circuito": {"errores": 0, "advertencias": 0},
        "Cod Trafo": {"errores": 0, "advertencias": 0},
        "Cod DANE": {"errores": 0, "advertencias": 0},
        "Ubicación": {"errores": 0, "advertencias": 0},
        "Dirección": {"errores": 0, "advertencias": 0},
        "Cond Especiales": {"errores": 0, "advertencias": 0},
        "Tipo de Area Esp": {"errores": 0, "advertencias": 0},
        "Cod Area Esp": {"errores": 0, "advertencias": 0},
        "Estrato": {"errores": 0, "advertencias": 0},
        "Altitud": {"errores": 0, "advertencias": 0},
        "Longitud": {"errores": 0, "advertencias": 0},
        "Latitud": {"errores": 0, "advertencias": 0},
        "Autogenerador": {"errores": 0, "advertencias": 0},
        "Exporta Energia": {"errores": 0, "advertencias": 0},
        "Capacidad Autogenerador": {"errores": 0, "advertencias": 0},
        "Tipo de generacion": {"errores": 0, "advertencias": 0},
        "Cod frontera Aut": {"errores": 0, "advertencias": 0},
        "Fecha entrada en operación": {"errores": 0, "advertencias": 0},
        "Contrato de respaldo": {"errores": 0, "advertencias": 0},
        "Capacidad respaldo": {"errores": 0, "advertencias": 0},
    }

    if len(campos) != 31:
        Logger.add_to_log("info", "\n" + "=" * 74)
        Logger.add_to_log("info", f"Fila {num_fila}: {campos}")
        Logger.add_to_log("error", f"❌ Fila {num_fila}: Número incorrecto de campos ({len(campos)}, esperados 31)")
        resumen_campos["Estructura de Fila"]["errores"] = 1
        return "error", 1, 0, resumen_campos
    
    errores = []
    advertencias = []
    
    # Validar cada campo usando tabla de validadores
    validadores = [
        (validar_niu, campos[0], "NIU"),
        (validar_cod_conexion, campos[1], "Cod Conexión"),
        (validar_tipo_c, campos[2], "Tipo de C"),
        (validar_nivel_tension, campos[3], "Nivel de Tension"),
        (validar_nivel_tension_prim, campos[4], "Nivel de Tension Primario"),
        (validar_porc_propiedad, campos[5], "% propiedad"),
        (validar_conex_red, campos[6], "Conex de Red"),
        (validar_id_cx, campos[7], "ID CX"),
        (validar_id_mercado, campos[8], "ID MERCADO"),
        (validar_grupo_calidad, campos[9], "Grupo de Calidad"),
        (validar_cod_frontera, campos[10], "Cod frontera"),
        (validar_cod_circuito, campos[11], "Cod Circuito"),
        (validar_cod_trafo, campos[12], "Cod Trafo"),
        (validar_cod_dane, campos[13], "Cod DANE"),
        (validar_ubicacion, campos[14], "Ubicación"),
        (validar_direccion, campos[15], "Dirección"),
        (validar_cond_especiales, campos[16], "Cond Especiales"),
        (validar_tipo_area_esp, campos[17], "Tipo de Area Esp"),
        (validar_cod_area_esp, campos[18], "Cod Area Esp"),
        (validar_estrato, campos[19], "Estrato"),
        (validar_altitud, campos[20], "Altitud"),
        (validar_longitud, campos[21], "Longitud"),
        (validar_latitud, campos[22], "Latitud"),
        (validar_autogenerador, campos[23], "Autogenerador"),
        (validar_exporta_energia, campos[24], "Exporta Energia"),
        (validar_capacidad_auto, campos[25], "Capacidad Autogenerador"),
        (validar_tipo_generacion, campos[26], "Tipo de generacion"),
        (validar_cod_frontera_aut, campos[27], "Cod frontera Aut"),
        (validar_fecha_operacion, campos[28], "Fecha entrada en operación"),
        (validar_contrato_respaldo, campos[29], "Contrato de respaldo"),
        (validar_capacidad_respaldo, campos[30], "Capacidad respaldo"),
    ]
    
    for validador, valor, nombre_campo in validadores:
        ok, msg = validador(valor)
        if ok == 2:  # Caso especial: warning (ej. Cod frontera sin "Frt")
            advertencias.append(msg)
            resumen_campos[nombre_campo]["advertencias"] += 1
        elif not ok:
            errores.append(msg)
            resumen_campos[nombre_campo]["errores"] += 1
    
    # Validar consistencias entre campos: cada advertencia se imputa a su campo destino
    advertencias_multicampo = validar_consistencias_multicampo(campos)
    for campo_destino, mensaje in advertencias_multicampo:
        advertencias.append(mensaje)
        resumen_campos[campo_destino]["advertencias"] += 1
    
    # Reportar resultado
    estado = "ok"
    if errores:
        Logger.add_to_log("info", "\n" + "=" * 74)
        Logger.add_to_log("info", f"Fila {num_fila}: {campos}")
        Logger.add_to_log("error", f"❌ Fila {num_fila}: {len(errores)} error(es)")

        if advertencias:
            Logger.add_to_log("info", f"⚠️ Fila {num_fila}: {len(advertencias)} advertencia(s)")
            for advertencia in advertencias:
                Logger.add_to_log("warn", f"   • {advertencia}")

        for error in errores:
            Logger.add_to_log("error", f"   • {error}")
        
        estado = "error_warning" if advertencias else "error"
    elif advertencias:
        Logger.add_to_log("info", "\n" + "=" * 74)
        Logger.add_to_log("info", f"Fila {num_fila}: {campos}")
        Logger.add_to_log("info", f"⚠️ Fila {num_fila}: {len(advertencias)} advertencia(s)")
        for advertencia in advertencias:
            Logger.add_to_log("warn", f"   • {advertencia}")
        estado = "warning"
    
    return estado, len(errores), len(advertencias), resumen_campos


def validar_archivo(lineas: list[str]) -> dict:
    """Procesa todos los registros del archivo y genera dos tipos de resumen.
    
    Args:
        lineas: Lista de líneas del archivo (incluyendo encabezado)
    
    Retorna: Dict con resumen de filas y resumen de errores/advertencias totales
    """
    filas_validas = 0
    filas_con_problemas = 0
    total_errores = 0
    total_advertencias = 0
    resumen_campos = {}
    
    # Procesar cada fila (saltar encabezado en índice 0)
    for i, linea in enumerate(lineas[1:], start=1):
        campos = linea.rstrip('\n').split(';')
        _, errores_fila, advertencias_fila, resumen_campos_fila = validar_registro(campos, i)
        
        total_errores += errores_fila
        total_advertencias += advertencias_fila

        for nombre_campo, conteos in resumen_campos_fila.items():
            if nombre_campo not in resumen_campos:
                resumen_campos[nombre_campo] = {"errores": 0, "advertencias": 0}
            resumen_campos[nombre_campo]["errores"] += conteos["errores"]
            resumen_campos[nombre_campo]["advertencias"] += conteos["advertencias"]
        
        if errores_fila == 0 and advertencias_fila == 0:
            filas_validas += 1
        else:
            filas_con_problemas += 1
    
    return {
        "resumen_filas": {
            "validas": filas_validas,
            "con_problemas": filas_con_problemas,
            "total": len(lineas) - 1,
        },
        "resumen_datos": {
            "total_errores": total_errores,
            "total_advertencias": total_advertencias,
            "total_registros": len(lineas) - 1,
        },
        "resumen_campos": resumen_campos,
    }
