# people-counter-client

People Counter Framework client scripts for running on client devices.



## Setup Instructions

**Simple (or if you're using one of our client devices)**

1. Fill up the **people_counter_config.ini** file with the relevant information
2. Place it in your /boot/ directory
   - If you are using a client device, insert the SD card into your computer and place it in the root of the boot drive
3. Power your device on and contact our support to see if your device is running as expected
   - The script that runs is **start_device.py** , which you can either manually run, or, if you're using our client device, should start running immediately
   - Note: The script should be run in **Python 3**. Ensure all dependencies are installed!



## Dependencies

You may install them using the install_deps.sh provided on a Linux system

- Python 3
- OpenCV 3.4.0+
  - https://pypi.org/project/opencv-python/
- google.cloud
  - https://pypi.org/project/google-cloud/
- google.auth
  - https://pypi.org/project/google-auth/
- methyl_auth_utils (in /lib)