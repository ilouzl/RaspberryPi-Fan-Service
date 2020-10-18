import time
import signal
import RPi.GPIO as GPIO

def exit_gracefully(self,signum):
    global pwm
    print("Preparing to close")
    pwm.stop()
    GPIO.cleanup()
    print("All clear to close...")
    exit(1)


signal.signal(signal.SIGINT, exit_gracefully)
signal.signal(signal.SIGTERM, exit_gracefully)

PWM_IO = 12 # this is board IO. BCM io is 18
PWM_FREQ = 100
CONTROL_PERIOD = 5


def get_cpu_temperature():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        t = f.readline ()
    t = float(t)/1000.0
    return t


GPIO.setmode(GPIO.BOARD)
print(GPIO.gpio_function(PWM_IO))
GPIO.setup(PWM_IO, GPIO.OUT)
print(GPIO.gpio_function(PWM_IO))
pwm = GPIO.PWM(PWM_IO, PWM_FREQ)   # Initialize PWM on pwmPin 100Hz frequency
print(GPIO.gpio_function(PWM_IO))
dc = 0

pwm.start(dc)

print("All set, starting control loop")

while True:
    t = get_cpu_temperature()
    # print(t)
    if t > 75:
        new_dc = 100
    elif t > 65:
        new_dc = 85
    elif t > 55:
        new_dc = 70
    elif t > 50:
        new_dc = 60
    else:
        new_dc = 0 
    if new_dc != dc:
        dc = new_dc
        pwm.ChangeDutyCycle(dc)
        print(time.time(), "t=%f, dc=%d"%(t, dc))
    time.sleep(CONTROL_PERIOD)
