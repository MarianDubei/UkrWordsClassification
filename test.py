from tensorflow.keras.models import load_model
import multiprocessing
import numpy as np
import time
import sys
import os


def eeg_log(log_file):
    os.system('putty -serial COM7 -sercfg 115200 -sessionlog ' + log_file)


def eeg_timer():
    time.sleep(3)
    print("Recording")
    for i in range(5):
        print(".")
        time.sleep(1)

    os.system('taskkill /IM "putty.exe" /F >nul 2>&1')
    print("\nComplete")


def get_word(log_file):

    # TODO: filter data
    N_logs = 1
    N_channels = 8
    N_samples = 1000

    X = np.zeros((N_logs, N_channels, N_samples))

    f = open(log_file, "r")
    lines = f.readlines()[38:1038]

    eeg_data = np.zeros(shape=(N_channels, N_samples))
    sample_counter = 0
    for i in range(N_samples):
        line = lines[i].split(" ")
        for k in range(8):
            eeg_data[k][sample_counter] = float(line[k])
        sample_counter += 1

    X[0, :, :] = eeg_data

    X_test = np.zeros((122, 128, N_channels))
    npt = 128
    stride = 8
    ctr = 0
    for i in range(0, N_logs):
        a = X[i, :, :]
        a = a.transpose()
        val = 0
        while val <= (len(a) - npt):
            x = a[val:val + npt, :]
            X_test[ctr, :, :] = x
            val = val + stride
            ctr = ctr + 1

    #model = load_model('models/1dcnn_lstm.h5')
    #pred = model.predict(X_test)

    print(pred)
    return "s"


if __name__ == '__main__':

    log_file = "C:\\Users\\dmr85\\Downloads\\UkrWordsClassification\\data\\test_logs\\record_2.log"
    os.add_dll_directory("C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.7/bin")

    while True:
        print("Start recording word[Y/n]:")
        s = input()
        if s == "n" or s == "N":
            break
        elif s == "" or s == "y" or s == "Y":

            process1 = multiprocessing.Process(target=eeg_log, args=(log_file,))
            process2 = multiprocessing.Process(target=eeg_timer)

            process1.start()
            process2.start()

            process1.join()
            process2.join()

            word = get_word(log_file)
            print("\nEnvisioned word: " + word + "\n")
