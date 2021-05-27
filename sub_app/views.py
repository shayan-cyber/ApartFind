from django.http.response import Http404
from django.shortcuts import render,HttpResponse
import pickle 
import pandas as pd
import sklearn
# Create your views here.
def home(request):
    
    return render(request, 'home.html')

def predict(request):
    with open("static/india_home_price_prediction.pickle", 'rb') as f:
        rndm_frst = pickle.load(f)
    print(rndm_frst.predict([[0,1,3,1300,1,1,12.9,77,1,1,0 ]]))
    if request.method =="POST":
        lat = request.POST.get('lat', '')
        long = request.POST.get('long', '')
        rera = request.POST.get('rera', '0')
        under_const = request.POST.get('under_const', '0')
        resale = request.POST.get('resale','0')
        ready_to_move = request.POST.get('ready_to_move', '0')
        type_of_seller = request.POST.get('type_of_seller','')
        owner = request.POST.get('owner', '0')
        sqft = request.POST.get('sqft', '')
        bhk_no = request.POST.get('bhk', '')
        bath_no = request.POST.get('bath', '')
        form_data ={
            'lat':lat,
            'long':long,
            'rera':rera,
            'under_const': under_const,
            'ready_to_move': ready_to_move,
            'resale': resale,
            'type_of_seller':type_of_seller,
            'sqft' : sqft,
            'bhk_no': bhk_no,
            'bath_no':bath_no
        }
        print(form_data)
        if type_of_seller =='Owner':
            prediction_ = rndm_frst.predict([[under_const, rera, bhk_no, sqft, ready_to_move, resale, long, lat, 1, 0,0]])
        
        if type_of_seller =='Dealer':
            prediction_ = rndm_frst.predict([[under_const, rera, bhk_no, sqft, ready_to_move, resale, long, lat, 1, 0,1]])
        if type_of_seller =='Builder':
            prediction_ = rndm_frst.predict([[under_const, rera, bhk_no, sqft, ready_to_move, resale, long, lat, 1, 1,0]])
        prediction_ = prediction_[0]
        price_per_sqft = (prediction_/float(sqft))*100
        form_data ={
            'lat':round(float(lat), 4),
            'long':round(float(long), 4),
            'rera':rera,
            'under_const': under_const,
            'ready_to_move': ready_to_move,
            'resale': resale,
            'type_of_seller':type_of_seller,
            'sqft' : sqft,
            'bhk_no': bhk_no,
            'bath_no':bath_no,
            'prediction_':prediction_,
            'ppsqft': price_per_sqft

        }
        print(prediction_)
        return render(request, "prediction.html", form_data)
    else:
        raise Http404()
    

    

