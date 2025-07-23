import math

class CalculateWaveBreakService:
    def __init__(self):
        self.miche_breaking_index = 0.78

    def calculate_wave_break_depth_by_miche(self, wave_height: float) -> float:
        point_break_depth = wave_height / self.miche_breaking_index
        return point_break_depth

    def calculate_incidence_angle(self, wave_direction_deg: float, coast_normal_deg: float) -> float:
        theta = abs(wave_direction_deg - coast_normal_deg) % 360

        if theta > 180:
            theta = 360 - theta

        if theta > 90:
            theta = 180 - theta

        return math.radians(theta)


    def calculate_wave_break_depth_by_miche_with_angle(self, wave_height: float, wave_direction_deg: float, coast_normal_deg: float) -> float:
        theta_rad = self.calculate_incidence_angle(wave_direction_deg, coast_normal_deg)
        gamma_theta = self.miche_breaking_index * math.cos(theta_rad)
        self.check_parallel_wave(gamma_theta)

        point_break_depth = wave_height / gamma_theta
        return point_break_depth

    def check_parallel_wave(self, gamma_theta: float,):
        if gamma_theta <= 0:
            raise ValueError("Invalid breaking index: gamma_theta <= 0")
