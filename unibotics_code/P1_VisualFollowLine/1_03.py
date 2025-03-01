# Paula García 1 de marzo: Adaptación del control al coche Ackermann

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
