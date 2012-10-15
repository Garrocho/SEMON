# coding: utf-8
# @author: Charles Tim Batista Garrocho
# @contact: ctgarrocho@gmail.com
# @copyright: (C) 2012-2012 Python Software Open Source

from gi.repository import Gtk
from handler import *
from datetime import datetime
import settings
try:
    import gi
    gi.require_version('Gtk', '3.0')
    IMPORTS = True
except:
    IMPORTS = False


class JanelaCliente(Gtk.Window):
    """
    Cria uma interface para o cliente.
    """
    def __init__(self):
        super(JanelaCliente, self).__init__()

        # Criando os elementos.
        self.layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.painelCentro = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.webCam = Gtk.Image()
        self.webCam.set_from_file('./img/default.jpg')

        self.status_bar = Gtk.Statusbar()
        self.context_id = self.status_bar.get_context_id('status')

        self.toolbar = CustomToolbar()
        self.toolbar.set_hexpand(True)

        self.botaoIniciar = Gtk.ToolButton(stock_id=Gtk.STOCK_MEDIA_PLAY)
        self.botaoObterImagem = Gtk.ToolButton(stock_id=Gtk.STOCK_GO_DOWN)
        self.botaoSalvarImagem = Gtk.ToolButton(stock_id=Gtk.STOCK_SAVE)
        self.botaoLimparImagem = Gtk.ToolButton(stock_id=Gtk.STOCK_CLEAR)
        self.botaoSair = Gtk.ToolButton(stock_id=Gtk.STOCK_QUIT)

        # Modificando as configuracoes dos elementos.
        self.botaoIniciar.set_label('Iniciar  ')
        self.botaoObterImagem.set_label('Imagem Atual')
        self.botaoSalvarImagem.set_label('Salvar Imagem')
        self.botaoLimparImagem.set_label('Limpar Tela')

        self.botaoIniciar.set_is_important(True)
        self.botaoObterImagem.set_is_important(True)
        self.botaoSalvarImagem.set_is_important(True)
        self.botaoLimparImagem.set_is_important(True)
        self.botaoSair.set_is_important(True)

        self.botaoSalvarImagem.set_sensitive(False)
        self.botaoLimparImagem.set_sensitive(False)

        # Adicionando os elementos.
        self.toolbar.insert(self.botaoIniciar, 0)
        self.toolbar.insert(self.botaoObterImagem, 1)
        self.toolbar.insert(self.botaoSalvarImagem, 2)
        self.toolbar.insert(self.botaoLimparImagem, 3)
        self.toolbar.insert(Gtk.SeparatorToolItem(), 4)
        self.toolbar.insert(self.botaoSair, 5)

        self.painelCentro.pack_start(self.webCam, False, False, 0)

        self.layout.pack_start(self.toolbar, False, False, 0)
        self.layout.pack_start(self.painelCentro, False, False, 0)
        self.layout.pack_end(self.status_bar, False, True, 0)

        self.add(self.layout)

        # Adicionando os eventos.
        self.botaoIniciar.connect('clicked', statusMonitoramento, self)
        self.botaoObterImagem.connect('clicked', obterImagemMonitoramento, self)
        self.botaoSalvarImagem.connect('clicked', salvarImagemMonitoramento, self)
        self.botaoLimparImagem.connect('clicked', limparImagemMonitoramento, self)
        self.botaoSair.connect('clicked', sairMonitoramento)

        # Configurando a janela.
        self.connect('delete_event', sairMonitoramento)
        self.set_size_request(640, 540)
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_title('SEMON - Sensor de Monitoramento de Salas de Servidores')
        self.show_all()

        cliente = Cliente()
        if cliente.conectaServidor():
            cliente.enviarMensagem(settings.STATUS)

            # Obtem o estado do monitoramento.
            if cliente.receberMensagem(settings.TAM_MSN) == settings.OK_200:
                resposta = cliente.receberMensagem(settings.TAM_MSN)
                self.botaoObterImagem.set_sensitive(True)
                if resposta == settings.EXECUTANDO:
                    self.status_bar.push(self.context_id, ' Monitoramento Iniciado')
                    self.botaoIniciar.set_stock_id(Gtk.STOCK_MEDIA_PAUSE)
                    self.botaoIniciar.set_label('Pausar')
                elif resposta == settings.PAUSADO:
                    self.status_bar.push(self.context_id, ' Monitoramento Pausado')
        else:
            self.botaoObterImagem.set_sensitive(False)
            self.status_bar.push(self.context_id, ' Monitoramento Desligado')

    def janelaEscolhePasta(self):
        """
        Chama o FileChooserDialog para pegar o diretório onde será salva a imagem.
        """
        dialogo = Gtk.FileChooserDialog('Por Favor Selecione uma Pasta', self, Gtk.FileChooserAction.SELECT_FOLDER, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, 'Salvar', Gtk.ResponseType.OK))
        resposta = dialogo.run()
        if resposta == Gtk.ResponseType.OK:
            resposta = dialogo.get_filename()
        else:
            resposta = None

        dialogo.destroy()
        return resposta


def dialogoErro(mensagem1, mensagem2):
    """
    Exibe um dialogo de erro com uma determinada mensagem.
    """
    dialog = Gtk.MessageDialog(message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.CLOSE, text=mensagem1)
    dialog.set_title('SEMON - Sensor de Monitoramento de Salas de Servidores')
    dialog.format_secondary_text(mensagem2)
    dialog.run()
    dialog.destroy()


class CustomToolbar(Gtk.Toolbar):
    """
    Instancia uma ToolBar customizada.
    """

    def __init__(self):
        """
        Configurando o Estilo do Toolbar.
        """
        super(CustomToolbar, self).__init__()
        context = self.get_style_context()
        context.add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)

    def insert(self, item, pos):
        """
        Verifica se o item e uma instancia do Gtk.ToolItem antes de coloca-lo no toolbar.
        """
        if not isinstance(item, Gtk.ToolItem):
            widget = Gtk.ToolItem()
            widget.add(item)
            item = widget

        super(CustomToolbar, self).insert(item, pos)
        return item

if __name__ == '__main__':
    if IMPORTS:
        janela = JanelaCliente()
        Gtk.main()
    else:
        dialogoErro('Erro ao Importar o GTK.', 'A sua versao do GTK nao e compativel com a versao do SEMON.\nNecessario Versao 3.0')
