import swisseph as swe
import datetime
import pytz
from django.shortcuts import render, get_object_or_404
from .models import KundliDetails

swe.set_ephe_path('')

def get_kundli_data(birth_date, birth_time, latitude, longitude, timezone_str):
    # Localize birth datetime to the correct timezone and convert to UTC
    local = pytz.timezone(timezone_str)
    local_dt = local.localize(datetime.datetime.combine(birth_date, birth_time), is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute / 60.0)
    houses, ascmc = swe.houses(jd, latitude, longitude, b'W')  # Use Whole Sign houses for Vedic

    planets = [
        (swe.SUN, 'Sun'),
        (swe.MOON, 'Moon'),
        (swe.MERCURY, 'Mercury'),
        (swe.VENUS, 'Venus'),
        (swe.MARS, 'Mars'),
        (swe.JUPITER, 'Jupiter'),
        (swe.SATURN, 'Saturn'),
        (swe.MEAN_NODE, 'Rahu'),
    ]
    planet_data = []
    rahu_lon = None

    def get_house_number(lon, houses):
        for i in range(12):
            start = houses[i]
            end = houses[(i + 1) % 12]
            if start < end:
                if start <= lon < end:
                    return i + 1
            else:
                if lon >= start or lon < end:
                    return i + 1
        return 12

    for planet_const, planet_name in planets:
        result, _ = swe.calc_ut(jd, planet_const)
        lon = result[0]
        if planet_name == 'Rahu':
            rahu_lon = lon
        house = get_house_number(lon, houses)
        planet_data.append({
            'name': planet_name,
            'degree': round(lon, 2),
            'house': house,
        })

    if rahu_lon is not None:
        ketu_lon = (rahu_lon + 180) % 360
        house = get_house_number(ketu_lon, houses)
        planet_data.append({
            'name': 'Ketu',
            'degree': round(ketu_lon, 2),
            'house': house,
        })

    house_cusps = [round(h, 2) for h in houses[:12]]
    return planet_data, house_cusps

def kundli_view(request, pk):
    person = get_object_or_404(KundliDetails, pk=pk)
    planet_data, house_cusps = get_kundli_data(
        person.birth_date,
        person.birth_time,
        person.latitude,
        person.longitude,
        person.timezone  # Use the timezone field from the model
    )
    house_cusps_dict = {str(i+1): house_cusps[i] for i in range(12)}
    house_order = [6, 10, 11, 7,
                   5, 0, 0, 8,
                   4, 0, 0, 9,
                   3, 2, 1, 12]
    context = {
        'person': person,
        'planet_data': planet_data,
        'house_cusps': house_cusps_dict,
        'house_order': house_order,
    }
    return render(request, 'kundli_north_indian.html', context)

def astrology_home(request):
    return render(request, 'astrology_home.html')