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
