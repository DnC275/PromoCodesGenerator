import os
import json

from datetime import datetime
from io import StringIO
from unittest import TestCase
from django.core.management import call_command
from core.management.commands._utils import get_codes_file_path


class GenerateCodesTestCase(TestCase):
    def setUp(self):
        self.file_name = 'test_codes_' + str(datetime.now()).replace(' ', '_')
        self.file_path = get_codes_file_path(self.file_name)
        while os.path.isfile(self.file_path):
            self.file_name = '_'.join(['test', self.file_name])

    def tearDown(self):
        os.remove(self.file_path)

    def call_command(self, *args, **kwargs):
        out = StringIO()
        call_command(
            'generate_codes',
            *args,
            stdout=out,
            stderr=StringIO(),
            **kwargs
        )
        return out.getvalue().strip()

    def test_generation(self):
        self.call_command('group1', 5, file=self.file_name)
        self.call_command('group2', 3, file=self.file_name)
        self.call_command('group1', 2, file=self.file_name)
        self.call_command('group3', 7, file=self.file_name)

        with open(self.file_path, 'r') as codes_file:
            data = json.load(codes_file)
            self.assertEqual(len(data), 17)

            codes_1 = self._get_codes_by_group(data, 'group1')
            self.assertEqual(len(codes_1), 7)

            codes_2 = self._get_codes_by_group(data, 'group2')
            self.assertEqual(len(codes_2), 3)

            codes_3 = self._get_codes_by_group(data, 'group3')
            self.assertEqual(len(codes_3), 7)

    def _get_codes_by_group(self, data, group):
        codes = []
        for code in data:
            if data[code] == group:
                codes.append(code)
        return codes
