import sys
import speech_recognition as sr
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTextEdit, QPushButton, QVBoxLayout, QFileDialog, QMessageBox


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
        
        #Create the main widget and layout
        central_widget = QWidget(self) #A container widget for layout
        layout = QVBoxLayout(central_widget) #Assign layout to widget

        #Create text area and record button
        self.textEdit = QTextEdit(self)
        self.recordButton = QPushButton('Start Recording', self)
        self.recordButton.clicked.connect(self.recordVoice)

        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)
        layout.addWidget(self.recordButton)

        container = QWidget()
        container.setLayout(layout)
            
    def recordVoice(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.recordButton.setText('Listening...')
            QApplication.processEvents() # Update the GUI
            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)
                self.textEdit.append(text)
            except sr.UnknownValueError:
                self.textEdit.append('Could not understand audio')
            except sr.RequestError:
                self.textEdit.append('Could not connect to the Google Web Speech API')
            
            self.recordButton.setText('Start Recording')
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VoiceNotepad()
    window.show()
    sys.exit(app.exec())
        