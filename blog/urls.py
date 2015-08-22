from django.conf.urls import url
from . import views
urlpatterns = [
	# url(r'^$', views.deck_choice, name='deck_choice'),
	url(r'^$', views.all_posts, name='all_posts'),
	url(r'^post/(?P<post_slug>[\w-]+)/$', views.post, name='post'),	
	url(r'^create-post/$', views.create_post, name='create_post'),
	url(r'^edit/(?P<post_slug>[\w-]+)/', views.edit_post, name='edit_post'),
]
