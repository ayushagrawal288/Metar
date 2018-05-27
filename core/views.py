# from django.shortcuts import render
# from django.views.generic import View
from django.http import HttpResponse
from core.redis import REDIS_CACHE
import requests
from datetime import date, timedelta
from core.utils import qs_to_dict
import json


def pingView(request):
    return HttpResponse(json.dumps({'data': "pong"}))


def infoView(request):
    if request.method == 'GET':
        params = qs_to_dict(request.META['QUERY_STRING'])
        scode = params.get('scode', '')
        nocache = int(params.get('nocache', 0))

        if len(scode) != 4:
            return HttpResponse(json.dumps({'message': "invalid scode value"}), status=400)

        if nocache not in (0, 1):
            return HttpResponse(json.dumps({'message': "invalid nocache value"}), status=400)

        if not nocache:
            metar_data = REDIS_CACHE.get(scode)
            if metar_data:
                print('from redis')
                return HttpResponse(metar_data)

        base_url = 'http://tgftp.nws.noaa.gov/data/observations/metar/stations/' + scode + '.TXT'
        response = requests.get(base_url)

        if response.status_code != 200:
            return HttpResponse(json.dumps({'message': "invalid scode value"}), status=400)

        data = response.content.decode('utf-8').split()[2:]
        index = 0
        dic = dict()
        dic.update({"station": data[index]})
        index += 1
        time = data[index]
        index += 1
        dic.update({"last_observation": date.today().replace(day=int(time[:2])).isoformat() + ' at ' + \
                           time[2:4] + ':' + time[4:6] + ' GMT'})

        st = data[index]
        index += 1
        if st =='AUTO':
            dic.update({st: "autonomic wheather reporting"})
            st = data[index]
            if st == 'COR':
                index += 1
                dic['last_observation'] = date.today().replace(day=int(data[1][:2])).isoformat() + ' at ' + \
                                          data[-1][:2] + ':' + data[-1][:4] + ' GMT'

        st = data[index]
        index += 1
        wind = "wind is blowing from " + str(int(st[:3])) + ' degrees (true) at a sustained speed of ' + \
               str(int(st[3:5])) + ' knots'
        if 'G' in st:
            wind = wind + 'with ' + st[6:8] + ' knots gusts.'
        dic.update({'wind': wind})

        st = data[index]
        if 'V' in st:
            index += 1
            dic.update({'wind_direction': "wind direction varying between " + str(int(st[:3])) + ' and ' +
                                          str(int(st[4:]))})

        st = data[index]
        if st.endswith('SM'):
            index += 1
            dic.update({'visibility': "the visibility is " + str(int(st[:-2])) + ' statute miles.'})

        st = data[index]
        if st.startswith('R'):
            index += 1
            if 'L' == st[3]:
                direction = 'Left'
            elif 'C' == st[3]:
                direction = 'Center'
            else:
                direction = 'Right'
            unit = ' ft' if st.endswith('FT') else 'meters'
            range_st = 'runway visual range for runway ' + str(int(st[1:3])) + direction + ' is ' + str(int(st[5:9])) \
                       + unit
            dic.update({'range': range_st})

        st = data[index]
        if 'CLR' == st:
            dic.update({'weather': 'sky is clear'})
            index += 1

        st = data[index]
        index += 1
        temp = st.split('/')
        if temp[0].startswith('M'):
            temp[0] = -1 * int(temp[0][1:])
        else:
            temp[0] = int(temp[0])
        if temp[1].startswith('M'):
            temp[1] = -1 * int(temp[1][1:])
        else:
            temp[1] = int(temp[1])
        dic.update({'temperature': "the current temperature is " + str(temp[0]) + ' C and the dewpoint is ' +
                                   str(temp[1]) + ' C.'})

        st = data[index]
        dic.update({'atmospheric_pressure': "is " + st[1:3] + '.' + st[3:] + ' inches of mercury.'})
        metar_data = json.dumps({'data': dic})
        REDIS_CACHE.set(scode, metar_data, ex=int(timedelta(minutes=5).total_seconds()))
        return HttpResponse(metar_data)

    return HttpResponse(json.dumps({'message': "method not allowed"}), status=405)


