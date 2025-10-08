class StorageNegativeException(Exception):

    def __init__(self, value1: int, value2: int):
        super().__init__(f'Нельзя уменьшить {value1} - {value2}')
