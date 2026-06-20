from typing import Pattern
from datetime import datetime
from .regex_patterns import (
    Alfanum10, Alfanum11, Alfanum12, Alfanum150,
    num1_5, num8_exacto, num_positivo_4dig,
    decimal_longitud, decimal_longitud_corto, decimal_latitud,
    decimal_capacidad_auto, decimal_capacidad_respaldo, fecha_ddmmaaaa
)

# === CONJUNTOS DE VALORES VÁLIDOS ===
TIPO_C_VALIDO = {"1", "2"}
NIVEL_TENSION_VALIDO = {"1", "2", "3", "4"}
NIVEL_TENSION_PRIM_VALIDO = {"0", "2", "3"}
PORC_PROPIEDAD_VALIDO = {"0", "50", "100", "101"}
CONEX_RED_VALIDO = {"1", "2"}
ID_MERCADO_VALIDO = "176"
GRUPO_CALIDAD_VALIDO = {"11", "12", "13", "21", "22", "23", "31", "32", "33"}
UBICACION_VALIDO = {"1", "2", "3"}
COND_ESPECIALES_VALIDO = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"}
TIPO_AREA_ESP_VALIDO = "0"
COD_AREA_ESP_VALIDO = "0"
ESTRATO_VALIDO = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"}
AUTOGENERADOR_VALIDO = {"1", "2", "3"}
EXPORTA_ENERGIA_VALIDO = {"1", "2"}
TIPO_GENERACION_VALIDO = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"}
CONTRATO_RESPALDO_VALIDO = {"1", "2"}

# === FUNCIONES AUXILIARES ===

def _validar_requerido(valor: str, mensaje_vacio: str) -> tuple[bool, str]:
    """Valida que el campo no esté vacío."""
    if valor.strip() == "":
        return False, mensaje_vacio
    return True, ""


def _validar_con_regex(
    valor: str,
    patron: Pattern[str],
    mensaje_vacio: str,
    mensaje_invalido: str,
) -> tuple[bool, str]:
    """Valida un campo contra un patrón regex."""
    ok, msg = _validar_requerido(valor, mensaje_vacio)
    if not ok:
        return ok, msg
    if not patron.match(valor):
        return False, mensaje_invalido
    return True, ""

def _validar_latitud(
    valor: str,
    patron: Pattern[str],
    mensaje_vacio: str,
) -> tuple[bool | int, str]:
    """Valida un campo contra un patrón regex."""
    ok, msg = _validar_requerido(valor, mensaje_vacio)
    if not ok:
        return 1, ""
    if not patron.match(valor):
        return 0, f"Latitud inválido: '{valor}' (debe ser decimal negativo, formato -XX.XXXX a -XX.XXXXXXXXXXXXXXX, 4-15 decimales)"
    return True, ""


def _validar_en_conjunto(
    valor: str,
    valores_validos: set[str] | str,
    mensaje_vacio: str,
    mensaje_invalido: str,
) -> tuple[bool, str]:
    """Valida que el campo sea uno de los valores permitidos."""
    ok, msg = _validar_requerido(valor, mensaje_vacio)
    if not ok:
        return ok, msg
    if valor not in valores_validos:
        return False, mensaje_invalido
    return True, ""


def _validar_nullable_con_regex(
    valor: str,
    patron: Pattern[str],
    mensaje_invalido: str,
) -> tuple[bool, str]:
    """Valida un campo que puede ser nulo (vacío) o debe cumplir regex."""
    if valor.strip() == "":
        return True, ""
    if not patron.match(valor):
        return False, mensaje_invalido
    return True, ""


def _validar_nullable_en_conjunto(
    valor: str,
    valores_validos: set[str] | str,
    mensaje_invalido: str,
) -> tuple[bool, str]:
    """Valida un campo que puede ser nulo o debe ser uno de los valores permitidos."""
    if valor.strip() == "":
        return True, ""
    if valor not in valores_validos:
        return False, mensaje_invalido
    return True, ""


def _validar_fecha_valida(fecha_str: str) -> bool:
    """Verifica que la fecha dd-mm-aaaa sea válida y no sea futura."""
    try:
        dia, mes, anio = fecha_str.split('-')
        fecha = datetime(int(anio), int(mes), int(dia))
        if fecha > datetime.now():
            return False
        return True
    except (ValueError, IndexError):
        return False


# === FUNCIONES DE VALIDACIÓN POR CAMPO ===

