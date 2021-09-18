from colorama import Fore, Back, Style
from scipy.io.wavfile import write
from typing import List

import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

import argparse
import random
import sys
import wave

CHANNELS = 2
SAMPLE_RATE = 44100
COLORS = [
    'r', 'g', 'b',
    'y', 'm', 'c',
]


def record(name: str, duration: int) -> str:
    output_file = name + '.wav'

    try:
        rec = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS, dtype=np.int16)
        sd.wait()
        write(output_file, SAMPLE_RATE, rec)
    except:
        raise Exception(Back.RED+Fore.WHITE+"Recording failed: {}"+Style.RESET_ALL .format(name))

    return output_file

def create_signal(file: str) -> np.ndarray:
    try:
        spf = wave.open(file, "r")
        signal = spf.readframes(-1)
        signal = np.frombuffer(signal, np.int16)
    except:
        raise Exception(Back.RED + Fore.WHITE + f"Read failed: {name}.wav" + Style.RESET_ALL)

    print(Fore.YELLOW + f"Signal was created ({file})\n" + Style.RESET_ALL)

    return signal

def ploty(count: int, names: List[str], signal_data: List[np.ndarray]) -> None:
    if count == 1:
        plt.plot(signal_data[0], random.choice(COLORS))
        plt.title(names[0])
    else:
        fig, axs = plt.subplots(count)

        for c in range(count):
            axs[c].plot(signal_data[c], random.choice(COLORS))
            axs[c].set_title(names[c])
    
        fig.tight_layout()
    plt.show()

def start(duration: int, count: int, names: List[str]) -> None:
    signal_data: List[np.ndarray] = []
    
    for name in names:
        input(Fore.GREEN + f"Start recording for {name} (Press enter)" + Style.RESET_ALL)
        print(Fore.BLUE + f"({name}) Recording..." + Style.RESET_ALL)
        
        rec = record(name, duration)
        
        signal = create_signal(rec)
        signal_data.append(signal)
    
    ploty(count, names, signal_data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--duration", type=int, required=True, help="recording duration")
    parser.add_argument("-c", "--count", type=int, required=True, help="count of sound")
    parser.add_argument("-n", "--names", type=str, required=True, help="list of name")

    args = parser.parse_args()
    
    duration: int = args.duration
    count: int = args.count
    names: List[str] = [str(name) for name in args.names.split(',')]

    if count != len(names):
        print(f"length of count and length of names must be same: {count} != {len(names)}")
        sys.exit(0)

    start(duration, count, names)
