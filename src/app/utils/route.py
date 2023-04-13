import os


def create_route_path(version, *args):
    return f'/{os.path.join("api", version, *args)}/'
