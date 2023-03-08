# mitwelten-cam-16mp

## Raspberry Pi Setup

Write the `Raspberry Pi OS Lite (64 Bit)` to an SD Card using Raspberry Pi Imager.
- Set Hostname
- Create User and Password
- Select OS: `Raspberry Pi OS Lite (64 Bit)`
- Select SD Card and click Write.

## Setup Script

Install the Camera dependencies
```sh
curl https://raw.githubusercontent.com/mitwelten/mitwelten-cam-16mp/main/scripts/install_camera_dependencies.sh | bash
```
Reboot 
```sh
sudo reboot
```
Clone this Repo and install dependencies
```sh
curl https://raw.githubusercontent.com/mitwelten/mitwelten-cam-16mp/main/scripts/install_mitwelten_cam.sh | bash
```
Add a systemd service to start the server automatically
```sh
curl https://raw.githubusercontent.com/mitwelten/mitwelten-cam-16mp/main/scripts/install_systemd_service.sh | bash
```



## Setup Step by Step

Update & Upgrade

```sh
sudo apt update 
sudo apt upgrade -y
```


Download and install the `libcamera_dev` and `libcamera_apps` from ArduCAM
```sh
wget -O install_pivariety_pkgs.sh https://github.com/ArduCAM/Arducam-Pivariety-V4L2-Driver/releases/download/install_script/install_pivariety_pkgs.sh
chmod +x install_pivariety_pkgs.sh

./install_pivariety_pkgs.sh -p libcamera_dev
./install_pivariety_pkgs.sh -p libcamera_apps
```

Install the imx519 driver
```sh
./install_pivariety_pkgs.sh -p imx519_kernel_driver_low_speed
```

Reboot the Pi
```sh
sudo reboot
```

*Optional: Test the Camera*
```sh
libcamera-still -t 5000 -n -o test.jpg
```

Install dependencies:
```sh
sudo apt install -y python3-kms++
sudo apt install -y python3-pyqt5 python3-prctl libatlas-base-dev ffmpeg python3-pip git
```


Clone this repo
```sh
cd ~
git clone https://github.com/mitwelten/mitwelten-cam-16mp.git
```

Install Server dependencies:
```sh
cd ~/mitwelten-cam-16mp
pip3 install -r requirements.txt
```


## Start the server
```sh
cd ~/mitwelten-cam-16mp/server
python3 app.py
```

You can now access the camera in a web browser:
http://your-camera-hostname.local:8080


Additional Steps that might be used:

- Expand the Filesystem:  `sudo raspi-config` &rarr; Advanced Options &rarr; Expand Filesystem
- Change password: `sudo raspi-config` &rarr; System Options &rarr; Password &rarr; enter new password
- Change hostname: `sudo raspi-config` &rarr; System Options &rarr; Hostname &rarr; enter new hostname
- Enable password authentication for ssh:
    ```sh
    sudo nano ssh/sshd_config
    ```
    Remove the line `PasswordAuthentication no`
- add more CMA Memory
    ```sh
    sudo nano /boot/config.txt
    ```
    replace the line `dtoverlay=vc4-kms-v3d` with `dtoverlay=vc4-kms-v3d,cma-256` and reboot.

## Configuration

Parameters can be configured in a yaml file next to `app.py`. It must be named `configuration.yaml` and have following structure:
```yaml
# Default config
camera:
  width: 4656
  height: 3496
  quality: 90
  focus_file: focus.txt
  default_focus: 4.8
server:
  port: 8080
  username: MY_USER
  password: MY_PASSWORD
```

To override the default configuration, make a copy of [sample_configuration.yaml](server/sample_configuration.yaml) and edit it.
```sh
cd ~/mitwelten-cam-16mp/server
cp sample_configuration.yaml configuration.yaml
nano configuration.yaml
```




## Starting the server as a systemd service

## Adjust Focus

## REST API Endpoints

### Snapshot

GET `/snapshot` or `/?action=snapshot`

Returns a JPEG Image

---

### Parameters

GET `/parameters`

Returns the configured camera parameters in JSON format.

Example:
```json
{
    "distance_cm": 30,
    "height": 3496,
    "lensposition": 5.58,
    "quality": 80,
    "width": 4656
}
```

POST `/parameters/lensposition` 

Updates the lensposition of the camera

Example payload:
```json
{
    "lensPosition": 5.41
}
```

Returns the updated lensPosition:
```json
{
    "lensPosition": 5.41
}
```

---

### Preview

GET `/preview`

Args:
- `size` int: the width of the image
- `quality` int: (0 .. 100) the JPEG quality of the preview
- `capture` flag: capture new image if set, send latest picture if not set

Returns a JPEG Image

---

### System

GET `/system`

Returns relevant system information in JSON format.

Example:
```json
{
    "cpu_pct": 0.8,
    "hostname": "raspberry",
    "ip_addr": "192.168.0.100",
    "mac_addr": "aa:aa:aa:aa:aa:aa",
    "mem_usage": 38.2,
    "online_since": "0:30:31",
    "temperature": 46.2,
    "time": "2023-03-08 13:21:27.056507"
}
```

### Camera Metadata

GET `/metadata`

Returns metadata of the latest image JSON format.

Example:
```json
{
    "AeLocked": false,
    "AfPauseState": 0,
    "AfState": 0,
    "AnalogueGain": 2.0,
    "ColourCorrectionMatrix": [
        1.1436830759048462,
        -0.004590064287185669,
        -0.13909322023391724,
        -0.1510423719882965,
        1.3705484867095947,
        -0.21950659155845642,
        0.038373641669750214,
        -0.26998230814933777,
        1.2316006422042847
    ],
    "ColourGains": [
        1.9632495641708374,
        1.7652636766433716
    ],
    "ColourTemperature": 4473,
    "DigitalGain": 1.0,
    "ExposureTime": 15713,
    "FocusFoM": 11477,
    "FrameDuration": 111092,
    "Lux": 841.9351806640625,
    "ScalerCrop": [
        0,
        0,
        4656,
        3496
    ],
    "SensorBlackLevels": [
        4096,
        4096,
        4096,
        4096
    ],
    "SensorTimestamp": 500875426000
}
```




