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
	url(r'^invalid/$', 'Auth.views.invalid_login'),
	url(r'^profile/$', 'Auth.views.user_profile'),
	url(r'^register/$', 'Auth.views.register_user'),
	url(r'^register_success/$', 'Auth.views.register_success'),
    url(r'^register/(?P<user_id>.*)/$', 'Auth.views.verify_user'),

    url(r'^password/$','django.contrib.auth.views.password_change',name='password_change'),
    url(r'^password/done/$','django.contrib.auth.views.password_change_done',name='password_change_done'),
    url(r'^password/reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    url(r'^password/password/reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^password/reset/complete/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),

)
#urlpatterns += patterns('django.contrib.auth.views',)

