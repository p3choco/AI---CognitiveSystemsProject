![Cognitive_Smile_Detector-2](https://github.com/p3choco/CognitiveSystemsProject/assets/62072811/211d00d8-4d2c-49a6-b861-efa5fe64287d)


# Cognitive Smile Detector

A project developed for the "Cognitive Systems" course, utilizing Kivy and Python to detect smiles in real-time.

## The purpouse of the project 

### Why smiling is important?

1. Improves mood: When we smile, endorphins - happiness hormones - are released, helping us feel better and reducing stress.
   
2. Supports mental health: Regularly smiling can help cope with depression and anxiety, improving overall quality of life.
   
3. Helps with communication: By smiling, we express positive emotions and convey to others that we are open to contact and willing to establish relationships.
   
4. Enhances interpersonal relationships: By smiling, we display a friendly and open attitude, which in turn facilitates establishing contacts with others and building positive relationships.
   
5. Improves appearance: A person who smiles appears more attractive and positive, which can help build a positive image.

### How you can use this app? 

There is a saying " If you want to improve something start monitoring it ". App helps in monitoring smile, therefore you can smile more during a day and have better mood. You can also improve your appearance at online meetings due to the same pronciple. 


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


<img width="1002" alt="Zrzut ekranu 2023-10-12 o 13 10 07" src="https://github.com/p3choco/CognitiveSystemsProject/assets/62072811/24d96685-fc22-452b-9bce-59fc2ce0cade">

### Statistics Screen
This screen displays the user's smile statistics:
- From the last hour.
- From the current day.
- From the entire week.

Statistics are presented in both graphical and numerical forms.

Data for stats is saved locally on user's device what provides seciurity and offline use possible


<img width="999" alt="Zrzut ekranu 2023-10-12 o 13 23 29" src="https://github.com/p3choco/CognitiveSystemsProject/assets/62072811/55360739-5612-407c-80db-2d89549a116f">

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
