from django.core.management.base import BaseCommand, CommandError
from example.polls.models import Poll
import requests

class Command(BaseCommand):
    args = 'None'
    help = 'Updates list of avaiable servers'

    def handle(self, *args, **options):
	print "test"
