from HAL import HAL
from GUI import GUI
import cv2
import numpy as np

# Configuración inicial
HAL.setV(2)  # Reducimos la velocidad para mejorar el control en curvas

# Parámetros PID ajustados para mejorar las curvas
Kp = 0.8  # Aumentamos la reacción
Kd = 0.15  # Disminuimos la amortiguación
Ki = 0.02  # Ligeramente más integral para curvas largas

previous_error = 0
integral = 0

def detect_red_line(image):
    """Detecta la línea roja en la imagen y devuelve una máscara binaria."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Rango de color rojo en HSV
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 + mask2

    # **Recortar la imagen** (evitar ruido en la parte superior e inferior)
    height = mask.shape[0]
    mask[:height // 2, :] = 0  # Eliminar parte superior
    mask[-height // 4:, :] = 0  # Eliminar parte inferior

    return mask

def calculate_error(mask):
    """Calcula el error como la diferencia entre el centro de la línea roja y el centro de la imagen."""
    moments = cv2.moments(mask)
    width = mask.shape[1]

    if moments["m00"] > 0:
        cx = int(moments["m10"] / moments["m00"])  # Centroide de la línea roja
        error = (cx - width // 2) / (width // 2)  # Normalizar error en rango [-1, 1]
    else:
        error = 0  # No se detectó la línea, mantener el último valor

    return error

while True:
    image = HAL.getImage()
    mask = detect_red_line(image)
    error = calculate_error(mask)

    # Control PID
    derivative = error - previous_error
    integral += error
    correction = Kp * error + Kd * derivative + Ki * integral

    # Ajustar la velocidad angular al rango [-1, 1]
    correction = max(-1.5, min(1.5, correction))

    HAL.setW(-correction)
    previous_error = error

    GUI.showImage(mask)

