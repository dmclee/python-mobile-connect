from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from mc_test import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ctm_ws.views.home', name='home'),
    # url(r'^ctm_ws/', include('ctm_ws.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^$', views.Index.as_view(), name="mc_test_index"),
    url(r'^get_profile$', views.GetProfilePage.as_view(), name="mc_test_getprofile"),
    url(r'^send_request$', views.send_request, name="mc_send_request")
)
