# coding: utf-8
# @author: Charles Tim Batista Garrocho
# @contact: charles.garrocho@gmail.com
# @copyright: (C) 2012-2013 Python Software Open Source

from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from detector import DetectorMovimentos
from datetime import datetime
from recursos import obterHoraAtual, Email
from getpass import getpass
from re import findall
from os import remove
import settings
import time
import cv2.cv as cv
import bz2
import smtplib
from sys import stderr

DETECTOR = DetectorMovimentos()
DETECTOR.estado = settings.ESTADO
SENHA = getpass('Forneça a senha de {0}: '.format(settings.EMAIL))


def statusMonitoramento(conexao):
    """
    Envia ao cliente o estado atual do monitoramento.
    """
    conexao.send(settings.OK_200)
    if DETECTOR.estado:
        conexao.send(settings.EXECUTANDO)
    else:
        conexao.send(settings.PAUSADO)


def login(conexao):
    """
    Verifica o login do cliente.
    """
    conexao.send(settings.OK_200)
    login = conexao.recv(1024)
    login = bz2.decompress(login)
    login = login.split('==0#_6_#0==')
    if login[0] == settings.EMAIL and login[1] == SENHA:
        conexao.send(settings.OK_200)
    else:
        conexao.send(settings.NAO_AUTORIZADO_401)


def iniciar(conexao=None):
    """
    Inicia o monitoramento. Vai processando as imagens e verificando
    se ocorre diferenças nas imagens, caso ocorra, um e-mail é enviado
    ao administrador da sala de servidores.
    """
    tempo_atual = time.time()
    while True:
        time.sleep(settings.CAPTURAR)
        DETECTOR.capturarImagemAtual()
        while not ((tempo_atual + settings.INTERVALO) > time.time()):
            DETECTOR.processaImagem()
            if DETECTOR.estado:
                if DETECTOR.verificaMovimento():
                    hora = obterHoraAtual()
                    email = Email(settings.EMAIL, settings.EMAIL)
                    cv.SaveImage('../imagens/{0}.jpg'.format(hora), DETECTOR.imagem_atual)
                    email.enviarEmail('[SEMON / {0}] Alerta de Movimento'.format(hora), 'Foi detectado um movimento na sala de servidores.', '../imagens/{0}.jpg'.format(hora), SENHA)
                    remove('../imagens/{0}.jpg'.format(hora))
            tempo_atual = time.time()


def obterImagemAtual(conexao):
    """
    Envia uma imagem atual do monitoramento para o cliente.
    """
    endereco = '../imagens/temp.jpg'
    cv.SaveImage(endereco, DETECTOR.imagem_atual)

    imagem = open(endereco)
    conexao.send(settings.OK_200)

    while True:
        dados = imagem.read(512)
        if not dados:
            break
        conexao.send(dados)

    imagem.close()
    remove(endereco)


def trataCliente(conexao, endereco):
    """
    Trata as novas requisições dos clientes.
    """
    requisicao = conexao.recv(settings.TAM_MSN)

    # Requisição de verificar estado do monitoramento.
    if requisicao == settings.STATUS:
        statusMonitoramento(conexao)

    # Requisição de logar no monitoramento.
    if requisicao == settings.LOGAR:
        login(conexao)

    # Requisição de iniciar monitoramento.
    elif requisicao == settings.INICIAR:
        conexao.send(settings.OK_200)
        DETECTOR.estado = True

    # Requisição de pausar monitoramento.
    elif requisicao == settings.PAUSAR:
        conexao.send(settings.OK_200)
        DETECTOR.estado = False

    # Requisição de obter uma imagem atual do monitoramento.
    elif requisicao == settings.IMAGEM:
        obterImagemAtual(conexao)

    # Requisição não autorizada.
    else:
        conexao.send(settings.NAO_AUTORIZADO_401)

    # Após a requisição ser realizada, a conexão é fechada.
    conexao.close()


def servidor():
    """
    Abre um novo soquete servidor para tratar as novas conexões do cliente.
    """
    soquete = socket(AF_INET, SOCK_STREAM)
    soquete.bind((settings.HOST, settings.PORTA))
    soquete.listen(1)
    Thread(target=iniciar).start()

    # Fica aqui aguardando novas conexões.
    while True:
        # Para cada nova conexão é criado um novo processo para tratar as requisições.
        Thread(target=trataCliente, args=(soquete.accept())).start()


if __name__ == '__main__':
    try:
        email = smtplib.SMTP(settings.SERVIDORES[findall(u'@(.*?)\.', settings.EMAIL)[0]], 587)
        email.ehlo()
        email.starttls()
        email.ehlo()
        email.login(settings.EMAIL, SENHA)
        email.close()
        Thread(target=servidor).start()
    except smtplib.SMTPAuthenticationError:
        stderr.write('Senha inválida de {0}\n'.format(settings.EMAIL))
