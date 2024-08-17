import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
import threading
import socket

class ChatCliente:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Login")

        # Definir o tamanho da tela
        self.janela.geometry("400x400")

        # Definir o estilo geral da interface
        self.janela.configure(bg="#2c3e50")

        # Solicita o nome do usuário antes de mostrar o chat
        self.nome = simpledialog.askstring("Nome", "Digite seu nome:")

        if not self.nome:
            messagebox.showerror("Erro", "Nome é obrigatório!")
            self.janela.quit()  # Encerra o aplicativo se o nome não for fornecido
        else:
            self.iniciar_chat()

    def iniciar_chat(self):
        # Muda o título da janela após o login
        self.janela.title(f"Chat - {self.nome}")

        # Cabeçalho estilizado
        cabecalho = tk.Label(self.janela, text=f"Bem-vindo ao Chat, {self.nome}!", bg="#34495e", fg="#ecf0f1", font=("Arial", 14, "bold"), pady=10)
        cabecalho.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Área de exibição das mensagens
        self.chat_area = scrolledtext.ScrolledText(self.janela, wrap=tk.WORD, state='disabled', bg="#ecf0f1", fg="#2c3e50", font=("Arial", 12))
        self.chat_area.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Campo de entrada para envio de mensagens
        self.msg_entry = tk.Entry(self.janela, width=40, bg="#ecf0f1", fg="#2c3e50", font=("Arial", 12))
        self.msg_entry.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.msg_entry.bind("<Return>", self.envia_mensagem)

        # Botão para enviar mensagens
        self.send_button = tk.Button(self.janela, text="Enviar", command=self.envia_mensagem, bg="#1abc9c", fg="#ecf0f1", font=("Arial", 12, "bold"), activebackground="#16a085")
        self.send_button.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Configurações de conexão do cliente
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.cliente.connect(('localhost', 7777))
        except:
            self.adicionar_mensagem("NÃO FOI POSSÍVEL SE CONECTAR AO SERVIDOR")
            return

        self.adicionar_mensagem(f"Conectado como {self.nome}!")

        # Configura tags para alinhar o texto
        self.chat_area.tag_configure('right', justify='right')
        self.chat_area.tag_configure('left', justify='left')

        # Thread para receber mensagens
        thread_receber = threading.Thread(target=self.recebe_mensagens)
        thread_receber.daemon = True
        thread_receber.start()

        # Configura a grade para expandir os widgets corretamente
        self.janela.grid_rowconfigure(1, weight=1)
        self.janela.grid_columnconfigure(0, weight=1)
        self.janela.grid_columnconfigure(1, weight=0)

    def recebe_mensagens(self):
        while True:
            try:
                msg = self.cliente.recv(2048).decode('utf-8')
                self.adicionar_mensagem(msg)
            except:
                self.adicionar_mensagem("NÃO FOI POSSÍVEL PERMANECER CONECTADO NO SERVIDOR.")
                self.cliente.close()
                break

    def envia_mensagem(self, event=None):
        msg = self.msg_entry.get()
        if msg:
            formatted_msg = f'<{self.nome}> {msg}'
            self.cliente.send(formatted_msg.encode('utf-8'))
            self.msg_entry.delete(0, tk.END)

    def adicionar_mensagem(self, msg):
        self.chat_area.config(state='normal')

        # Checa se a mensagem foi enviada por este cliente
        if msg.startswith(f'<{self.nome}>'):
            # Substitui o nome do usuário por "Eu" para as mensagens enviadas
            msg = msg.replace(f'<{self.nome}>', 'Eu', 1)
            # Adiciona a mensagem alinhada à direita
            self.chat_area.insert(tk.END, msg + '\n', 'right')
        else:
            # Adiciona a mensagem alinhada à esquerda
            self.chat_area.insert(tk.END, msg + '\n', 'left')

        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)

if __name__ == "__main__":
    janela = tk.Tk()
    app = ChatCliente(janela)
    janela.mainloop()
