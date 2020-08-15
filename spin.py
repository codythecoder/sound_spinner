from scipy.io import wavfile
from src.consts import *
import os
import tensorflow as tf
import numpy as np

name = 'hey'
folder = os.path.join(data_folder, name)


class Autoencoder(tf.keras.models.Model):
    def __init__(self, latent_size):
        super(Autoencoder, self).__init__()
        self.encoder = tf.keras.Sequential([
            tf.keras.layers.Dense(int(sample_size*0.8), activation='relu', input_shape=(sample_size,)),
            tf.keras.layers.Dense(int(sample_size*0.5), activation='relu'),
            tf.keras.layers.Dense(int(sample_size*0.2), activation='relu'),
            tf.keras.layers.Dense(latent_size, activation='relu'),
        ])

        self.decoder = tf.keras.Sequential([
            tf.keras.layers.Dense(int(sample_size*0.2), activation='relu'),
            tf.keras.layers.Dense(int(sample_size*0.5), activation='relu'),
            tf.keras.layers.Dense(int(sample_size*0.8), activation='relu'),
            tf.keras.layers.Dense(sample_size, activation='sigmoid'),
        ])

    def call(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded


files = os.listdir(folder)
print(files)

fs, _ = wavfile.read(os.path.join(folder, files[0]))
data = np.array([wavfile.read(os.path.join(folder, filename))[1][:,0]/max_value for filename in files])

sample_size = int(sample_size * fs)
print(sample_size, 'samples')

model = Autoencoder(latent_size)

model.compile(
    optimizer='adam',
    loss=tf.keras.losses.MeanSquaredError(),
)

print(data.shape)

model.fit(data, data, shuffle=True, epochs=10)

in_value = model.encoder(np.array([data[0]]))
print(in_value)
out = model.decoder(np.array([[0, 0]]))
print(out)
wavfile.write('out1.wav', fs, np.array(out[0]))
out = model.decoder(in_value)
print(out)
wavfile.write('out2.wav', fs, np.array(out[0]))
