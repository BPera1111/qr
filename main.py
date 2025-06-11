import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageTk
import io
import pyzbar.pyzbar as pyzbar
import pyautogui
import numpy as np
import keyboard
import threading
from time import sleep

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

# Nueva función para capturar área de pantalla
def capturar_area_pantalla():
    resultado.config(text="Selecciona el área con el código QR (presiona ESC para cancelar)")
    root.withdraw()  # Ocultar ventana principal temporalmente
    
    # Crear una nueva ventana transparente a pantalla completa
    selector = tk.Toplevel()
    selector.attributes("-fullscreen", True)
    selector.attributes("-alpha", 0.3)
    selector.configure(bg="black")
    
    area_seleccion = {"inicio_x": 0, "inicio_y": 0, "fin_x": 0, "fin_y": 0, "seleccionando": False}
    rectangulo = None
    
    def comenzar_seleccion(event):
        area_seleccion["inicio_x"] = event.x
        area_seleccion["inicio_y"] = event.y
        area_seleccion["seleccionando"] = True
        
        nonlocal rectangulo
        if rectangulo:
            selector.canvas.delete(rectangulo)
        
        rectangulo = selector.canvas.create_rectangle(
            event.x, event.y, event.x, event.y,
            outline="red", width=2
        )
    
    def actualizar_seleccion(event):
        if area_seleccion["seleccionando"]:
            area_seleccion["fin_x"] = event.x
            area_seleccion["fin_y"] = event.y
            
            selector.canvas.coords(
                rectangulo,
                area_seleccion["inicio_x"], area_seleccion["inicio_y"],
                area_seleccion["fin_x"], area_seleccion["fin_y"]
            )
    
    def finalizar_seleccion(event):
        if area_seleccion["seleccionando"]:
            area_seleccion["fin_x"] = event.x
            area_seleccion["fin_y"] = event.y
            area_seleccion["seleccionando"] = False
            
            # Asegurarse que las coordenadas estén en el orden correcto (inicio < fin)
            x1 = min(area_seleccion["inicio_x"], area_seleccion["fin_x"])
            y1 = min(area_seleccion["inicio_y"], area_seleccion["fin_y"])
            x2 = max(area_seleccion["inicio_x"], area_seleccion["fin_x"])
            y2 = max(area_seleccion["inicio_y"], area_seleccion["fin_y"])
            
            # Capturar el área seleccionada
            selector.destroy()
            sleep(0.2)  # Pequeña pausa para que la ventana desaparezca completamente
            
            try:
                # Capturar el área seleccionada
                screenshot = pyautogui.screenshot(region=(x1, y1, x2-x1, y2-y1))
                
                # Restaurar la ventana principal y procesar la captura
                root.after(100, lambda: procesar_captura(screenshot))
            except Exception as e:
                root.deiconify()
                resultado.config(text=f"Error en la captura: {str(e)}")
    
    def cancelar_seleccion(event=None):
        selector.destroy()
        root.deiconify()
        resultado.config(text="Captura cancelada")
    
    # Canvas transparente para dibujar la selección
    selector.canvas = tk.Canvas(selector, highlightthickness=0)
    selector.canvas.pack(fill="both", expand=True)
    # Aquí está el cambio: usar el mismo color que el selector en lugar de cadena vacía
    selector.canvas.configure(bg="black", highlightthickness=0)
    selector.canvas.bind("<ButtonPress-1>", comenzar_seleccion)
    selector.canvas.bind("<B1-Motion>", actualizar_seleccion)
    selector.canvas.bind("<ButtonRelease-1>", finalizar_seleccion)
    selector.bind("<Escape>", cancelar_seleccion)

    # Agregar un manejador para cerrar la ventana con la tecla 'q'
    def cerrar_ventana(event=None):
        cancelar_seleccion()
    
    selector.bind("q", cerrar_ventana)
    # Agregar un protocolo para el botón de cierre (X)
    selector.protocol("WM_DELETE_WINDOW", cancelar_seleccion)

def procesar_captura(screenshot):
    root.deiconify()  # Mostrar ventana principal nuevamente
    try:
        # Convertir la captura a formato PIL Image
        cargar_imagen(screenshot)
    except Exception as e:
        resultado.config(text=f"Error al procesar la captura: {str(e)}")

# Configuración de la interfaz gráfica
root = TkinterDnD.Tk()

root.title("Escanear Código QR de Imagen")
root.geometry("500x500")

# Panel para mostrar la imagen
panel = tk.Label(root)
panel.pack(pady=20)

# Etiqueta para mostrar el resultado (enlace del código QR)
resultado = tk.Label(root, text="Selecciona un área de pantalla o arrastra una imagen", wraplength=400)
resultado.pack(pady=20)

# Función para volver al estado inicial
def volver_al_inicio():
    panel.config(image=None)
    resultado.config(text="Selecciona un área de pantalla o arrastra una imagen")
    global enlace_qr
    enlace_qr = None

# Nuevo botón para capturar área de pantalla
capturar_btn = tk.Button(root, text="Capturar Área de Pantalla", command=capturar_area_pantalla)
capturar_btn.pack(pady=10)

# Botón para volver al inicio
volver_btn = tk.Button(root, text="Volver al Inicio", command=volver_al_inicio)
volver_btn.pack(pady=10)

# Configurar la interfaz para aceptar arrastrar y soltar archivos
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', arrastrar_imagen)

# Inicializar la variable global para almacenar el enlace del código QR
enlace_qr = None

# Iniciar la interfaz gráfica
root.mainloop()
