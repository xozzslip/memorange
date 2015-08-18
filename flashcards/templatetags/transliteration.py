from django import template

register = template.Library()
def upper(value):
	return str(value).upper()