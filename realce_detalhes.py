from PIL import Image
import math

def filtro_sobel(img:Image):
    gx_kernel = [
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ]
    gy_kernel = [
        [-1, -2, -1],
        [0, 0, 0],
        [ 1,  2,  1]
    ]

    w, h = img.size
    output = Image.new("L", img.size)
    pixels = img.load()

    out_pixels = output.load()


    for x in range(1, w - 1):
        for y in range(1, h - 1):
            total = 0
            gx = 0
            gy = 0
            for kx in range(-1, 2):
                for ky in range(-1, 2):
                    px = pixels[x + kx, y + ky]
                    gx = px * gx_kernel[kx + 1][ky + 1]
                    gy = px * gy_kernel[kx + 1][ky + 1]
            magnitude = int(math.sqrt(gx * gx + gy * gy))
            if magnitude > 255:
                magnitude = 255
            

            out_pixels[x, y] = magnitude
    return output

def realce_detalhes(img):
    img = img.convert("L")
    w, h = img.size
    filtrada = filtro_sobel(img)
    return filtrada


