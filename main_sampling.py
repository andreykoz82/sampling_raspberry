from machine import Pin
import utime
from oled import OLED_1inch3

LED = Pin(25, Pin.OUT)
SWITCH = Pin(0, Pin.OUT)
SENSOR = Pin(28, Pin.IN)

sampling_plan = {
    2: range(2, 9),
    3: range(9, 16),
    5: range(16, 26),
    8: range(26, 51),
    13: range(51, 91),
    20: range(91, 151),
    32: range(151, 281),
    50: range(281, 501),
    80: range(501, 1201),
    125: range(1201, 3201),
    200: range(3201, 10001),
    315: range(10001, 35001),
    500: range(35001, 150001),
    800: range(150001, 500001),
    1250: range(500001, 1000001)
}

def sample_size_iso(N):
  for k,v in sampling_plan.items():
    if N in v:
      return k


OLED = OLED_1inch3()
   
matrix_keys = [["*", "0", "#"],
               ["7", "8", "9"],
               ["4", "5", "6"],
               ["1", "2", "3"]]

keypad_rows = [18, 17, 16, 15]
keypad_columns = [19, 20, 21]

col_pins = []
row_pins = []

for x in range(0, 4):
    row_pins.append(Pin(keypad_rows[x], Pin.OUT))
    row_pins[x].value(1)
    
for x in range(0, 3):    
    col_pins.append(Pin(keypad_columns[x], Pin.IN, Pin.PULL_DOWN))
    col_pins[x].value(0)

OLED.text("ENTER LOT SIZE:",0,4,OLED.white)
OLED.show()
    
def scankeys():  
    for row in range(4):
        for col in range(3):
            row_pins[row].high()
            key = None
            
            if col_pins[col].value() == 1:
                key_press = matrix_keys[row][col]
                utime.sleep(0.3)
                return key_press
                    
        row_pins[row].low()
        
lot_size = []

while True:
    key = scankeys()
    if key in [str(x) for x in range(10)]:
        lot_size.append(key)
        print(lot_size)
        OLED.text(''.join(lot_size),0, 20, OLED.white)
    OLED.show()
    if key == "#":
        break
    
lot_size = int(''.join(lot_size))
sample_size = sample_size_iso(lot_size)

box_number = lot_size // sample_size
OLED.text('Box num: ' + str(box_number), 0, 30, OLED.white)
OLED.show()

counter = 0
LED.value(0)
SWITCH.value(0)
res = 0

while True:
    if counter == box_number:
        # LED.value(1)
        OLED.text('Reject box: '+str(box_number), 0, 40, OLED.white)
        SWITCH.value(1)
        OLED.show()
        utime.sleep(0.03)
        OLED.fill_rect(0,40,128,20,OLED.balck)
        counter = 0
        # LED.value(0)
        SWITCH.value(0)
    else:
        if SENSOR.value() == 1:
            res = 1
        else:
            counter += res
            res = 0
        
        OLED.text('Working: '+str(counter), 0, 50, OLED.white)
        OLED.show()
        OLED.fill_rect(0,50,128,20,OLED.balck)