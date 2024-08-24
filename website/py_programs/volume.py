from py_programs.word2num import word2num
from subprocess import call
import alsaaudio

def get_system_volume():
    mixer = alsaaudio.Mixer()
    volume = mixer.getvolume()[0]
    return volume

def volume(vol):
    if "?" in vol:
        return get_system_volume()
    if "increase" in vol:
        call(["amixer", "-D", "pulse", "sset", "Master", f"{word2num(vol)}%+"])
    elif "decrease" in vol:
        call(["amixer", "-D", "pulse", "sset", "Master", f"{word2num(vol)}%-"])
    elif "mute" in vol:
        call(["amixer", "-q", "-D", "pulse", "sset", "Master", "toggle"])
    else:
        f = call(["amixer", "-D", "pulse", "sset", "Master", f"{word2num(vol)}%"])
    return ""