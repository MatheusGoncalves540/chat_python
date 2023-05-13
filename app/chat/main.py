# Aqui você irá colocar funcionalidades adicional
# Funcao para ser criada, mostrar todo o historico de conversa armazenada



def validateClient(content):
    content.action = false
    if content['msg'].startswith('/getall'):
        content.action = true
        # VERIFICA SE E EXATAMENTO GETALL E DEVOLVE TUDO
        # SE NAO DA SPLIT E PEGA QUANTIDADE DE LINHRAS E DEVOLVE LINHAS

        # TRAZ TODAS AS MENSAGENS E DEVOLVE PRO CLIENT



        #FINAL CONTENT.result = dados
    return content
