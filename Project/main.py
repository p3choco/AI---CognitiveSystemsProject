from kivy.app import App
from kivy.core.image import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
import cv2
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_smile.xml')


class Launch(GridLayout):
    def __init__(self, **kwargs):
        super(Launch, self).__init__(**kwargs)
        self.cols = 1

        self.inside = GridLayout()
        self.inside.cols = 2

        self.inside.add_widget(Label(text="First Name: "))
        self.name = TextInput(multiline=False)
        self.inside.add_widget(self.name)

        self.inside.add_widget(Label(text="Last Name: "))
        self.lastName = TextInput(multiline=False)
        self.inside.add_widget(self.lastName)

        self.inside.add_widget(Label(text="Email: "))
        self.email = TextInput(multiline=False)
        self.inside.add_widget(self.email)

        self.add_widget(self.inside)

        self.submit = Button(text="Submit", font_size=40)
        self.submit.bind(on_press=self.videoTime)
        self.add_widget(self.submit)


    def detect(self, gray, frame):
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (0, 0, 255), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            smiles = smile_cascade.detectMultiScale(roi_gray, 1.8, 50)
            for (sx, sy, sw, sh) in smiles:
                cv2.rectangle(roi_color, (sx, sy), ((sx + sw), (sy + sh)), (0, 255, 0), 2)
        return frame

    def videoTime(self, instance):
        video_capture = cv2.VideoCapture(0)
        while video_capture.isOpened():
            ret, frame = video_capture.read()
            # if not ret:
            #     break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            canvas = self.detect(gray, frame)
            cv2.imshow('Video', canvas)

            # The control breaks once q key is pressed
            if cv2.waitKey(1) & 0xff == ord('q'):
                break
        video_capture.release()


class MyApp(App):
    def build(self):
        return Launch()



if __name__ == '__main__':
    app = MyApp()
    app.run()

