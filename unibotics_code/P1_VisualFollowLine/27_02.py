# Probando distintos parámetros para tener menos oscilaciones e ir más rápido

from HAL import HAL
from GUI import GUI
import cv2
import numpy as np

V_max = 15.0  # Velocidad en rectas
V_min = 3.0   # Velocidad en curvas cerradas
V_freno = 5.5  # Velocidad cuando detecta curva fuerte

# **PID para el giro**
Kp_w = 1.6   # Proporcional: Controla cuánto gira
Kd_w = 1.0   # Derivativo: Amortigua oscilaciones
Ki_w = 0.002  # Integral: Suaviza giros largos

# **Límites de giro**
W_max = 2.8  # Límite de giro para evitar sobrecorrección

# **Detección de la línea roja**
def detect_red_line(image):
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

# **Cálculo del error**
def calculate_error(mask):
    width = mask.shape[1]

    # **Encontrar contornos**
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        return None  # No se detectó la línea

    # **Escoger contorno más grande**
    largest_contour = max(contours, key=cv2.contourArea)

    # **Centroide de la línea**
    moments = cv2.moments(largest_contour)
    if moments["m00"] > 0:
        cx = int(moments["m10"] / moments["m00"])
    else:
        cx = width // 2  # Si falla, asumir centro de imagen

    # **Error normalizado [-1, 1]**
    error = (cx - width // 2) / (width // 2)

    return error

# **Bucle Principal**
previous_error_w = 0
integral_w = 0

while True:
    image = HAL.getImage()
    mask = detect_red_line(image)
    error = calculate_error(mask)

    if error is not None:
        abs_error = abs(error)

        # **Si el error es grande, reducimos velocidad (curva fuerte)**
        velocidad = V_freno if abs_error > 0.2 else V_max
        velocidad = max(V_min, min(V_max, velocidad))
        HAL.setV(velocidad)

        # **PID para el giro**
        derivative_w = error - previous_error_w
        integral_w += error
        correction_w = Kp_w * error + Kd_w * derivative_w + Ki_w * integral_w

        # **Limitar el giro**
        correction_w = max(-W_max, min(W_max, correction_w))
        HAL.setW(-correction_w)

        # **Actualizar errores previos**
        previous_error_w = error

    else:
        # **Si se pierde la línea, girar agresivamente en la última dirección conocida**
        HAL.setW(-3.0 if previous_error_w > 0 else 3.0)

    GUI.showImage(image)
