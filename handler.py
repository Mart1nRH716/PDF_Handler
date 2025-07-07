from tkinter import Image
from reportlab.pdfgen import canvas
import PyPDF2
from reportlab.lib.pagesizes import letter
from PIL import Image


# Función para combinar los archivos PDF en uno solo
def merge_pdfs(pdf_files, output_file):
    merger = PyPDF2.PdfMerger()

    for pdf_file in pdf_files:
        merger.append(pdf_file)

    merger.write(output_file)
    merger.close()

def extraer_y_crear_pdf(input_pdf, output_pdf, paginas_a_extraer):
    # Abre el archivo PDF de entrada en modo binario
    with open(input_pdf, 'rb') as archivo_entrada:
        # Crea un objeto de lector de PDF
        lector = PyPDF2.PdfReader(archivo_entrada)

        # Crea un objeto de escritor de PDF para el nuevo archivo
        escritor = PyPDF2.PdfWriter()

        # Itera sobre las páginas que se quieren extraer
        for pagina in paginas_a_extraer:
            # Ajusta el índice de la página para que sea compatible con Python (comienza desde 0)
            indice_pagina = pagina - 1

            # Verifica si el índice de la página está dentro del rango del PDF
            if 0 <= indice_pagina < len(lector.pages):
                # Obtiene la página y la agrega al nuevo archivo
                pagina_actual = lector.pages[indice_pagina]
                escritor.add_page(pagina_actual)

        # Abre el archivo de salida en modo binario y escribe las páginas seleccionadas
        with open(output_pdf, 'wb') as archivo_salida:
            escritor.write(archivo_salida)

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

# # Ejemplo dcomo pasar imagenes a pdf
# nombres_imagenes = ['92.jpg', '96.jpg']  # Reemplaza con los nombres de tus archivos de imagen
# nombre_pdf_salida = 'Tarea1.pdf'  # Nombre del archivo PDF de salida

# convertir_imagenes_a_pdf(nombres_imagenes, nombre_pdf_salida)




# Combinar pdfs

# Lista de nombres de los archivos PDF que deseas combinar
pdf_files = ["CartaPasante.pdf", "Certificado.pdf", "ConstanciaExamen4h_Val.pdf", "ConstanciaSS_2021630594.pdf",
             "AcuseTTEntregado(CartaResponsiva).pdf", ]

# output_pdf = "Romero_Hernandez_MartinManuel_2021630594.pdf"
output_pdf = "ROMERO_HERNANDEZ_MARTIN_MANUEL_2021630594.pdf"
# Llama a la función para combinar los PDFs
merge_pdfs(pdf_files, output_pdf)
print(f"Se han combinado {len(pdf_files)} archivos PDF en '{output_pdf}'.")



# # Ejemplo de exraccion de paginas de una pdf
# input_pdf = 'Estado de Cuenta.pdf'  # Reemplaza con el nombre de tu archivo de entrada
# output_pdf = 'primer_hoja_ec.pdf'  # Nombre del archivo de salida
# paginas_a_extraer = [2]  # Lista de números de página que se quieren extraer

# extraer_y_crear_pdf(input_pdf, output_pdf, paginas_a_extraer)