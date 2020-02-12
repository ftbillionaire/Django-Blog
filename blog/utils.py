from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import reverse

from .models import *

class ObjectDetailMixin:
	model = None
	template = None

	def get(self, request, slug):
		obj = get_object_or_404(self.model, slug__iexact=slug)
		return render(request, self.template, context={self.model.__name__.lower(): obj, 'admin_object':obj, 'detail':True})

class ObjectCreateMixin:
	form_model = None
	template = None

	def get(self, request):
		form = self.form_model()
		return render(request, self.template, context={'form':form}) 

	def post(self, request):
		bound_form = self.form_model(request.POST) #bound_form - fill form

		if bound_form.is_valid():
			new_obj = bound_form.save()
			return redirect(new_obj)
		return render(request, self.template, context={'form':bound_form})

class ObjectUpdateMixin:
	model = None
	form_model = None
	template = None

	def get(self, request, slug):
		obj = self.model.objects.get(slug__iexact=slug)
		bound_form = self.form_model(instance=obj)
		return render(request, self.template, context={'form':bound_form, self.model.__name__.lower():obj})

	def post(self, request, slug):
		obj = self.model.objects.get(slug__iexact=slug)
		bound_form = self.form_model(request.POST, instance=obj)

		if bound_form.is_valid():
			new_obj = bound_form.save()
			return redirect(new_obj)
		return render(request, self.template, context={'form':bound_form, self.model.__name__.lower():obj})

class ObjectDeleteMixin:
	model = None
	template = None
	url_temp_name = None
	def get(self, request, slug):
		obj = self.model.objects.get(slug__iexact=slug)
		return render(request, self.template, context={self.model.__name__.lower():obj})

	def post(self, request, slug):
		obj = self.model.objects.get(slug__iexact=slug)
		obj.delete()
		return redirect(reverse(self.url_temp_name)) 
		