import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES  # Para permitir arrastrar y soltar archivos
from PIL import Image, ImageTk
import io
import pyzbar.pyzbar as pyzbar

# Función para detectar y leer el código QR de una imagen
def leer_qr(imagen):
    # Detectar códigos QR en la imagen
    decoded_objects = pyzbar.decode(imagen)
    for obj in decoded_objects:
        # Si se detecta un QR, devolver el contenido
        return obj.data.decode('utf-8')
    return None  # Si no hay código QR

# Función para cargar la imagen y mostrarla
def cargar_imagen(imagen):
    try:
        # Redimensionar para mostrar la imagen en la interfaz
        imagen.thumbnail((300, 300))  # Redimensionar imagen
        img_tk = ImageTk.PhotoImage(imagen)
        
        # Mostrar imagen en la interfaz
        panel.config(image=img_tk)
        panel.image = img_tk  # Mantener referencia para evitar que se pierda
        
        # Intentar leer el código QR de la imagen
        qr_result = leer_qr(imagen)
        if qr_result:
            resultado.config(text=f'Código QR encontrado: {qr_result}')
            # Guardar el enlace en una variable para copiarlo después
            global enlace_qr
            enlace_qr = qr_result
        else:
            resultado.config(text='No se encontró un código QR.')
            enlace_qr = None
    except Exception as e:
        resultado.config(text=f'Error al procesar la imagen: {e}')
        panel.config(image=None)  # Eliminar imagen anterior en caso de error

# Función que se activa cuando se pega una imagen
def pegar_imagen(event=None):
    try:
        # Intentar obtener el contenido del portapapeles
        clipboard_content = root.clipboard_get()
        
        if clipboard_content:
            # Convertir el contenido del portapapeles en imagen
            image = Image.open(io.BytesIO(clipboard_content.encode('latin1')))
            cargar_imagen(image)
    except Exception as e:
        resultado.config(text=f'Error al pegar la imagen: {e}')

# Función que se activa cuando se arrastra una imagen
def arrastrar_imagen(event):
    try:
        # Obtener la ruta de la imagen
        image_path = event.data
        
        # Abrir la imagen desde la ruta
        image = Image.open(image_path)
        cargar_imagen(image)
    except Exception as e:
        resultado.config(text=f'Error al arrastrar la imagen: {e}')

# Función para copiar el enlace al portapapeles
def copiar_al_portapapeles():
    if enlace_qr:
        root.clipboard_clear()  # Limpiar el portapapeles
        root.clipboard_append(enlace_qr)  # Copiar el enlace del QR al portapapeles
        resultado.config(text=f'Enlace copiado al portapapeles: {enlace_qr}')
    else:
        resultado.config(text='No hay enlace para copiar.')

# Configuración de la interfaz gráfica
root = TkinterDnD.Tk()

root.title("Escanear Código QR de Imagen")
root.geometry("500x500")

# Panel para mostrar la imagen
panel = tk.Label(root)
panel.pack(pady=20)

# Etiqueta para mostrar el resultado (enlace del código QR)
resultado = tk.Label(root, text="Pega una imagen con Ctrl+V o arrástrala aquí", wraplength=400)
resultado.pack(pady=20)

# Botón para copiar el enlace al portapapeles
copiar_btn = tk.Button(root, text="Copiar Enlace al Portapapeles", command=copiar_al_portapapeles)
copiar_btn.pack(pady=20)

# Vincular la acción de pegar (Ctrl+V) a la función de pegar_imagen
root.bind("<Control-v>", pegar_imagen)

# Configurar la interfaz para aceptar arrastrar y soltar archivos
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', arrastrar_imagen)

# Inicializar la variable global para almacenar el enlace del código QR
enlace_qr = None

# Iniciar la interfaz gráfica
root.mainloop()
