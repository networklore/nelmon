"""nelmon.args.notifier."""

from nelmon.args.base import NelmonArguments


class NotifierArguments(NelmonArguments):
    """Base class for Notifiers."""

    def __init__(self, description, epilog=''):

        super(NotifierArguments, self).__init__(description, epilog)

        self.parser.add_argument('-H', help='Host', required=False)
        self.parser.add_argument('-n', help='Notification Type', required=False)
        self.parser.add_argument('-d', help='Service Description', required=False)
        self.parser.add_argument('-s', help='Host State', required=False)
        self.parser.add_argument('-S', help='Service State', required=False)
        self.parser.add_argument('-a', help='Host Address', required=False)
        self.parser.add_argument('-o', help='Host Output', required=False)
        self.parser.add_argument('-l', help='Long date time', required=False)
        self.parser.add_argument('-e', help='Service Output', required=False)
