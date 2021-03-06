from django.core.management.base import BaseCommand, CommandError
from django.core.serializers.json import DjangoJSONEncoder
from urllib.request import urlopen
import json
from shows.models import Episode
from shows.models import Show
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
      try:
        self.update_episodes_for_show(url, show.show_name)
      except:
        continue;
    # check for new seasons
    self.check_new_seasons();
      
  # Checks for any new seasons of the show and if so adds them to the database
  # and removes much older seasons
  def check_new_seasons(self):
    shows = Show.objects.all()
    for show in shows:
      resp = urlopen(show.wiki_url)
      html = BeautifulSoup(resp.read())
      try:
        nextSeason = html.findAll(text="Next")[0].parent.find_next_sibling("a").get('href');
        nsurl = 'http://en.wikipedia.org'
        if nextSeason.find("/") == 0:
          nsurl = nsurl + nextSeason;
        else:
          nsurl = nsurl + '/' + nextSeason;
        name = html.findAll(text="Next")[0].parent.find_next_sibling("a").contents[0];
        season_exists = False
        for s in shows:
          if s.wiki_url == nsurl:
            season_exists = True
        if season_exists:
          # see if this season is old and can be removed
          episodeTable = html.find("span", id="Episodes").parent.find_next_sibling("table");
          dateSpans = episodeTable.find_all("span", attrs={"class": "published"})
          if dateSpans and len(dateSpans) > 0:
            episodeDate = datetime.strptime(dateSpans[0].string, '%Y-%m-%d').date()
            if episodeDate < (date.today() - timedelta(days = 700)):
              show.delete();
          continue
        seasonName = self.form_show_season_name(show.show_name, name);
        newSeason = Show(show_name = seasonName, wiki_url = nsurl);
        newSeason.save()
      except:
        continue;
 
  # Helper to form the new show + season name based on the current name and the 
  # name of the new season.
  def form_show_season_name(self, currName, seasonName):
    seasonIndex = currName.find("Season");
    rootName = currName;
    if seasonIndex > 0:
      rootName = currName[0:seasonIndex];
    else:
      if currName.rfind("S") > len(currName) - 4:
        rootName = currName[0:currName.rfind("S")]
    return rootName + " " + seasonName;

  def update_episodes_for_show(self, url, showname):
    print("updating episodes for: " + showname + " " + url + "\n")
    response = urlopen(url)
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
