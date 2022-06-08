import pyfirmata
import time

comport='COM5'

board=pyfirmata.Arduino(comport)
pin = 9

board.digital[pin].mode = pyfirmata.SERVO



led_1=board.get_pin('d:13:o')
led_2=board.get_pin('d:12:o')
led_3=board.get_pin('d:11:o')
led_4=board.get_pin('d:10:o')



def door(facerec):
    if facerec==1:
        board.digital[pin].write(90)
        time.sleep(5)
        board.digital[pin].write(0)
        



def control(total):
    if total==0:
        led_4.write(0)
    elif total==1:
        led_1.write(0)
        led_2.write(0)
        led_3.write(1)
    elif total==2:
        led_1.write(0)
        led_2.write(1)
        led_3.write(0)
    elif total==3:
        led_1.write(1)
        led_2.write(0)
        led_3.write(0)
    elif total==4:
        led_1.write(0)
        led_2.write(0)
        led_3.write(0)
    elif total==5:
        led_4.write(1)
      
