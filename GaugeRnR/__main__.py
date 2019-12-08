from .application import Application


def main(argv=None):
    app = Application(argv)
    app.check()
