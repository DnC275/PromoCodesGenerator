from django.conf import settings
from django.core.management.base import BaseCommand

from ._utils import get_codes_file_path, read_data


class Command(BaseCommand):
    help = 'Get group name by promo code'

    def add_arguments(self, parser):
        parser.add_argument('code', type=str, help='Promo code')
        parser.add_argument('-f', '--file', type=str, default=settings.CODES_FILE_DEFAULT_NAME,
                            help='Name of the file for storing promo codes')

    def handle(self, *args, **kwargs):
        code = kwargs['code']
        file_name = kwargs['file']

        path = get_codes_file_path(file_name)
        codes_data = read_data(path)

        group = codes_data.get(code, None)

        if group:
            return f'код существует группа = {group}'
        return 'код не существует'
