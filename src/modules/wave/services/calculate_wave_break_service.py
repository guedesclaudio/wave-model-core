import math

class CalculateWaveBreakService:
    def __init__(self):
        self.miche_breaking_index = 0.78

    def calculate_wave_break_depth_by_miche(self, wave_height: float) -> float:
        """
        Calcula a profundidade mínima para quebra da onda com base no critério de Miche.
        """
        point_break_depth = wave_height / self.miche_breaking_index
        return point_break_depth

    def calculate_incidence_angle(self, wave_direction_deg: float, coast_normal_deg: float) -> float:
        """
        Calcula o ângulo de incidência θ entre a direção da onda e a normal da costa,
        limitado ao intervalo [0°, 90°], retornando o valor em radianos.
        """
        theta = abs(wave_direction_deg - coast_normal_deg) % 360

        # Reduz para [0°, 180°]
        if theta > 180:
            theta = 360 - theta

        # Reduz para [0°, 90°] (simetria do cosseno)
        if theta > 90:
            theta = 180 - theta

        return math.radians(theta)


    def calculate_wave_break_depth_by_miche_with_angle(self, wave_height: float, wave_direction_deg: float, coast_normal_deg: float) -> float:
        """
        Calcula a profundidade mínima para quebra da onda ajustando com base no ângulo de incidência.
        :param wave_height: Altura da onda (H) em metros.
        :param wave_direction_deg: Direção de onde a onda vem (em graus, 0 = Norte).
        :param coast_normal_deg: Direção normal à costa (em graus, 0 = Norte).
        """
        
        theta_rad = self.calculate_incidence_angle(wave_direction_deg, coast_normal_deg)
        gamma_theta = self.miche_breaking_index * math.cos(theta_rad)
        self.check_parallel_wave(gamma_theta)

        # Profundidade mínima para quebra
        point_break_depth = wave_height / gamma_theta
        return point_break_depth

    def check_parallel_wave(self, gamma_theta: float,):
        # Evita divisão por zero (ex: onda paralela à costa)
        if gamma_theta <= 0:
            raise ValueError("Invalid breaking index: gamma_theta <= 0")
