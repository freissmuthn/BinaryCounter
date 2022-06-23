#!/usr/bin/env python3
#Freißmuth Nicole 
#Stopwatch Zusatzprojekt

# eine "Stoppuhr" erstellen mit 3 Buttons (stop, start, reset)
# im sekundentakt bis 16 hochzählen 

from gpiozero import Button, LED, LEDBoard
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QTimer
from PyQt5.QtWidgets import (QWidget, QLCDNumber,
    QVBoxLayout, QApplication)

STOP_PIN = 22
RESET_PIN = 27
START_PIN = 17

leds=[LED(25),LED(24),LED(23),LED(18)]

class QtButton(QObject):
    
    changed = pyqtSignal()                              

    def __init__(self, pin):
        super().__init__()
        self.button = Button(pin) 
        self.button.when_pressed = self.gpioChange
        
    def gpioChange(self):
        self.changed.emit()                             

class StopWatch(QWidget):
    timer = QTimer()
    
    def __init__(self):
        super().__init__()
        self.initUi()
        self.count = 0

    def initUi(self):
        self.lcd = QLCDNumber()
        self.lcd.display(0)

        vbox = QVBoxLayout()
        vbox.addWidget(self.lcd)
        
        self.timer=QTimer()
        self.timer.timeout.connect(self.showTime)
        
        self.setLayout(vbox)                          
        self.setMinimumSize(400, 200)
        self.setWindowTitle('Stopwatch')                 
        self.show()
        
    def setLed (self, count):                          
        for i, led in enumerate(leds):
            if (count & 1<<i):                
                led.on()
            else:                
                led.off()
                
    def showTime(self):        
        if self.count == 15:
            self.count = -1   
        self.count += 1
            
        self.lcd.display(self.count)                    
        self.setLed(self.count)
        
    def startCounting(self):
        self.timer.start(1000) 
                
    def stopCounting(self):
        self.lcd.display(self.count)
        self.setLed(self.count)
        self.timer.stop()
                
    def resetCounting(self):
        self.count = 0
        self.lcd.display(self.count)
        self.setLed(self.count)

        
if __name__ ==  '__main__':
    app = QApplication([])
    gui = StopWatch()                                    
    buttonStart = QtButton(START_PIN)                         
    buttonStart.changed.connect(gui.startCounting)               
    buttonStop = QtButton(STOP_PIN)
    buttonStop.changed.connect(gui.stopCounting)
    buttonReset = QtButton(RESET_PIN)
    buttonReset.changed.connect(gui.resetCounting)
    app.exec_()
    