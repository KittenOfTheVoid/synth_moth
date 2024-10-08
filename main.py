import asyncio
import sys
from pathlib import Path

from PySide6.QtCore import QObject, Slot, Signal, QThread, Property
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, QmlElement
from PySide6.QtQuickControls2 import QQuickStyle
import PySide6.QtAsyncio as QtAsyncio

import synth_moth_chat_rc

from synth_moth import turn_off, turn_on, main_bot_thread
from bridge import chat

QML_IMPORT_NAME = "io.qt.textproperties"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
class Bridge(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot(str, float, str, result=str)
    def getTextColor(self, s, v, c):
        colorIntensity = int(v * 255)
        colorIntensityHex = "" + hex(colorIntensity)[2:]
        if s.lower() == "sred":
            return c[0]+colorIntensityHex.zfill(2)+c[3:]
        elif s.lower() == "sgreen":
            return c[0:3]+colorIntensityHex.zfill(2)+c[5:]
        elif s.lower() == "sblue":
            return c[0:5]+colorIntensityHex.zfill(2)

    @Slot(str, result=str)
    def getColor(self, s):
        if s.lower() == "red":
            return "#ef9a9a"
        elif s.lower() == "green":
            return "#a5d6a7"
        elif s.lower() == "blue":
            return "#90caf9"
        else:
            return "white"

    @Slot(float, result=int)
    def getSize(self, s):
        size = int(s * 34)
        if size <= 0:
            return 1
        else:
            return size

    @Slot()
    def turnOn(self):
        turn_on()


    @Slot()
    def turnOff(self):
        turn_off()

#async def main():
#asyncio.ensure_future(

        
if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    QQuickStyle.setStyle("Material")
    engine = QQmlApplicationEngine()
    print("start")
    qml_file = Path(__file__).parent / 'view.qml'
    engine.load(qml_file)
    main_bot_thread()
        
    if not engine.rootObjects():
        sys.exit(-1)
        
    engine.rootObjects()[0].setProperty('chat', chat)
    app.exec()	
#    QtAsyncio.run()
