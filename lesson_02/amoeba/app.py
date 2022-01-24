"""точка входа пользовательского приложения."""

from amoeba.main import Amoeba
from amoeba.fronts import front_controllers
from urls import urlpatterns
from settings import settings

app = Amoeba(
    urls=urlpatterns,
    settings=settings,
    fronts=front_controllers
)
