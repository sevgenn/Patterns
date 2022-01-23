"""Модуль, отвечающий за отрисовку страниц средствами jinja2."""

import os
from jinja2 import Template
from amoeba.request import Request


def create_template_dir(request: Request) -> str:
    """Возвращает путь до папки шаблонов."""
    return os.path.join(request.settings.get('BASE_DIR'), request.settings.get('TEMPLATE_DIR'))


def render(request: Request, template_name: str, **kwargs) -> str:
    """Возвращает шаблон в формате строки."""
    template_dir = create_template_dir(request)
    template_path = os.path.join(template_dir, template_name)
    # Если шаблона не существует, меняем путь:
    if not os.path.isfile(template_path):
        template_path = 'amoeba/templates/not_found.html'
    with open(template_path, encoding='utf-8') as f:
        template = Template(f.read())
    return template.render(**kwargs)
