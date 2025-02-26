# Paula Garcia 26 febrero 2025
# Añado PID para la velocidad y modifico PID para tener un giro más agresivo (girar más rápido en las curvas)
# Ya es capaz de recorrer todo el circuito simple lo único que tarda mucho tiempo y oscila bastante en las curvas, tengo que
# cambiar parámetros para poder mejorarlo

from HAL import HAL
from GUI import GUI
import cv2
import numpy as np

# **Configuración inicial**
V_max = 4.0  # Velocidad máxima en rectas
V_min = 1.5  # Velocidad mínima en curvas cerradas
V_pid_factor = 2.0  # Ajusta la sensibilidad del PID en la velocidad

# **Parámetros PID para el giro**
Kp_w = 1.2   # Aumentamos la reacción
Kd_w = 0.2   # Suaviza los cambios
Ki_w = 0.01  # Evita desviaciones acumuladas

# **Parámetros PID para la velocidad**
Kp_v = 2.5  # Ajusta cuánto reduce la velocidad en curvas
Kd_v = 0.1  # Suaviza cambios de velocidad
Ki_v = 0.01  # Evita aceleraciones o frenados bruscos acumulados

previous_error_w = 0
integral_w = 0
previous_error_v = 0
integral_v = 0

def detect_red_line(image):
    """Detecta la línea roja en la imagen y devuelve una máscara binaria."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # **Rango de color rojo en HSV**
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
    width = mask.shape[1]

    # **Encontrar contornos**
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        return None  # No se detectó la línea

    # **Escoger el contorno más grande**
    largest_contour = max(contours, key=cv2.contourArea)

    # **Calcular el centroide del contorno**
    moments = cv2.moments(largest_contour)
    if moments["m00"] > 0:
        cx = int(moments["m10"] / moments["m00"])
    else:
        cx = width // 2  # Si falla, asumir el centro de la imagen

    # **Error normalizado [-1, 1]**
    error = (cx - width // 2) / (width // 2)
    return error

while True:
    image = HAL.getImage()
    mask = detect_red_line(image)
    error = calculate_error(mask)

    if error is not None:
        # **PID para el giro**
        derivative_w = error - previous_error_w
        integral_w += error
        correction_w = Kp_w * error + Kd_w * derivative_w + Ki_w * integral_w

        # **Limitar el giro máximo**
        correction_w = max(-1.5, min(1.5, correction_w))
        HAL.setW(-correction_w)

        # **PID para la velocidad**
        derivative_v = abs(error) - abs(previous_error_v)  # Usamos el error absoluto
        integral_v += abs(error)
        correction_v = Kp_v * abs(error) + Kd_v * derivative_v + Ki_v * integral_v

        # **Calcular la velocidad dinámica según la curva**
        velocidad = V_max - (V_pid_factor * correction_v)
        velocidad = max(V_min, min(V_max, velocidad))
        HAL.setV(velocidad)

        # **Actualizar errores previos**
        previous_error_w = error
        previous_error_v = abs(error)

    else:
        # **Si se pierde la línea, sigue girando en la última dirección conocida**
        HAL.setW(-0.5 if previous_error_w > 0 else 0.5)

    GUI.showImage(mask)
