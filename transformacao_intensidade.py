from PIL import Image


def correcao_gama(img, gama):
    ## aplicação da correção gama na imagem amostra_1.png, que está com baixo
    ## contraste, o que dificulta na visualização
    ## gama = valor Y da correção
    img = img.convert("L")
    w, h = img.size
    pixels = img.load()


    output = Image.new("L", (w, h))

    out_pixels = output.load()
    for x in range(w):
        for y in range(h):
            v = pixels[x, y]/255 ## valor de intensidade normalizado do pixel
            out_v = int(v ** gama * 255) ## valor com a correção aplicada e normalização removida
            out_pixels[x , y] = out_v
    return output

