# coding: utf-8
# @author: Charles Tim Batista Garrocho
# @contact: charles.garrocho@gmail.com
# @copyright: (C) 2012-2013 Python Software Open Source

from gi.repository import Gtk, Gdk
from datetime import datetime
from recursos import Cliente
import settings
try:
    import gi
    gi.require_version('Gtk', '3.0')
    IMPORTS = True
except:
    IMPORTS = False


class JanelaCliente(Gtk.Window):
    """
    Cria uma interface que possibilita interacoes com o servidor.
    """

    def __init__(self):
        from handler import limparImagemMonitoramento, statusMonitoramento, obterImagemMonitoramento, salvarImagemMonitoramento
        super(JanelaCliente, self).__init__()

        # Criando os elementos.
        self.layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.painelCentro = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.webCam = Gtk.Image()
        self.webCam.set_from_file('../imagens/default.jpg')

        self.set_icon_from_file("../imagens/logo2.png")

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
        self.botaoSair.connect('clicked', Gtk.main_quit)

        # Configurando a janela.
        self.connect('delete_event', Gtk.main_quit)
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


class JanelaLogar(Gtk.Window):
    """
    Cria uma interface que possibilita o login do cliente.
    """

    def __init__(self, evento=None):
        from handler import logarMonitoramento
        Gtk.Window.__init__(self)
        self.set_icon_from_file("../imagens/logo2.png")

        painel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        self.add(painel)

        tbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        vbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        ibox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        zbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        self.logo = Gtk.Image()
        self.logo.set_from_file('../imagens/logo1.png')

        tbox.pack_start(self.logo, True, True, 0)
        painel.pack_start(tbox, True, False, 0)

        self.labelEmail = Gtk.Label('  E-Mail')
        vbox.pack_start(self.labelEmail, True, False, 0)

        self.entryEmail = Gtk.Entry()
        self.entryEmail.set_size_request(200, 30)
        self.entryEmail.set_tooltip_text('Forneca o e-mail do monitoramento.')
        vbox.pack_start(self.entryEmail, True, False, 0)

        painel.pack_start(vbox, True, False, 0)

        self.labelSenha = Gtk.Label('  Senha')
        hbox.pack_start(self.labelSenha, True, False, 0)

        self.entrySenha = Gtk.Entry()
        self.entrySenha.set_visibility(False)
        self.entrySenha.set_tooltip_text('Forneca a senha do seu endereco de e-mail.')
        self.entrySenha.set_size_request(200, 30)
        hbox.pack_start(self.entrySenha, True, False, 0)

        painel.pack_start(hbox, True, False, 0)

        self.botaoCancelar = Gtk.Button('Cancelar')
        zbox.pack_start(self.botaoCancelar, True, False, 0)
        self.botaoCancelar.set_size_request(110, 40)

        self.botaoLogar = Gtk.Button('Logar')
        zbox.pack_start(self.botaoLogar, True, False, 0)
        self.botaoLogar.set_size_request(110, 40)

        # Adicionando os eventos.
        self.botaoCancelar.connect('clicked', Gtk.main_quit)
        self.botaoLogar.connect('clicked', logarMonitoramento, self)
        self.entryEmail.connect('activate', logarMonitoramento, self)
        self.entrySenha.connect('activate', logarMonitoramento, self)

        painel.pack_start(zbox, True, False, 0)

        self.set_modal(True)
        self.set_resizable(False)
        self.connect('delete_event', Gtk.main_quit)
        self.set_size_request(270, 280)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_title('SEMON - Login')
        self.show_all()


def dialogoErro(janela, mensagem1, mensagem2):
    """
    Exibe um dialogo de erro com uma determinada mensagem.
    """
    dialog = Gtk.MessageDialog(janela, message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.CLOSE, text=mensagem1)
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
        JanelaLogar()
        Gtk.main()
    else:
        dialogoErro('Erro ao Importar o GTK.', 'A sua versao do GTK nao e compativel com a versao do SEMON.\nNecessario Versao 3.0')
