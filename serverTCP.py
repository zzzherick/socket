from forex_python.converter import CurrencyRates
import socket
import threading
import math

bind_ip = "localhost"
bind_port = 1234

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)
print("[*] Escutando %s:%d" %(bind_ip,bind_port))

valorDolar = CurrencyRates().get_rate('USD', 'BRL')
valorEuro = CurrencyRates().get_rate('EUR', 'BRL')

arredondar = True

def getValor(valor):
    start = False
    valor_final = ""

    for caracter in valor:
        if start:
            valor_final += caracter

        if caracter == ';':
            start = True

    return valor_final

def config(client_socket):
    print("\n---> Configuracao\n")
    msg = "\n1 DOLAR equivale a "+ str(valorDolar) +" REIAS\n1 EURO equivale a "+ str(valorEuro) +" REIAS"

    client_socket.send(msg)
    client_socket.close()

def configArredondar(info, client_socket):
    print("\n---> Arredondar\n")
    global arredondar

    if info:
        arredondar = True
        msg = "ATIVADO"
    else:
        arredondar = False
        msg = "DESATIVADO"

    msg = "\nARREDONDAR VALOR FOI "+ msg

    client_socket.send(msg)
    client_socket.close()

def dolarToReal(client_socket, request):
    print("\n---> Dolar para Real\n")

    valor = getValor(request)

    valor_final = (float(valor) * float(valorDolar))

    if arredondar:
        msg = "\n"+ valor +" DOLARES eh o equivalente a %.2f REAIS\n" % valor_final
    else:
        msg = "\n"+ valor +" DOLARES eh o equivalente a "+ str(valor_final) +" REAIS\n"
    
    client_socket.send(msg)
    client_socket.close()

def realToDolar(client_socket, request):
    print("\n---> Real para Dolar\n")
    
    valor = getValor(request)

    valor_final = (float(valor) / float(valorDolar))

    if arredondar:
        msg = "\n"+ valor +" REAIS eh o equivalente a %.2f DOLARES\n" % valor_final
    else:
        msg = "\n"+ valor +" REAIS eh o equivalente a "+ str(valor_final) +" DOLARES\n"

    client_socket.send(msg)
    client_socket.close()

def euroToReal(client_socket, request):
    print("\n---> Euro para Real\n")
    
    valor = getValor(request)

    valor_final = (float(valor) * float(valorEuro))

    if arredondar:
        msg = "\n"+ valor +" EUROS eh o equivalente a %.2f REAIS\n" % valor_final
    else:
        msg = "\n"+ valor +" EUROS eh o equivalente a "+ str(valor_final) +" REAIS\n"

    client_socket.send(msg)
    client_socket.close()            

def realToEuro(client_socket, request):
    print("\n---> Real para Euro\n")
    
    valor = getValor(request)

    valor_final = (float(valor) / float(valorEuro))

    if arredondar:
        msg = "\n"+ valor +" REAIS eh o equivalente a %.2f EUROS\n" % valor_final
    else:
        msg = "\n"+ valor +" REAIS eh o equivalente a "+ str(valor_final) +" EUROS\n"

    client_socket.send(msg)
    client_socket.close()

def encerrar(client_socket):
	client_socket.send("\n\nEncerrando conexao")
	client_socket.close()

def handle_client(client_socket):
	request = client_socket.recv(1024)
	
	print("\n[*] Recebido: %s" %request)
	print("\n-----------------\n")

	if request[0] == '1':
		dolarToReal(client_socket, request)
	elif request[0] == '2':
		realToDolar(client_socket, request)
	elif request[0] == '3':
		euroToReal(client_socket, request)
	elif request[0] == '4':
		realToEuro(client_socket, request)

	elif request == '5':
		config(client_socket)

	elif request.lower() == 'a':
		configArredondar(True, client_socket)
	elif request.lower() == 'd':
		configArredondar(False, client_socket)

	elif request.lower() == 'q':
		encerrar(client_socket)

while True:
	client, addr = server.accept()

	print("\n[*] Conexao aceita de: %s:%d" %(addr[0], addr[1]))

	client_handler = threading.Thread(target=handle_client, args=(client,))
	client_handler.start()