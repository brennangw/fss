from django.core.management.base import BaseCommand, CommandError
from hw4.models import PythonServers
import requests

class Command(BaseCommand):
  args = 'Arguments is not needed'
  help = 'Good Luck!'
 
  def handle(self, *args, **options):
    for server in PythonServers.objects.all():
		r = requests.get(server.address)
		if (r.status_code == 200):
			server.status = 1
			print server.address
		else:
			server.status = 0
		server.save()