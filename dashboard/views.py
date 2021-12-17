from django.core.checks.messages import INFO
from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from databases.models import *
# Create your views here.
def index(request):
    if (request.user.is_authenticated):
        stockobj = Stock.objects.raw("SELECT * FROM databases_stock ORDER BY beta DESC")
        name = request.user.username
        investordetails = Investor.objects.get(Username=name)
        
        bankobj=Bank.objects.get(Username=name)
        accno=bankobj.Account_no
        invested = Investment.objects.raw("SELECT id,Stock_ISIN_id FROM databases_investment WHERE User_Account_no_id='"+accno+"'")
        
        curr_invest=0
        curr =0 
        prev = 0
        for x in invested:
            curr_invest+=x.Quantity*x.Purchased_Value
            curr+=x.Quantity*(Stock.objects.get(ISIN=x.Stock_ISIN_id).Current_price)
            prev+=x.Quantity*(Stock.objects.get(ISIN=x.Stock_ISIN_id).Prev_Close)

        pl =curr_invest-curr
        plper=0
        if(curr_invest!=0):
            plper = (pl/curr_invest)*100
        userdata=Stock.objects.all()

        return render(request,'index_dash.html',{"investordetails":investordetails,userdata:":userdata" ,'stokcs':stockobj,"userinvested":invested,"dashvals":[int(curr_invest),int(curr),int(pl),round(plper,2),prev]})
    else:   
        return HttpResponse('error',status=404)
