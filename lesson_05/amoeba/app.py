"""точка входа пользовательского приложения."""

from amoeba.main import Amoeba, FakeApplication, LogApplication
from amoeba.fronts import front_controllers
from view import routes
from settings import settings


app = Amoeba(
    routes=routes,
    settings=settings,
    fronts=front_controllers
)

app_fake = FakeApplication(
    routes=routes,
    settings=settings,
    fronts=front_controllers
)

app_log = LogApplication(
    routes=routes,
    settings=settings,
    fronts=front_controllers
)
