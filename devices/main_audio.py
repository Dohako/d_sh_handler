from os import name as os_name
from subprocess import call
import sys

if os_name != 'nt':
    import alsaaudio as alsa
else:
    pass

def set_volume(param:str, logger) -> str:
    logger.info("Управление звуком зарегистрировано")
    if os_name != 'nt':
        volume = param
        if volume.isdigit():
            int_volume = int(volume)
            if int_volume > 100:
                audio_answer = call(['amixer', '-D', 'pulse', 'sset', 'Master', '100%'])
                message = f"Ставлю звук на максимум({audio_answer})"
            elif int_volume < 0:
                audio_answer = call(['amixer', '-D', 'pulse', 'sset', 'Master', '0%'])
                message = f"Выключаю звук({audio_answer})"
            else:
                audio_answer = call(['amixer', '-D', 'pulse', 'sset', 'Master', f'{int_volume}%'])
                message = f"Ставлю звук на {int_volume}({audio_answer})"
        else:
            audio_answer = call(['amixer', '-D', 'pulse', 'sset', 'Master', '0%'])
            message = f"Команда не распознана до конца, выключаю звук({audio_answer})"
    else:
        message = "Не та ОС"

    # self.bot.send_message(chat, message)
    logger.info(message)
    return message

def change_volume(volume: str, logger):
    logger.info("Управление звуком зарегистрировано")
    int_volume = normalize_param(volume)
    logger.info(f"{volume}")
    audio_answer = call(['amixer', '-D', 'pulse', 'sset', 'Headphone', f'{int_volume}%'])
    logger.info(str(audio_answer))
    return audio_answer

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

    def change_volume_alsa(self,volume:str):
        int_volume = normalize_param(volume)
        self.m.setvolume(int_volume)

    @staticmethod
    def test_mixers():
        mixers = alsa.mixers()
        answer = []
        for mixer in mixers:
            sub_return = call(['amixer', '-D', 'pulse', 'sset', f'{mixer}', f'0%'])
            answer.append([mixer,sub_return])
        return answer


if __name__ == '__main__':
    _, mode = sys.argv
    if os_name != 'nt':
        if mode == 'test':
            print(AudioHandler.test_mixers())
        AudioHandler.change_volume('100')
