from django.shortcuts import render
from django.db.models import Q
from .models import Stock


# Create your views here.
def stock_view(request):
    query = request.GET.get('q')
    if query:
        stocks = Stock.objects.filter(
            Q(symbol__icontains=query) | Q(name__icontains=query)
        )
    else:
        stocks = Stock.objects.all()
    
    context = {
        'stocks': stocks,
        'query': query
    }
    return render(request, 'dashboard/stock.html', context)

