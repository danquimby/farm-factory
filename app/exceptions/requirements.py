class NotEnoughException(Exception):

    def __init__(self, need_resources: set):
        super().__init__(f'Не хватает ресурсов {need_resources}')

class ExtraResourcesException(Exception):

    def __init__(self, extra_resources: set):
        super().__init__(f'Пришли лишние ресурсы {extra_resources}')
