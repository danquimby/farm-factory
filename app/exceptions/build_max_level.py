class BuildingMaxLevelException(Exception):
    def __init__(self, level: int):
        super().__init__(f'Здание выше максимального уровня {level}')
