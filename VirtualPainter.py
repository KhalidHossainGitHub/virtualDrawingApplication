# Imports
import cv2
import mediapipe as mp
import numpy as np
import os
import math

mpDrawing = mp.solutions.drawing_utils
mpHands = mp.solutions.hands

# For webcam input
cameraCapture = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cameraCapture.set(cv2.CAP_PROP_FPS, 30)
frameWidth = 1280
frameHeight = 720
cameraCapture.set(3, frameWidth)
cameraCapture.set(4, frameHeight)

# Image that will contain the drawing and then passed to the camera image
canvasImage = np.zeros((frameHeight, frameWidth, 3), np.uint8)

# Getting all header images in a list
imagesFolderPath = './images'  # Path to the images folder
imageList = os.listdir(imagesFolderPath)
overlayImagesList = []

# Load images with specific names
for imageName in ['selectRed.png', 'selectBlue.png', 'selectGreen.png', 'selectEraser.png']:
    imagePath = os.path.join(imagesFolderPath, imageName)
    image = cv2.imread(imagePath)
    if image is not None:
        overlayImagesList.append(image)

# Presettings:
headerImage = overlayImagesList[0] if overlayImagesList else np.zeros((125, frameWidth, 3), np.uint8)  # Default empty header
drawingColor = (0, 0, 255)
brushThickness = 20  # Thickness of the painting
tipIndices = [4, 8, 12, 16, 20]  # Fingertips indexes
lastX, lastY = [0, 0]  # Coordinates that will keep track of the last position of the index finger

