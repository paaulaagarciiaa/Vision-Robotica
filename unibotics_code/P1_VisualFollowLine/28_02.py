from HAL import HAL
from GUI import GUI
import cv2
import numpy as np

# **Velocidades**
V_max = 20.0  # Velocidad en rectas
V_min = 4.0   # Velocidad mínima en curvas cerradas
V_freno = 3.5  # Velocidad cuando detecta curva fuerte

# **PID para el giro**
Kp_w = 1.8   # Aumentamos la corrección en curvas
Kd_w = 2.5   # Mayor amortiguación para evitar oscilaciones
Ki_w = 0.000  # Eliminamos el parámetro integral (I) porque no es útil

# **Límite de giro**
W_max = 3.0  # Aumentamos el límite de giro para ayudar en curvas cerradas

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

    # **Recortar la imagen (evitar ruido en la parte superior e inferior)**
    height = mask.shape[0]
    mask[:height // 2, :] = 0  # Eliminar parte superior
    mask[-height // 4:, :] = 0  # Eliminar parte inferior

    return mask

# **Cálculo del error con punto adelantado**
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
        cx_center = int(moments["m10"] / moments["m00"])
    else:
        cx_center = width // 2  # Si falla, asumir el centro de la imagen

    # **Punto adelantado (más arriba en la imagen)**
    farthest_point = min(largest_contour, key=lambda p: p[0][1])
    cx_far = farthest_point[0][0]

    # **Ponderamos 95% el punto adelantado y 5% el centroide**
    cx = int(0.95 * cx_far + 0.05 * cx_center)

    # **Calcular el error normalizado [-1, 1]**
    error = (cx - width // 2) / (width // 2)

    return error

# **Bucle Principal**
previous_error_w = 0

while True:
    image = HAL.getImage()
    mask = detect_red_line(image)
    error = calculate_error(mask)

    if error is not None:
        abs_error = abs(error)

        # **Velocidad adaptativa: más baja en curvas cerradas**
        if abs_error > 0.3:
            velocidad = V_freno  # Si el error es alto, frenar más
        else:
            velocidad = V_max - (abs_error * (V_max - V_min))

        velocidad = max(V_min, min(V_max, velocidad))
        HAL.setV(velocidad)

        # **PID para el giro**
        derivative_w = error - previous_error_w
        correction_w = Kp_w * error + Kd_w * derivative_w

        # **Límite de giro**
        correction_w = max(-W_max, min(W_max, correction_w))
        HAL.setW(-correction_w)

        # **Actualizar errores previos**
        previous_error_w = error

    else:
        # **Si se pierde la línea, girar agresivamente en la última dirección conocida**
        HAL.setW(-3.0 if previous_error_w > 0 else 3.0)

    GUI.showImage(image)

