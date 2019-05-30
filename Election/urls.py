from django.conf.urls import  include,url
from django.contrib import admin
from . import views

urlpatterns = [
    # Examples:
    url(r'^login$', views.render_page, name='log_in-form'),
    url(r'^logout$', views.logout, name='log_out-form'),
    # url(r'^accounts/login/', views.render_page),
    url(r'^portal$', views.portal_render, name='portal-form'),
    url(r'^profiles$', views.profile_render, name='profile-form'),
    url(r'^castvote$', views.cast_vote_render, name='vote-casting-form'),
    url(r'^confirmation$', views.confirm_vote, name='vote-confirmation_form'),
    url(r'^results$', views.result_render, name='vote-casting-form'),
    url(r'^delete$', views.delete_render, name='vote-casting-form'),
    url(r'^discard$', views.confirm_discard, name='discard-form'),
    url(r'^enroll$', views.enroll_candidate, name='enroll-form'),
    url(r'', views.render_page, name='home'),

    # url(r'^$', 'Election_portal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


]
