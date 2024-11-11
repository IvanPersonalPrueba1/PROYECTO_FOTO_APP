from PIL import Image, ImageOps, ImageFilter
from matplotlib import pyplot as plt
import numpy as np # type: ignore
import os

carpetas = [
    'imagenes_con_bordes',
    'imagenes_filtros',
    'imagenes_contraste',
    'imagenes_redimensiones'
]

def leer_imagen(imagen_path):
    try:
        imagen = Image.open(imagen_path)
        return imagen
    except Exception as e:
        print(f"\nError al leer la imagen: {e}")
        return None
    
# Función para mostrar la imagen
def mostrar_imagen(imagen, titulo="Imagen"):
    if imagen:
        plt.imshow(imagen, cmap="gray")
        plt.title(titulo)
        plt.axis('off')
        plt.show()
    else:
        print("\nNo se puede mostrar la imagen.")
        
# Función para guardar la imagen generada
def guardar_imagen(imagen, nombre_archivo, carpeta):
    os.makedirs(carpeta, exist_ok=True)
    try:
        imagen.save(os.path.join(carpeta, f"{nombre_archivo}.jpg"))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(f"\nImagen guardada como {nombre_archivo}")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    except Exception as e:
        print(f"\nError al guardar la imagen: {e}")
        
plataforma_tamaños = {
    "Youtube": (1280, 720),
    "Instagram": (1080, 1080),
    "Twitter": (1200, 675),
    "Facebook": (1200, 630)
}

def resize_image(image_path, platforma):
    
    img = image_path

    target_width, target_height = plataforma_tamaños[platforma]

    width, height = img.size

    aspect_ratio = width / height

    if aspect_ratio > 1:  
        new_width = target_width
        new_height = int(target_width / aspect_ratio)
    else:  
        new_height = target_height
        new_width = int(target_height * aspect_ratio)

    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    new_img = Image.new("RGB", (target_width, target_height), (255, 255, 255))
    
    offset_x = (target_width - new_width) // 2
    offset_y = (target_height - new_height) // 2
    
    new_img.paste(img, (offset_x, offset_y))

    return new_img

def ajustar_contraste(image):
    original = image.copy()  
    ecualizada = ImageOps.equalize(original)  
    return  ecualizada

# Función para generar el boceto con los filtros de bordes
def generar_boceto_pil(imagen, filtro_bordes=ImageFilter.FIND_EDGES):
    if imagen is None:
        print("\nPrimero debes cargar una imagen correctamente.")
        return None
    imagen_gray = imagen.convert("L")
    imagen_contornos = imagen_gray.filter(filtro_bordes)
    return imagen_contornos

# Función que aplica el filtro seleccionado
def aplicar_filtro(imagen, filtro_nombre, exponente=10.0):
    filtros = {
        "BLUR": ImageFilter.GaussianBlur(radius=exponente),
        "CONTOUR": ImageFilter.CONTOUR,
        "DETAIL": ImageFilter.DETAIL,
        "EDGE_ENHANCE": ImageFilter.EDGE_ENHANCE,
        "EDGE_ENHANCE_MORE": ImageFilter.EDGE_ENHANCE_MORE,
        "EMBOSS": ImageFilter.EMBOSS,
        "FIND_EDGES": ImageFilter.FIND_EDGES,
        "SHARPEN": ImageFilter.UnsharpMask(
            radius=2, 
            percent=int(exponente * 100),  
            threshold=int(exponente * 3)   
        ),  
        "SMOOTH": ImageFilter.SMOOTH,  
    }
    
    filtro = filtros.get(filtro_nombre.upper())
    if filtro is None:
        raise ValueError(f"\nEl filtro {filtro_nombre} no es válido.")
    
    # Aplicar el filtro
    return imagen.filter(filtro)

filtros_disponibles = [
    "BLUR", "CONTOUR", "DETAIL", "EDGE_ENHANCE", "EDGE_ENHANCE_MORE", 
    "EMBOSS", "FIND_EDGES", "SHARPEN", "SMOOTH"
]

