"""Модуль запросов."""


class Request:
    """Класс запросов."""

    def __init__(self, environ: dict, settings: dict):
        self.form_get_params_dict(environ['QUERY_STRING'])
        self.environ = environ
        self.settings = settings
        self.extras = {}

    def __getattr__(self, item):
        """Позволяет возвращать вызываемы параметры."""
        return self.extras.get(item)

    def parse_input_data(self, data: str) -> dict:
        """Возвращает словарь параметров запроса."""
        result = {}
        if data:
            params = data.split('&')
            for item in params:
                param, value = item.split('=')
                result[param] = value
        return result

    def form_get_params_dict(self, raw_params: str):
        """Формирует словарь списков get-параметров."""
        return self.parse_input_data(raw_params)
