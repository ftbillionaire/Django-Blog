from django.http import HttpResponse
from django.shortcuts import redirect, render

# there're 2 types of redirect: permanent and 
# temporary. Although default is temporary, we can 
# make a permanent one using TRUE

def redirect_blog(request):
	return redirect('posts_list_url', permanent=True)