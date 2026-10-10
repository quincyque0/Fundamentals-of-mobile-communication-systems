import matplotlib.pyplot as plt
import numpy as np
import sys
import math
# manager = plt.get_current_fig_manager()
# manager.full_screen_toggle()


def dft(f):
    N = len(f)
    F = np.zeros(N, dtype=complex)
    for x in range(N):              
        s = 0j
        for n in range(N):         
            s += f[n] * complex(
                math.cos(2 * math.pi * x * n / N),
               -math.sin(2 * math.pi * x * n / N) 
            )
        F[x] = s
    return F
def idft(F):
    N = len(F)
    f = np.zeros(N, dtype=complex)
    for n in range(N):
        s = 0j
        for x in range(N):
            s += F[x] * complex(
                math.cos(2 * math.pi * x * n / N),
                math.sin(2 * math.pi * x * n / N)
            )
        f[n] = s / N
    return f

frequency = 12 * 8
disc_freq = frequency * 2

t = np.linspace(0, 1, disc_freq)
f = 18
y = [math.cos(12 * math.pi * f * i) + math.cos(8 * math.pi * f * i) for i in t]

t2 = np.linspace(0,1, disc_freq * 4)
y2 = [math.cos(12 * math.pi * f * i) + math.cos(8 * math.pi * f * i) for i in t2]


fig, axs = plt.subplots(2, 3, figsize=(14, 8))

fft_box = dft(y)
dft_box = dft(fft_box)
bytes_count = fft_box.nbytes
print(f"bc1{bytes_count}")

fft_box_2 = dft(y2)
dft_box_2 = dft(fft_box_2)
bytes_count_2 = fft_box_2.nbytes
print(f"bc2: {bytes_count_2}")
#просто грфик
# plt.plot(t, y, label='y = cos(12πft) + cos(8πft)', color='blue', linestyle='-', linewidth=1.5)
# plt.xlabel('Время', fontsize=12)
# plt.ylabel('Амплитуда', fontsize=12)
#dft 1
# plt.plot(t, dft_box, label='f', color='red', linestyle='-', linewidth=1.5)
# dft 2
axs[0, 0].plot(t, y, color='blue', linestyle='-', linewidth=1.5)
axs[0, 0].set_title('исходный')
axs[0, 0].grid(True)

axs[0, 1].plot(t, fft_box, label='f', color='red', linestyle='-', linewidth=1.5)
axs[0, 1].set_title('после fft')
axs[0, 1].grid(True)

axs[0, 2].plot(t, dft_box, label='f', color='green', linestyle='-', linewidth=1.5)
axs[0, 2].set_title('востановленный')
axs[0, 2].grid(True)

axs[1, 0].plot(t2, y2, color='blue', linestyle='-', linewidth=1.5)
axs[1, 0].set_title('исходный x 4')
axs[1, 0].grid(True)

axs[1, 1].plot(t2, fft_box_2, label='f', color='red', linestyle='-', linewidth=1.5)
axs[1, 1].set_title('после fft x 4')
axs[1, 1].grid(True)

axs[1, 2].plot(t2, dft_box_2, label='f', color='green', linestyle='-', linewidth=1.5)
axs[1, 2].set_title('востановленный x 4')
axs[1, 2].grid(True)

freqs = np.arange(len(fft_box)) * (disc_freq / len(fft_box))
amplitude = np.abs(fft_box)




# print(fft_box)


plt.tight_layout()
plt.show()