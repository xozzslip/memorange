from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
import json
from datetime import timedelta, datetime
from .models import Question, Deck, RepeatTime
from django.core.urlresolvers import reverse
from django.utils.datastructures import MultiValueDictKeyError

import random

@login_required
def deck_choice(request):
	deck_list = Deck.objects.all()
	deck_list = deck_list.filter(owner=request.user)
	question_list = []
	repeat_time_question = {}
	for deck in deck_list:
		view_q = []
		question_list = list(deck.question_set.all())
		for question in question_list:
			if question.next_repeat <= timezone.now():
				view_q.append(question)
		repeat_time_question[deck.id] = len(view_q)
	context = {'deck_list':deck_list, 'repeat_time_question':repeat_time_question}
	return render(request, 'flashcards/deck_choice.html', context)

@login_required	
def deck_details(request, deck_slug):
	if request.user.is_authenticated():		
		deck = get_object_or_404(Deck, slug=deck_slug, owner=request.user)
		question_list = deck.question_set.all().order_by('-pub_date')
		next_repeat_time = {}
		for question in question_list:
			time_left = question.next_repeat - timezone.now()
			next_repeat_time[question.id] = time_left
		context = {'question_list': question_list, 'deck_slug': deck_slug, 'deck':deck, 'next_repeat_time':next_repeat_time}
		return render(request, 'flashcards/deck_details.html', context)
	else:
		return HttpResponse('Войдите в свой профиль')

@login_required
def add_question(request, deck_slug):
	if request.user.is_authenticated():
		question_value = request.POST.get('question')
		answer_value = request.POST.get('answer')
		deck_value = get_object_or_404(Deck, slug=deck_slug, owner=request.user)
		if question_value:
			q = Question(question_text=question_value, answer_text=answer_value, deck=deck_value)
			q.save()
			return HttpResponseRedirect(reverse('deck_details', args=(deck_value.slug,)))
		else:
			return HttpResponse('Че?')
	else:
		return HttpResponse('Войдите в свой профиль')

@login_required
def question_in_deck(request, deck_slug):
	if request.user.is_authenticated():
		deck = get_object_or_404(Deck, slug=deck_slug, owner=request.user)
		question_list = deck.question_set.all()
		view_q = []
		for question in question_list:
			MAXYEAR = 9999
			if question.next_repeat.year != MAXYEAR:
				if question.next_repeat <= timezone.now():
					view_q.append(question)
		random.shuffle(view_q)
		view_q = sorted(view_q, key=lambda x: x.repition_number)

		NUMBERS_FOR_CHOICE = 3

		if len(view_q) >= NUMBERS_FOR_CHOICE:
			question = view_q[random.randint(0, NUMBERS_FOR_CHOICE - 1)]
		elif view_q:
			question=view_q[random.randint(0, len(view_q) - 1)]
		else:
			question = False
		
		if request.is_ajax():
			deck_is_empty = "false"
			if len(view_q) == 0:
				deck_is_empty = "true"
				context = {'question_text':"", 'answer_text':"", "question_id":"", "deck_is_empty": deck_is_empty}
			else:
				context = {'question_text': question.question_text, 'answer_text': question.answer_text, "question_id": question.id, "deck_is_empty": deck_is_empty}
			return JsonResponse(context)
		else:
			context = {'question':question, 'q_list':view_q}
			return render(request, 'flashcards/question_in_deck.html', context)
	else: 
		return HttpResponse('Войдите в свой профиль')


@login_required
def remember(request, deck_slug):
	if request.user.is_authenticated():
		question_id = request.POST["question_id"]
		question = get_object_or_404(Question, pk=question_id)
		remember = request.POST['remember']
		if remember == 'True':
			question.repition_number += 1
			question.last_repeat = timezone.now()	
			question.save()
		elif remember == 'False':
			question.repition_number = 0
			question.last_repeat = timezone.now()
			question.save() 
		elif remember == 'bad':
			if question.repition_number > 0:
				question.repition_number -= 1
				question.last_repeat = timezone.now()
				question.save()
			else:
				question.last_repeat = timezone.now()
				question.save()				
		return HttpResponseRedirect(reverse('question_in_deck', args=(deck_slug,)))
	else:
		return HttpResponse('Войдите в свой профиль')

@login_required
@csrf_protect
def create_deck(request):
	if request.is_ajax():
		if request.method == "POST":
			name = request.POST["name"]
			intervals = request.POST.getlist("times[]")

			formated_intervals = []
			if len(intervals) != 0:
				for i in range(len(intervals)):
					interval_splited = intervals[i].split(' ')
					if interval_splited[0] == 'сразу':
						time, created = RepeatTime.objects.get_or_create(time=timedelta(microseconds=0))
					elif interval_splited[1] == 'months':
						time, created = RepeatTime.objects.get_or_create(time=timedelta(days=30*float(interval_splited[0])))
					elif interval_splited[1] == 'days':
						time, created = RepeatTime.objects.get_or_create(time=timedelta(days=float(interval_splited[0])))
					elif interval_splited[1] == 'hours':
						time, created = RepeatTime.objects.get_or_create(time=timedelta(hours=float(interval_splited[0])))
					else:
						time, created = RepeatTime.objects.get_or_create(time=timedelta(seconds=60*float(interval_splited[0])))
					formated_intervals.append(time)
			else:
				time, created = RepeatTime.objects.get_or_create(time=timedelta(microseconds=0))
				formated_intervals.append(time)
				time, created = RepeatTime.objects.get_or_create(time=timedelta(seconds=60 * 20))
				formated_intervals.append(time)
				time, created = RepeatTime.objects.get_or_create(time=timedelta(hours=8))
				formated_intervals.append(time)
				time, created = RepeatTime.objects.get_or_create(time=timedelta(hours=24))
				formated_intervals.append(time)
				time, created = RepeatTime.objects.get_or_create(time=timedelta(days=3))
				formated_intervals.append(time)
				time, created = RepeatTime.objects.get_or_create(time=timedelta(days=7))
				formated_intervals.append(time)
				time, created = RepeatTime.objects.get_or_create(time=timedelta(days=30))
				formated_intervals.append(time)
				

			d = Deck(deck_name=name, owner=request.user)
			d.save()
			for i in range(len(formated_intervals)):
				d.repeat.add(formated_intervals[i])
			return HttpResponse("Ok")
	else:	
		return render(request, 'flashcards/create_deck.html')

def edit_question(request):
	if request.method == "POST":
		question_id = int(request.POST["question_id"])
		q = Question.objects.get(pk=question_id)
		q.question_text = request.POST["question_text"]
		q.answer_text = request.POST["answer_text"]
		q.save()
		return HttpResponse("Ok")
