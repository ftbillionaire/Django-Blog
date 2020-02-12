from django import forms
from .models import Tag, Post, Comment
from django.core.exceptions import ValidationError

# ModelForm provides its unique 'save', so there's no point for writing our own

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['author', 'text']

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['title', 'slug', 'body', 'image', 'tags']

		widgets = {
			'title':forms.TextInput(attrs={'class':'form-control'}),
			'slug':forms.TextInput(attrs={'class':'form-control'}),
			'body':forms.Textarea(attrs={'class':'form-control'}),
			'tags':forms.SelectMultiple(attrs={'class':'form-control'})
		}

	def clean_slug(self):
		new_slug = self.cleaned_data['slug'].lower()

		if new_slug == 'create':
			raise ValidationError("Slug can not be 'create'")
		if Post.objects.filter(slug__iexact=new_slug).count():
			raise ValidationError("Slug must be unique! We have the '{}' slug already".format(new_slug))

		return new_slug



class TagForm(forms.ModelForm):
	class Meta:
		model = Tag
		fields = ['title', 'slug']

		widgets = {
			'title':forms.TextInput(attrs={'class':'form-control'}),
			'slug':forms.TextInput(attrs={'class':'form-control'})
		}

	def clean_slug(self):
		new_slug = self.cleaned_data['slug'].lower()

		if new_slug == 'create':
			raise ValidationError("Slug can not be 'create'")

		if Tag.objects.filter(slug__iexact=new_slug).count():
			raise ValidationError("Slug must be unique! We have the '{}' slug already".format(new_slug))

		return new_slug  