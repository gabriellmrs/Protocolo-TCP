import threading # Para poder usar multithreading
import socket # Para criar a conexão de rede

clientes = []

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# Define o IPV4 e o TCP
    
    try:
        server.bind(('localhost', 7777)) # Ligar servidor
        server.listen() # Receber conexões
    except:
        return print('\nNÃO FOI POSSIVEL INICICAR O SERVIDOR!!!!\n')
    
    while True: # Vai ficar sempre aceitando conexões
        cliente, endereco = server.accept()
        clientes.append(cliente) # Vai adicionar o cliente na lista
        
        thread = threading.Thread(target=tratamentoMensagens, args=[cliente])
        thread.start()

# Vai tratar de receber a mensagem de cada usuario
def tratamentoMensagens(cliente):
    while True:
        try:
            msg = cliente.recv(2048)
            broadcast(msg)
            
        except:
            removeCliente(cliente)
            break

# Vai transmitir a mensagem para todos os outros usuarios
def broadcast(msg):
    for clienteItem in clientes:
        #if clienteItem != cliente:
            try:
                clienteItem.send(msg)
            except:
                removeCliente(clienteItem)
    
# Remove o cliente caso ele seja desconectado 
def removeCliente(cliente):
    clientes.remove(cliente)
    
    
    
main()