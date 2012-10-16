# coding: utf-8
# @author: Charles Tim Batista Garrocho
# @contact: ctgarrocho@gmail.com
# @copyright: (C) 2012-2012 Python Software Open Source

from gi.repository import Gtk
from recursos import Cliente, obterHoraAtual
import cv2.cv as cv
from gui import dialogoErro
from socket import socket, AF_INET, SOCK_STREAM
from shutil import copy2
import settings


def statusMonitoramento(evento, janela):
    """
    Modifica o estado do monitoramento do servidor.
    """
    cliente = Cliente()
    if cliente.conectaServidor():

        # Obtem o estado do monitoramento.
        cliente.enviarMensagem(settings.STATUS)
        if cliente.receberMensagem(settings.TAM_MSN) == settings.OK_200:
            resposta = cliente.receberMensagem(settings.TAM_MSN)
            print resposta
            # Verifica se o estado do monitoramento e de pausado.
            if resposta == settings.PAUSADO:
                cliente.conectaServidor()
                cliente.enviarMensagem(settings.INICIAR)
                if cliente.receberMensagem(settings.TAM_MSN) == settings.OK_200:

                    janela.status_bar.push(janela.context_id, ' Monitoramento Iniciado')
                    cliente.fecharConexao()
                    janela.botaoIniciar.set_stock_id(Gtk.STOCK_MEDIA_PAUSE)
                    janela.botaoIniciar.set_label('Pausar')

            # Verifica se o estado do monitoramento e de executando.
            elif resposta == settings.EXECUTANDO:
                cliente.conectaServidor()
                cliente.enviarMensagem(settings.PAUSAR)
                if cliente.receberMensagem(settings.TAM_MSN) == settings.OK_200:

                    janela.status_bar.push(janela.context_id, ' Monitoramento Pausado')
                    cliente.fecharConexao()
                    janela.botaoIniciar.set_stock_id(Gtk.STOCK_MEDIA_PLAY)
                    janela.botaoIniciar.set_label('Iniciar  ')
    else:
        cliente.fecharConexao()
        dialogoErro('Erro ao Estabelecer Conexao.', 'Nao Foi Possivel Modificar o Estado do Monitoramento.\t\t\nO Servidor Esta Desligado.')


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

    # Verifica se o servidor esta ligado.
    if cliente.conectaServidor():
        cliente.enviarMensagem(settings.IMAGEM)
        if cliente.receberMensagem(settings.TAM_MSN) == settings.OK_200:

            endereco = './img/temp2.jpg'
            arquivo = open(endereco, 'w')
            while True:
                dados = cliente.receberMensagem(512)
                if not dados:
                    break
                arquivo.write(dados)

            arquivo.close
            janela.webCam.set_from_file(endereco)
            janela.botaoSalvarImagem.set_sensitive(True)
            janela.botaoLimparImagem.set_sensitive(True)
            cliente.fecharConexao()
    else:
        cliente.fecharConexao()
        dialogoErro('Erro ao Estabelecer Conexao.', 'Nao Foi Possivel Modificar o Estado do Monitoramento.\t\t\nO Servidor Esta Desligado.')



def salvarImagemMonitoramento(evento, janela):
    """
    Salva a imagem atual em uma pasta escolhida pelo usuário.
    """
    diretorio = janela.janelaEscolhePasta()
    if diretorio is not None:
        imagem = '{0}.jpg'.format(obterHoraAtual())
        copy2('./img/temp2.jpg', '{0}/{1}.jpg'.format(diretorio, obterHoraAtual()))


def sairMonitoramento(event=None):
    Gtk.main_quit()
