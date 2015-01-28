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

def home(request):
  return http.HttpResponse("Shows home page")



