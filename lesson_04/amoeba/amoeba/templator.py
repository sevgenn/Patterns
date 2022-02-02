"""Модуль, отвечающий за отрисовку страниц средствами jinja2."""

from jinja2 import Template, FileSystemLoader
from jinja2.environment import Environment
from amoeba.request import Request


def render(request: Request, template_name: str, folder='templates', **kwargs) -> str:
    """Возвращает шаблон в формате строки."""

    env = Environment()
    env.loader = FileSystemLoader(folder)
    template = env.get_template(template_name)
    return template.render(**kwargs)
