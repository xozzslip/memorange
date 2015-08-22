from django import template

register = template.Library()

@register.filter
def key_variable(value, key):
	return value[key]

@register.filter
def card_plural_rus(value):
	if value >= 5 and value <= 20:
		return ''
	else:
		sign = str(value)[-1]
		if sign == '0': return ''
		elif sign == '1': return 'у'
		elif sign == '2' or sign == '3' or sign == '4': return 'ы'
		else: return ''

@register.filter
def time_format(value):
	if value.days < 0 or value.seconds < 0 or value.microseconds < 0:
		return 0
	elif value.days >= 365:
		return "%s years" % (value.days//365)
	elif value.days >= 30: 
		return "%s months" % (value.days//30)
	elif value.days >= 3:
		return "%s days" % (value.days)
	elif value.days > 0:
		return "%s days, %s hours" % (value.days, value.seconds%(3600 * 24)//3600)
	elif value.seconds//3600 > 5:
		return "%s hours" % (value.seconds//3600)
	elif value.seconds//3600 > 0:
		return "%s hours, %s minutes" % (value.seconds//3600, value.seconds%3600//60)
	elif value.seconds//60 > 0:
		return "%s minutes" % (value.seconds//60)
	elif value.seconds > 1:
		return "%s seconds" % (value.seconds)
	else: 
		return 0

@register.filter
def even_odd_partition(value, even_or_odd):
	odd_partition = []
	even_partition = []
	for i in range(len(value)):
		if i % 2 == 0:
			even_partition.append(value[i])
		else:
			odd_partition.append(value[i])
	if even_or_odd == 'even':
		return even_partition
	elif even_or_odd == 'odd':
		return odd_partition

@register.filter
def is_last_word_too_long(value):
	THE_LONGEST_WORD = 40 #count of symbols
	words = value.split(' ')
	if len(words[-1]) > THE_LONGEST_WORD:
		dif = len(words[-1]) - THE_LONGEST_WORD
		return value[:len(value) - dif] + '...'
	return value