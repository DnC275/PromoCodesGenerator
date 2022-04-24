import os
import json

from datetime import datetime
from io import StringIO
from unittest import TestCase
from django.core.management import call_command
from core.management.commands._utils import get_codes_file_path, write_data


class CheckPromocodeTestCase(TestCase):
    def setUp(self):
        self.existing_code = '11111111'
        self.not_existing_code = '11111112'
        self.group = 'group1'

        self.file_name = 'test_codes_' + str(datetime.now()).replace(' ', '_')
        self.file_path = get_codes_file_path(self.file_name)
        while os.path.isfile(self.file_path):
            self.file_name = '_'.join(['test', self.file_name])
        write_data({
            self.existing_code: self.group
        }, path=self.file_path)

    def tearDown(self):
        os.remove(self.file_path)

    def call_command(self, *args, **kwargs):
        out = StringIO()
        call_command(
            'check_promocode',
            *args,
            stdout=out,
            stderr=StringIO(),
            **kwargs
        )
        return out.getvalue().strip()

    def test_code_exists(self):
        out = self.call_command(self.existing_code, file=self.file_name)
        self.assertEqual(out, f'код существует группа = {self.group}')

    def test_code_not_exists(self):
        out = self.call_command(self.not_existing_code, file=self.file_name)
        self.assertEqual(out, 'код не существует')