# Campo 1: NIU
def validar_niu(valor: str) -> tuple[bool, str]:
    return _validar_con_regex(
        valor,
        Alfanum12,
        "NIU vacío",
        f"NIU inválido: '{valor}' (debe ser alfanumérico, hasta 12 caracteres)",
    )


# Campo 2: Cod Conexión
def validar_cod_conexion(valor: str) -> tuple[bool, str]:
    ok, msg = _validar_con_regex(
        valor,
        Alfanum10,
        "Cod Conexión vacío",
        f"Cod Conexión inválido: '{valor}' (debe ser alfanumérico, hasta 10 caracteres)",
    )
    if not ok:
        return ok, msg
    if " " in valor:
        return False, f"Cod Conexión no puede contener espacios: '{valor}'"
    return True, ""


# Campo 3: Tipo de C
def validar_tipo_c(valor: str) -> tuple[bool, str]:
    return _validar_en_conjunto(
        valor,
        TIPO_C_VALIDO,
        "Tipo de C vacío",
        f"Tipo de C inválido: '{valor}' (debe ser 1 o 2)",
    )


# Campo 4: Nivel de Tension
def validar_nivel_tension(valor: str) -> tuple[bool, str]:
    return _validar_en_conjunto(
        valor,
        NIVEL_TENSION_VALIDO,
        "Nivel de Tension vacío",
        f"Nivel de Tension inválido: '{valor}' (debe ser 1, 2, 3 o 4)",
    )


# Campo 5: Nivel de Tension Primario
def validar_nivel_tension_prim(valor: str) -> tuple[bool, str]:
    return _validar_en_conjunto(
        valor,
        NIVEL_TENSION_PRIM_VALIDO,
        "Nivel de Tension Primario vacío",
        f"Nivel de Tension Primario inválido: '{valor}' (debe ser 0, 2 o 3)",
    )


# Campo 6: % propiedad
def validar_porc_propiedad(valor: str) -> tuple[bool, str]:
    return _validar_en_conjunto(
        valor,
        PORC_PROPIEDAD_VALIDO,
        "% propiedad vacío",
        f"% propiedad inválido: '{valor}' (debe ser 0, 50, 100 o 101)",
    )


# Campo 7: Conex de Red
def validar_conex_red(valor: str) -> tuple[bool, str]:
    return _validar_en_conjunto(
        valor,
        CONEX_RED_VALIDO,
        "Conex de Red vacío",
        f"Conex de Red inválido: '{valor}' (debe ser 1 o 2)",
    )


# Campo 8: ID CX
def validar_id_cx(valor: str) -> tuple[bool, str]:
    return _validar_con_regex(
        valor,
        num1_5,
        "ID CX vacío",
        f"ID CX inválido: '{valor}' (debe ser numérico, hasta 5 dígitos)",
    )


# Campo 9: ID MERCADO
def validar_id_mercado(valor: str) -> tuple[bool, str]:
    ok, msg = _validar_requerido(valor, "ID MERCADO vacío")
    if not ok:
        return ok, msg
    if valor != ID_MERCADO_VALIDO:
        return False, f"ID MERCADO inválido: '{valor}' (debe ser 176)"
    return True, ""


# Campo 10: Grupo de Calidad
def validar_grupo_calidad(valor: str) -> tuple[bool, str]:
    return _validar_en_conjunto(
        valor,
        GRUPO_CALIDAD_VALIDO,
        "Grupo de Calidad vacío",
        f"Grupo de Calidad inválido: '{valor}' (valores permitidos: 11, 12, 13, 21, 22, 23, 31, 32, 33)",
    )


# Campo 11: Cod frontera
def validar_cod_frontera(valor: str) -> tuple[bool | int, str]:
    ok, msg = _validar_con_regex(
        valor,
        Alfanum12,
        "Cod frontera vacío",
        f"Cod frontera inválido: '{valor}' (debe ser alfanumérico, hasta 12 caracteres)",
    )
    if not ok:
        return ok, msg
    
    if " " in valor:
        return False, f"Cod frontera no puede contener espacios: '{valor}'"
    
    if not valor.startswith("Frt"):
        return 2, f"Cod frontera '{valor}' no inicia con 'Frt'"
    
    return True, ""


