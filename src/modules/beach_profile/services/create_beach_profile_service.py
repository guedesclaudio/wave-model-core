import pandas as pd
import matplotlib.pyplot as plt
from modules.storage.storage_service import StorageService
from modules.wave.services.calculate_wave_break_service import CalculateWaveBreakService
import os

class CreateBeachProfileService:
    def __init__(self, storage_service: StorageService, calculate_wave_break_service: CalculateWaveBreakService):
        self.storage_service = storage_service
        self.calculate_wave_break_service = calculate_wave_break_service

    def create_profiles_from_csv(self, profile_file_name: str, wave_data_file_name, output_dir: str = "./"):
        output_local_file_path = os.path.join(output_dir, profile_file_name)
        
        self.storage_service.download_file(profile_file_name, output_local_file_path)
        print("Download concluído (Etapa 1)")
        
        df = pd.read_csv(output_local_file_path)
        print("Leitura do arquivo concluída (Etapa 2)")
        
        col_triplets = self.transform_profile_array(df)

        self.process_profiles(col_triplets, df, profile_file_name)

        os.remove(output_local_file_path)


    def process_each_profile(self, x_col, y_col, d_col, profile_index, df, file_name): #TODO - TROCAR OS NOMES file_name por profile_file_name
        x, y, distance = self.get_params_from_profile(x_col, y_col, d_col, df)

        wave_height = 5 #TODO - ALTERAR para começar a usar o wave_data
        wave_break_depth = self.calculate_wave_break_service.calculate_wave_break_depth_by_miche(wave_height)

        break_point_x, break_point_y = self.define_break_point(x, y, wave_break_depth)
        output_local_path, output_remote_path = self.handle_file_name_path(file_name, profile_index)
        
        self.plot_profile(x, y, distance, break_point_x, break_point_y, wave_height, output_local_path)
        print("Etapa 3 concluída")
        
        self.upload_file(output_local_path, output_remote_path)
        

    def plot_profile(self, x, y, distance, break_point_x, break_point_y, wave_height, output_path):
        plt.figure(figsize=(10, 5))
        plt.plot(
            x, y,
            color="black",
            linewidth=2,
            label=f"Perfil de praia ({distance:.1f} m) | Altura da onda: {wave_height} m"
        )
        plt.fill_between(x, y, max(y) + 2, color="#a0522d", label="Terra")
        plt.fill_between(x, 0, y, color="#a1cfff", label="Mar")

        self.plot_wave_break_point(break_point_x, break_point_y)

        plt.gca().invert_yaxis()
        plt.xlabel("Distância (m)")
        plt.ylabel("Profundidade (m)")
        plt.title("Perfil de Praia 2D")
        plt.legend()
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

    def plot_wave_break_point(self, break_point_x, break_point_y):
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

    def transform_profile_array(self, df):
        col_triplets = [df.columns[i:i+3] for i in range(0, len(df.columns), 3)]
        return col_triplets

    def process_profiles(self, col_triplets, df, file_name): 
        for profile_index, (x_col, y_col, d_col) in enumerate(col_triplets, start=1):
            self.process_each_profile(x_col, y_col, d_col, profile_index, df, file_name)

    def define_break_point(self, x, y, wave_break_depth):
        break_point_x = None
        break_point_y = None
        
        for y_index, profile_depth in enumerate(y):
            if profile_depth <= wave_break_depth:
                print(wave_break_depth, profile_depth)
                break_point_x = x[y_index]
                break_point_y = profile_depth
        
        return break_point_x, break_point_y

    def upload_file(self, output_local_path, output_remote_path):
        self.storage_service.upload_file(output_local_path, output_remote_path)
        os.remove(output_local_path)

        print("Etapa 4 concluída")

    def handle_file_name_path(self, file_name, profile_index):
        profile_file_name = f"perfil_{file_name}_{profile_index}.png"
        output_local_path = os.path.join("./", f"{profile_file_name}")
        output_remote_path = f"outputs/images/{profile_file_name}"

        return output_local_path, output_remote_path

    def get_params_from_profile(self, x_col, y_col, d_col, df):
        x = df[x_col].dropna().tolist()
        y = df[y_col].dropna().tolist()
        d = df[d_col].dropna().tolist()

        min_len = min(len(x), len(y))
        x = x[:min_len]
        y = y[:min_len]
        distance = d[0]

        return x, y, distance     
