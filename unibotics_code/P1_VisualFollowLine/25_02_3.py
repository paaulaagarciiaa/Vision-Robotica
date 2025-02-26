# Paula Garcia 25 febrero cambiamos al coche ackermann
# Aunque los controladores no funcionasen perfectamente con el otro coche, como ya era capaz de dar una vuelta entera 
# (tardando más tiempo del que debería) intento modificar el código para que funcione en el mismo circuito pero con el coche Ackermann

# Las principales diferencias que hay que tener en cuenta son que el coche de antes puede girar sobre sí mismo,
# puede hacer giros cerrados sin moverse y responde rápido, pero oscila más.
# En cambio, el coche Ackermann no puede girar en el sitio, necesita moverse para girar y es más estable, 
# pero requiere más anticipación en curvas, por lo que habría que limitar su giro y reducir su velocidad en curvas cerradas.

# El coche Ackermann sigue usando setW(), pero el giro depende de la velocidad y del radio de giro del vehículo, por lo que setW() 
# no debería ser mayor a ±1.0, no puede girar bruscamente.
# En lugar de solo usar un punto adelantado, usamos dos puntos adelantados para predecir mejor la curva.

# Dificultades con las que me estoy encontrando es que el coche Ackermann en línea recta me oscila mucho, por la tracción trasera de este,
# y que el PID está sobrecorrigiendo en rectas


from HAL import HAL
from GUI import GUI
import cv2
import numpy as np

# **Configuración inicial**
V_max = 6.5  # Velocidad máxima en rectas (aumentada desde 6.0)
V_min = 3.8  # Velocidad mínima en curvas cerradas (subida desde 3.2)
V_pid_factor = 1.0  # Ajusta la sensibilidad del PID en la velocidad (antes 1.2)

# **Parámetros PID para el giro (suavizado en rectas, más fuerte en curvas)**
Kp_w = 1.1   # Menos agresivo en rectas para evitar oscilaciones
Kd_w = 0.25  # Más amortiguación para eliminar oscilaciones
Ki_w = 0.002  # Mínima contribución del integral para no acumular errores

# **Parámetros PID para la velocidad**
Kp_v = 0.9   # Reduce menos la velocidad en curvas
Kd_v = 0.2   # Más amortiguación para evitar cambios bruscos
Ki_v = 0.01  # Suaviza cambios de velocidad

# **Velocidad angular máxima permitida (simulación de Ackermann)**
W_max = 1.6  # Subida desde 1.3 para mejorar giros cerrados

# **Zona de reducción progresiva de giro en rectas**
DEAD_ZONE = 0.05  # Si el error es menor que esto, reducimos el giro en vez de eliminarlo

# **Inicialización de errores previos**
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
    """Calcula el error con un punto adelantado para anticipar la curva antes de llegar."""
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
        cx_center = int(moments["m10"] / moments["m00"])
    else:
        cx_center = width // 2  # Si falla, asumir el centro de la imagen

    # **Encontrar el punto más adelantado en la imagen (menor Y)**
    farthest_point = min(largest_contour, key=lambda p: p[0][1])  
    cx_far = farthest_point[0][0]  # Coordenada X del punto más adelantado

    # **Ponderar un 90% hacia el punto adelantado y un 10% hacia el centroide**
    cx = int(0.9 * cx_far + 0.1 * cx_center)

    # **Calcular el error normalizado [-1, 1]**
    error = (cx - width // 2) / (width // 2)
    return error

while True:
    image = HAL.getImage()
    mask = detect_red_line(image)
    error = calculate_error(mask)

    if error is not None:
        # **Si el error es menor que la zona muerta, reducimos la corrección en rectas**
        if abs(error) < DEAD_ZONE:
            correction_w = 0.3 * error  # Corrección más leve en rectas
            integral_w = 0  # Evitar acumulación de error en rectas
        else:
            # **PID para el giro**
            derivative_w = error - previous_error_w
            integral_w += error
            correction_w = Kp_w * error + Kd_w * derivative_w + Ki_w * integral_w

            # **Ajustar el giro máximo permitido a [-1.6, 1.6]**
            correction_w = max(-W_max, min(W_max, correction_w))

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
        HAL.setW(-1.0 if previous_error_w > 0 else 1.0)  # Gira más fuerte si se pierde la línea

    GUI.showImage(mask)