# Campo 12: Cod Circuito
def validar_cod_circuito(valor: str) -> tuple[bool, str]:
    return _validar_nullable_con_regex(
        valor,
        Alfanum10,
        f"Cod Circuito inválido: '{valor}' (debe ser alfanumérico, hasta 10 caracteres)",
    )


# Campo 13: Cod Trafo
def validar_cod_trafo(valor: str) -> tuple[bool, str]:
    ok, msg = _validar_nullable_con_regex(
        valor,
        Alfanum10,
        f"Cod Trafo inválido: '{valor}' (debe ser alfanumérico, hasta 10 caracteres)",
    )
    if not ok:
        return ok, msg
    if valor.strip() != "" and " " in valor:
        return False, f"Cod Trafo no puede contener espacios: '{valor}'"
    return True, ""


# Campo 14: Cod DANE
def validar_cod_dane(valor: str) -> tuple[bool, str]:
    return _validar_con_regex(
        valor,
        num8_exacto,
        "Cod DANE vacío",
        f"Cod DANE inválido: '{valor}' (debe ser numérico con exactamente 8 dígitos)",
    )


# Campo 15: Ubicación
def validar_ubicacion(valor: str) -> tuple[bool, str]:
    return _validar_en_conjunto(
        valor,
        UBICACION_VALIDO,
        "Ubicación vacío",
        f"Ubicación inválido: '{valor}' (debe ser 1, 2 o 3)",
    )


# Campo 16: Dirección
def validar_direccion(valor: str) -> tuple[bool, str]:
    return _validar_con_regex(
        valor,
        Alfanum150,
        "Dirección vacío",
        f"Dirección inválido: '{valor}' (debe ser alfanumérico, máximo 150 caracteres)",
    )


# Campo 17: Cond Especiales
def validar_cond_especiales(valor: str) -> tuple[bool, str]:
    return _validar_en_conjunto(
        valor,
        COND_ESPECIALES_VALIDO,
        "Cond Especiales vacío",
        f"Cond Especiales inválido: '{valor}' (debe ser 0-12)",
    )


# Campo 18: Tipo de Area Esp
def validar_tipo_area_esp(valor: str) -> tuple[bool, str]:
    ok, msg = _validar_requerido(valor, "Tipo de Area Esp vacío")
    if not ok:
        return ok, msg
    if valor != TIPO_AREA_ESP_VALIDO:
        return False, f"Tipo de Area Esp inválido: '{valor}' (debe ser 0)"
    return True, ""


# Campo 19: Cod Area Esp
def validar_cod_area_esp(valor: str) -> tuple[bool, str]:
    ok, msg = _validar_requerido(valor, "Cod Area Esp vacío")
    if not ok:
        return ok, msg
    if valor != COD_AREA_ESP_VALIDO:
        return False, f"Cod Area Esp inválido: '{valor}' (debe ser 0)"
    return True, ""


# Campo 20: Estrato
def validar_estrato(valor: str) -> tuple[bool, str]:
    return _validar_en_conjunto(
        valor,
        ESTRATO_VALIDO,
        "Estrato vacío",
        f"Estrato inválido: '{valor}' (debe ser 1-11)",
    )


# Campo 21: Altitud
def validar_altitud(valor: str) -> tuple[bool, str]:
    if valor.strip() == "":
        return 2, "El valor de Altitud está vacío, se recomienda completar"
    return _validar_nullable_con_regex(
        valor,
        num_positivo_4dig,
        f"Altitud inválido: '{valor}' (debe ser numérico positivo, hasta 4 dígitos)",
    )


# Campo 22: Longitud
def validar_longitud(valor: str) -> tuple[bool | int, str]:
    if valor.strip() == "":
        return 2, "El valor de Longitud está vacío, se recomienda completar"

    if not decimal_longitud.match(valor):
        # Decimal negativo válido pero con menos de 4 decimales: solo advertencia.
        if decimal_longitud_corto.match(valor):
            return 2, f"Longitud '{valor}' tiene menos de 4 decimales, se recomienda mayor precisión"
        return False, f"Longitud inválido: '{valor}' (debe ser decimal negativo, formato -XX.XXXX a -XX.XXXXXXXXXXXXXXX, 4-15 decimales)"

    try:
        longitud = float(valor)
        if longitud < -79.0425 or longitud > -66.84833333:
            return False, f"Longitud fuera de rango: '{valor}' (debe estar entre -79.0425 y -66.84833333)"
    except ValueError:
        return False, f"Longitud inválido: '{valor}' (no es un número decimal válido)"

    return True, ""


