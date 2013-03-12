# coding: utf-8
# @author: Charles Tim Batista Garrocho
# @contact: charles.garrocho@gmail.com
# @copyright: (C) 2012-2013 Python Software Open Source

from smtplib import SMTP
from re import findall
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from socket import socket, AF_INET, SOCK_STREAM, error
from datetime import datetime
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
    """
    Esta Classe permite criar conexões com um determinado host em uma determinada porta.
    """

    def __init__(self, host=settings.HOST, porta=settings.PORTA):
        self.host = host
        self.porta = porta

    def conectaServidor(self):
        """
        Retorna o estado da conexão do servidor.
        """
        try:
            self.soquete = socket(AF_INET, SOCK_STREAM)
            self.soquete.connect((self.host, self.porta))
            return True
        except error, msg:
            return False

    def enviarMensagem(self, mensagem):
        """
        Conecta a um host e porta, e envia a mensagem.
        """
        self.soquete.send(mensagem)

    def receberMensagem(self, tam=1024):
        """
        Recebe uma mensagem. O parametro tam pode ser definido.
        """
        return self.soquete.recv(tam)

    def fecharConexao(self):
        """
        Fecha a conexão do soquete.
        """
        self.soquete.close()


def obterHoraAtual():
    """
    Retorna um literal com a hora atual para ser utilizada como nome atual da imagem.
    """

    hoje = datetime.now()
    return '{0}-{1}-{2}-{3}-{4}-{5}'.format(hoje.day, hoje.month, hoje.year, hoje.hour, hoje.minute, hoje.second)
