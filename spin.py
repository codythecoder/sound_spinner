from scipy.io import wavfile
from src.consts import *
import os
import tensorflow as tf

name = 'hey'
folder = os.path.join(data_folder, name)

files = os.listdir(folder)
print(files)

fs, _ = wavfile.read(os.path.join(folder, files[0]))
data = [wavfile.read(os.path.join(folder, filename))[1][:,0]/max_value for filename in files]

sample_size = int(sample_size * fs)
print(sample_size, 'samples')

model = tf.keras.Sequential([
    tf.keras.layers.Dense(int(sample_size*0.8), activation='relu', input_shape=(sample_size,)),
    tf.keras.layers.Dense(int(sample_size*0.5), activation='relu'),
    tf.keras.layers.Dense(int(sample_size*0.2), activation='relu'),
    tf.keras.layers.Dense(latent_size, activation='relu'),
    tf.keras.layers.Dense(int(sample_size*0.2), activation='relu'),
    tf.keras.layers.Dense(int(sample_size*0.5), activation='relu'),
    tf.keras.layers.Dense(int(sample_size*0.8), activation='relu'),
    tf.keras.layers.Dense(sample_size, activation='sigmoid'),
])

model.compile(
    optimizer='adam',
    loss=tf.keras.losses.MeanSquaredError(),
)

print(data)

model.fit(data, data, epochs=10)
