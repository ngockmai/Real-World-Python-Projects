import sys
import speech_recognition as sr
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDial,
    QDoubleSpinBox,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QSlider,
    QSpinBox,
    QWidget,
    QVBoxLayout
)



# class SpeechRecognitionThread(QThread):
#     """Thread for speech recognition to avoid freezing the GUI"""
#     recognized_text = pyqtSignal(str)
#     error_signal = pyqtSignal(str)
#     def run(self):
#         recognizer = sr.Recognizer()
#         with sr.Microphone() as source:
#             try:
#                 audio = recognizer.listen(source, timeout = 5) #Listen for 5 seconds
#                 text = recognizer.recognize_google(audio)
#                 self.recognized_text.emit(text)
#             except sr.WaitTimeoutError:
#                 self.error_signal.emit('No speech detected within the timeout period')
#             except sr.UnknownValueError:
#                 self.error_signal.emit('Could not understand audio')
#             except sr.RequestError:
#                 self.error_signal.emit('Could not connect to the Google Web Speech API')
#             except Exception as e:
#                 self.error_signal.emit(f"An error occurred: {e}")

class VoiceNotepad(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Voice Controlled Notepad')
        self.setGeometry(100, 100, 600, 400)

        # Create the main widget and layout
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        widget = QLabel("Hello")
        font = widget.font()
        font.setPointSize(20)
        widget.setFont(font)
        widget.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        self.setCentralWidget(widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VoiceNotepad()
    window.show()
    sys.exit(app.exec())
