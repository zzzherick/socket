import socket

target_host = "localhost"
target_port = 1234

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_host, target_port))

def escolherOpcao():

    print("-- Escolha uma opcao de conversao --\n")

    opcao = raw_input("DOLAR PARA REAL ----> 1\n"
        "REAL PARA DOLAR ----> 2\n"
        "EURO PARA REAL  ----> 3\n"
        "REAL PARA EURO  ----> 4\n\n"
        "CONFIGURACOES   ----> 5\n\n"
        "ARREDONDAR VALORES (ATIVAR[a] \ DESATIVAR[d])\n\n"
        "SAIR            ----> q\n\n")      

                                  
    if opcao == "1" or opcao == "2" or opcao == "3" or opcao == "4":
        valor = raw_input("\nInforme o valor: ")
        opcao = opcao + ";" + valor

    client.send(str(opcao))

    response = client.recv(4096)
    print(response)

escolherOpcao()