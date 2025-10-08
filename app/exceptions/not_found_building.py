class NotFoundBuildingException(Exception):

    def __init__(self, building_schema: str):
        super().__init__(f'Не найдено здание {building_schema=}')
