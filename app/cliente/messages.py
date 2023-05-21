def carregar_msgs(username, usr_input_person, cliente):
    cliente.send(f"{username}%&-:%{usr_input_person}".encode('utf-8'))
    msgs = eval(cliente.recv(10240).decode('utf-8'))
    while msgs[0] != username:
        msgs = eval(cliente.recv(10240).decode('utf-8'))    
    del msgs[0]
    for mensagem in msgs:
        print(mensagem)