
import soundfile as sf
import matplotlib.pyplot as plt

plt.close('all')

data, samplerate = sf.read('C:/Users/Sarah/Downloads/BabyElephantWalk60.wav')

plt.plot(data)
plt.show()

print(data.shape)
print(samplerate)


