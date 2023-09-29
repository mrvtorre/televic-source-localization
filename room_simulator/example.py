import numpy as np
import matplotlib.pyplot as plt
import pyroomacoustics as pra

corpus = pra.datasets.CMUArcticCorpus(download=True, speaker=['bdl'])
sample = corpus.samples[0]

# Construct room
corners = np.array([[0, 0], [0, 3], [5, 3], [5, 1], [3, 1], [3, 0]]).T  # [x,y] in metres
room = pra.Room.from_corners(corners, fs=sample.fs, ray_tracing=True, air_absorption=True)
room.extrude(2.)  # metres

# Add source
room.add_source([1, 1, 0.7], signal=sample.data)

# Add  microphone
room.add_microphone([1.5, 1.5, 0.7])

fig, ax = room.plot()
ax.set_xlim([0, 5])
ax.set_ylim([0, 3])
ax.set_zlim([0, 2])

room.compute_rir()

room.plot_rir()

plt.show()
