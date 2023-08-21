import os
import time
from collections import deque
from datetime import date, datetime, timedelta
import cv2
import numpy as np
import matplotlib.pyplot as plt
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty



# Load the Haar cascade classifiers for face and smile detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

class Video(GridLayout):

    def __init__(self, **kwargs):
        super(Video, self).__init__(**kwargs)
        self.cols = 1
        self.capture = cv2.VideoCapture(0)
        self.image = Image(allow_stretch=True)
        self.sign = Label(size_hint_y=0.3)
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
        # Schedule the update function to be called at 30 frames per second
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, unused):
        ret, frame = self.capture.read()

        if ret:
            # Convert the frame to grayscale and detect faces and smiles
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = self.detect(gray, frame)
            frame = cv2.flip(frame, 0)

            # Create a texture from the frame and assign it to the image widget
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(frame.tobytes(), colorfmt='bgr', bufferfmt='ubyte')
            self.image.texture = texture

    def detect(self, gray, frame):
        # Detect faces in the grayscale frame
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        global pokerFrames
        global smileFrames
        global run_smile_ratio

        for (x, y, w, h) in faces:
            # Draw a rectangle around the detected face
            cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (0, 0, 255), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]

            # Detect smiles in the region of interest (face)
            smiles = smile_cascade.detectMultiScale(roi_gray, 1.8, 50)

            if len(smiles):
                # Display "SMILE" if a smile is detected
                self.sign.text = "SMILE"
                smileFrames += 1
            else:
                # Display "NOT" if no smile is detected
                self.sign.text = "NOT"

            pokerFrames += 1

            if pokerFrames >= 1000:
                # Calculate the smile ratio and save the data
                run_smile_ratio.append(smileFrames / pokerFrames)
                print("CHECK", run_smile_ratio)
                self.save(self)
                pokerFrames = 0
                smileFrames = 0

            for (sx, sy, sw, sh) in smiles:
                # Draw a rectangle around the detected smile
                cv2.rectangle(roi_color, (sx, sy), ((sx + sw), (sy + sh)), (0, 255, 0), 2)
        return frame

    def save(self, unused):
        global run_smile_ratio

        if not len(run_smile_ratio):
            print("Nothing to save")
            return

        # Get the current date
        today = date.today()
        file_name = "Days/" + today.strftime("%Y-%m-%d") + ".txt"

        if os.path.isfile(file_name):
            # If the file already exists, read the previous ratio and cycle number
            with open(file_name, "r") as file:
                lines = file.readlines()
                if len(lines) >= 2:
                    old_ratio = float(lines[0])
                    old_cycle_num = int(lines[1])

            # Calculate the new ratio and cycle number
            new_cycle_num = len(run_smile_ratio)
            new_ratio = sum(run_smile_ratio) / new_cycle_num
            cycle_num = old_cycle_num + new_cycle_num
            ratio = (old_ratio * old_cycle_num + new_ratio * new_cycle_num) / cycle_num
            print("File updated", file_name)

        else:
            # If the file doesn't exist, calculate the ratio and cycle number from scratch
            ratio = sum(run_smile_ratio) / len(run_smile_ratio)
            cycle_num = len(run_smile_ratio)
            print("File created", file_name)

        # Write the ratio and cycle number to the file
        with open(file_name, "w") as file:
            file.write(str(ratio) + "\n")
            file.write(str(cycle_num) + "\n")

        # Save the last hour's smile ratio and display the pie chart
        self.save_last_hour(run_smile_ratio.pop())
        run_smile_ratio = []





    def save_last_hour(self, new_value):
        file_name = "Last_Hour" + ".txt"
        max_values = 120  # Maximum number of stored values
        values = deque(maxlen=max_values)

        # Read existing values from the file
        if os.path.isfile(file_name):
            with open(file_name, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    value = float(line.strip())  # Convert to the appropriate type
                    values.append(value)

        # Add the new value
        values.append(new_value)

        # Write the values back to the file
        with open(file_name, 'w') as file:
            for value in values:
                file.write(str(value) + '\n')


class VideoWindow(Screen):
    def __init__(self, **kwargs):
        super(VideoWindow, self).__init__(**kwargs)
        self.layout = Video()
        self.add_widget(self.layout)
        self.add_widget(Button(text="Show Stats",  background_color='#503C9A', background_normal='', size_hint=(0.3, 0.05), pos_hint={'x': 0.33, 'y': 0.025}, on_press=self.go_to_stats))

    def go_to_stats(self, instance):
        app = App.get_running_app()
        app.root.current = "stats"


class StatsWindow(Screen):

    btn = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(StatsWindow, self).__init__(**kwargs)
        self.layout = GridLayout(cols=1)
        self.add_widget(self.layout)
        self.add_widget(Button(text="Go to video", background_color='#503C9A', background_normal='', size_hint=(0.3, 0.05), pos_hint={'x': 0.33, 'y': 0.025}, on_press=self.go_to_video))
        self.display_all_plots(self)
        Clock.schedule_interval(self.display_all_plots, 10)
        self.size = [1000,800]
        print(self.size)

    def do_last_hour_plot(self, unused):
        # Read the smile ratios from the "Last_Hour.txt" file
        smile_ratios = []

        with open("Last_Hour.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                smile_ratios.append(float(line))
        print(smile_ratios)

        ratio = sum(smile_ratios)/len(smile_ratios)
        self.layout.clear_widgets()
        if smile_ratios:
            labels = ['Smile', 'Not Smile']
            sizes = [ratio, 1 - ratio]
            colors = ['#FFA500', 'purple']

            # Create a pie chart and save it as an image file
            plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            plt.axis('equal')
            plt.title('Last Hour')

    def do_day_plot(self, unused):
        today = date.today()
        ratio = 0
        file_name = "Days/" + today.strftime("%Y-%m-%d") + ".txt"
        if os.path.isfile(file_name):
            # If the file exists, read the ratio
            with open(file_name, "r") as file:
                lines = file.readlines()
                if len(lines) >= 2:
                    ratio = float(lines[0])
        else:
            print("No Data")

        labels = ['Smile', 'Not Smile']
        sizes = [ratio, 1 - ratio]
        colors = ['#FFA500', 'purple']

        # Display the pie chart of smile vs not smile ratio
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        plt.title('This Day')

        # plt.show()

            
    def go_to_video(self, instance):
        app = App.get_running_app()
        app.root.current = "video"

    def do_week_plot(self, unused):
        from datetime import date, datetime, timedelta

        # Get the path to the directory with data files
        data_dir = 'Days/'

        # Get today's date
        today = date.today()

        # Create lists to store data about the time spent in the app and the amount of smile time
        app_time = []
        smile_time = []

        # Iterate over the last 7 days
        for i in range(7):
            # Calculate the date for the given day
            date = today - timedelta(days=i)

            # Create the path to the data file
            file_path = os.path.join(data_dir, date.strftime("%Y-%m-%d") + ".txt")

            # Check if the file exists
            if os.path.isfile(file_path):
                # Read data from the file
                with open(file_path, "r") as file:
                    lines = file.readlines()
                    if len(lines) >= 2:
                        # Get the time spent in the app
                        time_in_app = float(lines[1].strip())
                        app_time.append(time_in_app)

                        # Get the smile time
                        smile_ratio = float(lines[0].strip())
                        smile_time.append(time_in_app * smile_ratio)
                    else:
                        # If the file exists but doesn't have enough lines, set the value to 0
                        app_time.append(0)
                        smile_time.append(0)
            else:
                # If the file doesn't exist, set the value to None
                app_time.append(0)
                smile_time.append(0)

        # Reverse the order of the lists so the chart displays days in the correct order
        app_time.reverse()
        smile_time.reverse()

        # Create a list of days
        start_date = datetime.now() - timedelta(days=6)
        days = []

        for i in range(7):
            current_date = start_date + timedelta(days=i)
            day_name = current_date.strftime('%a')
            days.append(day_name)

        x = np.arange(len(app_time))  # Create an array of numbers from 0 to len(app_time)
        width = 0.7  # Width of the bars

        ax = plt.gca()

        app_time_hours = [time / 120 for time in app_time]
        smile_time_hours = [time / 120 for time in smile_time]

        plt.bar(x, app_time_hours, width, label='App Time', color='#2077B4')
        plt.bar(x, smile_time_hours, width, label='Smile Time', color='#FFA500')

        plt.xlabel('Days')
        plt.ylabel('Hours')
        plt.title('App Time vs. Smile Time')

        plt.xticks(x + width / 2, days)  # Set the x-axis labels to the appropriate dates

        # Adjust the x-axis labels to fit the chart bars
        plt.gca().set_xticklabels(days, rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', linewidth=0.7, alpha=0.6)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        max_hours = 12
        plt.ylim([0, max_hours])

        plt.legend()

    def display_all_plots(self, unused):
        # Size of the main chart window
        plt.figure(figsize=(15, 10))

        # Chart from the last hour (top-left)
        plt.subplot(2, 2, 1)
        self.do_last_hour_plot(None)

        # Daily chart (top-right)
        plt.subplot(2, 2, 3)
        self.do_day_plot(None)

        # Weekly chart (bottom, full width)
        plt.subplot(1, 2, 2)
        self.do_week_plot(None)

        plt.tight_layout()

        timestamp = str(int(time.time()))
        plt.savefig(timestamp + "chart.png")  # Save the chart as an image file

        # Create an Image widget and set the source to the saved image file
        image_widget = Image(source=timestamp + "chart.png", allow_stretch=True)
        plt.clf()
        os.remove(timestamp + "chart.png")

        # Clear the layout and add the Image widget
        self.layout.add_widget(image_widget)

class WindowManager(ScreenManager):
    pass
class MainApp(App):
    def build(self):
        self.title = 'Cognitive Project'
        Window.size =  (1000, 800)
        manager = WindowManager()

        manager.add_widget(VideoWindow(name="video"))
        manager.add_widget(StatsWindow(name="stats"))
        print(self.__sizeof__())
        Window.clearcolor = (1, 1, 1, 1)
        return manager

MainApp().run()
