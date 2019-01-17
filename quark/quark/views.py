from django.shortcuts import render, redirect
import pyrebase
import time
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

DEFAULT_BAL = 100

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

def profile(request):
    if request.session['uid'] == str(session_id):
        idtoken= request.session['uid']
        a = auth.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']
        e = database.child("users").child(a).child("email").get().val()
        n = database.child("users").child(a).child("name").get().val()
        g = database.child("users").child(a).child("gender").get().val()
        p = database.child("users").child(a).child("phone").get().val()
        c = database.child("users").child(a).child("college").get().val()
        r = database.child("users").child(a).child("rank").get().val()
        ac = database.child("users").child(a).child("accBal").get().val()
        return render(request,'profile.html',{"e":e,"n":n,"g":g,"p":p,"c":c,"r":r,"ac":ac})
        

    return render (request, 'homepage.html')
def ranking(request):
    ranklist = []
    new_ranklist=[]
    rank = database.child("users").get()
    for i in rank.each():
        balance=database.child("users").child(str(i.key())).get().val()['accBal']
        name_user=database.child("users").child(str(i.key())).get().val()['name']
        ranklist.append({'name_user':name_user,'accBal':accBal})
        new_ranklist=OrderedDict(sorted(ranklist.items()))
    return render(request, 'ranking.html', {'new_ranklist': new_ranklist })    

def home(request):
	return render(request, 'homepage.html', {"e":'sukdik'})

def news(request):
    newslist = []
    news = database.child("news").get()
    for i in news.each():
        newslist.append(i.val())
    return render(request, 'newspage.html', {'newsList': newslist })

def signOut(request):
    del request.session['uid']
    return render(request,'signOut.html')

def signUp(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        passw=request.POST.get('pass')
        gender=request.POST.get('gender')
        phone=request.POST.get('phone')
        college=request.POST.get('college')
        city=request.POST.get('city')
        try:
            user=auth.create_user_with_email_and_password(email,passw)
        except:
            message="Unable to create account try again"
            return render(request,"signUp.html",{"messg":message})
        
        uid = user['localId']
        data={'name':name,'email':email,'gender':gender,'phone': phone, 'college':college,'city':city,'accBal': DEFAULT_BAL, 'rank': 0}
        database.child("users").child(uid).set(data)
        return redirect('signin')	

    return render(request,"signUp.html")

def portfolio(request):
    stocksList = [] #list of dictionaries of each individual stock
    stocks = database.child("users").child("uid1").child("purchasedStocks").get() #replace uid1 with actual user's uid
    
    for i in stocks.each():
        #temp is a dictionary
        #stocksList is a list of dictionaries
        price = database.child("stocks").child( str(i.key()) ).get().val()['currPrice'] 
        temp = i.val()
        pPrice = temp['purchasedPrice']
        pPrice = (pPrice - price)/price
        temp.update({ 'change':  pPrice })
        stocksList.append(temp)

    return render(request, 'portfolio.html', { 'purchasedStocksList' : stocksList })

def buystock(request):
    if request.method == 'POST':
        time.sleep(10)
        data = { 
            'price' : request.POST.get('buyprice'),
            'qty' : request.POST.get('quantity')
        }
        database.child("testing").set(data)
        return render(request, 'buystock.html')

    return render(request, 'buystock.html')