with mpHands.Hands(min_detection_confidence=0.85, min_tracking_confidence=0.5, max_num_hands=1) as hands:
    while cameraCapture.isOpened():
        success, currentFrame = cameraCapture.read()
        if not success:
            print("Ignoring empty camera frame.")
            break
        
        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        currentFrame = cv2.cvtColor(cv2.flip(currentFrame, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writable to
        # pass by reference.
        currentFrame.flags.writeable = False
        handResults = hands.process(currentFrame)

        currentFrame = cv2.cvtColor(currentFrame, cv2.COLOR_RGB2BGR)
        if handResults.multi_hand_landmarks:
            for handLandmarks in handResults.multi_hand_landmarks:
                # Getting all hand points coordinates
                points = []
                for lm in handLandmarks.landmark:
                    points.append([int(lm.x * frameWidth), int(lm.y * frameHeight)])

                # Only go through the code when a hand is detected
                if len(points) != 0:
                    indexX, indexY = points[8]  # Index finger
                    middleX, middleY = points[12]  # Middle finger
                    thumbX, thumbY = points[4]  # Thumb
                    pinkyX, pinkyY = points[20]  # Pinky

                    ## Checking which fingers are up
                    fingers = []
                    # Checking the thumb
                    if points[tipIndices[0]][0] < points[tipIndices[0] - 1][0]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                    # The rest of the fingers
                    for id in range(1, 5):
                        if points[tipIndices[id]][1] < points[tipIndices[id] - 2][1]:
                            fingers.append(1)
                        else:
                            fingers.append(0)

                    ## Selection Mode - Two fingers are up
                    nonSelect = [0, 3, 4]  # indexes of the fingers that need to be down in the Selection Mode
                    if (fingers[1] and fingers[2]) and all(fingers[i] == 0 for i in nonSelect):
                        lastX, lastY = [indexX, indexY]

                        # Selecting the colors and the eraser on the screen
                        if indexY < 125:
                            if 170 < indexX < 295:
                                headerImage = overlayImagesList[0]
                                drawingColor = (0, 0, 255) # Set the drawing color to red (BGR format)
                            elif 436 < indexX < 561:
                                headerImage = overlayImagesList[1]
                                drawingColor = (255, 0, 0) # Set the drawing color to blue (BGR format)
                            elif 700 < indexX < 825:
                                headerImage = overlayImagesList[2]
                                drawingColor = (0, 255, 0) # Set the drawing color to green (BGR format)
                            elif 980 < indexX < 1105:
                                headerImage = overlayImagesList[3]
                                drawingColor = (0, 0, 0) # Set the drawing color to black (eraser)

                        cv2.rectangle(currentFrame, (indexX - 10, indexY - 15), (middleX + 10, middleY + 23), drawingColor, cv2.FILLED)

                    ## Stand by Mode - Checking when the index and the pinky fingers are open and dont draw
                    nonStandBy = [0, 2, 3]  # indexes of the fingers that need to be down in the Stand Mode
                    if (fingers[1] and fingers[4]) and all(fingers[i] == 0 for i in nonStandBy):
                        # The line between the index and the pinky indicates the Stand by Mode
                        cv2.line(currentFrame, (lastX, lastY), (pinkyX, pinkyY), drawingColor, 5)
                        lastX, lastY = [indexX, indexY]

                    ## Draw Mode - One finger is up
                    nonDraw = [0, 2, 3, 4]
                    if fingers[1] and all(fingers[i] == 0 for i in nonDraw):
                        # The circle in the index finger indicates the Draw Mode
                        cv2.circle(currentFrame, (indexX, indexY), int(brushThickness / 2), drawingColor, cv2.FILLED)
                        if lastX == 0 and lastY == 0:
                            lastX, lastY = [indexX, indexY]
                        # Draw a line between the current position and the last position of the index finger
                        cv2.line(canvasImage, (lastX, lastY), (indexX, indexY), drawingColor, brushThickness)
                        # Update the last position
                        lastX, lastY = [indexX, indexY]

                    ## Clear the canvas when the hand is closed
                    if all(fingers[i] == 0 for i in range(0, 5)):
                        canvasImage = np.zeros((frameHeight, frameWidth, 3), np.uint8)
                        lastX, lastY = [indexX, indexY]

                    ## Adjust the thickness of the line using the index finger and thumb
                    selecting = [1, 1, 0, 0, 0]  # Selecting the thickness of the line
                    setting = [1, 1, 0, 0, 1]     # Setting the thickness chosen
                    if all(fingers[i] == j for i, j in zip(range(0, 5), selecting)) or all(fingers[i] == j for i, j in zip(range(0, 5), setting)):
                        # Getting the radius of the circle that will represent the thickness of the draw
                        # using the distance between the index finger and the thumb.
                        radius = int(math.sqrt((indexX - thumbX) ** 2 + (indexY - thumbY) ** 2) / 3)

                        # Getting the middle point between these two fingers
                        midX, midY = [(indexX + thumbX) / 2, (indexY + thumbY) / 2]

                        # Getting the vector that is orthogonal to the line formed between
                        # these two fingers
                        vectorX, vectorY = [indexX - thumbX, indexY - thumbY]
                        vectorX, vectorY = [-vectorY, vectorX]

                        # Normalizing it
                        magnitude = math.sqrt(vectorX ** 2 + vectorY ** 2)
                        vectorX, vectorY = [vectorX / magnitude, vectorY / magnitude]

                        # Draw the circle that represents the draw thickness in (midX, midY) and orthogonally
                        # translated c units
                        c = 3 + radius
                        midX, midY = [int(midX - vectorX * c), int(midY - vectorY * c)]
                        cv2.circle(currentFrame, (midX, midY), int(radius / 2), drawingColor, -1)

                        # Setting the thickness chosen when the pinky finger is up
                        if fingers[4]:
                            brushThickness = radius
                            cv2.putText(currentFrame, 'Check', (pinkyX - 25, pinkyY - 8), cv2.FONT_HERSHEY_TRIPLEX, 0.8, (0, 0, 0), 1)

                        lastX, lastY = [indexX, indexY]

        # Setting the header in the video
        currentFrame[0:125, 0:frameWidth] = headerImage

        # The image processing to produce the image of the camera with the draw made in canvasImage
        imgGray = cv2.cvtColor(canvasImage, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 5, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(currentFrame, imgInv)
        finalOutput = cv2.bitwise_or(img, canvasImage)

        # Display the resulting frame
        cv2.imshow('Virtual Painter', finalOutput)

        # Check for key press; if 'q' is pressed, exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# When everything done, release the capture
cameraCapture.release()
cv2.destroyAllWindows()