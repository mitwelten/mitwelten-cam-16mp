import psutil
import time
import datetime
from gpiozero import CPUTemperature
import uuid
import socket


class HWStatus:
    def __init__(self):
        self.memory_pct = psutil.virtual_memory().percent
        self.gpiocputemp = CPUTemperature()
        self.cpu_temp = round(self.gpiocputemp.temperature, 1)
        self.cpu_pct = psutil.cpu_percent(interval=1, percpu=False)
        self.ip_address = psutil.net_if_addrs()["eth0"][0].address
        self.mac_addr = psutil.net_if_addrs()["eth0"][2].address
        self.hostname = socket.gethostname()
        self.update_time = datetime.datetime.utcnow()
        self.boot_time = psutil.boot_time()

    def update(self):
        self.memory_pct = psutil.virtual_memory().percent
        self.cpu_temp = round(self.gpiocputemp.temperature, 1)
        self.cpu_pct = psutil.cpu_percent(interval=1, percpu=False)
        self.update_time = datetime.datetime.utcnow()

    def get_status(self):
        return dict(
            mem_usage=self.memory_pct,
            cpu_pct=self.cpu_pct,
            mac_addr=self.mac_addr,
            ip_addr=self.ip_address,
            temperature=self.cpu_temp,
            hostname=self.hostname,
            time=str(self.update_time),
            online_since=str(
                datetime.timedelta(seconds=int(time.time() - self.boot_time))
            ),
        )
