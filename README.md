# openSesame

## Link to Devpost
https://devpost.com/software/sbhacks-gz8oix

## What is openSesame?
openSesame is a facial-recognition smart lock created by Timothy Yuan, Lucas Xia, Navid Mir, Toby Fischer, and Jacob Zhang for SB Hacks V
(January 11, 2019 - January 13, 2019). This idea was thought of to find a solution to students getting locked out of their residences 
or apartments. Using our website, users simply upload a single image of each person who can be admitted entry. Then getting access is as
simple as letting the door lock mechanism take a picture of one's face. 

## How does it work and what did we use?
With Python Libraries OpenCV and dlib, we used machine learning to recognize faces and process them to simple data files. We built the server with Javascript, the database with mySQL, and hosted the server on Google Cloud Platform. The front end of the website was built with Angular, while the door lock hardware used Arduino.

## Improvements/Extensions
The facial recognition could be improved, in its accuracy and its inability to take in more than one face at once.
The hardware would have to be configured/installed for doors.
