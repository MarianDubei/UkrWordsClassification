import multiprocessing
import time
import sys
import os


def eeg_log(log_file):
    os.system('putty -serial COM7 -sercfg 115200 -sessionlog C:\\Users\\dmr85\\Downloads\\UkrWordsClassification\\data\\logs\\record_' + log_file)

def eeg_timer(ukr_word):
    time.sleep(4)
    for j in range(20):
        for i in range(5):
            print(ukr_word)
            time.sleep(1)
    print("Finish")

if __name__ == '__main__':
    if sys.argv[1] == "victory":
	log_file = "victory.log"
	ukr_word = "Перемога"
    elif sys.argv[1] == "defeat":
	log_file = "lose.log"
	ukr_word = "Поразка"
    elif sys.argv[1] == "mystery":
	log_file = secret.log"
	ukr_word = "Таємниця"
    elif sys.argv[1] == "word":
	log_file = "word.log"
	ukr_word = "Слово"
    elif sys.argv[1] == "nothing":
	log_file = "nothing.log"
	ukr_word = ""

    start = time.time()

    process1 = multiprocessing.Process(target=eeg_log, args=(log_file,))
    process2 = multiprocessing.Process(target=eeg_timer, args=(ukr_word,))

    process1.start()
    process2.start()

    process1.join()
    process2.join()


    end = time.time()
    print("Final time", end - start)
