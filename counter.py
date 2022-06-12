#!/usr/bin/env python3
# 2021 nr@bulme.at

from gpiozero import Button
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtWidgets import (QWidget, QLCDNumber,
    QVBoxLayout, QApplication)
from gpiozero import LEDBoard, LED
from signal import pause

DOWN_PIN = 22
RESET_PIN = 27
UP_PIN = 17 
leds=[LED(18),LED(23),LED(24),LED(25)]
#eigene Klasse für LEDs erstellen
#Counter mit den LEDs visualisieren
# nicht in den negativen Bereich zählen, bei 0 wieder zu 15 wechseln

class QtButton(QObject):
    changed = pyqtSignal()

    def __init__(self, pin):
        super().__init__()
        self.button = Button(pin) 
        self.button.when_pressed = self.gpioChange        

    def gpioChange(self):
        self.changed.emit()

class Counter(QWidget):
    minimum = 15
    maximum = 0
    
    def __init__(self):
        super().__init__()
        self.initUi()
        self.count = 0

    def initUi(self):
        self.lcd = QLCDNumber()
        self.lcd.display(0)

        vbox = QVBoxLayout()
        vbox.addWidget(self.lcd)

        self.setLayout(vbox)
        self.setMinimumSize(400, 200)
        self.setWindowTitle('Counter Freißmuth')
        self.show()

    def leds (self, count):
        self.length = len(leds)
        for i in range(self.length):
            bit = 2 ** i # 2^i --> 1 2 4 8 
            value = int(count / bit) 
            if value % 2 == 1:
                self.leds[i].on()
            else:
                self.leds[i].off()
            
    def cUp(self):
        if(self.count >= self.minumum && self.count < self.maximum)
            self.count += 1
        self.leds(self.count)
        self.lcd.display(self.count)
        
    def cDown(self):
        if (self.count == self.self.maximum):
            self.count -= 1
        self.lcd.display(self.count)
        self.leds(self.count)
        
    def cReset(self):
        self.count = self.minimum #0
        self.lcd.display(self.count)

if __name__ ==  '__main__':
    app = QApplication([])
    gui = Counter()
    btnUp = QtButton(UP_PIN)
    btnReset = QtButton(RESET_PIN)
    btnDown = QtButton(DOWN_PIN)
    btnReset.changed.connect(gui.cReset)
    btnDown.changed.connect(gui.cDown)
    btnUp.changed.connect(gui.cUp)
