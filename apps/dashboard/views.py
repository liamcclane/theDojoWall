from django.shortcuts import render, redirect
from apps.dashboard.models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request,'dashboard/login_reg.html')


def register(request):
    print('where am i erroring')
    # include some logic to validate user input before adding them to the database!
    print('*'*25)
    print(request.POST)
    print('*'*25)
    
    errors = User.objects.validation(request.POST)

    if len(errors)>0:
        # render the same home page/registraion form with error messages

        # keys in error dictonary add it to the messages
        messages.error(request, errors['first_name'], extra_tags='first_name')

        print(errors)

        return render(request,'dashboard/login_reg.html',errors)
    
    else:
        print('INSIDE THE ELSE STATEMENT WHERE WE CREATE A NEW USER AND GO TO THE WELCOME PG')
        # only ecrypt the password and continue on if all the validations have passed
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())  # create the hash    
        
        # be sure you set up your database so it can store password hashes this long (60 characters)
        # make sure you put the hashed password in the database, not the one from the form!
        User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'], email=request.POST['email'], hashedPw=pw_hash) 

        newestUser = User.objects.last()
        request.session['userid'] = newestUser.id
        return redirect("/wall") # never render on a post, always redirect!    




def login(request):
    # see if the username provided exists in the database
    user = User.objects.filter(email=request.POST['email']) # why are we using filter here instead of get?
    
    if user: 
        # note that we take advantage of truthiness here: an empty list will return false
        logged_user = user[0]
        
        # assuming we only have one user with this email address, 
        # the user would be first in the list we get back
        # of course, we should have some logic to prevent duplicates of emails 
        # when we create users use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
        if bcrypt.checkpw(request.POST['hashPw'].encode(), logged_user.hashedPw.encode()):
            
            # if we get True after checking the password, we may put the user id in session
            request.session['userid'] = logged_user.id
            
            # never render on a post, always redirect!
            return redirect('/wall')
        else:
            return render(request,'dashboard/login_reg.html',context = {'wrongPw': 'no email or PASSWORD is wrong'})
    
    else:


        # if we didn't find anything in the database by searching by username or if the passwords don't match, 
        # redirect back to a safe route
        return render(request,"dashboard/login_reg.html",context={'wrongPw':'no EMAIL or password is wrong'})


def wallPg(request):

    if 'userid' in request.session:


        if request.session['userid'] == User.objects.last().id:
            greeting = 'To the side for the first time ever'
        else:
            greeting = 'Welcome Back'

        lst = []
        for i in Post.objects.all():
            lst.insert(0,i)
        
        # print(lst)
        
        context = {
            'user' : User.objects.get(id = request.session['userid']),
            'greeting': greeting,
            'posts' : lst,
            'comments' : Comment.objects.all(),
        }
        print(context['user'])
        print( context['comments'])
        # print(Comment.objects.all())

        return render(request,'dashboard/wall.html',context)
    else:
        return redirect('/')


def createComment(request):
    print('*'*25)
    print(request.POST)

    # get the post that we need to pass into the create function
    postToAppend = Post.objects.get(id = request.POST['postId'])
    personWhoCommented = User.objects.get(id = request.session['userid'])

    Comment.objects.create(content = request.POST['content'],commentor = personWhoCommented, post= postToAppend)
    
    return redirect('/wall')


def createPost(request):
    print('inside the create a post function')
    print('*'*25)
    print(request.POST)

    # validate if the post have anything in it

    user_logged = User.objects.get(id=request.session['userid'])

    Post.objects.create(content=request.POST['content'],poster=user_logged)

    return redirect('/wall')

def deletePost(request, post_id):
    
    deleteP = Post.objects.get(id = post_id)
    
    deleteP.delete()


    return redirect('/wall')


def deleteComment(request, comment_id):
    
    deleteC = Comment.objects.get(id = comment_id)
    
    deleteC.delete()


    return redirect('/wall')



def logout(request):

    if 'userid' in request.session:
    
        del request.session['userid']

    return redirect('/')

