import pandas as pd
import astropy.coordinates
from astropy.coordinates import SkyCoord  
from tkinter import *
import tkinter.messagebox
import pyperclip
import math
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import webbrowser
# ------------------------------- Constantes  -------------------------------

cores = ["Qualquer", "Ciano", "Branco", "Amarelo", "Laranja", "Vermelho"]

visibilidades = ["Qualquer", "Urbano", "Suburbano", "Rural"]

constelacoes = ['Qualquer', 'Andromeda', 'Antlia', 'Apus', 'Aquarius', 'Aquila', 'Ara', 'Aries', 'Auriga', 'Boötes', 'Caelum', 
                'Camelopardalis', 'Cancer', 'Canes Venatici', 'Canis Major', 'Canis Minor', 'Capricornus', 'Carina', 'Cassiopeia', 
                'Centaurus', 'Cepheus', 'Cetus', 'Chamaleon', 'Circinus', 'Columba', 'Coma Berenices', 'Corona Australis', 
                'Corona Borealis', 'Corvus', 'Crater', 'Crux', 'Cygnus', 'Delphinus', 'Dorado', 'Draco', 'Equuleus', 'Eridanus', 
                'Fornax', 'Gemini', 'Grus', 'Hercules', 'Horologium', 'Hydra', 'Hydrus', 'Indus', 'Lacerta', 'Leo', 'Leo Minor',
                  'Lepus', 'Libra', 'Lupus', 'Lynx', 'Lyra', 'Mensa', 'Microscopium', 'Monoceros', 'Musca', 'Norma', 'Octans', 
                  'Ophiucus', 'Orion', 'Pavo', 'Pegasus', 'Perseus', 'Phoenix', 'Pictor', 'Pisces', 'Pisces Austrinus', 'Puppis', 
                  'Pyxis', 'Reticulum', 'Sagitta', 'Sagittarius', 'Scorpius', 'Sculptor', 'Scutum', 'Serpens', 'Sextans', 'Taurus', 
                  'Telescopium', 'Triangulum', 'Triangulum Australe', 'Tucana', 'Ursa Major', 'Ursa Minor', 'Vela', 'Virgo',
                    'Volans', 'Vulpecula']

fundo_certificado_ciano = 'certificado_ciano.png'
fundo_certificado_branco = 'certificado_branco.png'
fundo_certificado_amarelo = 'certificado_amarelo.png'
fundo_certificado_laranja = 'certificado_laranja.png'
fundo_certificado_vermelho = 'certificado_vermelho.png'


# ------------------------------- Leitura da base de dados -------------------------------

df = pd.read_csv('estrelas.csv')
# ------------------------------- Funções -------------------------------

def sobre(m):

    mensagem = "Esse programa foi feito por Natanael Antonioli para o Desmistificando: registro de nomes estelares \n \n"
    mensagem = mensagem + "Se você pretende batizar uma estrela e se surpreendeu com esse programa ser gratuito, tenho uma boa e uma má notícia. \n"
    mensagem = mensagem + "A boa notícia: o certificado emitido por esse programa é tão válido quanto o das empresas que cobram pelo serviço. \n"
    mensagem = mensagem + "A má notícia: nenhum dos certificados tem qualquer valor. \n "
    mensagem = mensagem + "Sério. O certificado diz que você pode chamar o Sol de sei lá, Cássio. Mas você sempre pôde chamar o Sol do que quisesse. \n"
    mensagem = mensagem + "Ninguém mais vai reconhecer o nome que você escolheu. Nem o governo, nem a comunidade científica, ninguém. \n"
    mensagem = mensagem + "Ainda assim, se um certificado é importante para você, sinta-se livre para imprimí-lo e emuldurá-lo. \n"
    m.configure(text = mensagem)

def get_color(magnitude):

    if magnitude < 0:
        return fundo_certificado_ciano
    elif magnitude < 0.25:
        return fundo_certificado_branco
    elif magnitude < 0.80:
        return fundo_certificado_amarelo
    elif magnitude < 1.40:
        return fundo_certificado_laranja
    else: 
        return fundo_certificado_vermelho


def clicked(m):

    
    # Declara variáveis globais
    global nome
    global cor
    global visibilidade
    global constelacao
    global latitude

    # Lê essas variáveis
    nome = inputnome.get(1.0, "end-1c")
    latitude = inputlat.get(1.0, "end-1c")
    try:
        latitude = float(latitude)
    except:
        pass
    cor = drop_cor_vari.get()
    visibilidade = drop_visi_vari.get()
    constelacao = drop_const_vari.get()


    devolve_estrela(m)

