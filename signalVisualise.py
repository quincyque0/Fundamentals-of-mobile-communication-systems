import matplotlib.pyplot as plt
import numpy as np
import math
manager = plt.get_current_fig_manager()
manager.full_screen_toggle()

frequency = 12 * 8
disc_freq = frequency * 2

t = np.linspace(0, 1, disc_freq)
f = 18
y = [math.cos(12 * math.pi * f * i) + math.cos(8 * math.pi * f * i) for i in t]
# fft_box = 
# fft_box = np.fft.fft(y)
# plt.plot(t, y, label='y = cos(12πft) + cos(8πft)', color='blue', linestyle='-', linewidth=1.5)
plt.plot(t, fft_box, label='f', color='red', linestyle='-', linewidth=1.5)

plt.xlabel('Время', fontsize=12)
plt.ylabel('Амплитуда', fontsize=12)

plt.grid(True, alpha=0.3)
plt.legend(fontsize=10)

# print(fft_box)


plt.tight_layout()
plt.show()