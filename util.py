from argparse import ArgumentParser

class ParserExit(RuntimeError):
    """INTERNAL API"""

    def __init__(self, status=0, message=None):
        self.status = status
        self.message = message

class ArgParser(ArgumentParser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _print_message(self, message, file=None):
        # do nothing
        pass

    def exit(self, status=0, message=None):
        raise ParserExit(status=status, message=message)

    def parse_args(self, args=None, namespace=None):
        return super().parse_args(args=args, namespace=namespace)

base_parser = ArgParser(add_help=False)

base_parser.add_argument('-f', action='store_const', const=True, default=False)
base_parser.add_argument('-h', action='store_true', default=False)

def gen_parser():
    return ArgParser(add_help=False, parents=[base_parser])