# Menú de opciones
def menu():
    imagen_input = None
    while True:
        print("\nMenú de opciones:")
        print("========================================")
        print("1. Cargar imagen")
        print("2. Redimensionar imagen")
        print("3. Ecualizar imagen")
        print("4. Aplicar filtro FIND EDGES")
        print("5. Aplicar filtro CONTOUR")
        print("6. Aplicar filtro DETAIL")
        print("7. Aplicar Filtros")
        print("8. Salir")
        print("========================================")
        opcion = input("Elige una opción (1-8): ")

        if opcion == "1":
            imagen_path = input("Introduce la ruta de la imagen: ")
            imagen_input = leer_imagen(imagen_path)
            if imagen_input:
                print("\n")
                print("========================================")
                print("Imagen cargada y procesada exitosamente.")
                print("========================================")


        elif opcion == "2":
            if imagen_input is None:
                print("\nPrimero debes cargar una imagen.")
            else:
                while True:
                    print("\nOpciones de tamaños disponibles:")
                    for plataforma, tamaño in plataforma_tamaños.items():
                        print(f"{plataforma}: {tamaño}")
                    
                    plataforma_elegida = input("\nElige una plataforma para obtener su tamaño (Youtube, Instagram, Twitter, Facebook): ")
                    
                    if plataforma_elegida in plataforma_tamaños:
                        tamaño = plataforma_tamaños[plataforma_elegida]
                        print("========================================")
                        print(f"\nSe selecciono el tamaño para {plataforma_elegida}: {tamaño}")
                        print("========================================")
                        break
                    else:
                        print("\nPlataforma no válida, por favor elige una opción válida.")
                    
                imagen_redimensionada = resize_image(imagen_input, plataforma_elegida)
                
                mostrar_imagen(imagen_redimensionada, f"Imagen Redimensionada para{plataforma_elegida}")

                guardar_imagen(imagen_redimensionada, f"imagenes_redimensinada_{plataforma_elegida}", "imagenes_redimensiones")
                
        elif opcion == "3":
            if imagen_input is None:
                print("\nPrimero debes cargar una imagen.")
            else:
                print("========================================")
                imagen_ecualizada = ajustar_contraste(imagen_input)

                mostrar_imagen(imagen_ecualizada, "Imagen Ecualizada")
        
                guardar_imagen(imagen_ecualizada, "imagenes_Ecualizada", "imagenes_contraste")

        elif opcion == "4":
            if imagen_input is None:
                print("\nPrimero debes cargar una imagen.")
            else:
                print("========================================")
                imagen_boceto = generar_boceto_pil(imagen_input, filtro_bordes=ImageFilter.FIND_EDGES)

                mostrar_imagen(imagen_boceto, "Imagen con filtro FIND_EDGES")
                
                guardar_imagen(imagen_boceto, "imagenes_con_filtro_FIND_EDGES", "imagenes_con_bordes")
        
        elif opcion == "5":
            if imagen_input is None:
                print("\nPrimero debes cargar una imagen.")
            else:
                print("========================================")
                imagen_boceto = generar_boceto_pil(imagen_input, filtro_bordes=ImageFilter.CONTOUR)

                mostrar_imagen(imagen_boceto, "Imagen con filtro CONTOUR")

                guardar_imagen(imagen_boceto, "imagenes_con_filtro_CONTOUR", "imagenes_con_bordes")

        elif opcion == "6":
            if imagen_input is None:
                print("\nPrimero debes cargar una imagen.")
            else:
                print("========================================")
                imagen_boceto = generar_boceto_pil(imagen_input, filtro_bordes=ImageFilter.DETAIL)

                mostrar_imagen(imagen_boceto, "Imagen con filtro DETAIL")
        
                guardar_imagen(imagen_boceto, "imagenes_con_filtro_DETAIL", "imagenes_con_bordes")
        
        elif opcion == "7":
            if imagen_input is None:
                print("\nPrimero debes cargar una imagen.")
            else:
                print("========================================")
                while True:
                    print("\nFiltros disponibles:")
                    for i, filtro in enumerate(filtros_disponibles, 1):
                        print(f"{i}. {filtro}")
                        
                    filtro_usuario = input("\nElige un filtro (escribe el nombre): ").strip().upper()
                    
                    if filtro_usuario not in filtros_disponibles:
                        print(f"\nEl filtro '{filtro_usuario}' no es válido. Por favor, elige uno de la lista.")
                    else:
                        print(f"\nFiltro seleccionado: {filtro_usuario}")
                        break

                imagen_filtrada_usuario = aplicar_filtro(imagen_input, filtro_usuario)

                # Mostrar imágenes antes y después del filtro
                plt.figure(figsize=(10, 5))
                plt.subplot(1, 2, 1)
                plt.imshow(imagen_input)
                plt.title("Original")
                plt.axis('off')

                plt.subplot(1, 2, 2)
                plt.imshow(imagen_filtrada_usuario)
                plt.title(f"{filtro_usuario} (Elegido)", color='red')  
                plt.axis('off')

                guardar_imagen(imagen_filtrada_usuario,f"imagen_con_filtro_{filtro_usuario}","imagenes_filtros")
                plt.savefig(f"imagenes_filtros\\imagen_con_filtros_comparacion.jpg")
                plt.show()

                # Mostrar todas las imágenes aplicando todos los filtros
                plt.figure(figsize=(15, 15))

                for i, filtro in enumerate(filtros_disponibles, 1):
                    imagen_filtrada = aplicar_filtro(imagen_input, filtro)
                    plt.subplot(3, 3, i)
                    plt.imshow(imagen_filtrada)
                    plt.title(filtro)
                    plt.axis('off')

                plt.savefig("imagenes_filtros\\filtros_aplicados.jpg")
                plt.show()
                
        elif opcion == "8":
            print("\n")
            print("======================")
            print("Saliendo del programa.")
            print("======================")
            break
        
        else:
            print("\nOpción no válida, por favor elige entre 1 y 8.")

# Ejecutar el menú
if __name__ == "__main__":
    menu()      