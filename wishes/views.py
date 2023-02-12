from django.shortcuts import render

from wishes.models import Wish


def index(request):
    wishes_list = Wish.objects.order_by('time').reverse()
    context = {'wishes_list': wishes_list}
    return render(request, 'index.html', context)
