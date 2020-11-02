import os
import subprocess
import soundfile as sf
import sounddevice as sd

from numpy import ndarray
from modi.util.conn_util import AIModuleFaultsException
from typing import Tuple


class AIMic:
    def __init__(self):
        try:
            sd.check_input_settings('wm8960')
        except ValueError:
            raise AIModuleFaultsException(
                "AI Mic not found! Please contact our CS team."
            )
        self.RATE = 44100
        for idx, device in enumerate(sd.query_devices()):
            if 'wm8960' in device:
                sd.default.device = idx
                break

    def write_audio(self, file_path: str, data: ndarray,
                    sampling_rate: int = 44100) -> None:
        sf.write(file_path, data, sampling_rate)

    def record(self, duration: float) -> Tuple[ndarray, float]:
        """ Record sound data catched by MODI AI shield

        :param duration: Duration for reconrding (Seconds)
        :type duration: float
        :return: Numpy array of the recording
        """
        if os.path.exists('/var/run/gpio_fan.pid'):
            subprocess.run(["sudo", "python3",
                "/usr/src/rpi-daemon-py/gpio_fan.py", "stop"])
            data = sd.rec(duration * self.RATE,
                          samplerate=self.RATE,
                          channels=1)
            sd.wait()
            subprocess.run(["sudo", "python3",
                "/usr/src/rpi-daemon-py/gpio_fan.py", "start"])
            return data, self.RATE

        else:
            data = sd.rec(duration * self.RATE,
                          samplerate=self.RATE,
                          channels=1)
            sd.wait()
            return data, self.RATE
