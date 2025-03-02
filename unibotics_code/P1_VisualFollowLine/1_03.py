# Paula García 1 de marzo --> Adaptación del control al coche Ackermann

# Objetivo:
# Se busca adaptar el código para que el coche Ackermann complete el mismo circuito en aproximadamente 50 segundos, 
# como lo hacía el coche anterior. Para ello, es necesario modificar la lógica de control, ya que el comportamiento 
# del coche Ackermann es diferente.

# Diferencias clave entre ambos coches:
# El coche anterior:
#   - Puede girar sobre sí mismo sin necesidad de moverse.
#   - Puede hacer giros cerrados instantáneos, lo que permite correcciones rápidas.
#   - Es más reactivo, pero tiende a oscilar más en curvas debido a su sistema de tracción y dirección.

# El coche Ackermann:
#   - No puede girar sobre su propio eje, necesita moverse para cambiar de dirección.
#   - Es más estable en curvas, pero requiere mayor anticipación en los giros.
#   - Su capacidad de giro está limitada por su radio de giro, lo que implica que no puede hacer correcciones bruscas.

# Ajustes necesarios para el coche Ackermann:
# - Se sigue utilizando `setW()`, pero en este caso, el valor de `W` representa la curvatura del giro y no un giro instantáneo.
# - `setW()` no debe ser mayor a ±1.0, ya que giros más agresivos pueden hacer que el coche pierda tracción.
# - En lugar de solo un punto adelantado, se usan dos puntos adelantados para prever mejor la curvatura de la trayectoria.
# - Es necesario limitar la velocidad en curvas cerradas para evitar que el coche se salga de la trayectoria.

# Dificultades encontradas:
# - En línea recta, el coche Ackermann oscila más que el anterior. Esto puede deberse a su sistema de tracción trasera, 
#   que introduce cierto retraso en la respuesta del giro.
# - El PID está sobrecorrigiendo en rectas, posiblemente porque el coche reacciona con cierto retraso y las pequeñas 
#   variaciones en la dirección se amplifican a altas velocidades. Se debe ajustar `Kd` para amortiguar estos efectos.

# Sin modificar el código, el coche ackerman es capaz de dar la vuelta entera, tardando aproximadamente algo más de 2 minutos y medio, y 
# oscilando mucho más en las rectas, podemos ver que es un coche más nerviso.

# Para que el coche vibre menos una idea es meter una banda muerta, para evitar que el coche reaccione a pequeñas variaciones en el error.
# Metíendole la banda muerta de 0.07 oscila un poco menos en rectas (aunque sigue oscilando), pero hay veces que se acaba chocando,
# va el coche un poco sin control.

# También he probado en ponerle un umbral al valor absoluto

from HAL import HAL
from GUI import GUI
import cv2
import numpy as np

# **Velocidades optimizadas**
V_max = 20.0   # Velocidad en rectas
V_min = 6.0    # Velocidad mínima en curvas cerradas
V_freno = 4.5  # Velocidad en curvas cerradas

# **PID para el giro**
Kp_w = 1.2     # Corrección más suave en curvas
Kd_w = 1.2     # Menos reacción para evitar sobrecorrecciones
Ki_w = 0.000   # Eliminamos el parámetro integral (I)

# **Límite de giro más controlado**
W_max = 0.5  # Evita giros bruscos en curvas cerradas

# **Banda muerta para evitar oscilaciones en rectas**
DEAD_ZONE = 0.08  # Aumentada para reducir vibraciones

# **Suavizado del giro para evitar cambios bruscos**
SMOOTHING_FACTOR = 0.5  # Suaviza la transición de giros

# **Umbrales de error**
ERROR_CURVA_MODERADA = 0.3  # Umbral para reducir velocidad de forma progresiva
ERROR_CURVA_CERRADA = 0.5   # Umbral para aplicar freno más fuerte

# **Detección de la línea roja**
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

# **Cálculo del error con punto adelantado**
def calculate_error(mask, frame):
    width = mask.shape[1]

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        return None  

    largest_contour = max(contours, key=cv2.contourArea)

    moments = cv2.moments(largest_contour)
    if moments["m00"] > 0:
        cx_center = int(moments["m10"] / moments["m00"])
    else:
        cx_center = width // 2  

    farthest_point = min(largest_contour, key=lambda p: p[0][1])
    cx_far = farthest_point[0][0]

    cx = int(0.95 * cx_far + 0.05 * cx_center)
    error = (cx - width // 2) / (width // 2)

    cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 2)  
    cv2.circle(frame, (cx, farthest_point[0][1]), 5, (0, 255, 0), -1)  
    cv2.line(frame, (width // 2, frame.shape[0]), (cx, farthest_point[0][1]), (0, 255, 0), 2)

    return error

# **Bucle Principal**
previous_error_w = 0
previous_correction_w = 0  # Guardar la última corrección de giro para suavizado
lost_line_counter = 0  

while True:
    image = HAL.getImage()
    mask = detect_red_line(image)
    error = calculate_error(mask, image)

    if error is not None:
        abs_error = abs(error)

        # **Reducción de velocidad con umbrales**
        if abs_error > ERROR_CURVA_CERRADA:
            velocidad = max(V_freno - 1.0, V_max - (abs_error * (V_max - V_min)) * 1.8)  
        elif abs_error > ERROR_CURVA_MODERADA:
            velocidad = max(V_freno, V_max - (abs_error * (V_max - V_min)) * 1.3)  
        else:
            velocidad = V_max - (abs_error * (V_max - V_min))

        velocidad = max(V_min, min(V_max, velocidad))
        HAL.setV(velocidad)

        # **PID para el giro con banda muerta**
        derivative_w = error - previous_error_w

        if abs(error) < DEAD_ZONE:
            correction_w = 0  
        else:
            correction_w = Kp_w * error + Kd_w * derivative_w

        # **Aplicar suavizado de giro**
        correction_w = (SMOOTHING_FACTOR * previous_correction_w) + ((1 - SMOOTHING_FACTOR) * correction_w)

        # **Límite de giro restringido**
        correction_w = max(-W_max, min(W_max, correction_w))
        HAL.setW(-correction_w)

        # **Guardar valores previos**
        previous_correction_w = correction_w
        previous_error_w = error
        lost_line_counter = 0

    else:
        # **Si se pierde la línea, reducir velocidad y corregir con más suavidad**
        lost_line_counter += 1

        if lost_line_counter < 10:
            HAL.setV(4.0)  # Reduce más la velocidad
            HAL.setW(-0.5 if previous_error_w > 0 else 0.5)  # Giro mucho más controlado
        else:
            HAL.setV(3.0)  
            HAL.setW(0)  

    GUI.showImage(image)

