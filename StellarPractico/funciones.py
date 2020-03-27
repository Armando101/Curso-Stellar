from stellar_sdk.keypair import Keypair
from stellar_sdk import Server
from stellar_sdk.network import Network
from stellar_sdk.transaction_builder import TransactionBuilder
from stellar_sdk.exceptions import NotFoundError, BadResponseError, BadRequestError
import requests
import json


def crear_llaves():
	"""
	Todas las cuentas tienen una llave pública y una semilla secreta.
	Esta función genera las llaves
	"""
	llaves = {}
	pair = Keypair.random()

	llaves["privada"] = pair.secret
	llaves["publica"] = pair.public_key

	file = open("Llaves.txt", "a")
	file.write(str(llaves)+"\n")
	file.close()

	print("Llave pública: ", pair.public_key)
	print("Llave privada: ", pair.secret)

	return llaves

def crear_cuenta(public_key):
	"""
	Crea una cuenta haciendo una petición al friendbot de Stellar
	"""	
	response = requests.get(f"https://friendbot.stellar.org?addr={public_key}")

	if response.status_code == 200:
		print("Felicidades, ahora tienes una nueva cuenta ;) \n")
	else:
		print("Ocurrión un error :( tu cuenta no pudo ser creada")


def obtener_informacion(public_key):
	"""
	Obtenemos los detalles de la cuenta y verificamos el saldo
	"""
	server = Server("https://horizon-testnet.stellar.org")

	account = server.accounts().account_id(public_key).call()

	for balance in account['balances']:
		print("Tipo: ", balance['asset_type'], "\n Balance: ", balance['balance'])

# Enviar y recibir pagos

def enviar_pagos(llave_publica_origen, llave_publica_destino, pair, monto = "50", activo='XLM', nota="Primera transacción"):
	"""
	Esta función evia lumens
	"""
	server = Server("https://horizon-testnet.stellar.org")
	# Verificamor que la cuenta exista

	try:
		server.load_account(llave_publica_destino)
	except NotFoundError:
		raise Exception("No existe la cuenta de destino")

	source_account = server.load_account(llave_publica_origen)

	base_fee = server.fetch_base_fee()

	# Realizamos la transcción
	transaction = (
		TransactionBuilder(
				source_account = source_account, 
				network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
				base_fee=base_fee,
			)
		# Especificamos el tipo de asset a transaccionar
			.append_payment_op(destination = llave_publica_destino, amount=monto, asset_code=activo)
			# Indicamos una nota
			.add_text_memo(nota)
			.set_timeout(10)
			.build()
		)
	# Firmamos la transacción
	transaction.sign(pair)

	# Finalmente nvíamos la transacción

	try:
		response = server.submit_transaction(transaction)
		print("Response: ", response)
	except (BadResponseError, BadRequestError) as error:
		print("Ocurrió un error :(\n", error)

def cargar_llaves(archivo="Llaves.txt", posicion=1):
	file = open(archivo, "r")
	llaves = ''
	for i, linea in enumerate(file.readlines()):
		if i == posicion:
			break
		llaves =linea

	file.close()

	llaves_dict = json.loads(llaves)

	print("La llave pública es: ", llaves_dict['publica'], "\nLa llave privada es: ", llaves_dict['privada'])

	return llaves_dict
