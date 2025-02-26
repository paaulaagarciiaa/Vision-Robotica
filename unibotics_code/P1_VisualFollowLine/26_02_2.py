# Paula García 26 febrero nuevo código mejorado
# Consigo mejorar un poco la velocidad, aunque todavía debería de ir más rápido, con el código anterior tarda aproximadamente
# 14 min en dar una vuelta completa y con este 7 min
# Tengo que intentar mejorar que no se salga tanto de la línea roja, ya que el control de giro no es lo suficientemente preciso, lo bueno que como no deja de
# buscar la línea el coche acaba el circuito sin ninguna complicación

from HAL import HAL
from GUI import GUI
import cv2
import numpy as np

# Aumento velocidad
V_max = 7  # Velocidad máxima en rectas (antes 4.0)
V_min = 4.0  # Velocidad mínima en curvas cerradas (antes 2.0)
V_pid_factor = 1.2  # Ajusta la sensibilidad del PID en la velocidad

# Parámetros PID para el giro
Kp_w = 1.8   # Más agresivo en curvas
Kd_w = 0.05  # Menos amortiguación para reaccionar más rápido
Ki_w = 0.01  # Pequeña compensación de error acumulado

# Parámetros PID para la velocidad
Kp_v = 1.8   # Reduce menos la velocidad en curvas
Kd_v = 0.3   # Más amortiguación para evitar cambios bruscos
Ki_v = 0.01  # Suaviza cambios de velocidad

previous_error_w = 0
integral_w = 0
previous_error_v = 0
integral_v = 0

# Detectar línea roja
def detect_red_line(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 + mask2

    height = mask.shape[0]
    mask[:height // 2, :] = 0  
    mask[-height // 4:, :] = 0  

    return mask

def calculate_error(mask):
    width = mask.shape[1]

    # Encontrar contornos
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        return None  

    # Escoger contorno más grande
    largest_contour = max(contours, key=cv2.contourArea)

    # Centroide del contorno
    moments = cv2.moments(largest_contour)
    if moments["m00"] > 0:
        cx_center = int(moments["m10"] / moments["m00"])
    else:
        cx_center = width // 2  

    # Encontrar el punto más adelantado en la imagen (menor Y)
    farthest_point = min(largest_contour, key=lambda p: p[0][1])  
    cx_far = farthest_point[0][0]  # Coordenada X del punto más adelantado

    # Ponderar un 85% hacia el punto adelantado y un 15% hacia el centroide
    cx = int(0.85 * cx_far + 0.15 * cx_center)

    # Calcular el error normalizado
    error = (cx - width // 2) / (width // 2)
    return error

while True:
    image = HAL.getImage()
    mask = detect_red_line(image)
    error = calculate_error(mask)

    if error is not None:
        # PID para el giro
        derivative_w = error - previous_error_w
        integral_w += error
        correction_w = Kp_w * error + Kd_w * derivative_w + Ki_w * integral_w

        # Aumentar el giro máximo permitido a [-2.5,2.5]
        correction_w = max(-2.5, min(2.5, correction_w))
        HAL.setW(-correction_w)

        # PID para la velocidad
        derivative_v = abs(error) - abs(previous_error_v)  # error absoluto
        integral_v += abs(error)
        correction_v = Kp_v * abs(error) + Kd_v * derivative_v + Ki_v * integral_v

        # Calcular la velocidad dinámica según la curva
        velocidad = V_max - (V_pid_factor * correction_v)
        velocidad = max(V_min, min(V_max, velocidad))
        HAL.setV(velocidad)

        # Actualizar
        previous_error_w = error
        previous_error_v = abs(error)

    else:
        # Si se pierde la línea, sigue girando en la última dirección conocida
        HAL.setW(-0.5 if previous_error_w > 0 else 0.5)

    GUI.showImage(mask)

