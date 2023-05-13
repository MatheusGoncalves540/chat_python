# Aqui sera colocado o codigo que recebe e envia os dados como servidor
# Aqui você também chama a funcao que armazena no banco que está dentro de db/model/chat


# Aqui você irá chamar a funcao adicional 

# Toda mensagem recebida passa por uma funcao de analise
#   - Se a mensagem for "/getall" deve trazer todo o historico
    # - Se a mensagem for "/getall numero" exemplo /getall 100 -> deve trazer as ultimas 100 mensagens


from app.functions.logger import console

def server():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('localhost', 8080))

    servidor.listen()
    cliente, end = servidor.accept()

    username = "SERVER"


def startServer():
    server()
    while True:
        msg = json.loads(cliente.recv(10240).decode('utf-8'))
        console(f"{msg['name']}: {msg['msg']}, Horário: {msg['hora']}")
        console(datetime.datetime.strptime(msg['hora'],'%Y-%m-%d %H:%M:%S.%f'))
        addClientMessage(msg)
        valmsg = validateClient(msg)
        if valmsg.action == true:
            server_input = valmsg.result
        else:
            #enviando msg pro cliente
            server_input = input('Resposta: ')
            
        msg_env = '{' + f''' "name":"{username}",
                "msg":"{server_input}",
                "hora":"{datetime.datetime.now()}"
                ''' + '}'
        cliente.send(msg_env.encode('utf-8'))
        addServerMessage(msg_env)