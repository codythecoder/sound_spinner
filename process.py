from scipy.io import wavfile
import os
from src.misc import mkdirpath
from src.consts import *

filename = 'hey.wav'


name = filename.rsplit('.', 1)[0]
mkdirpath(os.path.join(data_folder, name))

print(os.path.join(data_folder, name, '_'))

fs, data = wavfile.read(os.path.join(data_folder, filename))

pre_spike = int(pre_spike * fs)
sample_size = int(sample_size * fs)

i = j = 0
while i < len(data):
    if data[i, 0] > min_limit:
        start = i - pre_spike
        end = start + sample_size
        print(start, end)
        wavfile.write(os.path.join(data_folder, name, f'{j:0>3}.wav'), fs, data[start:end])
        i = end
        j += 1
    i += 1
