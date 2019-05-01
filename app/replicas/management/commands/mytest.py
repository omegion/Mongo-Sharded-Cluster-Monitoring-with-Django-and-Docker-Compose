from django.core.management.base import BaseCommand
from django.conf import settings
import json

from replicas.tasks import  start_benchmark

class Command(BaseCommand):
    help = 'Deploy a MTA with NEO tool'

    def handle(self, *args, **options):
        print('Starting Import University...')
        
        start_benchmark('shard01a')
        # check_status('shard01a')
        # create_data()
        # mycol = mydb["customers"]
        
        # dblist = client.list_database_names()
        # print(dblist)
        
        pass