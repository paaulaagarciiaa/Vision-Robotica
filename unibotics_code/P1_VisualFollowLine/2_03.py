#Mejorando tiempo coche ackerman 88 segundos circuito simple


from HAL import HAL
from GUI import GUI
import cv2
import numpy as np

# **Velocidades optimizadas**
V_max = 7.0   # Velocidad en rectas
V_min = 3.5    # Velocidad mínima en curvas cerradas
V_freno = 2.0  # Velocidad en curvas cerradas

# **PID para el giro**
Kp_w = 1.2     # Corrección más suave en curvas
Kd_w = 1.2     # Menos reacción para evitar sobrecorrecciones
Ki_w = 0.000   # Eliminamos el parámetro integral (I)

# **Límite de giro más controlado**
W_max = 0.6  # Evita giros bruscos en curvas

# **Banda muerta para evitar oscilaciones en rectas**
DEAD_ZONE = 0.08  # Aumentada para reducir vibraciones

# **Suavizado del giro para evitar cambios bruscos**
SMOOTHING_FACTOR = 0.6  # Suaviza la transición de giros

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
    cx = int(0.99 * cx_far + 0.01 * cx_center)  # Anticipación extrema
    error = (cx - width // 2) / (width // 2)
    cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 2)
    cv2.circle(frame, (cx, farthest_point[0][1]), 5, (0, 255, 0), -1)
    cv2.line(frame, (width // 2, frame.shape[0]), (cx, farthest_point[0][1]), (0, 255, 0), 2)
    return error

# Bucle Principal
previous_error_w = 0
previous_correction_w = 0
previous_velocity = V_max
lost_line_counter = 0

# Variables para anticipación y PID adaptativo
curve_threshold = 0.25  # Detección ultratemprana
anticipation_factor = 1.8  # PID superagresivo

while True:
    image = HAL.getImage()
    image = cv2.GaussianBlur(image, (5, 5), 0)
    mask = detect_red_line(image)
    error = calculate_error(mask, image)

    if error is not None:
        abs_error = abs(error)
        is_curve = abs_error > curve_threshold
        if is_curve:
            target_velocity = V_freno  # Frenado a máxima potencia
        else:
            target_velocity = V_max - (abs_error * (V_max - V_min))
        if abs_error > 0.5:
            target_velocity = V_freno

        velocity = (0.7 * previous_velocity) + (0.3 * target_velocity)
        velocity = max(V_min, min(V_max, velocity))
        HAL.setV(velocity)
        previous_velocity = velocity

        derivative_w = error - previous_error_w
        if abs(error) < DEAD_ZONE:
            correction_w = 0
        else:
            if is_curve:
                kp_curve = Kp_w * anticipation_factor
                kd_curve = Kd_w * anticipation_factor
                correction_w = kp_curve * error + kd_curve * derivative_w + Ki_w * error
                if abs(correction_w) < 0.2 : # Giro forzado en curvas.
                    correction_w = 0.3 * (-1 if correction_w < 0 else 1)
            else:
                correction_w = Kp_w * error + Kd_w * derivative_w + Ki_w * error

        correction_w = (SMOOTHING_FACTOR * previous_correction_w) + ((1 - SMOOTHING_FACTOR) * correction_w)
        W_max_curve = W_max * 1.3 if is_curve else W_max
        correction_w = max(-W_max_curve, min(W_max_curve, correction_w))

        if abs_error > 0.6:
            HAL.setW(-correction_w)
        else:
            HAL.setW(-correction_w)

        previous_correction_w = correction_w
        previous_error_w = error
        lost_line_counter = 0

    else:
        # Si se pierde la línea, giro gradual
        lost_line_counter += 1

        if lost_line_counter < 10:
            HAL.setV(3.0)
            # Giro gradual en la dirección de la última corrección
            HAL.setW(previous_correction_w * 0.7)
        else:
            HAL.setV(2.5)
            HAL.setW(0)

    GUI.showImage(image)
