from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from generateapp.generate.TFdeepsurv import generate
import pandas as pd
# Create your views here.
def index(myrequest):
    pamdict = {'name':'666'}
    return render(myrequest,'generateapp/templates/form.html',pamdict)

# def ajax(request):
#     smokingStatus = int(request.POST.get("smokingStatus"))
#     Age = int(request.POST.get("Age"))
#     SBP = int(request.POST.get("SBP"))
#     TC = float(request.POST.get("TC"))
#     Hb = int(request.POST.get("Hb"))
#     HDL = float(request.POST.get("HDL"))
#     _24HourUrinaryProtein = float(request.POST.get("_24HourUrinaryProtein"))
    
#     params = [[smokingStatus, Age, SBP, TC, Hb, HDL, _24HourUrinaryProtein, 0, 0]]
#     res = generate(params)
#     return render(request, 'generateapp/templates/result.html', res)
#     # return JsonResponse(res)

def result(request):
    if request.method == 'GET':
        return render(request, 'generateapp/templates/result.html')

    smokingStatusStr = request.POST.get("smokingStatus")
    AgeStr = request.POST.get("Age")
    SBPStr = request.POST.get("SBP")
    TCStr = request.POST.get("TC")
    HbStr = request.POST.get("Hb")
    HDLStr = request.POST.get("HDL")
    _24HourUrinaryProteinStr = request.POST.get("_24HourUrinaryProtein")

    smokingStatus = int(smokingStatusStr if smokingStatusStr is not None and smokingStatusStr != "" else "0")
    Age = int(AgeStr if AgeStr is not None and AgeStr != "" else "0")
    SBP = int(SBPStr if SBPStr is not None and SBPStr != "" else "0")
    TC = float(TCStr if TCStr is not None and TCStr != "" else "0")
    Hb = float(HbStr if HbStr is not None and HbStr != "" else "0")
    HDL = float(HDLStr if HDLStr is not None and HDLStr != "" else "0")
    _24HourUrinaryProtein = float(_24HourUrinaryProteinStr if _24HourUrinaryProteinStr is not None and _24HourUrinaryProteinStr != "" else "0")
    
    params = [[smokingStatus, Age, SBP, TC, Hb, HDL, _24HourUrinaryProtein, 0, 0]]
    
    res = generate(params)
    return render(request, 'generateapp/templates/result.html', res)