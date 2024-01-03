from datetime import datetime
import numpy as np
import mne
from mne_realtime import LSLClient
import tensorflow as tf
import multiprocessing as mp
from fbcca import fbcca_realtime
import pickle
import mne_lsl

# this is the host id that identifies your stream on LSL
host_id = 'openbcigui'
# this is the max wait time in seconds until client connection
wait_max = 10
# this is to end this program
end = 0

list_freqs = [6,4.3,7.6,10]
num_harms = 6
num_fbs = 4

# name: mi_model
mi_pred = 0

with open('variables.pickle', 'rb') as f:
    binary_class_dict = pickle.load(f)
    band_dict = pickle.load(f)
    CSPs = pickle.load(f)

mi_model = tf.keras.saving.load_model(filepath)

def MI_pred(epoch, model = mi_model, binary_class_dict = binary_class_dict, band_dict = band_dict, CSPs = CSPs, sfreq = 125):
    sample_per_step = int(sfreq / 2)

    data_of_combination = {}

    for binary_class in binary_class_dict.values():
        class1, class2 = binary_class
        Bl, Bh = band_dict[binary_class]
        epochs_fil = epoch.copy().filter(Bl, Bh, method='iir', verbose=False)
        data_fil = epochs_fil.get_data(copy=True)

        # 原本的算法
        data_csp = CSPs[(class1, class2)].transform(data_fil)

        section1 = np.log(np.var(data_csp[:, :, :sfreq], axis=2, keepdims=True))
        section2 = np.log(
            np.var(data_csp[:, :, sample_per_step * 1:sample_per_step * 1 + sfreq], axis=2, keepdims=True))
        section3 = np.log(
            np.var(data_csp[:, :, sample_per_step * 2:sample_per_step * 2 + sfreq], axis=2, keepdims=True))
        data_of_combination[binary_class] = np.concatenate((section1, section2, section3), axis=2)

    merged_arrays = []

    for binary_class in data_of_combination:
        array = data_of_combination[binary_class]
        merged_arrays.append(array)

    data_merged = np.concatenate(merged_arrays, axis=1)

    X_shape = data_merged.shape
    X_test = data_merged.reshape((X_shape[0], X_shape[1], X_shape[2], 1, 1))

    # print(model.predict(X_test))
    pred = np.argmax(model.predict(X_test), axis=-1)[0] +6
    return pred


with LSLClient(info=None, host=host_id, wait_max=wait_max) as client:
    client_info = client.get_measurement_info()
    sfreq = int(client_info['sfreq'])
    X = []

    while (end!=True):
        epoch = client.get_data_as_epoch(n_samples=sfreq*2)
        X_new = epoch.get_data()

        np.concatenate((X, X_new), axis=1)
        print(X)


        q = mp.Queue()
        p1 = mp.Process(target=MI_pred, args=('epoch',))
        p2 = mp.Process(target=fbcca_realtime, args=(X, list_freqs, sfreq,num_harms,num_fbs))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        mi_pred = q.get()
        ssvep_pred = q.get()


        if mi_pred == 6: #BH
            mi_output = 'Up'
        elif mi_pred == 7: #F
            mi_output = 'Down'
        elif mi_pred == 8: #LH
            mi_output = 'Left'
        elif mi_pred == 9: #RH
            mi_output = 'Right'
        else: #SSVEP
            mi_output = 'idle'


        if ssvep_pred == 0:
            ssvep_output = 'E'
        elif ssvep_pred == 1:
            ssvep_output = 'A'
        elif ssvep_pred == 2:
            ssvep_output = 'B'
        elif ssvep_pred == 3:
            ssvep_output = 'C'
        else:
            ssvep_output = 'idle'



        current_time = datetime.now()

        with open('log.txt', 'a') as f:
            f.write(str(current_time) + ' ' + str(mi_output) + ' ' + str(ssvep_output) + '\n')
