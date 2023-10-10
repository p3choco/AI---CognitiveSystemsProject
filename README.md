![Cognitive_Systems_Project](https://github.com/p3choco/CognitiveSystemsProject/assets/62072811/33a4fbef-dc7e-4a03-ab0e-791aca909972)

# Cognitive Smile Detector

A project developed for the "Cognitive Systems" course, utilizing Kivy and Python to detect smiles in real-time.

## Table of Contents
- [About the Project](#about-the-project)
- [Installation and Configuration](#installation-and-configuration)
- [Usage](#usage)
  * [Main Screen](#main-screen)
  * [Statistics Screen](#statistics-screen)
  * [Recalibration Screen](#recalibration-screen)
- [License](#license)

## About the Project
The "Cognitive Smile Detector" is an desktop application written in Python using the Kivy framework. This application leverages facial recognition technology to determine whether the user is smiling. The project was created as part of the "Cognitive Systems" course.

## Installation and Configuration
1. Clone the GitHub repository.
2. Install the required packages using `pip install -r requirements.txt`.
3. Launch the application using `python main.py`.

## Usage
### Main Screen
The main screen displays the camera feed. At the bottom of the screen, information is displayed indicating whether the user is smiling.

### Statistics Screen
This screen displays the user's smile statistics:
- From the last hour.
- From the current day.
- From the entire week.

Statistics are presented in both graphical and numerical forms.

Data for stats is saved locally on user's device what provides seciurity and offline use possible

### Recalibration Screen
This screen allows you to adjust the facial recognition model for a specific user. To recalibrate:
1. Ensure the face is clearly visible on screen.
2. Follow the on-screen instructions, performing various facial expressions.
3. Once completed, the model will adjust to your face and current lighting conditions.

#### Used method
Sometimes opencv models don't work great with particular lightning or face. In recalibration app makes 40 sec video of user's face ( only in last 20 sec user smiles ). After that labeled dataset is formed and passed to teach convolutional neural network.
After 60 secounds app saves model calibrated to specific face and lighting conditions and uses it to tell if user smiles

## License
The "Cognitive Smile Detector" application is provided under the MIT license. 
