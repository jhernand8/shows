from django.core.management.base import BaseCommand, CommandError
from django.core.serializers.json import DjangoJSONEncoder
import urllib2
import json
from shows.models import Episode
from shows.models import Show
from sets import Set
from datetime import date
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup


# Cron job that fetches episodes from wikipedia.
class Command(BaseCommand):
  def handle(self, *args, **options):
    # first remove all episodes
    allEps = Episode.objects.all()
    for ep in allEps:
      ep.delete()

    # now add episodes
    shows = Show.objects.all();
    for show in shows:
      # handle current show
      url = show.wiki_url
      self.update_episodes_for_show(url, show.show_name)
 
    # check for new seasons
    self.check_new_seasons();
      
  # Checks for any new seasons of the show and if so adds them to the databae  
  def check_new_seasons(self):
    shows = Show.objects.all()
    for show in shows:
      resp = urllib2.urlopen(show.wiki_url)
      html = BeautifulSoup(resp.read())
      try:
        nextSeason = html.findAll(text="Next").[0].parent.find_next_sibling("a").get('href');
        nsurl = 'http://en.wikipedia.org/' + nextSeason;
        name = html.findAll(text="Next").[0].parent.find_next_sibling("a").contents[0];
        season_exists = False
        for s in shows:
          if s.wiki_url == nsurl:
            season_exists = True
        if season_exists:
          continue
        newSeason = Show(show_name = (show.show_name + name), wiki_url = nsurl);
        newSeason.save()
      except:
        continue;
 
  def update_episodes_for_show(self, url, showname):
    response = urllib2.urlopen(url)
    data = response.read()
    html = BeautifulSoup(data)
    episodeTable = html.find("span", id="Episodes").parent.find_next_sibling("table");
    dateSpans = episodeTable.find_all("span", attrs={"class": "published"})
    min_date = date.today() - timedelta(days = 30)
    count = 0;
    for ds in dateSpans:
      count = count + 1
      #title = ds.parent.parent.find_previous_sibling("td", attrs={"class": "summary"}).contents[0]
      title = "Episode " + str(count)
      datestr = ds.string
      epdate = datetime.strptime(datestr, '%Y-%m-%d').date()
      if (epdate < min_date) :
        continue
      ep = Episode(show_name=showname, episode_name = title, date = epdate)
      ep.save()
