import asyncio
import sys
import os
from pathlib import Path
from dotenv import dotenv_values
from dotenv import load_dotenv

from PySide6.QtCore import QObject, Slot, Signal, QThread, Property, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine, QmlElement
from PySide6.QtQuickControls2 import QQuickStyle

import synth_moth_chat_rc

from synth_moth import TwitchChatBot

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

os.environ["QT_QPA_PLATFORM"] = "windows"

def main():
    app = QApplication(sys.argv)
    QQuickStyle.setStyle("Material")

    engine = QQmlApplicationEngine()

    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    
    config = dotenv_values(".env")

    bot = TwitchChatBot(
        app_id=config['CLIENT_ID'],
        app_secret=config['SECRET'],
        target_channel=config['TARGET_CHANNEL'] 
    )

    engine.rootContext().setContextProperty("twitchBot", bot)

    qml_file = 'qrc:/view.qml'
    engine.load(QUrl(qml_file))   # или qrc:/view.qml

    if not engine.rootObjects():
        print("Ошибка загрузки QML")
        sys.exit(-1)

    sys.exit(app.exec())

if __name__ == "__main__":
    # Этот способ самый надёжный с QtAsyncio
    try:
        main()
    except Exception as e:
        print(f"Критическая ошибка: {e}")
    finally:
        # Принудительная очистка (на всякий случай)
        QApplication.quit()