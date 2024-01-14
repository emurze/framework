from server.app_fixture import app_fixture
from server.container import ServerContainer


def run() -> None:
    server = ServerContainer(app_factory=lambda: app_fixture)
    server.setup()
    server.run()
