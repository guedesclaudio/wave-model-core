from typing import Dict, List, Tuple
import pandas as pd
import matplotlib.pyplot as plt
from modules.storage.storage_service import StorageService
from modules.wave.services.calculate_wave_break_service import CalculateWaveBreakService
from modules.beach_profile.contracts.beach_profile_contract import PlotParams, ProfileParams
import os

class CreateBeachProfileService:
    def __init__(self, storage_service: StorageService, calculate_wave_break_service: CalculateWaveBreakService):
        self.storage_service = storage_service
        self.calculate_wave_break_service = calculate_wave_break_service

    def create_profiles_from_csv(self, profile_file_name: str, wave_data_file_name: str, output_dir: str = "./"):
        os.makedirs(output_dir, exist_ok=True)
        output_local_profile_file_path = os.path.join(output_dir, profile_file_name)
        output_local_wave_data_file_path = os.path.join(output_dir, wave_data_file_name)
        
        print(f"Iniciando download de '{profile_file_name}' e '{wave_data_file_name}'...")
        self.storage_service.download_file(profile_file_name, output_local_profile_file_path)
        self.storage_service.download_file(wave_data_file_name, output_local_wave_data_file_path)
        print("Download concluído (Etapa 1)")
        
        df_profile = pd.read_csv(output_local_profile_file_path)
        df_wave_data = pd.read_csv(output_local_wave_data_file_path)
        print("Leitura do arquivo concluída (Etapa 2)")
        
        col_triplets = self.transform_profile_array(df_profile)

        self.process_profiles(col_triplets, df_profile, profile_file_name, df_wave_data)

        os.remove(output_local_profile_file_path)
        os.remove(output_local_wave_data_file_path)
        print(f"Arquivos temporários em '{output_dir}' removidos.")

    def process_each_profile(self, params: ProfileParams) -> None:
        x_list, y_list, distance = self.get_params_from_profile(
            params.x_list, params.y_list, params.distance, params.df_profile
        )

        break_point_x, break_point_y = self.define_break_point(x_list, y_list, params.wave_break_depth)
        output_local_path, output_remote_path = self.handle_profile_file_name_path(
            params.profile_file_name, params.profile_index, params.wave_height
        )
        
        plot_params = PlotParams(
            x_list=x_list,
            y_list=y_list,
            distance=distance,
            break_point_x=break_point_x,
            break_point_y=break_point_y,
            wave_height=params.wave_height,
            output_path=output_local_path
        )
        self.plot_profile(plot_params)
        print("Etapa 3 concluída")
        
        self.upload_file(output_local_path, output_remote_path)
        
    def plot_profile(self, params: PlotParams) -> None:
        plt.figure(figsize=(10, 5))
        plt.plot(
            params.x_list, params.y_list,
            color="black",
            linewidth=2,
            label=f"Perfil de praia ({params.distance:.1f} m) | Altura da onda: {params.wave_height} m"
        )
        plt.fill_between(params.x_list, params.y_list, max(params.y_list) + 2, color="#a0522d", label="Terra")
        plt.fill_between(params.x_list, 0, params.y_list, color="#a1cfff", label="Mar")

        self.plot_wave_break_point(params.break_point_x, params.break_point_y)

        plt.gca().invert_yaxis()
        plt.xlabel("Distância (m)")
        plt.ylabel("Profundidade (m)")
        plt.title("Perfil de Praia 2D")
        plt.legend()
        plt.tight_layout()
        plt.savefig(params.output_path)
        plt.close()

    def plot_wave_break_point(self, break_point_x: float, break_point_y: float) -> None:
        if break_point_x is None and break_point_y is None:
            return
        
        label = f"Quebra da onda (x={break_point_x:.2f}, y={break_point_y:.2f})"
        
        plt.scatter(break_point_x, break_point_y, color='red', zorder=5, label=label)
        plt.annotate(
            "Ponto de quebra", xy=(break_point_x, break_point_y),
            xytext=(break_point_x + 5, break_point_y + 1),
            arrowprops=dict(facecolor='red', shrink=0.05),
            fontsize=10, color='red'
        )

    def transform_profile_array(self, df: pd.DataFrame) -> List[Tuple[str, str, str]]:
        num_columns_validation = 3

        if len(df.columns) % num_columns_validation != 0:
            raise ValueError("O número de colunas no DataFrame do perfil não é um múltiplo de 3 para formar triplas (X, Y, D).")
        
        col_triplets = [df.columns[i:i+num_columns_validation] for i in range(0, len(df.columns), num_columns_validation)]
        return col_triplets

    def process_profiles(
        self,
        col_triplets: List[Tuple[str, str, str]], 
        df_profile: pd.DataFrame, 
        profile_file_name: str, 
        df_wave_data: pd.DataFrame
    ) -> None:
        wave_height_list: List[float] = self.get_params_from_wave_data(df_wave_data)
        wave_break_data_list: List[Dict[str, float]] = self.create_wave_break_depth_list(wave_height_list)
        print(wave_height_list, "wave_height_list")
        print(wave_break_data_list, "wave_break_data_list")

        for wave_data in wave_break_data_list:
            current_wave_height = wave_data['wave_height']
            current_wave_break_depth = wave_data['wave_break_depth']

            for profile_index, (x_col, y_col, d_col) in enumerate(col_triplets, start=1):
                params = ProfileParams(
                    x_list=x_col,
                    y_list=y_col,
                    distance=d_col,
                    profile_index=profile_index,
                    df_profile=df_profile,
                    profile_file_name=profile_file_name,
                    wave_break_depth=current_wave_break_depth,
                    wave_height=current_wave_height
                )
                self.process_each_profile(params)

    def define_break_point(self, x_list: List[float], y_list: List[float], wave_break_depth: float) -> Tuple[str | None, str | None]:
        break_point_x = None
        break_point_y = None
        
        for y_index, profile_depth in enumerate(y_list):
            if profile_depth <= wave_break_depth:
                print(wave_break_depth, profile_depth)
                break_point_x = x_list[y_index]
                break_point_y = profile_depth
        
        return break_point_x, break_point_y

    def upload_file(self, output_local_path: str, output_remote_path: str) -> None:
        self.storage_service.upload_file(output_local_path, output_remote_path)
        os.remove(output_local_path)

        print("Etapa 4 concluída")

    def handle_profile_file_name_path(self, file_name: str, profile_index: int, wave_height: float) -> Tuple[str, str]:
        base_name = os.path.splitext(os.path.basename(file_name))[0]
        profile_file_name = f"profile_{base_name}_{profile_index}_{wave_height}.png"
        output_local_path = os.path.join("./", f"{profile_file_name}")
        output_remote_path = f"outputs/images/{profile_file_name}"

        return output_local_path, output_remote_path

    def get_params_from_profile(self, x_col: str, y_col: str, d_col: str, df_profile: pd.DataFrame) -> Tuple[List[float], List[float], float]:
        x = df_profile[x_col].dropna().tolist()
        y = df_profile[y_col].dropna().tolist()
        d = df_profile[d_col].dropna().tolist()

        min_len = min(len(x), len(y))
        x = x[:min_len]
        y = y[:min_len]
        distance = d[0]

        return x, y, distance

    def get_params_from_wave_data(self, df_wave_data: pd.DataFrame) -> List[float]:
        col_name = "height"
        wave_height_list = df_wave_data[col_name].dropna().tolist()

        return wave_height_list

    def create_wave_break_depth_list(self, wave_height_list: List[float]) -> List[Dict[str, float]]:
        wave_break_data_list: List[Dict[str, float]] = list(map(
            lambda wave_height: {
                'wave_height': wave_height,
                'wave_break_depth': self.calculate_wave_break_service.calculate_wave_break_depth_by_miche(wave_height)
            },
            wave_height_list
        ))

        return wave_break_data_list
