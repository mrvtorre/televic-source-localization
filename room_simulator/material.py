import pyroomacoustics as pra
import os
import io
import json
from typing import Optional, TypedDict


class MaterialDict(TypedDict):
    description: str
    coeffs: list[float]
    center_freqs: list[int]


class RoomMaterials(TypedDict):
    ceiling: pra.Material
    floor: pra.Material
    east: pra.Material
    west: pra.Material
    north: pra.Material
    south: pra.Material


class Material:
    def __init__(self, wall_mat: Optional[MaterialDict] = None, ceiling_mat: Optional[MaterialDict]
                 = None, floor_mat: Optional[MaterialDict] = None) -> None:

        _materials_database_fn = os.path.join(os.path.dirname(__file__), "data/materials.json")
        with io.open(_materials_database_fn, "r", encoding="utf8") as f:
            self.materials_data = json.load(f)

        self.center_freqs = self.materials_data["center_freqs"]

        # Construct default materials
        self._construct_default_materials()

        # Override if arguments are not None
        if ceiling_mat is not None:
            self.ceiling_mat = ceiling_mat
        if floor_mat is not None:
            self.floor_mat = floor_mat
        if wall_mat is not None:
            self.wall_mat = wall_mat

        self.room_materials = self._construct_room_materials()

    def _construct_default_materials(self):
        coeffs = self.materials_data["absorption"]["Ceiling absorbers"]["ceiling_plasterboard"]["coeffs"]
        self.ceiling_mat: MaterialDict = {
            "description": "Example ceiling material",
            "coeffs": coeffs,
            "center_freqs": self.center_freqs[:len(coeffs)],
        }
        coeffs = self.materials_data["absorption"]["Floor coverings"]["carpet_thin"]["coeffs"]
        self.floor_mat: MaterialDict = {
            "description": "Example floor material",
            "coeffs": coeffs,
            "center_freqs": self.center_freqs[:len(coeffs)],
        }
        coeffs = self.materials_data["absorption"]["Wood"]["plywood_thin"]["coeffs"]
        self.wall_mat: MaterialDict = {
            "description": "Example wall material",
            "coeffs": coeffs,
            "center_freqs": self.center_freqs[:len(coeffs)],
        }

    def _construct_room_materials(self) -> RoomMaterials:
        d = pra.make_materials(
            ceiling=self.ceiling_mat,
            floor=self.floor_mat,
            east=self.wall_mat,
            west=self.wall_mat,
            north=self.wall_mat,
            south=self.wall_mat,
        )

        return d

    def get_ceiling_materials(self) -> MaterialDict:
        return self.ceiling_mat

    def get_floor_materials(self) -> MaterialDict:
        return self.floor_mat

    def get_wall_materials(self) -> MaterialDict:
        return self.wall_mat

    def get_room_materials(self) -> RoomMaterials:
        return self.room_materials


if __name__ == "__main__":
    materials = Material()
