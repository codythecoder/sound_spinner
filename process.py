from scipy.io import wavfile
import os
from src.misc import mkdirpath

data_folder = r'./data'
filename = 'hey.wav'

min_limit = 8000
bits = 16

pre_spike = 0.08
sample_size = 0.2



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
