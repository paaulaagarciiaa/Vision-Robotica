from GUI import GUI
from HAL import HAL
import cv2
import numpy as np

# Parámetros del control PID
kp = 0.005
Ki = 0.0
Kd = 0.002

prev_error = 0
error_sum = 0

# Límite de velocidad angular
MAX_W = 3.0

# Velocidades mínima y máxima
V_MIN = 3.5  # Más rápida en curvas
V_MAX = 10.0  # Mucho más rápida en rectas

def detect_red_line(image):
    """Detecta la línea roja y recorta el área de interés."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 + mask2

    # Recortar imagen para evitar distracciones
    height = mask.shape[0]
    mask[:height // 3, :] = 0
    mask[-height // 6:, :] = 0

    return mask

while True:
    frame = HAL.getImage()
    mask = detect_red_line(frame)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        line_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(line_contour)

        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            # Centro de la imagen
            image_center = frame.shape[1] // 2
            error = cX - image_center
            error_abs = abs(error)

            # Control PID
            p_control = kp * error
            error_sum = max(min(error_sum + error, 500), -500)
            i_control = Ki * error_sum
            d_control = Kd * (error - prev_error)
            prev_error = error

            steering = p_control + i_control + d_control

            # Calcular velocidad angular con límite
            angular_velocity = np.clip(-steering, -MAX_W, MAX_W)

            # Ajustar velocidad según el error (rectas rápidas, curvas más lentas)
            speed = V_MAX - (error_abs / image_center) * (V_MAX - V_MIN)
            speed = np.clip(speed, V_MIN, V_MAX)

            HAL.setV(speed)
            HAL.setW(angular_velocity)

            # **Dibujar contornos y centro de la línea**
            cv2.drawContours(frame, [line_contour], -1, (0, 255, 0), 2)  # Contorno verde
            cv2.circle(frame, (cX, cY), 5, (0, 255, 0), -1)  # Punto verde en el centro de la línea

    GUI.showImage(frame)
