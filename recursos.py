# @author: Charles Tim Batista Garrocho
# @contact: ctgarrocho@gmail.com
# @copyright: (C) 2012-2012 Python Software Open Source

from smtplib import SMTP
from re import findall
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from socket import socket, AF_INET, SOCK_STREAM
import settings

class Email(object):
    """
    Esta classe permite o envio de e-mail com uma imagem anexada. A classe suporta hotmail, yahoo e gmail.
    """

    def __init__(self, remetente, destinatario):
        """
        O construtor cria o e-mail e adiciona no cabecalho do e-mail o remetente e o destinatario.
        """
        self.remetente = remetente
        self.destinatario = destinatario
        self.email = MIMEMultipart('related')
        self.corpoMensagem = MIMEMultipart('alternative')
        self.email['From'] = remetente
        self.email['To'] = destinatario
        self.servidorEmail = SMTP(settings.SERVIDORES[findall(u'@(.*?)\.', remetente)[0]], 587)
        
    def enviarEmail(self, titulo, texto, enderecoImagem, senha):
        """
        Envia o e-mail. Recebe como argumento titulo, texto e o endereco da imagem que sera anexada no corpo da mensagem.
        """
        self.corpoMensagem.attach(MIMEText(texto))
        self.email['Subject'] = titulo
        self.email.attach(self.corpoMensagem)
        arqImg = open(enderecoImagem, 'rb')
        imagem = MIMEImage(arqImg.read())
        arqImg.close()
        
        imagem.add_header('Content-ID', '<image1>')
        self.email.attach(imagem)
        
        self.servidorEmail.ehlo()
        self.servidorEmail.starttls()
        self.servidorEmail.ehlo()
        self.servidorEmail.login(self.remetente, senha)
        self.servidorEmail.sendmail(self.remetente, self.destinatario, self.email.as_string())
        self.servidorEmail.close()

class Cliente:
    
    def __init__(self, host = settings.HOST, porta = settings.PORTA):
        self.host = host
        self.porta = porta
        self.soquete = socket(AF_INET, SOCK_STREAM)
        
    def enviarMensagem(self, mensagem):
        self.soquete.connect((self.host, self.porta))
        self.soquete.send(mensagem)
        
    def receberMensagem(self, tam = 1024):
        return self.soquete.recv(tam)
    
    def fecharConexao(self):
        self.soquete.close()
        
def obterHoraAtual(self):
    """
    Retorna um literal com a hora atual para ser utilizada como nome atual da imagem.
    """
    hoje = datetime.now()
    return '{0}-{1}-{2}-{3}-{4}-{5}.jpg'.format(hoje.day, hoje.month, hoje.year, hoje.hour, hoje.minute, hoje.second)
