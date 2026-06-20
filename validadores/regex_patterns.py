import re

# Compilar regex una sola vez

# === ALFANUMÉRICOS ===
Alfanum10 = re.compile(r'^[A-Za-z0-9]{1,10}$')  # Cod Conexión, Cod Circuito, Cod Trafo
Alfanum11 = re.compile(r'^[A-Za-z0-9]{1,11}$')  # Cod Frontera Aut
Alfanum12 = re.compile(r'^[A-Za-z0-9]{1,12}$')  # NIU, Cod Frontera (genérico)
Alfanum150 = re.compile(r'^[A-Za-z0-9\-\s]{1,150}$')  # Dirección (permite guiones y espacios)

# === NUMÉRICOS ENTEROS ===
num1_5 = re.compile(r'^\d{1,5}$')  # ID CX (hasta 5 dígitos)
num8_exacto = re.compile(r'^\d{8}$')  # Cod DANE (8 dígitos exactos)
num1_3 = re.compile(r'^\d{1,3}$')  # Ubicación, Cond Especiales, etc.
num_positivo_4dig = re.compile(r'^\d{1,4}$')  # Altitud (positivo, hasta 4 dígitos)

# === DECIMALES ===
# Longitud: formato -XX.XXXX a -XX.XXXXXXXXXXXXXXX (2 enteros, 4-15 decimales, negativo)
decimal_longitud = re.compile(r'^-\d{2}\.\d{4,15}$')

# Latitud: formato -XX.XXXX a XX.XXXXXXXXXXXXXXX (2 enteros, 4-15 decimales, positivo o negativo)
decimal_latitud = re.compile(r'^-?\d{1,2}\.\d{4,15}$')

# Capacidad Autogenerador: 8 enteros + 2 decimales
decimal_capacidad_auto = re.compile(r'^\d{1,8}\.\d{2}$')

# Capacidad Respaldo: 8 enteros + 2 decimales Positivos
decimal_capacidad_respaldo = re.compile(r'^\d{1,8}\.\d{2}$')

# === FECHAS ===
# Formato dd-mm-aaaa
fecha_ddmmaaaa = re.compile(r'^\d{2}-\d{2}-\d{4}$')