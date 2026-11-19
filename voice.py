import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import sounddevice as sd

filename = "meow.wav"
Fs, y = wavfile.read(filename)

if y.ndim > 1:
    y = y[:, 0]

if y.dtype == np.int16:
    y = y / 32768.0

factor = 10
y_down = y[::factor]
Fs_down = Fs // factor

def compute_spectrum(signal, sample_rate):
    N_samples = len(signal)
    fft_vals = np.fft.rfft(signal)
    freqs = np.fft.rfftfreq(N_samples, d=1.0 / sample_rate)
    amplitudes = np.abs(fft_vals) / N_samples
    amplitudes[1:] *= 2.0
    return freqs, amplitudes

freqs_orig, amp_orig = compute_spectrum(y, Fs)
freqs_down, amp_down = compute_spectrum(y_down, Fs_down)

def find_bandwidth(freqs, amps, threshold_ratio=0.01):
    threshold = np.max(amps) * threshold_ratio
    active_indices = np.where(amps >= threshold)[0]
    return freqs[active_indices[-1]] 

bw_orig = find_bandwidth(freqs_orig, amp_orig)
bw_down = find_bandwidth(freqs_down, amp_down)

print(f"Ширина спектра оригинального сигнала: {bw_orig:.1f} Гц : {Fs/2:.1f} Гц)")
print(f"Ширина спектра прореженного сигнала:   {bw_down:.1f} Гц : {Fs_down/2:.1f} Гц)")

fig, axes = plt.subplots(2, 1, figsize=(11, 7))

axes[0].plot(freqs_orig, amp_orig, color='navy', lw=0.7)
axes[0].set_title(f"Амплитудный спектр оригинала (Fs = {Fs} Гц)")
axes[0].set_xlabel("Частота, Гц")
axes[0].set_ylabel("Амплитуда")
axes[0].set_xlim([0, Fs / 2])
axes[0].grid(True, linestyle="--", alpha=0.6)

axes[1].plot(freqs_down, amp_down, color='crimson', lw=0.7)
axes[1].set_title(f"Амплитудный спектр прореженного сигнала (Fs = {Fs_down} Гц= {factor})")
axes[1].set_xlabel("Частота, Гц")
axes[1].set_ylabel("Амплитуда")
axes[1].set_xlim([0, Fs_down / 2])
axes[1].grid(True, linestyle="--", alpha=0.6)

plt.tight_layout()
plt.show()

f0 = 100.0
Fs_sim = 2000.0
T_sim = 1.0
t_sim = np.linspace(0, T_sim, int(Fs_sim * T_sim), endpoint=False)

x_analog = np.sin(2 * np.pi * f0 * t_sim)

def quantize_adc(x, bits):
    L_max = (2 ** bits) - 1
    x_scaled = (x + 1.0) / 2.0 * L_max
    x_quant = np.clip(np.round(x_scaled), 0, L_max)
    x_reconstructed = (x_quant / L_max) * 2.0 - 1.0
    return x_quant, x_reconstructed

bit_depths = [3, 4, 5, 6]
freqs_ref, amp_ref = compute_spectrum(x_analog, Fs_sim)
print("Играет оригинал")
sd.play(y, Fs)
sd.wait()

print(f"Играет прореженный сигнал (Fs = {Fs_down} Гц)")
sd.play(y_down, Fs_down)
sd.wait()
plt.figure(figsize=(12, 9))


for idx, bits in enumerate(bit_depths, 1):
    x_q_int, x_q_rec = quantize_adc(x_analog, bits)
    error = x_q_rec - x_analog
    mean_abs_error = np.mean(np.abs(error))
    
    print(f"Разрядность: {bits} бит (уровней: {2**bits:2d}) | "f"Средняя ошибка: {mean_abs_error:.5f}")
    
    f_q, a_q = compute_spectrum(x_q_rec, Fs_sim)
    
    plt.subplot(len(bit_depths), 1, idx)
    plt.plot(freqs_ref, amp_ref, color='gray', linestyle='--', label='Исходная синусоида (без квантования)')
    plt.plot(f_q, a_q, color='tab:red', lw=0.8, label=f'Квантование {bits} бит')
    plt.title(f'Спектр при разрядности АЦП {bits} бит (MAE = {mean_abs_error:.5f})')
    plt.xlabel('Частота, Гц')
    plt.ylabel('Амплитуда')
    plt.xlim([0, 500])
    plt.legend(loc='upper right')
    plt.grid(True, linestyle="--", alpha=0.5)
   

plt.tight_layout()
plt.show()