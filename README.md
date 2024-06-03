# Camera Recognition and Mosaic Generation Project

This project allows you to run an application that uses the camera for image capture and processing, and it also allows the generation of a mosaic from the captured images.

## Prerequisites

Before starting, make sure you have Python 3 installed on your system. If you don't have it, download and install it from the [official Python website](https://www.python.org/).

## Instructions to Run the Project with the Camera

1. **Open a terminal** on your system.

2. **Install the required libraries** by executing the following commands:

    ```bash
    pip install opencv-python-headless
    pip install mediapipe
    ```

3. **Run the main script** of the project:

    ```bash
    python3 main.py
    ```

This command will start the application that will use the camera for image capture and processing.

## Instructions to Generate the Mosaic

1. **Open a new terminal** on your system.

2. **Run the mosaic generation script**:

    ```bash
    python3 MakeMosaico.py
    ```

This command will start the process of generating a mosaic from the captured images.

## Notes

- Make sure your camera is connected and working properly before starting the main script.
- The scripts `main.py` and `MakeMosaico.py` should be in the same directory, or the path to them should be correctly specified in the terminal.
- If you encounter any issues, check that all dependencies are installed correctly and that there are no permission errors accessing the camera or the file system.
