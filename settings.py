# @author: Charles Tim Batista Garrocho
# @contact: ctgarrocho@gmail.com
# @copyright: (C) 2012-2012 Python Software Open Source

# Host (Ip do Servidor), PORTA (Porta do Servidor)
HOST = 'localhost'
PORTA = 3333

# Servidores de E-mail
SERVIDORES = dict([('hotmail', 'smtp.live.com'), ('live', 'smtp.live.com'), ('yahoo', 'smtp.mail.yahoo.fr'), ('gmail', 'smtp.gmail.com')])

# Status do Monitoramento
LIGADO = '0'
EXECUTANDO = '1'
PAUSADO = '2'

# Tipos de Requisicoes do Cliente
STATUS = '0'
INICIAR = '1'
PAUSAR = '2'
IMAGEM = '3'
DESLIGAR = '4'
CONFIGURAR = '5'

# Tipos de Respostas do Servidor
OK_200 = '0'
NAO_AUTORIZADO_401 = '1'
