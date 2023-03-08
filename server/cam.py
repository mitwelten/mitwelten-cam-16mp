from picamera2 import Picamera2
from libcamera import controls
from PIL import Image
from PIL import ImageDraw
from io import BytesIO
import os
import time
import datetime

# Picamera2.set_logging(Picamera2.DEBUG)


class Focus:
    def __init__(self, focus_file, default_focus=4.8):
        self.focus_file = focus_file
        self.focus = default_focus

        if not os.path.exists(self.focus_file):
            print("Focus file does not exist")
            self.focus = default_focus
            self._write_focus_to_file()
        else:
            self._read_from_file()

    def get_focus(self):
        return self.focus

    def get_distance_cm(self):
        return round(83.4342 / (self.focus - 2.8028))

    def set_focus(self, new_focus):
        self.focus = new_focus
        self._write_focus_to_file()

    def _write_focus_to_file(self):
        with open(self.focus_file, "w") as f:
            f.write(str(self.focus))

    def _read_from_file(self):
        with open(self.focus_file, "r") as f:
            focus_from_file = float(f.read())
        self.focus = focus_from_file


class Camera:
    def __init__(self, width, height, quality=90):
        self.camera = Picamera2()
        self.config = self.camera.create_still_configuration(buffer_count=1, queue=True)
        self.width = width
        self.height = height
        self.quality = quality
        self.config["main"]["size"] = (self.width, self.height)
        self.camera.configure(self.config)
        self.pil_image = None
        self.capture_duration = None
        self.metadata = None
        self.capture_time = 0

    def set_focus(self, lensposition):
        self.camera.set_controls({"AfMode": 0, "LensPosition": lensposition})

    def enable_autofocus(self):
        self.camera.set_controls({"AfMode": controls.AfModeEnum.Continuous})

    def get_metadata(self):
        return self.metadata

    def get_capture_duration(self):
        return self.capture_duration

    def start(self):
        self.camera.start()

    def stop(self):
        self.camera.stop()

    def capture(self, acceptable_age_s=1):
        if time.time() - acceptable_age_s > self.capture_time:
            t0 = time.time()
            request = self.camera.capture_request()
            self.pil_image = request.make_image("main")
            self.metadata = request.get_metadata()
            request.release()
            self.capture_duration = time.time() - t0
            #print("Capture duration", self.capture_duration)
        if self.pil_image:
            self.capture_time = time.time()
            return True
        return False

    def get_jpeg(self, quality=None):
        if self.pil_image is None:
            return None
        quality = quality if quality is not None else self.quality
        bio = BytesIO()
        self.pil_image.save(bio, "JPEG", quality=quality)
        bio.seek(0)
        return bio

    def get_preview(self, thumbnail_size=1200, quality=None, text=True):
        t00 = time.time()
        if self.pil_image is None:
            return None
        quality = quality if quality is not None else self.quality
        t0 = time.time()
        img = self.pil_image.copy()
        #print("copy", time.time() - t0)
        t0 = time.time()

        img.thumbnail((thumbnail_size, thumbnail_size), Image.NEAREST)
        if text:
            ImageDraw.Draw(img).text(  # Image
                (0, 0), str(datetime.datetime.utcnow()), (255, 0, 0)
            )
        #print("thn", time.time() - t0)
        t0 = time.time()

        bio = BytesIO()
        img.save(bio, "JPEG", quality=quality)

        bio.seek(0)
        #print("save and seek", time.time() - t0)
        #print("total", time.time() - t00)
        return bio
