import os
from datetime import date

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.window import Window
import cv2

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

    def go(self, thing):
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, dt):
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
            print(pokerFrames)
            if pokerFrames == 1000:
                run_smile_ratio.append(smileFrames/pokerFrames)
                print("CHECK", run_smile_ratio)
                pokerFrames = 0
                smileFrames = 0

            for (sx, sy, sw, sh) in smiles:
                cv2.rectangle(roi_color, (sx, sy), ((sx + sw), (sy + sh)), (0, 255, 0), 2)
        return frame
    def save(self, thing):
        global run_smile_ratio
        today = date.today()
        file_name = "Days/" + today.strftime("%Y-%m-%d") + ".txt"

        if os.path.isfile(file_name):
            # Jeśli plik już istnieje, zaktualizuj wartość
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



class MainApp(App):
    def build(self):
        self.title = 'Cognitive Project'
        Window.size = (800, 585)
        launch = Launch()
        return launch

    def on_stop(self):
        launch = self.root
        launch.save(self)
        if launch.capture.isOpened():
            launch.capture.release()

MainApp().run()
