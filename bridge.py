from PySide6.QtCore import QObject, Slot, Signal, Property

class Chat(QObject):
    newChatMessage = Signal(str)

    def __init__(self):
        QObject.__init__(self)
        self.new_message = ""

    def read_new_message(self):
        return self.new_message

    def set_new_message(self, new_msg):
        self.new_message = new_msg

    chat_message = Property(str, read_new_message, notify=newChatMessage)

chat = Chat()