def devolve_estrela(m):

    # Determina variáveis de cor

    min_cor = 0
    max_cor = 999

    if cor == "Ciano":
        min_cor = -100
        max_cor = 0

    elif cor == "Branco":
        min_cor = 0.0
        max_cor = 0.25

    elif cor == "Amarelo":
        min_cor = 0.25
        max_cor = 0.80
    elif cor == "Laranja":
        min_cor = 0.80
        max_cor = 1.40
    elif cor == "Vermelho":
        min_cor = 1.40
        max_cor = 100

    # Determina variáveis de visibilidade
    max_magnitude = 100
    if visibilidade == "Urbano":
        max_magnitude = 4.5
    elif visibilidade == "Suburbano":
        max_magnitude = 6.5

    # Determina a variável de latitude

    visivel = 0
    if isinstance(latitude, float) or isinstance(latitude, int):
        visivel = 1

    # Produz a lista de estrelas

    if constelacao != "Qualquer":
        busca = df.loc[df['Const'] == constelacao]
    else:
        busca = df

    busca = busca.loc[busca['Color'] > min_cor]
    busca = busca.loc[busca['Color'] <= max_cor]
    busca = busca.loc[busca['VTmag'] < max_magnitude]

    if visivel == 1 and latitude > 0:
        busca = busca.loc[busca['DEdeg'] + latitude > 90]
    elif visivel == 1 and latitude < 0:
        busca = busca.loc[busca['DEdeg'] + latitude < -90]

    # Agora, já temos uma lista de candidatas

    if busca.empty:
        mensagem = "Nenhuma estrela encontrada. Mude os filtros."
    else:

        busca = busca.sample(n=1) # Escolhemos uma aleatoriamente. 

        constelacao_encontrada =  busca['Const'].values[0]
        ra_encontrado = busca['RAdeg'].values[0]
        deg_encontrado = busca['DEdeg'].values[0]
        mag_encontrada = busca['Color'].values[0]

        # Avisamos que a estrela foi encontrada

        mensagem = "Estrela encontrada! \n \n"
        mensagem = mensagem + "A estrela fica na constelação de " + constelacao_encontrada + ". \n \n"
        mensagem = mensagem + "Suas coordenadas RA DEC em J200 são: " + str(ra_encontrado) + " , " + str(deg_encontrado) + "\n \n"
        mensagem = mensagem + "Certificado exportado!"

        m.configure(text = mensagem)

        # Copiamos o código para o Stelarium

        pyperclip.copy('core.moveToRaDecJ2000("' + str(ra_encontrado) + '","' + str(deg_encontrado) + '");')
        spam = pyperclip.paste()

        # Produzimos o certificado

        img = Image.open(get_color(mag_encontrada))
        font = ImageFont.truetype("lemon.otf", 80)
        draw = ImageDraw.Draw(img)
        W,H = img.size

        text = str(ra_encontrado) + ',' + str(deg_encontrado) + "   " + constelacao_encontrada
        _, _, w, h = draw.textbbox((0, 0), text, font=font)
        draw.text(((W-w)/2, 2580), text, font=font, fill=(255, 255, 255))

        text = nome
        _, _, w, h = draw.textbbox((0, 0), text, font=font)
        draw.text(((W-w)/2, 2920), text, font=font, fill=(255, 255, 255))

        img.save('Certificado-' + nome + '.pdf')
        webbrowser.open_new('Certificado-' + nome + '.pdf')

    
    

# Define a janela
window = Tk()
window.resizable(0,0)
window.title("Batizador de estrelas da Fábrica de Noobs ")
window.geometry('800x350')

global_offset = 10
x_offset_adjust = 23

# Texto
titulo_buscar = Label(window, text="Esse programa permite batizar estrelas no céu. Para isso, selecione os detalhes da estrela que deseja batizar, e localizaremos uma estrela \n com as características pedidas.")
titulo_buscar.place(x=10 + x_offset_adjust, y=10 + global_offset, in_=window)

# Campo de nome
inputnome = Text(window, height=1, width=50)
inputnome.place(x=10 + x_offset_adjust, y=100 + global_offset, in_=window)

titulo_nome = Label(window, text="Nome: ")
titulo_nome.place(x=10 + x_offset_adjust, y=75 + global_offset, in_=window)

# Campo de cor

titulo_nome = Label(window, text="Cor: ")
titulo_nome.place(x=10 + x_offset_adjust, y=125 + global_offset, in_=window)

drop_cor_vari = StringVar()
drop_cor_vari.set("Qualquer")
drop_cor = OptionMenu( window, drop_cor_vari , *cores)
drop_cor.place(x=10 + x_offset_adjust, y=150 + global_offset, in_=window)


# Campo de visibilidade

titulo_nome = Label(window, text="Visibilidade: ")
titulo_nome.place(x=150 + x_offset_adjust, y=125 + global_offset, in_=window)

drop_visi_vari = StringVar()
drop_visi_vari.set("Qualquer")
drop_cor = OptionMenu( window, drop_visi_vari , *visibilidades)
drop_cor.place(x=150 + x_offset_adjust, y=150 + global_offset, in_=window)

# Campo de constelação

titulo_nome = Label(window, text="Constelação: ")
titulo_nome.place(x=300 + x_offset_adjust, y=125 + global_offset, in_=window)

drop_const_vari = StringVar()
drop_const_vari.set("Qualquer")
drop_cor = OptionMenu( window, drop_const_vari , *constelacoes)
drop_cor.place(x=300 + x_offset_adjust, y=150 + global_offset, in_=window)


# Campo de latitude
inputlat = Text(window, height=1, width=50)
inputlat.place(x=450 + x_offset_adjust, y=100 + global_offset, width= 100, in_=window, )

titulo_lat = Label(window, text="Visível na latitude: ")
titulo_lat.place(x=450 + x_offset_adjust, y=75 + global_offset, in_=window)

# Resultado

mensagem = ""

resultado = Label(window, text=mensagem)
resultado.place(x=10 + x_offset_adjust, y=200 + global_offset, width= 750, in_=window)


# Botão

btn = Button(window, text="Gerar!", command=lambda: clicked(resultado))
btn.place(x=575 + x_offset_adjust, y=95 + global_offset, in_=window)

btn = Button(window, text="Sobre", command=lambda: sobre(resultado))
btn.place(x=650 + x_offset_adjust, y=95 + global_offset, in_=window)


window.mainloop()

