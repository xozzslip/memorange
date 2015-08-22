from django import template

register = template.Library()

@register.filter
def section(value, length):
	return value[0:length]