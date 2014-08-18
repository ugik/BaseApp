from django.conf.urls import patterns, include, url
#from django.contrib import admin

#admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'Auth.views.index'),

# user auth & registration
	url(r'^login/$', 'Auth.views.login'),
	url(r'^auth/$', 'Auth.views.auth_view'),
	url(r'^logout/$', 'Auth.views.logout'),
	url(r'^loggedin/$', 'Auth.views.loggedin'),
	url(r'^verified/$', 'Auth.views.verified'),
	url(r'^invalid/$', 'Auth.views.invalid_login'),
	url(r'^profile/$', 'Auth.views.user_profile'),
	url(r'^register/$', 'Auth.views.register_user'),
	url(r'^register_success/$', 'Auth.views.register_success'),
    url(r'^register/(?P<user_id>.*)/$', 'Auth.views.verify_user'),
)

