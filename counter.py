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
leds=[LED(25),LED(24),LED(23),LED(18)]

class QtButton(QObject):
    changed = pyqtSignal()

    def __init__(self, pin):
        super().__init__()
        self.button = Button(pin) 
        self.button.when_pressed = self.gpioChange        

    def gpioChange(self):
        self.changed.emit()

class Counter(QWidget):    
    def __init__(self):
        super().__init__()
        self.initUi()
        self.count = 0
        self.minimum = 0
        self.maximum = 15
        self.bitmax = 16

    def initUi(self):
        self.lcd = QLCDNumber()
        self.lcd.display(0)

        vbox = QVBoxLayout()
        vbox.addWidget(self.lcd)

        self.setLayout(vbox)
        self.setMinimumSize(400, 200)
        self.setWindowTitle('Counter Freißmuth')
        self.show()
    def triggerLeds (self, count):
        for i, led in enumerate(leds): 
            if(count &1<<i):
                led.on()
            else:
                led.off()
            
    def cUp(self):
        if self.count == self.maximum:
            self.count = -1
        self.count += 1
        self.lcd.display(self.count)
        self.triggerLeds(self.count)
        
    def cDown(self):
        if self.count == self.minimum:
            self.count = self.bitmax
        self.count -= 1
        self.lcd.display(self.count)
        self.triggerLeds(self.count)
        
    def cReset(self):
        self.count = self.minimum 
        self.lcd.display(self.count)
        self.triggerLeds(self.count)

if __name__ ==  '__main__':
    app = QApplication([])
    gui = Counter()
    btnUp = QtButton(UP_PIN)
    btnReset = QtButton(RESET_PIN)
    btnDown = QtButton(DOWN_PIN)
    btnReset.changed.connect(gui.cReset)
    btnDown.changed.connect(gui.cDown)
    btnUp.changed.connect(gui.cUp)
    app.exec_()
