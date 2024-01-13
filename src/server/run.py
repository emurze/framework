from server.container import ServerContainer


def run() -> None:
    server = ServerContainer()
    server.run()
