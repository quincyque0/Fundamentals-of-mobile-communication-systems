import math 
import numpy as np
import matplotlib.pyplot as plt


TXPowerBS = 46
N_BS = 3
TXPowerUE = 24
AntGainBS = 21
PenetrationM = 15
INTERF = 1


FRQ_AREA = 1.8
BW_UL = 10 * 10**6
BW_DL = 20 * 10**6

NoiseFigure_BS = 2.4
NoiseFigure_UE = 6
SINR_DL = 2
SINR_UL = 4
MIMO = 2
AREA = 100000
AREA_2 = 4000


MIMO_GAIN = 3
A = 46.3
B = 33.9
AREA_MALL_KM2 = 4    

# 1 Выполните расчет бюджета восходящего канала, используя
# входные данные и определите уровень максимально допустимых потерь
# сигнала MAPL_UL.
ThermalNoise_BS = -174 + 10 * math.log10(BW_UL)
RXSensBS = NoiseFigure_BS + ThermalNoise_BS + SINR_UL
FeederLoss = 2 + 0.4 + 0.5

MAPL_UL = TXPowerUE - FeederLoss + AntGainBS + MIMO_GAIN - INTERF - PenetrationM - RXSensBS
print(f"MAPL_UL(бюджета восходящего канала): {MAPL_UL}")

# 2 Выполните расчет бюджета нисходящего канала, используя
# входные данные и определите уровень максимально допустимых потерь
# сигнала MAPL_DL.
ThermalNoise_UE = -174 + 10*math.log10(BW_DL)
RXSensUE =  NoiseFigure_UE + ThermalNoise_UE + SINR_DL

MAPL_DL = TXPowerBS - FeederLoss + AntGainBS + MIMO_GAIN - INTERF - PenetrationM - RXSensUE
print(f"MAPL_DL(бюджета ниссходящего канала): {MAPL_DL}")

# 3 Постройте зависимость величины входных потерь радиосигнала от
# расстояния между приемником и передатчиком по всем трем описанным в п.2.2
# моделям. Выберите нужную модель для заданных условий.


#UMINLOS
frq = np.linspace(100, 100000, 1000)
distance = 1000
UMINLOS_PL =  26 * np.log10(frq) + 22.7 + 36.7 * np.log10(distance)
plt.figure(figsize=(10, 6))
plt.plot(frq, UMINLOS_PL, color='tab:blue', linewidth=2, label='UMi-NLOS Path Loss')
plt.title('UMi-NLOS Path Loss vs Frequency (d = 1000 m)', fontsize=14)
plt.xlabel('Frequency, MHz', fontsize=12)
plt.ylabel('Path Loss, dB', fontsize=12)
plt.grid(True, which='both', linestyle='--', alpha=0.7)
plt.legend(fontsize=11)
# plt.xscale('log')  

plt.tight_layout()
plt.show()

# Определите радиус базовой станции в восходящем и нисходящем каналах. По меньшему из полученных значений
#  рассчитайте площадь одной базовой станции и, исходя из заданной площади, вычислите требуемое количество 
# базовых станций (сайтов), необходимое для обеспечения непрерывного покрытия на этой территории.

d_UL = 10 ** ((MAPL_UL - 26 * np.log10(FRQ_AREA) - 22.7) / 36.7)
d_DL = 10 ** ((MAPL_DL - 26 * np.log10(FRQ_AREA) - 22.7) / 36.7)
print(f"Радиус UL: {d_UL:.0f} м")
print(f"Радиус DL: {d_DL:.0f} м")

R = min(d_UL, d_DL)   
S = 1.95 * R**2                             
N = math.ceil(AREA_MALL_KM2 / S)   
print(f"Радиус (меньший): {R}")
print(f"Площадь одной БС: {S:.3f}")
print(f"Количество БС: {N}")