import sys, tty, termios
import numpy as np
import sounddevice as sd

SR = 44100
t = np.linspace(0, 1.2, int(SR * 1.2), False)

def synth(f):
    s = sum(np.sin(2 * np.pi * f * n * (1 + 0.0004 * n**2) * t) * np.exp(-2.5 * n * t) / n for n in range(1, 5))
    return (s / np.max(np.abs(s)) * 0.75).astype(np.float32)

chars = "zsxdcvgbhnjmq2w3er5t6y7u"
samples = {c: synth(440 * 2 ** ((i - 9) / 12)) for i, c in enumerate(chars)}

fd = sys.stdin.fileno()
old = termios.tcgetattr(fd)
tty.setraw(fd)

while True:
    k = sys.stdin.read(1)
    if k in samples:
        sd.play(samples[k], SR)
