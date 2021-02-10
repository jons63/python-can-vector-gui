# Python-Can Vector Gui

A simple python gui for sending and logging can/serial messages with a CanCase.
Python-can has wrapped the Vector XL driver library for easy usage with Python.
This project aims to create a "Canalyzer lite" with some additional feature. 
I have been lacking a tool that combines all the elements of embedded development.
As a start, it shall be possible to load a test sequence. A use case is to test
security access which requires calculating CMACs and encrypting/decrypting message
before sending a reply. Using python across all steps enables a more streamlined
development process. Later it shall also be possible to flash hardware by integrating
gdb into the application, allowing the test process to be done within one application.