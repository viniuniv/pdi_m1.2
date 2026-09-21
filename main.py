# Tratamento de imagens raio-x
# Para o trabalho, foram escolhidas imagens com diversos tipos de imperfeições, como baixo
# contraste e poluição visual, além de uma imagem com boa visibilidade para testar mais 
# concretamente os métodos de processamento e de medida de qualidade.

# as operações foram implementadas em seus respectivos scripts e, equanto podem ser aplicadas às imagens
# em qualquer ordem, foram testadas diferentes combinações até encontrar as que melhor perforamaram nas
# métricas de qualidade

from PIL import Image, ImageDraw, ImageFont

from realce_detalhes import *
from transformacao_intensidade import *
from tratamento_ruido import *
from metricas import *


img1_nome = "amostra1.png"
img2_nome = "amostra2.png"
img3_nome = "amostra3.png"
img4_nome = "amostra4.png"
## carregando as imagens
img_1 = Image.open("dataset/"+img1_nome) ## imagem 1 - baixo contraste e objetos altamente convoluídos
img_2 = Image.open("dataset/"+img2_nome) ## imagem 2 - visibilidade e qualidade boas 
img_3 = Image.open("dataset/"+img3_nome) ## imagem 3 - baixo contraste entre ossos e pele/músculos
img_4 = Image.open("dataset/"+img4_nome) ## imagem 4 - ossos altamente convoluídos

def pipeline_1(img):
    ## PIPIELINE 1:
    ## correção gama
    ## realce de detalhes (filtro Sobel)
    img = realce_detalhes(img)
    img = correcao_gama(img, .9)
    return img



def pipeline_2(img):
    ## PIPELINE 2:    
    ## tratamento de ruído
    ## relace de detalhes (filtro Sobel)
    img = tratamento_ruido(img)
    img = realce_detalhes(img)
    return img

def main():
    imgs = [img_1, img_2, img_3, img_4]
    for i in range(len(imgs)):
        fname = "amostra"+str(i+1)+".png"
        img = imgs[i]
        img = aplicar_ruido(img)
        img.save(rf"\output\com_ruido\{fname}")

        p1 = pipeline_1(img)
        p1.save(rf"\output\p1\{fname}")

        p2 = pipeline_2(img)
        p2.save(rf"\output\p2\{fname}")





def gerar_lado_a_lado(img_name):
    ## gera a comparação da imagem de referência com a imagem com ruído e as pipelines, além de adicionar
    ## texto contendo as notas RMSE e SSIM em suas respectivas imagens filtradas
    img_ref:Image = Image.open("dataset/"+img_name).convert("L")
    img_ruido = Image.open("output/com_ruido/"+img_name).convert("L")
    img_p1 = Image.open("output/p1/"+img_name).convert("L")
    img_p2 = Image.open("output/p2/"+img_name).convert("L")
    w, h = img_ref.size

    ## gera a imagem de saída com a original e a saída das duas pipelines
    ## (já geradas salvas nos diretórios output/p1 e output/p2)
    output = Image.new("L", (w * 4, h))
    output.paste(img_ref)
    output.paste(img_ruido, (w, 0))
    output.paste(img_p1, (w*2, 0))
    output.paste(img_p2, (w*3, 0))

    resultado_rmse = metrica_rmse(img_name)
    resultado_ssim = metrica_ssim(img_name)

    font = ImageFont.load_default(size=24)
    texto_ref = "ORIGINAL"
    texto_ruido = "RUÍDO"
    texto_p1 = "PIPELINE 1\nRMSE: " + str(round(resultado_rmse[0], 4))+"\nSSIM: " + str(round(resultado_ssim[0], 4))
    texto_p2 = "PIPELINE 2\nRMSE: " + str(round(resultado_rmse[1], 4))+"\nSSIM: " + str(round(resultado_ssim[1], 4))

    cor_texto = "#FFFFFF"
    if img_name == "amostra2.png":
        cor_texto = "#000000" ## para o texto aparecer sob o fundo branco da amostra 2
    
    
    draw = ImageDraw.Draw(output)
    draw.text((0, 5), texto_ref,fill=cor_texto, font=font)
    draw.text((w, 5), texto_ruido, fill=cor_texto, font=font)
    draw.text((w * 2, 5), texto_p1,fill=cor_texto, font=font)
    draw.text((w * 3, 5), texto_p2,fill=cor_texto, font=font)
    output.save(rf"\output\lado_a_lado\{img_name}")

gerar_lado_a_lado("amostra1.png")
gerar_lado_a_lado("amostra2.png")
gerar_lado_a_lado("amostra3.png")
gerar_lado_a_lado("amostra4.png")

# main()

"""
Imagens de resultado lado-a-lado disponíveis em output/lado_a_lado

Resultados RMSE:
    RMSE amostra1.png
    P1: 26.3050
    P2: 16.4838

    RMSE amostra2.png
    P1: 56.6294
    P2: 51.1332

    RMSE amostra3.png
    P1: 31.4820
    P2: 21.5230

    RMSE amostra4.png
    P1: 36.1442
    P2: 26.3452

    Na métrica RMSE, que, grosseiramente, calcula o quão parecidas com imagem original a imagem filtrada ficou, 
    as pipelines tiveram perfórmaces parecidas, com pontuações relativamente ruins (quase todas acima de 20)
    porém, a pipeline 2 demonstrou pontuações ligeiramente melhores em todas as imagens.

Resultados SSIM:
    SSIM:  amostra1.png
    P1: 0.1908
    P2: 0.5984

    SSIM:  amostra2.png
    P1: 0.3157
    P2: 0.6143

    SSIM:  amostra3.png
    P1: 0.2276
    P2: 0.6653

    SSIM:  amostra4.png
    P1: 0.2279
    P2: 0.6305

    Na métrica SSIM, que busca avaliar de forma mais objetiva o quão "legíveis" as imagens ficaram em comparação com a original, 
    os resultados para ambas as pipelines variaram entre ~0.2 e ~0.7, o que é um resultado relativamente
    ruim comparado à imagem de referência, mas, novamente, a pipeline 2 demonstrou resultados bem melhorews para as amostras.

    CONCLUSÃO:
        Enquanto esse projeto tem escopo limitado e, na prática, para resolver problemas como esse, é necessário um entendimento mais
        profundo do que médicos e enfermeiros valorizam e desvalorizam em uma imagem de raio X, foi notado o potencial das téncicas de 
        processamento, a pipeline 2, que performou melhor em todas as métricas para todas as imagens, especialmente devido ao uso de técnicas
        de tratamento de ruído, que são feitas para lidar com ruídos com o que foi induzido artificalmente, claramente gerou um resultado que
        melhor elimina as imperfeições das imagens e, teoricamente, seria a que mais facilita o trabalho de profissionais da saúde.
"""