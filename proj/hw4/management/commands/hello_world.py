from django.core.management.base import BaseCommand
 
class Command(BaseCommand):
  args = 'Arguments is not needed'
  help = 'Django admin custom command poc.'
 
  def handle(self, *args, **options):
    self.stdout.write("Hello World")
