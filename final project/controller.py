import pyfirmata
import time

comport='COM4'
board=pyfirmata.ArduinoMega(comport)
time.sleep(1)

board.digital[9].mode = pyfirmata.SERVO

servo = board.get_pin('d:9:o')
led_1=board.get_pin('d:13:o')
# led_2=board.get_pin('d:12:o')
# led_3=board.get_pin('d:11:o')
led_4=board.get_pin('d:10:o')


def door(facerec):
    print(facerec)
    if facerec==1:
        servo.write(180)
        time.sleep(5)
        servo.write(0)
        time.sleep(3)
        led_4.write(1)
        

def control(total):
    print(total)
    if total==0:
        led_4.write(0)
    elif total==1:
        led_1.write(1)
    elif total==2:
        led_1.write(0)
    elif total==3:
        servo.write(180)
    elif total==4:
        servo.write(0)
    elif total==5:
        led_4.write(1)
      
if __name__ == '__main__':
    main()