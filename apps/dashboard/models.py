from __future__ import unicode_literals
from django.db import models
import re
# Create your models here.


# this manager call validates both the posts and comments
class MessageManager(models.Manager):

    def validation(self,postData):

        errors={}

        if len(postData['content'])<=1:
            errors['noContent'] = 'you cannot not comment nothing'

        return errros





class UserManager(models.Manager):

    def validation(self, postData):

        errors = {}

        # check if the email is unique against all the users
        for user in User.objects.all():
            if user.email == postData['email']:
                errors['notUniqueEmail'] = 'email already exists'

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address"

        if len(postData['first_name']) < 2:
            errors['first_name'] = 'Please enter a longer first name'

        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Please enter a longer last name'

        if len(postData['password']) < 8:
            errors['shortPassword'] = 'Please enter a longer password, must be over 8 charaters long'

        if postData['password'] != postData['password2']:
            errors['misMatch'] = 'your passwords do NOT match'

        return errors


class User(models.Model):

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    
    hashedPw = models.CharField(max_length=100)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()

    def __repr__(self):
        return f'id is {self.id}: {self.first_name} {self.last_name} '




class Post(models.Model):
    
    content = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MessageManager()

    def __repr__(self):
        return f'{self.content} id is {self.id}, owner is {self.poster.first_name}'





class Comment(models.Model):

    content = models.TextField()
    commentor = models.ForeignKey(User, related_name='comments')
    post = models.ForeignKey(Post, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MessageManager()

    def __repr__(self):
        return f'{self.id} comment says : {self.content} by {self.commentor.first_name}'




