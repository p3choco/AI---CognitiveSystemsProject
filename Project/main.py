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
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (0, 0, 255), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            smiles = smile_cascade.detectMultiScale(roi_gray, 1.8, 50)
            if len(smiles):
                self.sign.text = "SMILE"
            else:
                self.sign.text = "NOT"

            for (sx, sy, sw, sh) in smiles:
                cv2.rectangle(roi_color, (sx, sy), ((sx + sw), (sy + sh)), (0, 255, 0), 2)
        return frame

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
