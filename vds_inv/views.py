from django.http import JsonResponse
from django.shortcuts import render
from vds_inv import balances


def spares(request):
    return render(request, 'vds_inv/spares.html', {'spares': balances.get_balances()})


def requests(request):
    return JsonResponse(balances.get_requests())
