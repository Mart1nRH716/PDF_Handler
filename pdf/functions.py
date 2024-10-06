from reportlab.pdfgen import canvas
import PyPDF2
from reportlab.lib.pagesizes import letter
from PIL import Image
from zipfile import ZipFile
import os
from django.conf import settings
# Función para combinar los archivos PDF en uno solo
def merge_pdfs(pdf_files, output_file):
    merger = PyPDF2.PdfMerger()

    for pdf_file in pdf_files:
        merger.append(pdf_file)

    merger.write(output_file)
    merger.close()


def extraer_y_crear_pdf(input_pdf, output_pdf, paginas_a_extraer):
    input_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', input_pdf)
    output_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', 'extraido_pdfs', output_pdf)

    # Verifica si el archivo de entrada existe
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"El archivo {input_path} no existe.")

    # Asegúrate de que el directorio de salida exista
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Extraer páginas del PDF
    with open(input_path, 'rb') as archivo_entrada:
        lector = PyPDF2.PdfReader(archivo_entrada)
        escritor = PyPDF2.PdfWriter()

        for pagina in paginas_a_extraer:
            indice_pagina = pagina - 1
            if 0 <= indice_pagina < len(lector.pages):
                pagina_actual = lector.pages[indice_pagina]
                escritor.add_page(pagina_actual)

        with open(output_path, 'wb') as archivo_salida:
            escritor.write(archivo_salida)

    return output_path  # Devuelve la ruta del archivo de salida


def convertir_imagenes_a_pdf(nombres_imagenes, nombre_pdf_salida):
    # Crea un nuevo archivo PDF
    pdf_salida = canvas.Canvas(nombre_pdf_salida, pagesize=letter)

    # Itera sobre la lista de nombres de imágenes
    for nombre_imagen in nombres_imagenes:
        # Abre la imagen usando Pillow
        imagen = Image.open(nombre_imagen)

        # Obtiene las dimensiones de la página y la imagen
        ancho_pagina, alto_pagina = letter
        ancho_imagen, alto_imagen = imagen.size

        # Calcula el escalado para que la imagen se ajuste a la página
        escala = min(ancho_pagina / ancho_imagen, alto_pagina / alto_imagen)

        # Calcula las nuevas dimensiones de la imagen
        nueva_ancho = ancho_imagen * escala
        nueva_alto = alto_imagen * escala

        # Calcula la posición en la que se debe colocar la imagen en la página
        x = (ancho_pagina - nueva_ancho) / 2
        y = (alto_pagina - nueva_alto) / 2

        # Agrega la imagen a la página del PDF
        pdf_salida.drawInlineImage(nombre_imagen, x, y, width=nueva_ancho, height=nueva_alto)

        # Agrega una nueva página para la siguiente imagen
        pdf_salida.showPage()

    # Cierra el archivo PDF
    pdf_salida.save()
