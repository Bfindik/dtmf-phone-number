import numpy as np
from scipy.io.wavfile import write
from scipy.io.wavfile import read
from matplotlib import pyplot as plt
import math


# frekansa göre ses üretme fonksiyonu
def generate_dtmf_tone(f1, f2, duration, fs, amplitude):
    N = int(fs * duration)
    t = np.linspace(0, duration, N, False)
    sample = np.zeros(N)
    sample = amplitude * np.sin(2 * np.pi * f1 * t) + \
        amplitude * np.sin(2 * np.pi * f2 * t)
    return sample


def calculate_frequency_my_number(segment, sample_rate):
    numbers = []
    transform = np.fft.fft(segment, sample_rate)

   # plt.plot(transform)
   # plt.show()

    mat1 = [0, 0, 0, 0]  # 697,770,852,941
    mat2 = [0, 0, 0]  # 1209,1336,1477

    for i in range(len(transform)//2):

        if transform[i] > transform.max()/2:
            # print(i)
            if (abs(i-697) < 10):
                mat1[0] = 1
            elif (abs(i-770) < 10):
                mat1[1] = 1
            elif (abs(i-852) < 10):
                mat1[2] = 1
            elif (abs(i-941) < 10):
                mat1[3] = 1
            elif (abs(i-1209) < 10):
                mat2[0] = 1
            elif (abs(i-1336) < 10):
                mat2[1] = 1
            elif (abs(i-1477) < 10):
                mat2[2] = 1

    return mat1, mat2
def calculate_frequency(segment, sample_rate):
    numbers = []
    transform = np.fft.fft(segment, sample_rate)
    # plt.plot(transform)
    # plt.show()
    

    mat1 = [0, 0, 0, 0]  # 697,770,852,941
    mat2 = [0, 0, 0]  # 1209,1336,1477

    for i in range(len(transform)//2):

        if transform[i] > 15000:
            # print(i)
            if (abs(i-697) < 10):
                mat1[0] = 1
            elif (abs(i-770) < 10):
                mat1[1] = 1
            elif (abs(i-852) < 10):
                mat1[2] = 1
            elif (abs(i-941) < 10):
                mat1[3] = 1
            elif (abs(i-1209) < 10):
                mat2[0] = 1
            elif (abs(i-1336) < 10):
                mat2[1] = 1
            elif (abs(i-1477) < 10):
                mat2[2] = 1

    return mat1, mat2

duration = 0.2
fs = 8000
amplitude = 0.5
pause_duration = 0.1
audio = []
number = "05312507018"
dtmf_freqs = [
    [697, 770, 852, 941], [1209, 1336, 1477]
]

for digit in number:
    if digit == '1':
        f1 = dtmf_freqs[0][0]
        f2 = dtmf_freqs[1][0]
    elif digit == '2':
        f1 = dtmf_freqs[0][0]
        f2 = dtmf_freqs[1][1]
    elif digit == '3':
        f1 = dtmf_freqs[0][0]
        f2 = dtmf_freqs[1][2]
    elif digit == '4':
        f1 = dtmf_freqs[0][1]
        f2 = dtmf_freqs[1][0]
    elif digit == '5':
        f1 = dtmf_freqs[0][1]
        f2 = dtmf_freqs[1][1]
    elif digit == '6':
        f1 = dtmf_freqs[0][1]
        f2 = dtmf_freqs[1][2]
    elif digit == '7':
        f1 = dtmf_freqs[0][2]
        f2 = dtmf_freqs[1][0]
    elif digit == '8':
        f1 = dtmf_freqs[0][2]
        f2 = dtmf_freqs[1][1]
    elif digit == '9':
        f1 = dtmf_freqs[0][2]
        f2 = dtmf_freqs[1][2]
    elif digit == '*':
        f1 = dtmf_freqs[0][3]
        f2 = dtmf_freqs[1][0]
    elif digit == '0':
        f1 = dtmf_freqs[0][3]
        f2 = dtmf_freqs[1][1]
    elif digit == '#':
        f1 = dtmf_freqs[0][3]
        f2 = dtmf_freqs[1][2]
    tone = generate_dtmf_tone(f1, f2, duration, fs, amplitude)
    audio.extend(tone)
    audio.extend(np.zeros(int(pause_duration * fs)))
audio = np.array(audio, dtype=np.float32)
write('dtmf.wav', fs, audio)
# plt.plot(audio)
# plt.show()

sample_rate, audio_data = read("dtmf.wav")
# plt.plot(audio)
# plt.show()
#plt.stem(audio)
#plt.show()
digits=[]
segments = np.array_split(audio_data, 11)

for segment in segments:
    numbers, numbers2 = calculate_frequency_my_number(segment, sample_rate)
    print(numbers, numbers2)
    for i in range(0,4):
        if numbers[i]==1:
            if i==0:
                for j in range(0,3):
                    if numbers2[j]==1:
                        if j==0:
                            digits.append(1)
                        if j==1:
                            digits.append(2)
                        if j==2:
                            digits.append(3)
            if i==1:
                for j in range(0,3):
                    if numbers2[j]==1:
                        if j==0:
                            digits.append(4)
                        if j==1:
                            digits.append(5)
                        if j==2:
                            digits.append(6)
            if i==2:
                for j in range(0,3):
                    if numbers2[j]==1:
                        if j==0:
                            digits.append(7)
                        if j==1:
                            digits.append(8)
                        if j==2:
                            digits.append(9)
            if i==3:
                for j in range(0,3):
                    if numbers2[j]==1:
                        if j==0:
                            digits.append('*')
                        if j==1:
                            digits.append(0)
                        if j==2:
                            digits.append('#')
print(digits)
sample_rate, audio_data = read("Ornek.wav")
digits=[]
segments = np.array_split(audio_data, 11)
# plt.plot(audio)
# plt.show()
#plt.stem(audio)
#plt.show()
for segment in segments:
    numbers, numbers2 = calculate_frequency(segment, sample_rate)
    print(numbers, numbers2)
    for i in range(0,4):
        if numbers[i]==1:
            if i==0:
                for j in range(0,3):
                    if numbers2[j]==1:
                        if j==0:
                            digits.append(1)
                        if j==1:
                            digits.append(2)
                        if j==2:
                            digits.append(3)
            if i==1:
                for j in range(0,3):
                    if numbers2[j]==1:
                        if j==0:
                            digits.append(4)
                        if j==1:
                            digits.append(5)
                        if j==2:
                            digits.append(6)
            if i==2:
                for j in range(0,3):
                    if numbers2[j]==1:
                        if j==0:
                            digits.append(7)
                        if j==1:
                            digits.append(8)
                        if j==2:
                            digits.append(9)
            if i==3:
                for j in range(0,3):
                    if numbers2[j]==1:
                        if j==0:
                            digits.append('*')
                        if j==1:
                            digits.append(0)
                        if j==2:
                            digits.append('#')
print(digits)
