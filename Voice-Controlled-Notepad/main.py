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
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTextEdit
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

class VoiceNotepad(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Voice Controlled Notepad')
        self.setGeometry(100, 100, 600, 400)

        # Create widgets
        self.text_edit = QTextEdit()
        self.button_1 = QPushButton('Start Listening')
        self.button_2 = QPushButton('Save to File')
        self.label = QLabel('Ready')

        #Connect button signals to slots
        
        self.button_1.clicked.connect(self.button_1_clicked)
        self.button_2.clicked.connect(self.button_2_clicked)

        # Create layouts
        vbox = QVBoxLayout()
        
        #Add widgets to the layout
        vbox.addWidget(self.text_edit)
        vbox.addWidget(self.button_1)
        vbox.addWidget(self.button_2)

        #Set the main layout
        self.setLayout(vbox)

        self.show()

    def button_1_clicked(self):
        self.label.setText('Listening...')
        self.text_edit.append('Button 1 is pressed')
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout = 5) #Listen for 5 seconds
                text = self.recognizer.recognize_google(audio)
                self.text_edit.append(text + '\n')
                self.label.setText('Ready')
        except sr.UnknownValueError:
            self.label.setText('Speech could not be understood')
        except sr.RequestError as e:
            self.label.setText(f'Could not request results from Google Speech Recognition service; {e}')
        except Exception as e:
            self.label.setText(f'An error occurred: {e}')            
    
    def button_2_clicked(self):
        self.label.setText('Saving to file...')
        self.text_edit.append('Button 2 is pressed')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VoiceNotepad()
    
    app.exec()
