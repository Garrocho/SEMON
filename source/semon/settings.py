# @author: Charles Tim Batista Garrocho
# @contact: charles.garrocho@gmail.com
# @copyright: (C) 2012-2013 Python Software Open Source

# Host (Ip do Servidor), PORTA (Porta do Servidor)
HOST = 'localhost'
PORTA = 7777

# Defina aqui o estado inicial do monitoramento.
ESTADO = False

# Defina aqui o intervalo de verificacao do monitoramento.
INTERVALO = 5

# Defina aqui o intervalo de capturar imagem do monitoramento.
CAPTURAR = 1

# Defina aqui o email do administrador da sala de monitoramento.
EMAIL = 'charles.garrocho@gmail.com'

# Servidores de E-mail
SERVIDORES = dict([('hotmail', 'smtp.live.com'), ('live', 'smtp.live.com'), ('yahoo', 'smtp.mail.yahoo.fr'), ('gmail', 'smtp.gmail.com')])

# Tipo de Mensagem de Status do Monitoramento. Nao alterar.
EXECUTANDO = 'EXECUT'
PAUSADO = 'PAUSAD'

# Tipos de Requisicoes do Cliente. Nao alterar.
STATUS = 'STATUS'
LOGAR = 'LOGAR_'
INICIAR = 'INICIA'
PAUSAR = 'PAUSAR'
IMAGEM = 'IMAGEM'
DESLIGAR = 'DESLIG'
CONFIGURAR = 'CONFIG'

# Tamanho das Mensagens de requisicao.
TAM_MSN = 6

# Tipos de Respostas do Servidor. Nao alterar.
OK_200 = 'OK_200'
NAO_AUTORIZADO_401 = 'NO_401'
