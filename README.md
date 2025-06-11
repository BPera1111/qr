# Escáner de Códigos QR

## Descripción
Esta aplicación permite escanear y leer códigos QR de manera sencilla y rápida, ya sea desde una imagen en tu ordenador o capturando un área específica de la pantalla.

## Características principales
- **Arrastrar y soltar imágenes** para leer códigos QR
- **Capturar área de pantalla** para escanear códigos QR sin necesidad de tomar capturas previas
- **Interfaz sencilla** e intuitiva
- **Detección automática** del contenido del código QR
- **Selección precisa** mediante rectángulo de selección visible

## Requisitos
- Python 3.x
- Bibliotecas:
  - tkinter / tkinterdnd2
  - PIL (Pillow)
  - pyzbar
  - pyautogui
  - numpy

## Instalación

### Usando pip
Instala las dependencias necesarias:
```bash
pip install pillow pyzbar pyautogui numpy tkinterdnd2
```

### Desde el código fuente
1. Clona este repositorio:

2. Instala las dependencias:
```bash
pip install pillow pyzbar pyautogui numpy tkinterdnd2
```

## Uso

### Ejecución normal
```bash
python main.py
```

## Cómo utilizar la aplicación

### Método 1: Arrastrar y soltar
1. Abre la aplicación
2. Arrastra una imagen con código QR a la ventana
3. La aplicación leerá automáticamente el código y mostrará su contenido

### Método 2: Capturar área de pantalla
1. Haz clic en el botón "Capturar Área de Pantalla"
2. La ventana principal se ocultará y aparecerá una capa transparente
3. Haz clic y arrastra para seleccionar el área que contiene el código QR
4. Al soltar el botón del ratón, se capturará el área y se procesará automáticamente
5. Para cancelar, presiona ESC o la tecla Q

### Reinicio
- Usa el botón "Volver al Inicio" para limpiar la imagen y resultados actuales

## Licencia
Este proyecto está bajo la Licencia MIT.

---

*Desarrollado por TU_NOMBRE*