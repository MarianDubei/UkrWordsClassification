import matplotlib.pyplot as plt
from scipy import signal
import seaborn as sns
import pandas as pd


def hex_to_dec(s):
    return int(s, 16)


def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val


def hex_to_dec_twos_comp(s):
    return twos_comp(hex_to_dec(s), 24)


def counts_to_volts(counts):
    return (int(counts)/24)*((4.5)/(2**24))


def get_channels_from_file(filename, counts=False):
    f = open(filename, "r")
    lines = f.readlines()
    eeg_data = [] # samples
    eeg_counter = 0
    for line in lines:
        line = line.split(" ")
        eeg_data.append([])
        for i in range(len(line)):
            if counts:
                eeg_data[eeg_counter].append(counts_to_volts(line[i]))
            else:
                eeg_data[eeg_counter].append(float(line[i]))
        eeg_counter += 1

    eeg_channels = [[] for x in range(8)]
    for sample in eeg_data:
        for i in range(8):
            eeg_channels[i].append(sample[i])
    return eeg_channels


def manual_filter_file(data, counts=True):

    f = open(data, "r", errors='ignore')
    lines = f.readlines()[41:1041]
    eeg_data = []
    eeg_counter = 0
    for line in lines:
        line = line.split(" ")
        eeg_data.append([])
        for i in range(len(line)):
            if counts:
                eeg_data[eeg_counter].append(counts_to_volts(line[i]))
            else:
                eeg_data[eeg_counter].append(float(line[i]))
        eeg_counter += 1

    # current_range = [[1, 2], [1, 2]]
    current_range = [[-5, 5], [-5, 5]]

    for i in range(1, len(eeg_data) - 1):
        for j in range(0, 4):
            if eeg_data[i][j] < current_range[0][0] or eeg_data[i][j] > current_range[0][1]:
                eeg_data[i][j] = (eeg_data[i - 1][j] + eeg_data[i + 1][j]) / 2
        for j in range(4, 8):
            if eeg_data[i][j] < current_range[1][0] or eeg_data[i][j] > current_range[1][1]:
                eeg_data[i][j] = (eeg_data[i - 1][j] + eeg_data[i + 1][j]) / 2

    # f = open("data/no_filter_logs/record_" + data.split('.')[0].split("_")[-1] + ".log", "w")
    # for i in range(len(eeg_data)):
    #     if i == 17000:
    #         break
    #     l = [str(x) for x in eeg_data[i]]
    #     s = " ".join(l) + '\n'
    #     f.write(s)
    #
    # f.close()
    return eeg_data


def filter_channel(filtered_eeg_channel, channel_number):
    dataset_y=[]
    dataset_x=[]
    x=0
    for a in filtered_eeg_channel:
     dataset_y.append(float(a))
     x=x+1
     dataset_x.append(x)

    def butter_highpass(cutoff, fs, order=3):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
        return b, a

    def butter_highpass_filter(data, cutoff, fs, order=5):
        b, a = butter_highpass(cutoff_high, fs, order=order)
        y = signal.filtfilt(b, a, data)
        return y

    def butter_lowpass(cutoff, fs, order=4):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
        return b, a

    def butter_lowpass_filter(data, cutoff, fs, order=4):
        b, a = butter_lowpass(cutoff, fs, order=order)
        y = signal.lfilter(b, a, data)
        return y

    fps = 206
    cutoff_high=0.5
    cutoff_low=10

    filtered_sine_high = butter_highpass_filter(dataset_y, cutoff_high, fps)
    filtered_sine_low =  butter_lowpass_filter(dataset_y, cutoff_low, fps)
    filtered_high_pass= butter_lowpass_filter(filtered_sine_high, cutoff_low, fps)

    return filtered_high_pass

def word_decryptor(l):
    j = int(sum(l)/len(l))
    if j == 3:
        word = "Слово"
    if j == 2:
        word = "Таємниця"
    if j == 1:
        word = "Поразка"
    if j == 0:
        word = "Перемога"
    else:
        word = "Nothing"

    return word
