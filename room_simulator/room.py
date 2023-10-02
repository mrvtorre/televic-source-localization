import numpy as np
import pyroomacoustics as pra
from typing import Optional, Any
from nptyping import NDArray, Shape, Float
import material


class Room:
    def __init__(self, walls: NDArray[Shape["3"], Float],
                 materials: Optional[material.Material] = None, fs: int = 16000) -> None:
        self.fs = fs

        assert walls.ndim == 1, f"Invalid dimension of `walls` (expected shape (3,) not {walls.shape})"
        assert walls.shape[
            0] == 3, f"Invalid dimension of `walls` (expected shape (3,) not {walls.shape})"

        self.walls = walls

        if materials is None:
            self.materials = material.Material()
        else:
            self.materials = materials

        self.room = self._construct_room()
        self.n_sources = 0
        self.n_mics = 0

    def _construct_room(self) -> pra.ShoeBox:
        room_materials = self.materials.get_room_materials()

        room = pra.ShoeBox(
            self.walls,
            fs=self.fs,
            materials=room_materials,
            max_order=40,
            use_rand_ism=True)

        return room

    def add_source(self, source: pra.SoundSource) -> None:
        self.room.add_soundsource(source)
        self.n_sources += 1

    def add_mic(self, loc: NDArray[Shape['3'], Float],
                directivity: Optional[pra.Directivity] = None) -> None:
        self.room.add_microphone(loc, self.fs, directivity)
        self.n_mics += 1

    def compute_rir(self) -> dict[str, NDArray[Shape["N"], Float]]:
        self.room.compute_rir()
        rirs = self.room.rir
        if rirs is None:
            raise ValueError("Computed rirs is empty")

        assert len(rirs) == self.n_mics
        assert len(rirs[0]) == self.n_sources

        ret_rirs = {}
        for mic in range(self.n_mics):
            for src in range(self.n_sources):
                key = f"src{src}_mic{mic}"
                ret_rirs[key] = rirs[mic][src]

        return ret_rirs

    def plot(self):
        return self.room.plot()

    def plot_rirs(self, kind: str = "ir"):
        ret = self.room.plot_rir(kind=kind)
        if ret is not None:
            return ret


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    walls = np.array([5, 3, 3])

    room = Room(walls)

    # Add a source somewhere in the room
    room.add_source(pra.SoundSource([1, 1, 1.8]))
    room.add_mic(np.array([1.5, 1.8, 1.0]))

    # room.image_source_model()
    fig, ax = room.plot()
    ax.set_xlim([-1, 6])
    ax.set_ylim([-1, 4])
    ax.set_zlim([-1, 4])

    rir = room.compute_rir()

    room.plot_rirs()

    plt.show()
    print("d")
