from django import template, views

register = template.Library()

@register.filter(name='addcss')
def addcss(field, css):
	return field.as_widget(attrs={"class":css})
	

from django import template
from django.core.urlresolvers import resolve

@register.filter(name='activelink', is_safe=True)
def activelink(request, url):
	if url in resolve(request.get_full_path()).namespaces:
			return "active"
	return ''