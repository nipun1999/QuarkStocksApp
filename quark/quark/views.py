from django.shortcuts import render, redirect
import pyrebase
from django.contrib import auth as dj_auth

config = {
	'apiKey': "AIzaSyDS_XIGRfuaSIwTQbwWF_nSdVlXdM6uvyY",
    'authDomain': "quarkstocksapp.firebaseapp.com",
    'databaseURL': "https://quarkstocksapp.firebaseio.com",
    'projectId': "quarkstocksapp",
    'storageBucket': "quarkstocksapp.appspot.com",
    'messagingSenderId': "779348030725"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()

news = [
    {'title' : 'News number 1', 'desc' : 'News number 1 talks about things....', 'author' : 'R1'},
    {'title' : 'News number 2', 'desc' : 'News number 2 talks about things....', 'author' : 'R2'},
    {'title' : 'News number 3', 'desc' : 'News number 3 talks about things....', 'author' : 'R3'},
]

def signIn(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        passw = request.POST.get('pass')
        try:
            user = auth.sign_in_with_email_and_password(email,passw)
        except:
            message="invalid credentials"
            return render(request,"signIn.html",{"messg":message})

        #print(user['idToken'])
        user = auth.refresh(user['refreshToken'])
        global session_id 
        session_id = user['idToken']
        print(auth.get_account_info(user['idToken']))
        request.session['uid']=str(session_id)
        return redirect('page1')

    return render(request, 'signIn.html')

def page1(request):
    if request.session['uid'] == str(session_id):
        return render(request, 'page1.html')

    return render (request, 'homepage.html')

def home(request):
	return render(request, 'homepage.html', {"e":'sukdik'})

def news(request):
    news = database.child("news").get()
    for i in news.each():
        print(i.val())
    return render(request, 'newspage.html') #{'newsList':news})

def signOut(request):
    del request.session['uid']
    return render(request,'signOut.html')

def signUp(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        passw=request.POST.get('pass')
        try:
            user=auth.create_user_with_email_and_password(email,passw)
        except:
            message="Unable to create account try again"
            return render(request,"signUp.html",{"messg":message})
        
        uid = user['localId']
        data={"name":name,"status":"1"}
        database.child("users").child(uid).child("details").set(data)
        return redirect('signin')	

    return render(request,"signUp.html")