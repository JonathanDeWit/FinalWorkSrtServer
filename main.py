import signal
import time
import subprocess
import threading

from ApiRequest import ApiRequest, SystemState, VideoStream

apiRequest = ApiRequest()


def startup():
    apiRequest.login()

    print('JWT Token:', apiRequest.jwtToken)

    if apiRequest.jwtToken != "":
        return True
    else:
        return False


thread_dict = {}
process_dict = {}


def startSrtVideoPipeline(videoStream):
    try:
        print("Create pipeline input port: "+str(videoStream.incomingStreamPort)+" output port:"+str(videoStream.outgoingStreamPort))
        gstreamer_command = ["gst-launch-1.0", "srtserversrc", "uri=srt://:"+str(videoStream.incomingStreamPort), "!", "srtclientsink",
                             "uri=srt://:"+str(videoStream.outgoingStreamPort)]
        p = subprocess.Popen(gstreamer_command)

        process_dict[videoStream.id] = p
    except:
        print("Creation of the pipeline failed")


if __name__ == '__main__':
    start = startup()

    if start:
        beg_time = time.time()
        checkDelay = 3

        print("Check status")
        status = []



        # t = threading.Thread(target=startSrtVideoPipeline, args=(VideoStream(),))
        # threads.append(t)
        # t.start()
        #
        # time.sleep(60)

        while True:
            if (time.time() - beg_time) > checkDelay:
                beg_time = time.time()

                print("Check status")
                newStatus = apiRequest.getSystemState()

                if len(newStatus) > 0:
                    # Sort lists to create 1 list for the users where new video streams need to be created
                    # and another list with the users where the video streams need to be deleted
                    toDeleteUsers = []
                    toCreateUsers = []
                    oldStatusUser = set()
                    newStatusUser = set()

                    for user in newStatus:
                        newStatusUser.add(user.appUserId)
                    for user in status:
                        oldStatusUser.add(user.appUserId)
                        if user.appUserId not in newStatusUser:
                            toDeleteUsers.append(user)
                    for user in newStatus:
                        if user.appUserId not in oldStatusUser:
                            toCreateUsers.append(user)

                    print("To Dell: " + str(len(toDeleteUsers)))
                    print("To Create " + str(len(toCreateUsers)))

                    for user in toCreateUsers:
                        for videoStreams in user.videoStreams:
                            print(videoStreams.incomingStreamPort)
                            # Run new Thread with the new gstreamer SRT pipeline related to videoStream.
                            t = threading.Thread(target=startSrtVideoPipeline, args=(videoStreams,))
                            thread_dict[videoStreams.id] = t
                            t.start()
                    for user in toDeleteUsers:
                        for videoStreams in user.videoStreams:
                            print("Delete videoStream: "+videoStreams.id)
                            if videoStreams.id in thread_dict:
                                print("End thread")
                                thread_dict[videoStreams.id].join()
                                del thread_dict[videoStreams.id]
                            if videoStreams.id in process_dict:
                                print("End thread")
                                process_dict[videoStreams.id].kill()
                                del process_dict[videoStreams.id]

                    status = newStatus
                else:
                    if len(status) > 0:
                        print("Delete all videoStreams")
                        for user in status:
                            for videoStreams in user.videoStreams:
                                print("Delete videoStream: "+videoStreams.id)
                                if videoStreams.id in thread_dict:
                                    print("End thread")
                                    thread_dict[videoStreams.id].join()
                                    del thread_dict[videoStreams.id]
                                if videoStreams.id in process_dict:
                                    print("End thread")
                                    process_dict[videoStreams.id].kill()
                                    del process_dict[videoStreams.id]
                            status.remove(user)
            time.sleep(3)
    else:
        print("Unable to authenticate")
        # threads = []
