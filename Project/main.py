import os
from collections import deque
from datetime import date

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.window import Window
import cv2
import matplotlib.pyplot as plt

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

class Launch(GridLayout):

    def __init__(self, **kwargs):
        super(Launch, self).__init__(**kwargs)
        self.cols = 1
        self.capture = cv2.VideoCapture(0)
        self.image = Image(allow_stretch=True)
        self.sign = Label(size_hint_y= 0.3)
        self.add_widget(self.image)
        self.add_widget(self.sign)
        global pokerFrames
        global smileFrames
        global run_smile_ratio
        pokerFrames = 0
        smileFrames = 0
        run_smile_ratio = []
        self.go(self)

    def go(self, unused):
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, unused):
        ret, frame = self.capture.read()

        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = self.detect(gray, frame)
            frame = cv2.flip(frame, 0)

            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(frame.tobytes(), colorfmt='bgr', bufferfmt='ubyte')

            self.image.texture = texture

    def detect(self, gray, frame):
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        global pokerFrames
        global smileFrames
        global run_smile_ratio

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (0, 0, 255), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            smiles = smile_cascade.detectMultiScale(roi_gray, 1.8, 50)

            if len(smiles):

                self.sign.text = "SMILE"
                smileFrames +=1;
            else:
                self.sign.text = "NOT"

            pokerFrames += 1;

            if pokerFrames >= 1000:
                run_smile_ratio.append(smileFrames/pokerFrames)
                print("CHECK", run_smile_ratio)
                self.save(self)
                pokerFrames = 0
                smileFrames = 0

            for (sx, sy, sw, sh) in smiles:
                cv2.rectangle(roi_color, (sx, sy), ((sx + sw), (sy + sh)), (0, 255, 0), 2)
        return frame
    def save(self, unused):
        global run_smile_ratio

        if not len(run_smile_ratio):
            print("Nothing to save")
            return

        today = date.today()
        file_name = "Days/" + today.strftime("%Y-%m-%d") + ".txt"

        if os.path.isfile(file_name):

            with open(file_name, "r") as file:
                lines = file.readlines()
                if len(lines) >= 2:
                    old_ratio = float(lines[0])
                    old_cycle_num = int(lines[1])


            new_cycle_num = len(run_smile_ratio)
            new_ratio = sum(run_smile_ratio) / new_cycle_num
            cycle_num = old_cycle_num + new_cycle_num
            ratio = (old_ratio *old_cycle_num + new_ratio*new_cycle_num)/ cycle_num
            print("File updated", file_name)


        else:
            ratio = sum(run_smile_ratio) / len(run_smile_ratio)
            cycle_num = len(run_smile_ratio)
            print("File created", file_name)


        with open(file_name, "w") as file:
            file.write(str(ratio) + "\n")
            file.write(str(cycle_num) + "\n")

        self.save_last_hour(run_smile_ratio.pop())
        run_smile_ratio = []

        self.show_plot(self)

    def show_plot(self, unused):
        today = date.today()
        file_name = "Days/" + today.strftime("%Y-%m-%d") + ".txt"
        if os.path.isfile(file_name):

            with open(file_name, "r") as file:
                lines = file.readlines()
                if len(lines) >= 2:
                    ratio = float(lines[0])

        else:
            print("Brak Danych")

        labels = ['Smile', 'Not Smile']
        sizes = [ratio, 1 - ratio]
        colors = ['orange', 'purple']

        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')  # Ustawienie równych osi
        plt.title('Ratio of Smile vs Not Smile')

        plt.show()

    def save_last_hour(self,new_value):
        file_name = "Last_Hour" + ".txt"
        max_values = 24  # Maksymalna liczba przechowywanych wartości
        values = deque(maxlen=max_values)

        # Odczytaj istniejące wartości z pliku
        if os.path.isfile(file_name):
            with open(file_name, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    value = float(line.strip())  # Konwersja na odpowiedni typ
                    values.append(value)

        # Dodaj nową wartość
        values.append(new_value)

        # Zapisz wartości z powrotem do pliku
        with open(file_name, 'w') as file:
            for value in values:
                file.write(str(value) + '\n')

        hour_ratio = sum(values)/len(values)
        labels = ['Smile', 'Not Smile']
        sizes = [hour_ratio, 1 - hour_ratio]
        colors = ['orange', 'purple']

        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')  # Ustawienie równych osi
        plt.title('Last Hour Smiles')

        plt.show()


class MainApp(App):
    def build(self):
        self.title = 'Cognitive Project'
        Window.size = (800, 585)
        launch = Launch()
        return launch

    def on_stop(self):
        launch = self.root
        if launch.capture.isOpened():
            launch.capture.release()

MainApp().run()
