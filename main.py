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
    """
    An object that encapsulates all the information about the person
    taking the trip.
    """

    def __init__(self, data):
        self._data = data

    def __getattr__(self, name):
        return self._data[name]

    @classmethod
    def from_config(cls):
        data = {
            'first_name': config.first_name,
            'last_name': config.last_name,
            'street': config.street,
            'city': config.city,
            'psc': config.psc,
            'email': config.email,
            'zssk_card_id': config.zssk_card_id,
            'zssk_card_reg': config.zssk_card_reg,
        }
        return cls(data)


class Trip(object):
    """
    An object that encapsulates all the information about the planned
    trip.
    """

    def __init__(self, start, end, time, date=None, via=None):
        self.start = start
        self.end = end
        self.time = time
        self.date = date or datetime.date.today().strftime('%Y.%M.%D')
        self.via = via


class TicketMachine(LoggerMixin):

    @property
    def plugins(self):
        """
        Returns a dictionary of plugins available.
        """

        return {
            plugin_class.identifier: plugin_class
            for plugin_class in Plugin.plugins
        }

    def get_plugin(self, identifier):
        """
        Returns a plugin class corresponding to the given identifier.
        """

        try:
            return self.plugins[identifier]
        except KeyError:
            self.error('Machine "{0}" is not available'.format(identifier))

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

        machine = self.get_plugin(arguments['<machine>'])


if __name__ == '__main__':
    machine = TicketMachine()
    machine.main()
