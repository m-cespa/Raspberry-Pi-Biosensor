from PWM_Motor import PWM_Motor, initialize_gpio, cleanup_gpio
import time

try:
        initialize_gpio()
        peltier = PWM_Motor(24, 25, 1000)
        peltier.run(100, forward=True)  # Run at 50% power, forward direction
        time.sleep(5)  # Run for 5 seconds
        peltier.run(100, forward=False)  # Run at 50% power, forward direction
        time.sleep(5)  # Run for 5 seconds
        peltier.stop()
finally:
        peltier.cleanup()
        cleanup_gpio()