# Campo 23: Latitud
def validar_latitud(valor: str) -> tuple[bool, str]:
    if valor.strip() == "":
        return 2, "El campo Latitud está vacío, se recomienda completar"
    
    ok, msg = _validar_latitud(
        valor,
        decimal_latitud,
        "",
        #f"Latitud inválido: '{valor}' (debe ser decimal, formato 2 enteros + 4-15 decimales)",
    )
    if not ok:
        return ok, msg
    
    
    try:
        latitud = float(valor)
        if latitud < -4.208333333 or latitud > 12.44611111:
            return False, f"Latitud fuera de rango: '{valor}' (debe estar entre -4.208333333 y 12.44611111)"
    except ValueError:
        return False, f"Latitud inválido: '{valor}' (no es un número decimal válido)"
    
    return True, ""


# Campo 24: Autogenerador
def validar_autogenerador(valor: str) -> tuple[bool, str]:
    return _validar_en_conjunto(
        valor,
        AUTOGENERADOR_VALIDO,
        "Autogenerador vacío",
        f"Autogenerador inválido: '{valor}' (debe ser 1, 2 o 3)",
    )


# Campo 25: Exporta Energia
def validar_exporta_energia(valor: str) -> tuple[bool, str]:
    return _validar_nullable_en_conjunto(
        valor,
        EXPORTA_ENERGIA_VALIDO,
        f"Exporta Energia inválido: '{valor}' (debe ser 1, 2 o vacío)",
    )


# Campo 26: Capacidad Autogenerador
def validar_capacidad_auto(valor: str) -> tuple[bool, str]:
    return _validar_nullable_con_regex(
        valor,
        decimal_capacidad_auto,
        f"Capacidad Autogenerador inválido: '{valor}' (debe ser decimal, formato 8 enteros + 2 decimales)",
    )


# Campo 27: Tipo de generacion
def validar_tipo_generacion(valor: str) -> tuple[bool, str]:
    return _validar_nullable_en_conjunto(
        valor,
        TIPO_GENERACION_VALIDO,
        f"Tipo de generacion inválido: '{valor}' (debe ser 1-11 o vacío)",
    )


# Campo 28: Cod frontera Aut
def validar_cod_frontera_aut(valor: str) -> tuple[bool, str]:
    return _validar_nullable_con_regex(
        valor,
        Alfanum11,
        f"Cod frontera Aut inválido: '{valor}' (debe ser alfanumérico, hasta 11 caracteres)",
    )


# Campo 29: Fecha entrada en operación
def validar_fecha_operacion(valor: str) -> tuple[bool, str]:
    if valor.strip() == "":
        return True, ""
    
    ok, msg = _validar_con_regex(
        valor,
        fecha_ddmmaaaa,
        "",
        f"Fecha entrada en operación inválido: '{valor}' (debe ser dd-mm-aaaa)",
    )
    if not ok:
        return ok, msg
    
    if not _validar_fecha_valida(valor):
        return False, f"Fecha entrada en operación inválido: '{valor}' (fecha no válida o es futura)"
    
    return True, ""


# Campo 30: Contrato de respaldo
def validar_contrato_respaldo(valor: str) -> tuple[bool, str]:
    return _validar_nullable_en_conjunto(
        valor,
        CONTRATO_RESPALDO_VALIDO,
        f"Contrato de respaldo inválido: '{valor}' (debe ser 1, 2 o vacío)",
    )


# Campo 31: Capacidad respaldo
def validar_capacidad_respaldo(valor: str) -> tuple[bool, str]:
    return _validar_nullable_con_regex(
        valor,
        decimal_capacidad_respaldo,
        f"Capacidad respaldo inválido: '{valor}' (debe ser decimal positivo, formato 8 enteros y 2 decimales)",
    )


# === REGLAS CONDICIONALES (CROSS-FIELD) ===

