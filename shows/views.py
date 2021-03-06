from django import http
from django.template import RequestContext, loader
import json
import sys
from bs4 import BeautifulSoup
from datetime import date
from datetime import timedelta
import json
from json import JSONEncoder
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe
from shows.models import Episode
from shows.models import Show

def home(request):
  episodes = Episode.objects.all()
  episodes = sorted(episodes, key=lambda sn: sn.date)
  outStr = "<b>Shows home page</b><br/>\n";
  outStr += "<style> span.show { display: inline-block; width: 210px; } </style> ";
  nameSpan = "<span class='show'>";
  for episode in episodes:
    if (episode.date >= (date.today() + timedelta(days = -7))):
      break;
    outStr += nameSpan + episode.show_name + "</span> " + str(episode.date) + "  " + episode.episode_name;
    outStr += "<br/>\n";

  outStr += "<br/><br/><br/>Past and Upcoming Week<br/><br/>";
  for episode in episodes:
    if (episode.date > (date.today() + timedelta(days = 7))):
      break;
    if (episode.date < (date.today() + timedelta(days = -7))):
      continue;
    outStr += nameSpan + episode.show_name + "</span> <b>" + str(episode.date) + "(" + form_weekday_str(episode.date.weekday()) + ")</b>  " + episode.episode_name;
    outStr += "<br/>\n";
  
  outStr += "<br/><br/>Upcoming<br/><br/>";
  for episode in episodes:
    if (episode.date < (date.today() + timedelta(days = 7))):
      continue;
    outStr += nameSpan + episode.show_name + "</span> <b>" + str(episode.date) + "</b>  " + episode.episode_name;
    outStr += "<br/>\n";
  outStr += "<br/><br/><br/> data from wikipedia:";

  links = [];
  for show in Show.objects.all():
    links.append(show.wiki_url);
  links.sort();
  for link in links:
    outStr += "<a href=\"" + link + "\">" + link + "</a><br/>";
  return http.HttpResponse(outStr);

# Returns day string for day of week.
def form_weekday_str(weekday):
  if weekday == 6:
    return "Sunday"
  if weekday == 0:
    return "Monday"
  if weekday == 1:
    return "Tuesday"
  if weekday == 2:
    return "Wednesday"
  if weekday == 3:
    return "Thursday"
  if weekday == 4:
    return "Friday"
  if weekday == 5:
    return "Saturday"
  return ""


