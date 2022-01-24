"""Модуль запросов."""


class Request:
    """Класс запросов."""

    def __init__(self, environ: dict, settings: dict):
        self.form_get_params_dict(environ['QUERY_STRING'])
        content_length = self.get_wsgi_data_length(environ)
        self.form_post_params_dict(environ['wsgi.input'].read(content_length))
        self.environ = environ
        self.settings = settings
        self.extras = {}

    def __getattr__(self, item):
        """Позволяет возвращать вызываемые параметры."""
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
        self.GET = self.parse_input_data(raw_params)

    def get_wsgi_data_length(self, environ) -> int:
        """Возвращает данные POST запроса."""
        content_length_data = environ.get('CONTENT_LENGTH')
        return int(content_length_data) if content_length_data else 0

    def form_post_params_dict(self, raw_params: bytes):
        """Формирует словарь списков post-параметров."""
        params = raw_params.decode('utf-8')
        print(params)
        self.POST = self.parse_input_data(params)
