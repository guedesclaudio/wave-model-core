from dataclasses import dataclass
from typing import List
import pandas as pd

@dataclass
class ProfileParams:
    x_list: List[float]
    y_list: List[float]
    distance: float
    profile_index: int
    df_profile: pd.DataFrame
    profile_file_name: str
    wave_break_depth: float
    wave_height: float

@dataclass
class PlotParams:
    x_list: List[float]
    y_list: List[float]
    distance: float
    break_point_x: float
    break_point_y: float
    wave_height: float
    output_path: str
