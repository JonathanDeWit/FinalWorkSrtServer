# Final Work Srt Media Server
This project is part of my Final Work project for my Bachelor degree in Applied Computer Science at the Erasmus Brussel University of Applied Sciences and Arts.
My project mainly consisted of building a video surveillance system by using microcontrollers.
If you want to know more about the project, I invite you to consult the following links:

[Final Work Paper](https://github.com/JonathanDeWit/FinalWorkSrtServer/blob/master/FinalWorkPaper.pdf) (NL)

Other related repositories:
* [ESP32-CAM microcontroller surveillance camera](https://github.com/JonathanDeWit/FinalWorkESP32CamLiveCamera)
* [ASP.NET API](https://github.com/JonathanDeWit/FinalWorkApi)
* [Raspberry PI automated video convertor](https://github.com/JonathanDeWit/FinalWorkRaspberryPiConvertor)
* [Android App](https://github.com/JonathanDeWit/FinalWorkAndroidApp)


## Purpose
This GitHub repo contains an python project meant for running on Ubuntu.
This project primary goal is to function as a multimedia server to be able to receive live SRT video streams transmitted by the different Raspberry Pi’s an then be able to send the live stream back to the player (Android app) how wants to consume it.

Every incoming SRT signal will com from a python program using FFmpeg on a Raspberry Pi. You can find this code [here](https://github.com/JonathanDeWit/FinalWorkRaspberryPiConvertor)
Every API call you will find in this project was directed to the ASP.Net API which you can find [here](https://github.com/JonathanDeWit/FinalWorkApi)

 ## Prerequisite
To use this project it is required to install the open source command line tool [GStreamer](https://ffmpeg.org/) with the [srtsink](https://gstreamer.freedesktop.org/documentation/srt/srtsink.html?gi-language=c) plugin to bale to user the SRT protocol.

To install GStreamer with the srtsink plugin you need to execute the following commands:

sudo apt-get update sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev

sudo apt-get install libsrt1-dev

sudo apt-get install gstreamer1.0-plugins-bad
 
It’s also important to mention that you will need to install Python 3.9 or higher.

The domain name and path of the API request are stored in ‘conf.csv’ if you want to change it feel free to edit this file.
The username and password of the SrtServer user are stored in ‘profile.csv’ if you want to change it feel free to edit this file. 



 ## Primary features
 - listen to a specific port waiting for an incoming SRT live video stream and provide an SRT output stream on a specific port.
   - Every SRT pipeline is executed on an individual thread.
 - Make API calls.
   - authenticate and store the JWT token.
     - Replace the JWT token when it is about to expire.
   - Retreave the system status.


 ## SRT pipeline
The SRT media server will check almost every second using the API to see witch user activated there security system to be able to create all the SRT pipelines needed for all the live streams. When a user disable there security system every pipeline related to that user is stopped and deleted.
It worth noting that every pipeline is executing in his own thread
 
To create the RTSP pipeline to listen for a incoming SRT live video and create an outgoing SRT video stream on another port used the following GStreamer command:
 
gst-launch-1.0 srtserversrc uri=srt://: < port > ! srtclientsink uri=srt://: < port >
