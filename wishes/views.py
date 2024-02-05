from django.shortcuts import render

from wishes.models import Wish

def get_statistics(wishes):

    wishes_count = {
        0: len(wishes),
        4: len([w for w in wishes if w.rarity == 4]),
        5: len([w for w in wishes if w.rarity == 5]),
    }
    probabilities = {
        4: round(wishes_count[4] / wishes_count[0] * 100, 4),
        5: round(wishes_count[5] / wishes_count[0] * 100, 4),
    }

    gaps = {
        5: [],
        4: [],
    }
    counters = {
        5: 0,
        4: 0,
    }

    for wish in wishes:
        for i in [4,5]:
            counters[i] += 1

        if wish.rarity in [4,5]:
            gaps[wish.rarity].append(counters[wish.rarity])
            counters[wish.rarity] = 0


    median_roll_count = {
        5: round(sum(gaps[5]) / len(gaps[5]), 6),
        4: round(sum(gaps[4]) / len(gaps[4]), 6),
    }

    return wishes_count, probabilities, median_roll_count, counters





def index(request):
    query = dict()
    rarity_list = request.GET.getlist('rarity')
    if rarity_list:
        query['rarity__in'] = rarity_list
    banner_list = request.GET.getlist('banner')
    if banner_list:
        query['banner_type__in'] = banner_list

    sorting = request.GET.get('sort', 'time')
    is_asc = request.GET.get('asc', 'false')

    wishes_list = Wish.objects.filter(**query).order_by('time')

    wishes_count, probabilities, median_roll_count, counters = get_statistics(wishes_list)

    wishes_list.order_by(sorting)
    if is_asc == 'false':
        wishes_list = wishes_list.reverse()

    context = {
        'wishes_list': wishes_list,
        'wishes_count': wishes_count,
        'probabilities': probabilities,
        'median_roll_count': median_roll_count,
        'counters': counters,
    }
    return render(request, 'index.html', context)
