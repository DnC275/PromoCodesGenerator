from django.conf import settings
from django.core.management.base import BaseCommand

from ._utils import generate_code, read_data, get_codes_file_path, write_data


class Command(BaseCommand):
    help = 'Generates promo codes for group'

    def add_arguments(self, parser):
        parser.add_argument('group', type=str, help='Group name')
        parser.add_argument('amount', type=int, help='Promo codes amount')
        parser.add_argument('-f', '--file', type=str, default=settings.CODES_FILE_DEFAULT_NAME,
                            help='Name of the file for storing promo codes')

    def handle(self, *args, **kwargs):
        group = kwargs['group']
        amount = kwargs['amount']
        file_name = kwargs['file']

        path = get_codes_file_path(file_name)
        codes_data = read_data(path)

        for i in range(amount):
            self._set_promocode(codes_data, group)

        write_data(codes_data, path=path)

    def _set_promocode(self, codes_data, group):
        code = generate_code()
        if code in codes_data:
            self._set_promocode(codes_data, group)
            return

        codes_data[code] = group

