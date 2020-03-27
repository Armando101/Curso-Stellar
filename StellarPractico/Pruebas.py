import funciones
# Obtener las llaves
llaves = funciones.crear_llaves()

# Crear cuenta
funciones.crear_cuenta(llaves['publica'])

# Obtener información de la cuenta
funciones.obtener_informacion(llaves['publica'])
