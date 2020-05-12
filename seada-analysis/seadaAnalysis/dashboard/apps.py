from django.apps import AppConfig
import sys
import os


class DashboardConfig(AppConfig):
    name = 'dashboard'

    def ready(self):
        start_path = os.getcwd()
        os.chdir('../../seada-ingest')
        sys.path.append(os.path.join(os.getcwd()))
        os.chdir(start_path)

