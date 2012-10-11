# coding: utf-8
# @author: Charles Tim Batista Garrocho
# @contact: ctgarrocho@gmail.com
# @copyright: (C) 2012-2012 Python Software Open Source

from gi.repository import Gtk
from recursos import Cliente
from gui import dialogoErro
from socket import socket, AF_INET, SOCK_STREAM
from shutil import copy2
import settings


def verificaStatus():
    """
    Retorna o estado da conexão do servidor.
    """
    soquete = socket(AF_INET, SOCK_STREAM)
    soquete.settimeout(1.5)
    resposta = soquete.connect_ex((settings.HOST, settings.PORTA))
    soquete.close()
    return '{0}'.format(resposta)


def statusMonitoramento(evento, janela):
    """
    Modifica o estado do monitoramento do servidor.
    """
    # Pega o estado da conexão.
    resposta = verificaStatus()
    if resposta == '0':
        cliente = Cliente()
        cliente.enviarMensagem(settings.STATUS)

        # Obtem o estado do monitoramento.
        if cliente.receberMensagem(1) == settings.OK_200:
            resposta = cliente.receberMensagem(1)
            cliente.fecharConexao()
        else:
            resposta = settings.OK_200
            cliente.fecharConexao()

    # Verifica o estado do monitoramento.
    if resposta == settings.PAUSADO:
        iniciarMonitoramento(janela)
    elif resposta == settings.EXECUTANDO:
        pausarMonitoramento(janela)
    else:
        dialogoErro('Erro ao Estabelecer Conexao.', 'Nao Foi Possivel Modificar o Estado do Monitoramento.\t\t\nO Servidor Esta Desligad.')


def iniciarMonitoramento(janela):
    """
    Envia uma mensagem ao servidor para iniciar o monitoramento.
    """
    cliente = Cliente()
    cliente.enviarMensagem(settings.INICIAR)

    if cliente.receberMensagem(1) == settings.OK_200:
        janela.status_bar.push(janela.context_id, ' Monitoramento Iniciado')
        cliente.fecharConexao()
        janela.botaoIniciar.set_stock_id(Gtk.STOCK_MEDIA_PAUSE)
        janela.botaoIniciar.set_label('Pausar')
    else:
        dialogoErro('Erro ao Iniciar o Monitoramento.', 'Parece que o Servidor Nao Respondeu. Tente Novamente.')


def pausarMonitoramento(janela):
    """
    Envia uma mensagem ao servidor para pausar o monitoramento.
    """
    cliente = Cliente()
    cliente.enviarMensagem(settings.PAUSAR)
    if cliente.receberMensagem(1) == settings.OK_200:

        janela.status_bar.push(janela.context_id, ' Monitoramento Pausado')
        cliente.fecharConexao()
        janela.botaoIniciar.set_stock_id(Gtk.STOCK_MEDIA_PLAY)
        janela.botaoIniciar.set_label('Iniciar  ')
    else:
        dialogoErro('Erro ao Pausar o Monitoramento.', 'Parece que o Servidor Nao Respondeu. Tente Novamente.')


def limparImagemMonitoramento(evento, janela):
    """
    Limpa a imagem atual do cliente.
    """
    janela.webCam.set_from_file('./img/default.jpg')
    janela.botaoSalvarImagem.set_sensitive(False)
    janela.botaoLimparImagem.set_sensitive(False)


def obterImagemMonitoramento(evento, janela):
    """
    Envia uma mensagem ao servidor para obter uma imagem do monitoramento.
    """
    cliente = Cliente()
    cliente.enviarMensagem(settings.IMAGEM)
    while cliente.receberMensagem(1) != settings.OK_200:
        cliente.enviarMensagem(settings.IMAGEM)

    arquivo = open('img.jpg', 'w')
    while True:
        dados = cliente.receberMensagem(512)
        if not dados:
            break
        arquivo.write(dados)

    arquivo.close

    janela.webCam.set_from_file('img.jpg')
    janela.botaoSalvarImagem.set_sensitive(True)
    janela.botaoLimparImagem.set_sensitive(True)
    cliente.fecharConexao()


def salvarImagemMonitoramento(evento, janela):
    """
    Salva a imagem atual uma escolhida pelo usuário.
    """
    diretorio = janela.janelaEscolhePasta()
    if diretorio != None:
        copy2('img.jpg', '{0}/{1}'.format(diretorio, janela.obterHoraAtual()))


def sairMonitoramento(evento = None):
    Gtk.main_quit()
