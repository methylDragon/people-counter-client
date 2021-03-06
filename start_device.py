from lib.people_counter_device import PeopleCounterDevice
import time

while True:
    try:
        try:
            device = PeopleCounterDevice('/boot/people_counter_config.ini')
        except:
            device = PeopleCounterDevice('people_counter_config.ini')

            time.sleep(5)

        last_send_time = 0

        while True:
            try:
                if (int(time.time() - last_send_time) > int(device.request_frequency)):
                    last_send_time = int(time.time())

                    saved_frame_status = device.cap_and_save_frame()

                    if device.movement_detected and saved_frame_status:
                        device.upload_file_and_send_request()
                    else:
                        pass

                time.sleep(5)
            except Exception as e:
                with open("ERROR_LOG", "a") as f:
                    f.write(e)
                    f.write('\n')

                print("\n[ERROR]: Restarting Script")
                try:
                    device.cap.release()
                except:
                    pass

                print("Error:", e)
                time.sleep(300)

                break

    except Exception as e:
        print("\n[ERROR]: Restarting Script")

        try:
            device.cap.release()
        except:
            pass

        print("Error:", e)
        time.sleep(300)

        # Uncomment this if you want the script to STOP if there's any error
        #break

device.cap.release()
