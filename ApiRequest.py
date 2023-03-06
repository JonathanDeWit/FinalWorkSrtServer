import requests
import json
import csv
import time


class ApiRequest:
    def __init__(self):
        self.apiUrl = ""
        self.srtServerPath = ""
        self.userName = "null"
        self.apiPassword = "null"
        self.jwtToken = ""
        self.tokenCreationTime = time.time()
        self.tokenValidationTime = 3600

        # Open CSV and import api url, username and password
        with open('conf.csv', mode='r') as file:
            # read CSV conf file
            reader = csv.reader(file)
            row = next(reader)
            # extract the username and password from the row
            self.apiUrl = row[0]
            self.srtServerPath = row[1]
        with open('profile.csv', mode='r') as file:
            # read CSV conf file
            reader = csv.reader(file)
            row = next(reader)
            # extract the username and password from the row
            self.userName = row[0]
            self.apiPassword = row[1]

    def checkTokenValidation(self):

        if (time.time() - self.tokenCreationTime) < self.tokenValidationTime:
            return True
        else:
            return False

    def login(self):
        # Get request with a json body with the username and password of the srt server
        payload = {"Email": self.userName, "Password": self.apiPassword}
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.apiUrl + self.srtServerPath + "/login", data=json.dumps(payload), headers=headers)

        jwtToken = "null"
        if response.status_code == 200:
            json_response = response.json()
            self.jwtToken = json_response.get('jwtToken')
            self.tokenCreationTime = time.time()
            return self.jwtToken
        else:
            print('Request failed with status code', response.status_code)
            return jwtToken

    def getSystemState(self):
        system_states = []
        if self.checkTokenValidation():
            headers = {"Authorization": "Bearer " + self.jwtToken}
            response = requests.get(self.apiUrl + self.srtServerPath + "/getSystemState", headers=headers)


            if response.status_code == 200:
                json_data = json.loads(response.text)
                for state_data in json_data:
                    video_streams = []

                    for stream in state_data["videoStreams"]:
                        videoStream = VideoStream(
                            stream["Id"],
                            stream["SrtServerUserId"],
                            stream["CameraUserId"],
                            stream["IncompingStreamPort"],
                            stream["OutgoingStreamPort"])
                        video_streams.append(videoStream)

                    system_state = SystemState(
                        state_data["AppUserId"],
                        state_data["SysState"],
                        state_data["DeviceHasUser"],
                        video_streams)

                    system_states.append(system_state)
            else:
                print('Request failed with status code', response.status_code)
        else:
            self.login()

        return system_states


class SystemState:

    def __init__(self, app_user_id=0, sys_state=False, device_has_user=False, video_streams=[]):
        self.appUserId = app_user_id
        self.sysState = sys_state
        self.deviceHasUser = device_has_user
        self.videoStreams = video_streams


class VideoStream:
    def __init__(self, video_id="", srt_server_user_id=0, camera_user_id=0, incoming_stream_port=0,
                 outgoing_stream_port=0):
        self.id = video_id
        self.srtServerUserId = srt_server_user_id
        self.cameraUserId = camera_user_id
        self.incomingStreamPort = incoming_stream_port
        self.outgoingStreamPort = outgoing_stream_port
