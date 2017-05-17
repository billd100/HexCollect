from django.contrib import admin
from django.forms import Textarea

from Blog.models import BlogPost

# form
from django import forms
from django.forms import ModelForm, Textarea

class BlogPostForm(forms.ModelForm):
	class Meta:
		model = BlogPost
		fields = (
			'title',
			'author',
			'content',
		)

		widgets = {
			'content': forms.Textarea({'cols': 100, 'rows': 150}),
		}

class BlogAdmin(admin.ModelAdmin):
	exclude = ('slug'),
	form = BlogPostForm

admin.site.register(BlogPost, BlogAdmin)
