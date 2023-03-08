from flask import Flask, request,  send_file, render_template
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import os
import time
import datetime
import yaml
from cam import Camera, Focus
from hwmonitoring import HWStatus

CONFIG_FILE = "configuration.yaml"
DEFAULT_CONFIG = {
    "camera": {
        "width": 4656,
        "height": 3496,
        "quality": 90,
        "focus_file": "focus.txt",
        "default_focus": 4.8,
    },
    "server": {"port": 8080, "username": "MY_USER", "password": "MY_PASSWORD"},
}
config = DEFAULT_CONFIG
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except Exception as exc:
            print("could not load config from file. using default config.")
            config = DEFAULT_CONFIG


camera = config.get("camera")
QUALITY = camera.get("quality", 90)
WIDTH = camera.get("width", 4656)
HEIGHT = camera.get("height", 3496)
FOCUS_FILE = camera.get("focus_file", "focus.txt")
DEFAULT_FOCUS = camera.get("default_focus", 4.8)
server = config.get("server")

USERNAME = server.get("username", "MY_USER")
PASSWORD = server.get("password", "MY_PASSWORD")
PORT = server.get("port", 8080)


users = {USERNAME: generate_password_hash(str(PASSWORD))}
app = Flask(__name__)
auth = HTTPBasicAuth()
hw = HWStatus()
cam = Camera(WIDTH, HEIGHT, QUALITY)
focus = Focus(FOCUS_FILE, DEFAULT_FOCUS)
cam.start()
cam.set_focus(focus.get_focus())
time.sleep(1)
cam.capture()


@auth.verify_password
def verify_password(uname, passwd):
    if uname in users and check_password_hash(users.get(uname), passwd):
        return uname


@app.route("/", methods=["GET"])
@auth.login_required
def index():
    qargs = request.args
    if "action" in qargs:
        action = qargs["action"]
        if action == "snapshot":
            return capture()
    return render_template("index.html", hostname=hw.hostname)


@app.route("/snapshot", methods=["GET"])
@auth.login_required
def capture():
    if not cam.capture():
        print("Capture failed")
        return "Failed to capture image", 500
    return send_file(cam.get_jpeg(), mimetype="image/jpeg")


@app.route("/preview", methods=["GET"])
@auth.login_required
def preview():
    qargs = request.args
    if "capture" in qargs:
        cam.capture(acceptable_age_s=5)

    img_size = qargs.get("size")
    img_quality = qargs.get("quality")
    img_size = 1200 if img_size is None else int(img_size)
    img_quality = cam.quality if img_quality is None else int(img_quality)

    return send_file(
        cam.get_preview(thumbnail_size=img_size, quality=img_quality),
        mimetype="image/jpeg",
    )


@app.route("/focus", methods=["GET"])
@auth.login_required
def focus_route():
    return render_template("focus.html", hostname=hw.hostname)


@app.route("/parameters", methods=["GET"])
@auth.login_required
def get_param_info():
    return dict(
        lensposition=focus.get_focus(),
        distance_cm=focus.get_distance_cm(),
        width=cam.width,
        height=cam.height,
        quality=cam.quality,
    )


@app.route("/parameters/lensposition", methods=["POST"])
@auth.login_required
def update_focus():
    qargs = request.json
    lp = float(qargs.get("lensPosition"))
    focus.set_focus(lp)
    cam.set_focus(focus.get_focus())
    return dict(lensPosition=focus.get_focus())


@app.route("/metadata", methods=["GET"])
@auth.login_required
def get_cam_metadata():
    return cam.get_metadata()


@app.route("/status", methods=["GET"])
@auth.login_required
def status():
    return render_template("status.html", hostname=hw.hostname)


@app.route("/system")
@auth.login_required
def get_system_info():
    hw.update()
    return hw.get_status()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=False)
