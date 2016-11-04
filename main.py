import importlib
from config import config
from plugins import Plugin
from logger import LoggerMixin


class Person(object):
    pass


class Trip(object):
    pass


class TicketMachine(LoggerMixin):

    def import_plugins(self):
        import machines

        # pylint: disable=broad-except
        for module in machines.__all__:
            try:
                module_id = "{0}.{1}".format('machines', module)
                importlib.import_module(module_id)
                self.debug(module_id + " loaded successfully.")
            except Exception as exc:
                self.warning(
                    "The {0} {1} module could not be loaded: {2} "
                    .format(module, category.__name__[:-1], str(exc)))
                self.log_exception()

    def main(self):
        self.setup_logging()
        self.import_plugins()


if __name__ == '__main__':
    machine = TicketMachine()
    machine.main()
