from django.contrib import admin
from django.urls import path

admin.autodiscover()

import shows.views

urlpatterns = [
    # Examples:
    # url(r'^$', 'shows.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    path('admin/', admin.site.urls),
    path('home/', shows.views.home),
    path('/', shows.views.home),
]
