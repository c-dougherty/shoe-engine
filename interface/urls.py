from django.conf.urls import include, url
from rsc.views import home
#from django.views.generic import RedirectView
from django.conf import settings
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
     #url(r'^rsc/', include('rsc.urls', namespace="rsc")),
     url(r'^$', home, name='home'),
     url(r'^admin/', admin.site.urls),
     #url(r''
     ##url(r'^viewfigure/', 'rsc.views.viewfigure'),
     ##url(r'^download/(?P<loc>.+)/$', 'rsc.views.download'),
     #url(r'^download/(?P<loc>~[^0-9A-Za-z\\/]~)/$', 'rsc.views.download'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    ## url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
    ##        'document_root': settings.MEDIA_ROOT,
    ##    }),
    # Uncomment the next line to enable the admin:
]

   
