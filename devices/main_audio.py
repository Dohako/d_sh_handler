import os
import subprocess
import sys

if os.name != 'nt':
    import alsaaudio as alsa
else:
    pass


class AudioHandler:
    def __init__(self):
        self.mixers = alsa.mixers()
        if 'Master' in self.mixers:
            self.m = alsa.Mixer('Master')  # Headphone
        elif 'Headphone' in self.mixers:
            self.m = alsa.Mixer('Headphone')
        else:
            self.m = None
        if self.m:
            current_volume = self.m.getvolume()
            self.m.setvolume(0)

    @staticmethod
    def change_volume(volume: str):
        int_volume = AudioHandler.normalize_param(volume)
        audio_answer = subprocess.call(['amixer', '-D', 'pulse', 'sset', 'Master', f'{int_volume}%'])
        return audio_answer

    def change_volume_alsa(self,volume:str):
        int_volume = AudioHandler.normalize_param(volume)
        self.m.setvolume(int_volume)

    @staticmethod
    def normalize_param(volume):
        if volume.isdigit():
            int_volume = int(volume)
            if int_volume > 150:
                int_volume = 100
            elif int_volume < 0:
                int_volume = 0
        else:
            int_volume = 0
        return int_volume

    @staticmethod
    def test_mixers():
        mixers = alsa.mixers()
        answer = []
        for mixer in mixers:
            sub_return = subprocess.call(['amixer', '-D', 'pulse', 'sset', f'{mixer}', f'0%'])
            answer.append([mixer,sub_return])
        return answer


if __name__ == '__main__':
    _, mode = sys.argv
    if os.name != 'nt':
        if mode == 'test':
            print(AudioHandler.test_mixers())
        AudioHandler.change_volume('100')
