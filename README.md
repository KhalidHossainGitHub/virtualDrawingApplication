# Virtual Drawing Application

The **Virtual Drawing Application** is a gesture-based virtual drawing tool built using **MediaPipe** and **OpenCV**. This tool enables real-time hand tracking, allowing users to draw on the screen using their index finger. The application is intuitive and responsive, designed for users to create digital art using natural hand gestures.

<p align="center">
  <img width="932" alt="Selecting Colors" src="tutorialGifs/Virtual Painter - Selecting Colors.gif">
  <br>
  <b>Figure 1: Selecting colors using the index and middle finger.</b>
</p>

## Project Overview

The Virtual Drawing Application enables users to:

- **Selection Mode**: Activate the mode using your index and middle finger to choose colors or switch to the eraser from the color palette displayed at the top of the screen.
- **Draw Mode**: Draw on the screen using your index finger. The application tracks your finger's movement in real-time to draw smoothly.
- **Adjustable Brush Thickness**: Control the thickness of the brush by changing the distance between your thumb and index finger. The pinky finger acts as an indicator for size selection.
- **Clear Screen**: Simply close your hand to erase the entire drawing.
- **Standby Mode**: Use the combination of your index and pinky finger to enter Standby Mode, allowing you to pause and resume drawing or to start a new section without interference.

<p align="center">
  <img width="600" alt="Writing Demo" src="tutorialGifs/Virtual Painter - Standby Mode.gif">
  <br>
  <b>Figure 2: Writing using Standby Mode.</b>
</p>

## Features

- **Gesture-Based Drawing**: Enables users to draw naturally using finger gestures.
- **Color and Eraser Selection**: Easy access to various drawing tools such as colors and an eraser.
- **Dynamic Brush Control**: Adjust brush size on the fly using hand gestures.
- **Screen Clearing**: Erase the entire screen with a simple gesture.
- **Real-Time Hand Tracking**: The application tracks hand movements accurately and in real-time using the MediaPipe library.

<p align="center">
  <img width="600" alt="Adjusting Thickness" src="tutorialGifs/Virtual Painter - Adjusting Thickness.gif">
  <br>
  <b>Figure 3: Adjusting brush thickness by changing the distance between index and thumb.</b>
</p>

## Technologies Used

- **MediaPipe**: For real-time hand tracking.
- **OpenCV**: For capturing video feed and rendering the drawings.
- **Python**: For integrating the libraries and managing the application logic.

## How to Use

1. **Install Dependencies**:
   - Open your terminal and install the required libraries using the following commands:
     ```bash
     pip install opencv-python
     pip install numpy
     pip install mediapipe
     ```

2. **Run the Application**:
   - After installing the dependencies, run the main Python script to start the application:
     ```bash
     python virtualPainter.py
     ```

3. **Use Hand Gestures to Draw**:
   - Use your index finger to draw on the screen.
   - To select a color or eraser, raise your index and middle fingers to activate **Selection Mode**.
   - Adjust the brush size by varying the distance between your thumb and index finger while keeping your pinky finger up.
   - Clear the screen by closing your hand.
   - Enter **Standby Mode** using your index and pinky fingers to pause drawing temporarily.

<p align="center">
  <img width="600" alt="Clearing the Screen" src="tutorialGifs/Virtual Painter - Clearing Screen.gif">
  <br>
  <b>Figure 4: Clearing the screen by closing hand.</b>
</p>