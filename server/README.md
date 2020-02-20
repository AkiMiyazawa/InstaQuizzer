# MyClicker Desktop Side

## Goals
The goal of this project was to create a free (in both senses) replacement for the iClicker classroom polling technology used in many courses (especially at UCLA).

In order to accomplish this goal, I created this MyClicker server for teachers to use. All they need to do is setup their students to send in JSON responses with "user_id" and "answer" fields, and the MyClicker server will store statistics on both the students and the class. I developed this project in tandem with a classmate who created an Android application which sent the JSON responses from clients (students) to this desktop application.

## Features
This desktop application uses Python for everything. I used the [pygubu](https://github.com/alejandroautalan/pygubu) GUI development application to rapidly develop the GUI for all 3 menus in the application. The Desktop.ui file in this repository is the file created by this application, which is loaded by TkInter to create the GUI in main_menu.py.

### Main Menu - main_menu.py
This is the entry point for the application, and if the teacher desires to use the application, they should type the command

`$ python3 main_menu.py`

Note that you need to use Python >=3.5 for this project, as it uses Python's `asyncio` library as of the 3.5 update

The main menu of this application presents the teacher with two options. The first is to create a presentation, which consistsof a series of questions and answers. The second is to load that presentation and present it to the class with real-timepolling of the class. The main menu also contains a file entry box. The file selected in this box is either the file created by content creation mode if the teacher selects content creation mode, or the presentation opened if the teacher selectspresentation mode.

### Content Creation Mode - ContentCreation.py
ContentCreation.py is the file which controls the content-creation side of the application. This application enables teachers to enter in question text, as well as the correct answer and incorrect answers. Teachers can go back and forth between questions in a given session in order to edit previously created questions. When the teacher clicks "Done Creating Questions", the questions they created, which during creation mode are saved into a Python dictionary, are written into a JSON file so that they can be loaded by Presentation mode

### Presentation Mode - Presentation.py
This is the mode in which the teacher will present to the class. They can present questions created in Content Creation Mode to the whole class in full screen. By clicking "Start Accepting Answers", they can tell the server to start accepting input from the class. After the class has answered the questions, the teacher can click "Show Class Data" to show the correct answer, as well as the distribution of the class's answers. The presentation file also starts the server file running in a separate process, as if the server ran in the same process it would block the teacher from interacting with the Presentation application. The Presentation also opens a socket connection with the server to communicate data and events between the two processes.

### Server Details - MyClickerServer.py
I used Python 3's relatively new `asyncio` asynchronous event loop capabilities to build the server. This library has a built in TCP server, so I created a protocol for that server which accepted the JSON answers we desired. The server handles, validates, and parses the JSON data responses from the students. It then stores these data into User and QuestionStats classes to keep track of user data and class data, respectively. It also accepts requests from the Presentation through the pipe between the two processes. The most important of these requests are the requests for class data, the request to update the correct answer in the server, and the request to end the server process, which makes the server write all of the user data to the user.json file, which stores data in a JSON-like (but not exactly JSON) file.
