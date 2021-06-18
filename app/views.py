from django.shortcuts import render, redirect
from django.urls import reverse
from app import settings
from app.settings import BUS_STATION_CSV
from django.core.paginator import Paginator


def index(request):
    return redirect(reverse(bus_stations))


def data_base():
    bus_base = []
    with open(BUS_STATION_CSV, 'r', encoding="cp1251") as file:
        file.readline()
        for data in file:
            name = data.split(';')[1].split('»')[0][1:]+'»'
            street = data.split(';')[1].split('», ')[-1][:-1]
            district = data.split(';')[6]
            bus_base.append({'Name': name, 'Street': street, 'District': district})
    return bus_base


new_base = data_base()


def bus_stations(request):
    bus_station_list = []
    current_page = request.GET.get('page', '1')
    mark_start = int(current_page) * settings.STR_PER_PAGE - settings.STR_PER_PAGE
    mark_end = int(current_page) * settings.STR_PER_PAGE
    max_mark = round(len(new_base) / settings.STR_PER_PAGE + 0.5)

    for data in new_base[mark_start: mark_end]:
        bus_station_list.append(data)

    if int(current_page) <= 1:
        prev_page_url = None
    else:
        prev_page_url = str(f'?page={int(current_page)-1}')
    if int(current_page) >= max_mark:
        next_page_url = None
    else:
        next_page_url = str(f'?page={int(current_page) + 1}')

    return render(request, 'index.html', context={
        'bus_stations': bus_station_list,
        'current_page': f'<MYPage {current_page} of {max_mark}>',
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    })


def pagi_view(request):
    number = request.GET.get('page')
    paginator = Paginator(new_base, settings.STR_PER_PAGE)
    pagi = paginator.get_page(number)
    msg = pagi.object_list
    if pagi.has_next():
        next_number = f'?page={pagi.next_page_number()}'
    else:
        next_number = None
    if pagi.has_previous():
        previous_number = f'?page={pagi.previous_page_number()}'
    else:
        previous_number = None
    return render(request, 'index.html', context={
        'bus_stations': msg,
        'current_page': pagi,
        'prev_page_url': previous_number,
        'next_page_url': next_number,
    })
