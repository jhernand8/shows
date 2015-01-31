from django.core.management.base import BaseCommand, CommandError
from django.core.serializers.json import DjangoJSONEncoder
import urllib2
import json
from shows.models import Episode
from shows.models import Show
from sets import Set
from datetime import date
from datetime import timedelta


# Cron job that fetches episodes from wikipedia.
class Command(BaseCommand):
  def handle(self, *args, **options):
    shows = Show.objects.all();
    for show in shows:
      # handle current show
