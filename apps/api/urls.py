from django.conf.urls import url

from apps.api import views

urlpatterns = [
    url(r'^nba/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})$',
        views.nba_results, name='nba_results'),
]