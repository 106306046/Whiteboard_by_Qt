import matplotlib.pyplot as plt
from mne_realtime import LSLClient
import time

import numpy as np
from sklearn import preprocessing
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

import mne
from mne.datasets import sample
from mne.decoding import Vectorizer, FilterEstimator

from mne_realtime import StimServer
from mne_realtime import MockRtClient

import multiprocessing as mp

from fbcca import fbcca

print(__doc__)

# this is the host id that identifies your stream on LSL
host_id = 'openbcigui'
# this is the max wait time in seconds until client connection
wait_max = 10
# this is to end this program
end = 0

list_freqs = []
num_harms = 3
num_fbs = 5

# TODO: classifior for the eeg data
# name: mi_model


with StimServer(port=4218) as stim_server:
    with LSLClient(info=None, host=host_id, wait_max=wait_max) as client:
        client_info = client.get_measurement_info()
        sfreq = int(client_info['sfreq'])

        stim_server.start(verbose=True)

        while (end!=True):
            epoch = client.get_data_as_epoch(n_samples=sfreq)
            X = epoch.get_data()
            stim_server.add_trigger(11)

            '''
            q = mp.Queue()
            p1 = mp.Process(target=pred_model, args=('mi_model',))
            p2 = mp.Process(target=fbcca, args=(X, list_freqs, sfreq, num_harms, num_fbs))
            p1.start()
            p2.start()
            p1.join()
            p2.join()
            mi_pred = q.get()
            ssvep_pred = q.get()

            y_pred = ssvep_pred*10 + mi_pred

            stim_server.add_trigger(y_pred)
            '''
