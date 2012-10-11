# @author: Charles Tim Batista Garrocho
# @contact: ctgarrocho@gmail.com
# @copyright: (C) 2012-2012 Python Software Open Source

# Host (Ip do Servidor), PORTA (Porta do Servidor)
HOST = 'localhost'
PORTA = 3335

# Defina aqui o estado inicial do monitoramento.
DETECTOR = True

# Defina aqui o intervalo de verificacao do monitoramento.
INTERVALO = 10 

# Defina aqui o email do administrador da sala de monitoramento.
EMAIL = 'ctgarrocho@gmail.com'

# Servidores de E-mail
SERVIDORES = dict([('hotmail', 'smtp.live.com'), ('live', 'smtp.live.com'), ('yahoo', 'smtp.mail.yahoo.fr'), ('gmail', 'smtp.gmail.com')])

# Tipo de Mensagem de Status do Monitoramento. Nao alterar.
LIGADO = '0'
EXECUTANDO = '1'
PAUSADO = '2'

# Tipos de Requisicoes do Cliente. Nao alterar.
STATUS = '0'
INICIAR = '1'
PAUSAR = '2'
IMAGEM = '3'
DESLIGAR = '4'
CONFIGURAR = '5'

# Tipos de Respostas do Servidor. Nao alterar.
OK_200 = '0'
NAO_AUTORIZADO_401 = '1'
