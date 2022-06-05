import os
from pathlib import Path

# included to be able to debug this individual file without running the server
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stockspot.settings")
# django.setup()

from django.core.management.base import BaseCommand, CommandError
from data_loader.wrappers.Wrapper import Wrapper

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
FILE_PATH = Path.joinpath(BASE_DIR, 'resource')
FILE_LIST = os.listdir(FILE_PATH)
FILES_SORTED_BY_SIZE = sorted(FILE_LIST,
                              key=lambda x: os.stat(os.path.join(FILE_PATH, x)).st_size)


class Command(BaseCommand):
    """
    Class to handle arguments from the terminal.

    Will only handle `load_data` argument.
    `python manage.py load_data`
    """
    help = f'Reads the name of data file and loads up the class responsible for the file then validates ' \
           f'and stores them'
    wrapper = Wrapper()
    wrapper_subclasses = wrapper.subclasses.keys()

    def handle(self, *args, **options):
        """
        This function will run when `python manage.py load_data is run`.

        It will load the files in resource folder according to their sizes, separate the names of the files
        from the format and send each to load_data function.
        """
        self.stdout.write(self.style.SUCCESS('******** STARTING FILE LOAD *******'))

        if len(FILE_LIST) == 0:
            raise FileNotFoundError("Folder is empty")

        for file in FILES_SORTED_BY_SIZE:
            try:
                name_of_file = file.split('.')

                if not name_of_file[1] == 'json':
                    self.stdout.write(self.style.ERROR(f'Only .json files accepted'))
                    continue

                file_name = name_of_file[0]
                loaded = self.load_file(file_name)
                if loaded:
                    self.stdout.write(self.style.SUCCESS(f'******** SUCCESSFULLY LOADED {file_name} *******'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Only .json files accepted'))

    def load_file(self, file_name) -> bool:
        """
        This function receives the file_name. It loads the different Wrapper classes and matches with the name of the
        file then uses the wrapper class to validate and save the record. Does not allow duplicates.

        To add more wrapper classes, please add a new class and add the file name in the decorator.

        Skips the file and return None if wrapper class is not implemented.
        Returns True if finished validating and saving.

        :param file_name: string
        :return: bool
        """
        if file_name not in self.wrapper_subclasses:
            self.stdout.write(self.style.ERROR(
                f'******* {file_name} has not been implemented in  wrappers class. *******'
            ))
            return None
        file_wrapper = self.wrapper.create(file_name)
        json_file_path = FILE_PATH.joinpath(FILE_PATH, f'{file_name}.json')
        file_wrapper.handle_file_upload(json_file_path)
        return True
