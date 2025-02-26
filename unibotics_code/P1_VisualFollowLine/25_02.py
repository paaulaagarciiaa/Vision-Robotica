# Paula García 25 febrero
# Primer código entendiendo el problema
# Primer problema es reconocer la línea roja, para ello se convierte la imagen a HSV y filtra los colores rojos.
# Luego, elimina partes irrelevantes de la imagen para evitar ruido.
# Ajustar la dirección con un PID para corregir giro y seguir la línea
# Calcula el error de posición ponderado entre el centroide y el punto adelantado, modifica la velocidad de forma proporcional a la magnitud del error,
# redunciéndola en curvas
# El coche cuando llega a la primera curva se acaba saliendo y se choca contra la pared, tengo que seguir ajustando para corregirlo


from HAL import HAL
from GUI import GUI
import cv2
import numpy as np

HAL.setV(2)  

# Parámetros PID ajustados para mejorar las curvas
Kp = 0.8  # Aumentamos la reacción
Kd = 0.15  # Disminuimos la amortiguación
Ki = 0.02  # Ligeramente más integral para curvas largas

previous_error = 0
integral = 0

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

    # Recortar imagen
    height = mask.shape[0]
    mask[:height // 2, :] = 0  
    mask[-height // 4:, :] = 0  

    return mask

def calculate_error(mask):
    moments = cv2.moments(mask)
    width = mask.shape[1]

    if moments["m00"] > 0:
        cx = int(moments["m10"] / moments["m00"])  # Centroide de la línea roja
        error = (cx - width // 2) / (width // 2)  # Normalizar error
    else:
        error = 0 

    return error

while True:
    image = HAL.getImage()
    mask = detect_red_line(image)
    error = calculate_error(mask)

    # Control PID
    derivative = error - previous_error
    integral += error
    correction = Kp * error + Kd * derivative + Ki * integral

    # Ajustar la velocidad angular al rango [-1.5, 1.5]
    correction = max(-1.5, min(1.5, correction))

    HAL.setW(-correction)
    previous_error = error

    GUI.showImage(mask)

