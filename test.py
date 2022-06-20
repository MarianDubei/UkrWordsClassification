from tensorflow.keras.models import load_model
import ukr_words_eeg_processing
import multiprocessing
import numpy as np
import time
import sys
import os


def eeg_log(log_file):
    os.system('sudo putty /dev/ttyUSB0 -serial -sercfg 115200,8,n,1,N -sessionlog ' + log_file + ' > /dev/null 2>&1')
    # Windows
    # os.system('putty -serial COM7 -sercfg 115200 -sessionlog ' + log_file)


def eeg_timer():
    time.sleep(4)
    print("Recording")
    for i in range(5):
        print(".")
        time.sleep(1)

    os.system('sudo killall putty')
    # Windows
    # os.system('taskkill /IM "putty.exe" /F >nul 2>&1')
    print("\nComplete")


def get_word(log_file):

    raw_eeg_data = ukr_words_eeg_processing.manual_filter_file(log_file)

    eeg_channels = [[] for x in range(8)]
    for sample in raw_eeg_data:
        for i in range(8):
            eeg_channels[i].append(sample[i])

    filtered_eeg_channels = []
    for i in range(8):
        filtered_eeg_channels.append(ukr_words_eeg_processing.filter_channel(eeg_channels[i], i + 1))

    lines = []
    for i in range(len(filtered_eeg_channels[0])):
        l = []
        for j in range(8):
            l.append(filtered_eeg_channels[j][i])
        l = [str(x) for x in l]
        lines.append(" ".join(l))

    N_logs = 1
    N_channels = 8
    N_samples = 1000

    X = np.zeros((N_logs, N_channels, N_samples))

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

    model = load_model('models/1dcnn_lstm_v2.h5')
    pred = model.predict(X_test)

    Y_pred = np.argmax(pred, axis=1)
    return ukr_words_eeg_processing.word_decryptor(Y_pred)


if __name__ == '__main__':

    log_file = "/home/neizer/Diploma/UkrWordsClassification/data/test_logs/record_3.log"

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
