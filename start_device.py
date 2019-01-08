from lib.people_counter_device import PeopleCounterDevice
import time

while True:
    try:
        try:
            device = PeopleCounterDevice('/boot/config.ini')
        except:
            device = PeopleCounterDevice('config.ini')

        last_send_time = 0

        while True:
            if (int(time.time() - last_send_time) > int(device.request_frequency)):
                last_send_time = int(time.time())

                saved_frame_status = device.cap_and_save_frame()

                if device.movement_detected and saved_frame_status:
                    device.upload_file_and_send_request()
                else:
                    pass

    except Exception as e:
        print("\n[ERROR]: Restarting Script")
        device.cap.release()
        print("Error:", e)
        time.sleep(1)

        # Uncomment this if you want the script to STOP if there's any error
        #break

device.cap.release()