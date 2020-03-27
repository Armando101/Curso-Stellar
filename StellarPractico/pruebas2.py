import funciones
from stellar_sdk.keypair import Keypair

# Declaramos las llaves
llaves = funciones.cargar_llaves()

# Obtenemos información de la cuenta
funciones.obtener_informacion(llaves['publica'])

llave_destino = 'GCC5CSSNWMHRV2SPV6UV4LZ3FF2LSDQVKF775ZDIOAVA3XIQVIJR3JCJ'

# declaramos la llave secreta
source_secret_key = llaves['privada']

# Generamos la llave secreta
source_keypair = Keypair.from_secret(source_secret_key)

funciones.enviar_pagos(llaves['publica'], llave_destino, source_keypair, nota='Armando to Memo')

print()
print()
print()

funciones.obtener_informacion(llave_destino)
print()
print()
print()
funciones.obtener_informacion(llaves['publica'])

