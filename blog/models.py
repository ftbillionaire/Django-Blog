from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from time import time

class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None): #like required*
		if not email:
			raise ValueError("Users must have an email address")
		if not username:
			raise ValueError("Usres must have an username")
		
		user = self.model(
			email = self.normalize_email(email), #convert to lower case fot db
			username = username
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email = self.normalize_email(email),
			password = password,
			username = username
		)

		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)


class Account(AbstractBaseUser):
	email = models.EmailField(verbose_name='email', max_length=60, unique=True)
	username = models.CharField(max_length=30, unique=True)
	date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	#we can add everything: first name, last name and etc.

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	objects = MyAccountManager() #where should the MAM takes the data

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True

class Comment(models.Model):
	post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
	author = models.CharField(max_length=30)
	text = models.TextField()
	created_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.text

	class Meta:
		ordering = ['-created_date']

def gen_slug(sl):
	new_slug = slugify(sl, allow_unicode=True)
	return new_slug + '-' + str(int(time()))

class Post(models.Model):
	title = models.CharField(max_length = 150, db_index=True)
	slug = models.SlugField(max_length=150, blank=True, unique=True)
	body = models.TextField(blank=True, db_index=True)
	image = models.ImageField(upload_to='images', blank=True)
	tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
	date_pub = models.DateTimeField(auto_now_add=True)

	def get_absolute_url(self):
		return reverse("post_detail_url", kwargs={"slug": self.slug})

	def get_update_url(self):
		return reverse('post_update_url', kwargs={'slug':self.slug})

	def get_delete_url(self):
		return reverse('post_delete_url', kwargs={'slug':self.slug})

	def save(self, *args, **kwargs): # args and kwargs will be sent to the constructor of father's class
		if not self.id:
			self.slug = gen_slug(self.title)
		super().save(*args, **kwargs) # super() - class Model

	def __str__(self):
		return '{}'.format(self.title)

	class Meta:
		ordering = ['-date_pub'] # '-' means vice versa: it will sort from the newest to the oldest

class Tag(models.Model):
	title = models.CharField(max_length=50)
	slug = models.SlugField(max_length=50, unique=True)

	def get_absolute_url(self):
		return reverse('tag_detail_url', kwargs={'slug':self.slug})

	def get_update_url(self):
		return reverse('tag_update_url', kwargs={'slug':self.slug})

	def get_delete_url(self):
		return reverse('tag_delete_url', kwargs={'slug':self.slug})

	def __str__(self):
		return '{}'.format(self.title)

	class Meta:
		ordering = ['title']