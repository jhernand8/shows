from django.core.management.base import BaseCommand, CommandError
from django.core.serializers.json import DjangoJSONEncoder
import urllib2
import json
from shows.models import Episode
from shows.models import Show
from sets import Set
from datetime import date
from datetime import timedelta
from bs4 import BeautifulSoup


# Cron job that fetches episodes from wikipedia.
class Command(BaseCommand):
  def handle(self, *args, **options):
    shows = Show.objects.all();
    for show in shows:
      # handle current show
      url = show.wiki_url
      self.update_episodes_for_show(url, show.show_name)
    self.update_episodes_for_show("http://en.wikipedia.org/wiki/NCIS_%28season_12%29", "ncis");
    print "\n\n\n agents of shield:\n\n\n";
    self.update_episodes_for_show("http://en.wikipedia.org/wiki/Agents_of_S.H.I.E.L.D._%28season_2%29", "shield")
    
  def update_episodes_for_show(self, url, showname):
    response = urllib2.urlopen(url)
    data = response.read()
    html = BeautifulSoup(data)
    episodeTable = html.find("span", id="Episodes").parent.find_next_sibling("table");
    dateSpans = episodeTable.find_all("span", attrs={"class": "published"})
    for ds in dateSpans:
      title = ds.parent.parent.find_previous_sibling("td", attrs={"class": "summary"}).contents[0]
      title = str(title)
      ep = Episode(show_name=showname, episode_name = title, episode_date = ds.string)
      ep.save()
