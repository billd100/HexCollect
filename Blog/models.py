from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
class BlogPost(models.Model):
	title = models.CharField(max_length=50)
	author = models.CharField(max_length=20)
	content = models.CharField(max_length=5000)

	pub_date = models.DateTimeField(
		auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	slug = models.SlugField(max_length=50, unique=True)
	
	def get_absolute_url(self):
		return reverse('blog:blog_post', args=[self.slug])

	def save(self, *args, **kwargs):
		# slugify if no slug or if title has changed
		if not self.slug or self.slug != slugify(self.title):
			self.slug = slugify(self.title)
		super(BlogPost, self).save(*args, **kwargs)
		
	def __str__(self):
		return self.title
