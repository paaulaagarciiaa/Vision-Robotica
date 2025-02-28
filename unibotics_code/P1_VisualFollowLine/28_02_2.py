#intento con cambio de visualización, ahora visualiza dos líneas con el contorno de la línea roja

from HAL import HAL
from GUI import GUI
import cv2
import numpy as np

# **Velocidades**
V_max = 30.0  # Velocidad en rectas
V_min = 6.0   # Velocidad mínima en curvas suaves
V_freno = 4.0  # Velocidad cuando detecta curva fuerte

# **PID para el giro (ajustado para reducir oscilaciones)**
Kp_w = 1.6   
Kd_w = 1.2   # Reducido de 1.7 a 1.2 para evitar sobrecorrecciones
Ki_w = 0.000  

# **Límite de giro**
W_max = 3.0  

# **Umbral de error para evitar oscilaciones innecesarias**
error_threshold = 0.05  # No corregir si el error es menor que este valor

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
    mask[:height // 2, :] = 0  
    mask[-height // 4:, :] = 0  

    return mask

# **Cálculo del error con punto adelantado y visualización**
def calculate_error(mask, image):
    width = mask.shape[1]

    # **Encontrar contornos**
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        return None  

    # **Escoger contorno más grande**
    largest_contour = max(contours, key=cv2.contourArea)

    # **Centroide de la línea**
    moments = cv2.moments(largest_contour)
    if moments["m00"] > 0:
        cx_center = int(moments["m10"] / moments["m00"])
    else:
        cx_center = width // 2  

    # **Punto adelantado (más arriba en la imagen)**
    farthest_point = min(largest_contour, key=lambda p: p[0][1])
    cx_far = farthest_point[0][0]
    cy_far = farthest_point[0][1]  

    # **Ponderamos 70% el punto adelantado y 30% el centroide**
    cx = int(0.7 * cx_far + 0.3 * cx_center)

    # **Calcular el error normalizado [-1, 1]**
    error = (cx - width // 2) / (width // 2)

    # **Visualización: Dibujar contornos y puntos de referencia**
    cv2.drawContours(image, [largest_contour], -1, (0, 255, 0), 2)  
    cv2.circle(image, (cx_far, cy_far), 5, (0, 255, 0), -1)  
    cv2.circle(image, (cx_center, cy_far), 5, (255, 0, 0), -1)  
    cv2.line(image, (width // 2, cy_far - 20), (width // 2, cy_far + 20), (0, 255, 0), 2)  

    return error

# **Bucle Principal**
previous_error_w = 0

while True:
    image = HAL.getImage()
    mask = detect_red_line(image)
    error = calculate_error(mask, image)

    if error is not None:
        abs_error = abs(error)

        # **Aplicar umbral: Evitar correcciones innecesarias**
        if abs_error > error_threshold:
            derivative_w = error - previous_error_w
            correction_w = Kp_w * error + Kd_w * derivative_w
            correction_w = max(-W_max, min(W_max, correction_w))
            HAL.setW(-correction_w)
        else:
            HAL.setW(0)  # Mantener el coche estable en línea recta

        # **Velocidad adaptativa**
        if abs_error > 0.3:  
            velocidad = V_freno  
        elif abs_error > 0.1:  
            velocidad = V_min + (V_max - V_min) * (1 - abs_error / 0.3)
        else:  
            velocidad = V_max  

        velocidad = max(V_min, min(V_max, velocidad))
        HAL.setV(velocidad)

        # **Actualizar error anterior**
        previous_error_w = error

    else:
        # **Si se pierde la línea, hacer una búsqueda más progresiva**
        HAL.setV(V_min)
        HAL.setW(-2.0 if previous_error_w > 0 else 2.0)  # Antes era -3.0 y 3.0

    # **Mostrar imagen con visualización**
    GUI.showImage(image)
