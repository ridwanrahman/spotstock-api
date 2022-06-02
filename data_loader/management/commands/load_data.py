import os
from pathlib import Path
from data_loader.wrappers.Wrapper import Wrapper
from django.core.management.base import BaseCommand, CommandError

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
FILE_PATH = Path.joinpath(BASE_DIR, 'resource')
FILE_LIST = os.listdir(FILE_PATH)

class Command(BaseCommand):
    help = f'Reads the name of data file and loads up the class responsible for the file then validates ' \
           f'and stores them'
    wrapper = Wrapper()
    wrapper_subclasses = wrapper.subclasses.keys()

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('******** STARTING FILE LOAD *******'))

        if len(FILE_LIST) == 0:
            raise FileNotFoundError("Folder is empty")

        for file in FILE_LIST:
            name_of_file = file.split('.')
            file_name = name_of_file[0]
            self.load_file(file_name)


    def load_file(self, file_name):
        if file_name not in self.wrapper_subclasses:
            raise FileNotFoundError("Only files with name people and company is supported")
        file_wrapper = self.wrapper.create(file_name)
        file_wrapper.handle_file_upload(file_name)


if __name__ == '__main__':
    a = Command()
    a.handle()
