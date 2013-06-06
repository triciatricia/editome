from django.conf.urls import patterns, include, url
from django.conf import settings
from editdatabase.views import about, search, download, literature, contact, additionalinfo, tutorial

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	('^$',about),
	('^search/$', search),
	('^about/$', about),
	('^download/$', download),
	('^literature/$', literature),
	('^contact/$', contact),
	('^additionalinfo/$', additionalinfo),
	('^tutorial/$', tutorial),
    # Examples:
    # url(r'^$', 'editdatabase.views.home', name='home'),
    # url(r'^editdatabase/', include('editdatabase.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
	('^' + settings.STATIC_DIR + '/(?P<path>.*)$', 
		'django.views.static.serve', 
		{ 'document_root': settings.STATIC_ROOT, }
	),
)
