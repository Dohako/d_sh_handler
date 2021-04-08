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
            m = alsa.Mixer('Master')  # Headphone
        elif 'Headphone' in self.mixers:
            m = alsa.Mixer('Headphone')
        else:
            m = None
        if m:
            current_volume = m.getvolume()
            m.setvolume(0)

    @staticmethod
    def change_volume(volume: str):
        if volume.isdigit():
            int_volume = int(volume)
            if int_volume > 150:
                int_volume = 100
            elif int_volume < 0:
                int_volume = 0
        else:
            int_volume = 0
        audio_answer = subprocess.call(['amixer', '-D', 'pulse', 'sset', 'Master', f'{int_volume}%'])
        return audio_answer

    @staticmethod
    def test_mixers():
        mixers = alsa.mixers()
        answer = []
        for mixer in mixers:
            answer.append(subprocess.call(['amixer', '-D', 'pulse', 'sset', f'{mixer}', f'0%']))
        return answer


if __name__ == '__main__':
    _, mode = sys.argv
    if os.name != 'nt':
        if mode == 'test':
            print(AudioHandler.test_mixers())
        # AudioHandler.change_volume('100')