def validar_consistencias_multicampo(campos: list[str]) -> list[tuple[str, str]]:
    """
    Valida las reglas condicionales entre múltiples campos.
    Retorna una lista de tuplas (campo_destino, advertencia), donde campo_destino
    es el nombre del campo al que se imputa la advertencia en el resumen por campo.

    Campos indexados (0-based):
    [0] NIU
    [1] Cod Conexión
    [2] Tipo de Conexión
    [3] Nivel de Tension (secundaria)
    [4] Nivel de Tension Primario
    [5] % propiedad
    [6] Conex de Red
    [7] ID CX
    [8] ID MERCADO
    [9] Grupo de Calidad
    [10] Cod frontera
    [11] Cod Circuito
    [12] Cod Trafo
    [13] Cod DANE
    [14] Ubicación
    [15] Dirección
    [16] Condiciones Especiales
    [17] Tipo de Area Especial
    [18] Cod Area Especial
    [19] Estrato
    [20] Altitud
    [21] Longitud
    [22] Latitud
    [23] Autogenerador
    [24] Exporta Energia
    [25] Capacidad Autogenerador
    [26] Tipo de generacion
    [27] Cod frontera Autogeneración
    [28] Fecha entrada en operación
    [29] Contrato de respaldo
    [30] Capacidad respaldo
    """
    advertencias: list[tuple[str, str]] = []

    # Regla 1: Campo 5 (Nivel Tension Primario) depende de Campo 4 (Nivel Tension)
    nivel_sec = campos[3]
    nivel_prim = campos[4]

    if nivel_sec == "1":
        if nivel_prim not in ("2", "3"):
            advertencias.append((
                "Nivel de Tension Primario",
                f"Si Nivel de Tension (secundaria) = 1, entonces Nivel de Tension Primario debe ser 2 o 3, pero es '{nivel_prim}'",
            ))
    else:
        if nivel_prim != "0":
            advertencias.append((
                "Nivel de Tension Primario",
                f"Si Nivel de Tension (secundaria) = {nivel_sec}, entonces Nivel de Tension Primario debe ser 0, pero es '{nivel_prim}'",
            ))

    # Regla 2: Campo 12 (Cod Circuito) condicional a Campo 3 (Tipo de C)
    tipo_c = campos[2]
    cod_circuito = campos[11].strip()
    cod_conexion = campos[1]

    if tipo_c == "1":
        if cod_circuito == "":
            advertencias.append((
                "Cod Circuito",
                "Si Tipo de conexión = 1, entonces Cod Circuito no puede ser nulo",
            ))
        elif cod_circuito != cod_conexion:
            advertencias.append((
                "Cod Circuito",
                f"Si Tipo de conexión = 1, entonces Cod Circuito debe ser igual a Cod Conexión ('{cod_conexion}'), pero es '{cod_circuito}'",
            ))

    # Regla 3: Campo 13 (Cod Trafo) condicional a Campo 3 (Tipo de C)
    cod_trafo = campos[12].strip()

    if tipo_c == "2":
        if cod_trafo == "":
            advertencias.append((
                "Cod Trafo",
                "Si Tipo de conexión = 2, entonces Cod Trafo no puede ser nulo",
            ))
        elif cod_trafo != cod_conexion:
            advertencias.append((
                "Cod Trafo",
                f"Si Tipo de conexión = 2, entonces Cod Trafo debe ser igual a Cod Conexión ('{cod_conexion}'), pero es '{cod_trafo}'",
            ))

    # Regla 4: Campos 25-31 (Exporta Energia, Capacidad Auto, Tipo Generacion, etc.) deben ser nulos si Autogenerador = 3
    autogenerador = campos[23]

    if autogenerador == "3":
        campos_autogen = [
            ("Exporta Energia", campos[24]),
            ("Capacidad Autogenerador", campos[25]),
            ("Tipo de generacion", campos[26]),
            ("Cod frontera Aut", campos[27]),
            ("Fecha entrada en operación", campos[28]),
            ("Contrato de respaldo", campos[29]),
            ("Capacidad respaldo", campos[30]),
        ]
        for nombre_campo, valor in campos_autogen:
            if valor.strip() != "":
                advertencias.append((
                    nombre_campo,
                    f"Si Autogenerador = 3, entonces {nombre_campo} debe ser nulo, pero tiene valor '{valor}'",
                ))

    # Regla 5: Campo 31 (Capacidad respaldo) debe ser nulo si Campo 30 (Contrato respaldo) = 2
    contrato_respaldo = campos[29].strip()
    capacidad_respaldo = campos[30].strip()

    if contrato_respaldo == "2":
        if capacidad_respaldo != "":
            advertencias.append((
                "Capacidad respaldo",
                f"Si Contrato de respaldo = 2, entonces Capacidad respaldo debe ser nulo, pero tiene valor '{capacidad_respaldo}'",
            ))

    return advertencias
