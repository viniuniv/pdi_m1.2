from PIL import Image
import numpy as np

def filtro_gaussiano(img:Image):
    ## código parcialmente reaproveitado do trabalho M1.1
    matriz = [
        [1, 2, 1],
        [2, 4, 2],
        [1, 2, 1]
    ] 

    w, h = img.size
    output = Image.new("L", img.size)
    pixels = img.convert("L").load()
    out_pixels = output.load()
    divisor = sum([sum(r) for r in matriz])
    if divisor == 0:
        divisor = 1

    for x in range(1, w - 1):
        for y in range(1, h - 1):
            total = 0

            for x1 in range(-1, 2):
                for y1 in range(-1, 2):
                    total += pixels[x + x1, y + y1] * matriz[x1][y1]

            out_pixels[x, y] = total//divisor
    return output


def aplicar_ruido(img):
    img_arr = np.array(img, dtype = np.float32)
    noise = np.random.normal(0, 10, img_arr.shape)
    noise_arr = img_arr + noise
    img = Image.fromarray(noise_arr).convert("L")
    return img

def tratamento_ruido(img):
    img = img.convert("L")
    w, h = img.size


    output = Image.new("L", (w, h))
    filtrada = filtro_gaussiano(img)
    output.paste(filtrada)

    return output
