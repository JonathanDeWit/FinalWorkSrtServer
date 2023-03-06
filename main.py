import signal
import time
import subprocess
import threading

from ApiRequest import ApiRequest, SystemState

apiRequest = ApiRequest()


def startup():
    apiRequest.login()

    print('JWT Token:', apiRequest.jwtToken)

    if apiRequest.jwtToken != "":
        return True
    else:
        return False




# statusA = apiRequest.getSystemState()
# statusB = apiRequest.getSystemState()
#
# unique_states = []
# app_user_ids = set()
#
# # Loop through stateA and add appUserId values to the set
# for state in statusB:
#     app_user_ids.add(state.appUserId)
#
# # Loop through stateB and add unique elements to unique_states list
# for state in statusA:
#     if state.appUserId not in app_user_ids:
#         unique_states.append(state)
#         app_user_ids.add(state.appUserId)



if __name__ == '__main__':
    start = startup()

    if start:
        beg_time = time.time()
        checkDelay = 3

        print("Check status")
        status = []

        # command = ["gst-launch-1.0", "srtserversrc", "uri=srt://:40001", "!", "srtclientsink", "uri=srt://:50001"]
        # subprocess.run(command)
        # while True:
        #     if (time.time() - beg_time) > checkDelay:
        #         beg_time = time.time()
        #
        #         print("Check status")
        #         newStatus = apiRequest.getSystemState()
        #
        #         if len(newStatus) > 0:
        #             # Sort lists to create 1 list for the users where new video streams need to be created
        #             # and another list with the users where the video streams need to be deleted
        #             toDeleteUsers = []
        #             toCreateUsers = []
        #             oldStatusUser = set()
        #             newStatusUser = set()
        #
        #             for user in newStatus:
        #                 newStatusUser.add(user.appUserId)
        #             for user in status:
        #                 oldStatusUser.add(user.appUserId)
        #                 if user.appUserId not in newStatusUser:
        #                     toDeleteUsers.append(user)
        #             for user in newStatus:
        #                 if user.appUserId not in oldStatusUser:
        #                     toCreateUsers.append(user)
        #
        #             print("To Dell: "+str(len(toDeleteUsers)))
        #             print("To Create "+str(len(toCreateUsers)))
        #             status = newStatus
        #         else:
        #             print("Delete all treads")
        #
        #     time.sleep(3)
    else:
        print("Unable to authenticate")
        # threads = []