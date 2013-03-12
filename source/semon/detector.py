# @author: Charles Tim Batista Garrocho
# @contact: charles.garrocho@gmail.com
# @copyright: (C) 2012-2013 Python Software Open Source

from datetime import datetime
from sys import exit, stderr
import cv2.cv as cv


class DetectorMovimentos():
    """
    Esta classe permite a deteccao de movimentos de uma determinada webcam.
    """

    def __init__(self):
        """
        O construtor obtem a referencia da webcam e cria uma janela para exibir as imagens.
        """
        # Variavel que vai definir o estado do monitoramento.
        self.estado = True

        # Obtendo a referencia da captura da webCam.
        self.webCam = cv.CaptureFromCAM(0)

        # Obtendo a imagem atual da webCam.
        self.imagem_atual = cv.QueryFrame(self.webCam)

        if self.imagem_atual is None:
            stderr.write('A Web Cam esta desligada. Por favor ligue-a\n')
            exit()
        else:
            # Cria uma nova imagem que sera utilizada para descobrir os contornos na imagem_atual.
            self.imagem_cinza = cv.CreateImage(cv.GetSize(self.imagem_atual), cv.IPL_DEPTH_8U, 1)

            # Cria uma nova imagem que sera utilizada para converter a imagem atual em 32F.
            self.imagem_auxiliar = cv.CreateImage(cv.GetSize(self.imagem_atual), cv.IPL_DEPTH_32F, 3)

            # Imagem sera utilizada para guardar a diferenca entre a imagem atual e anterior.
            self.imagem_diferenca = None

            # Obtendo a area total da imagem da webCam.
            self.area = self.imagem_atual.width * self.imagem_atual.height
            self.area_corrente = 0

            self.imagem_diferenca = cv.CloneImage(self.imagem_atual)
            self.imagem_anterior = cv.CloneImage(self.imagem_atual)

            # Tenho que converter a imagem_atual em 32F para poder calcular a media em "RuningAvg".
            cv.Convert(self.imagem_atual, self.imagem_auxiliar)

    def capturarImagemAtual(self):
        """
        Obtem a imagem atual da webCam.
        """
        self.imagem_atual = cv.QueryFrame(self.webCam)

    def processaImagem(self):
        """
        Crio uma imagem cinza a partir da atual para o programa ficar mais rapido, crio uma imagem com a
        diferenca da imagem anterior e a imagem atual, e binarizo a imagem cinza para filtrar pixels pequenos.
        """
        # Remove os falsos positivos.
        cv.Smooth(self.imagem_atual, self.imagem_atual)

        # Aqui eu coloco um tempo de execucao entre as imagens.
        cv.RunningAvg(self.imagem_atual, self.imagem_auxiliar, 0.05)

        # Covertendo de volta a imagem para poder trabalhar.
        cv.Convert(self.imagem_auxiliar, self.imagem_anterior)

        # Cria uma nova imagem com a diferenca entre a imagem anterior e a atual.
        cv.AbsDiff(self.imagem_atual, self.imagem_anterior, self.imagem_diferenca)

        # Converte a imagem atual em escala de cinza.
        cv.CvtColor(self.imagem_diferenca, self.imagem_cinza, cv.CV_RGB2GRAY)

        # Binariza a imagem. Para poder filtrar pixels pequenos.
        cv.Threshold(self.imagem_cinza, self.imagem_cinza, 50, 255, cv.CV_THRESH_BINARY)

    def verificaMovimento(self):
        """
        Obtem os contornos da imagem cinza e soma a area deles para verificar se ouve diferenca.
        Caso a soma da area dos contornos seja maior que o "0" retorna True, caso contrario False.
        """
        # Encontra os contornos dos objetos na imagem cinza.
        contornos = cv.FindContours(self.imagem_cinza, cv.CreateMemStorage(0))

        while contornos:
            self.area_corrente += cv.ContourArea(contornos)
            contornos = contornos.h_next()

        # Faco uma media da area corrente.
        movimentos = (self.area_corrente * 100) / self.area
        self.area_corrente = 0

        if movimentos > 0:
            return True
        else:
            return False
