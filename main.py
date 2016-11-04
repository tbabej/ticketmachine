"""
Usage: ticketmachine <machine> --from=<city> --to=<city> --time=<value> [--date=<today>] [--via=<city>]

Options:
  --date=DATE    Date to search for [default: today]
"""

import importlib
from docopt import docopt

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
                    "The {0} module could not be loaded: {1} "
                    .format(module, str(exc)))
                self.log_exception()

    def main(self):
        arguments = docopt(__doc__, version='ticketmachine')
        self.setup_logging(level='debug')
        self.import_plugins()


if __name__ == '__main__':
    machine = TicketMachine()
    machine.main()
