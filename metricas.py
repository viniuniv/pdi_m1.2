from PIL import Image
import numpy as np
from skimage.metrics import structural_similarity as ssim


def metrica_rmse(img_name):
    ## aplica a métrica RMSE para a imagem, que precisa
    ## já ter sido passada por ambas as pipelines e salva corretamente
    img_ref = Image.open("dataset/"+img_name).convert("L")
    img_p1 = Image.open("output/p1/"+img_name).convert("L")
    img_p2 = Image.open("output/p2/"+img_name).convert("L")

    matriz_ref = np.asarray(img_ref, dtype = np.float32)
    matriz_p1 = np.asarray(img_p1, dtype = np.float32)
    matriz_p2 = np.asarray(img_p2, dtype = np.float32)

    rmse_p1 = np.sqrt(np.mean((matriz_ref - matriz_p1) ** 2))
    rmse_p2 = np.sqrt(np.mean((matriz_ref - matriz_p2) ** 2))

    ## imprime os resultados das métricas no console e retorna-os 
    ## na forma de uma tupla
    print("RMSE " + img_name)
    print(f"P1: {rmse_p1:.4f}")
    print(f"P2: {rmse_p2:.4f}")
    return (rmse_p1, rmse_p2)

def metrica_ssim(img_name):
    ## aplica a métrica SSIM para a imagem, que precisa
    ## já ter sido passada por ambas as pipelines e salva corretamente
    img_ref = Image.open("dataset/"+img_name).convert("L")
    img_p1 = Image.open("output/p1/"+img_name).convert("L")
    img_p2 = Image.open("output/p2/"+img_name).convert("L")

    matriz_ref = np.asarray(img_ref, dtype = np.uint8)
    matriz_p1 = np.asarray(img_p1, dtype = np.uint8)
    matriz_p2 = np.asarray(img_p2, dtype = np.uint8)

    ssim_p1 = ssim(matriz_ref, matriz_p1)
    ssim_p2 = ssim(matriz_ref, matriz_p2)
    
    ## imprime os resultados das métricas no console e retorna-os 
    ## na forma de uma tupla
    print("SSIM: ", img_name)
    print(f"P1: {ssim_p1:.4f}")
    print(f"P2: {ssim_p2:.4f}")
    return (ssim_p1, ssim_p2)