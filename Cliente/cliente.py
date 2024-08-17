import threading # Para poder usar multithreading
import socket # Para criar a conexão de rede

def main():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# Define o IPV4 e o TCP
    
    try:
        cliente.connect(('localhost', 7777))
    except:
        return print('\nNÃO FOI POSSIVEL SE CONECTAR\n')
    
    nome = input('SEU NOME: ')
    print('\nCONECTADO!!!')
    
    # Duas threads para que as duas funções rode ao mesmo tempo
    thread1 = threading.Thread(target=recebeMensagens, args=[cliente])
    thread2 = threading.Thread(target=enviaMensagens, args=[cliente, nome])
    
    #Executa as threads
    thread1.start()
    thread2.start()
    
def recebeMensagens(cliente): # É responsavel por RECEBER mensagens enviadas pelo SERVIDOR
    while True:
        try:
            msg = cliente.recv(2048).decode('utf-8')
            print(msg+'\n')
        except:
            print('\nNão foi possível permanecer conectado no servidor!\n')
            print('Pressione <Enter> Para continuar...')
            cliente.close()
            break

def enviaMensagens(cliente, nome):# É responsavel por ENVIAR mensagens para o SERVIDOR
    while True:
        try:
            msg = input('\n')
            cliente.send(f'<{nome}> {msg}'.encode('utf-8'))
        except:
            return
    
    
    
    
main()