from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'^$', views.deck_choice, name='deck_choice'),
	url(r'^(?P<deck_slug>[\w-]+)/$', views.deck_details, name='deck_details'),	
	url(r'^(?P<deck_slug>[\w-]+)/add_question/$', views.add_question, name='add_question'),	
	url(r'^(?P<deck_slug>[\w-]+)/study/$', views.question_in_deck, name='question_in_deck'),
	url(r'^(?P<deck_slug>[\w-]+)/question/remember$', views.remember, name='remember'),
	url(r'^create-deck$', views.create_deck, name='create_deck'),
	url(r'^deck/question/edit$', views.edit_question, name="edit_question"),


]