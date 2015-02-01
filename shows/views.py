from django import http
from django.template import RequestContext, loader
import urllib2
import json
import sys
from bs4 import BeautifulSoup
from datetime import date
import json
from json import JSONEncoder
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe
from sets import Set
from shows.models import Episode
def home(request):
  episodes = Episode.objects.all()
  episodes = sorted(episodes, key=lambda sn: sn.date)
  outStr = "Shows home page<br/>\n";
  for episode in episodes:
    outStr += episode.show_name + ": " + str(episode.date) + "  " + episode.episode_name;
    outStr += "<br/>\n";
  return http.HttpResponse(outStr);



