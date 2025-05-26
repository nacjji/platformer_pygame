class DifficultySettings:
    def __init__(self,
                 platform_width_decrease,
                 moving_platform_speed,
                 moving_platform_max_speed,
                 moving_platform_chance,
                 transform_min_speed,
                 transform_max_speed,
                 transform_min_width_ratio,
                 vanish_interval,
                 vanish_duration,
                 vanish_platform_chance,
                 score_multiplier):
        self.platform_width_decrease = platform_width_decrease
        self.moving_platform_speed = moving_platform_speed
        self.moving_platform_max_speed = moving_platform_max_speed
        self.moving_platform_chance = moving_platform_chance
        self.transform_min_speed = transform_min_speed
        self.transform_max_speed = transform_max_speed
        self.transform_min_width_ratio = transform_min_width_ratio
        self.vanish_interval = vanish_interval
        self.vanish_duration = vanish_duration
        self.vanish_platform_chance = vanish_platform_chance
        self.score_multiplier = score_multiplier


# 난이도별 설정 객체 생성
EASY = DifficultySettings(
    platform_width_decrease=0,  # 미적용
    moving_platform_speed=1,
    moving_platform_max_speed=4,
    moving_platform_chance=0.2,
    transform_min_speed=0.4,
    transform_max_speed=2.4,
    transform_min_width_ratio=0.3,
    vanish_interval=3000,
    vanish_duration=500,
    vanish_platform_chance=0.1,
    score_multiplier=0.9
)

NORMAL = DifficultySettings(
    platform_width_decrease=1,
    moving_platform_speed=2,
    moving_platform_max_speed=5,
    moving_platform_chance=0.3,
    transform_min_speed=0.5,
    transform_max_speed=2.0,
    transform_min_width_ratio=0.2,
    vanish_interval=2000,
    vanish_duration=1000,
    vanish_platform_chance=0.2,
    score_multiplier=1.0
)

HARD = DifficultySettings(
    platform_width_decrease=2,
    moving_platform_speed=3,
    moving_platform_max_speed=6,
    moving_platform_chance=0.4,
    transform_min_speed=0.6,
    transform_max_speed=1.6,
    transform_min_width_ratio=0.1,
    vanish_interval=1000,
    vanish_duration=1500,
    vanish_platform_chance=0.3,
    score_multiplier=1.5
)

# 난이도 설정 매핑
DIFFICULTY_SETTINGS = {
    "Easy": EASY,
    "Normal": NORMAL,
    "Hard": HARD
}
