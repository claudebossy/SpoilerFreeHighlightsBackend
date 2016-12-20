from django.conf.urls import *  # NOQA
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = [
    url(r'^api/', include('apps.api.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

# This is only needed when using runserver.
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
