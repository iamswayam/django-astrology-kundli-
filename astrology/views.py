import swisseph as swe
import datetime
import pytz
from django.shortcuts import render, redirect, get_object_or_404
from .models import KundliDetails
from .forms import KundliDetailsUserForm


import ephem

def astrology_home(request):
    return render(request, 'astrology_home.html')

def user_signup(request):
    if request.method == 'POST':
        form = KundliDetailsUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('astrology_home')
    else: 
        form = KundliDetailsUserForm()
    return render(request, 'astrology/kundli_form.html', {'form': form})

swe.set_ephe_path('')

# ZODIAC_SIGNS = [
#     "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
#     "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
# ]

# ZODIAC_SIGNS = [
#     "♈", "♉", "♊", "♋", "♌", "♍", "♎", "♏", "♐", "♑", "♒", "♓",  
# ]

ZODIAC_SIGNS = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
]

def get_sign_and_degree(lon):
    sign_index = int(lon // 30)
    sign_degree = lon % 30
    return ZODIAC_SIGNS[sign_index], round(sign_degree, 2)

def get_kundli_data(birth_date, birth_time, latitude, longitude, timezone_str):
    local = pytz.timezone(timezone_str)
    local_dt = local.localize(datetime.datetime.combine(birth_date, birth_time), is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute / 60.0)
    houses, ascmc = swe.houses(jd, latitude, longitude, b'W')  # Whole Sign
    ayanamsa = swe.get_ayanamsa(jd)

    ascendant_sidereal = (ascmc[0] - ayanamsa) % 360
    asc_sign, asc_degree = get_sign_and_degree(ascendant_sidereal)

    planets = [
        (swe.SUN, 'Su'),
        (swe.MOON, 'Mo'),
        (swe.MERCURY, 'Me'),
        (swe.VENUS, 'Ve'),
        (swe.MARS, 'Ma'),
        (swe.JUPITER, 'Ju'),
        (swe.SATURN, 'Saturn'),
        (swe.MEAN_NODE, 'Ra'),
    ]
    planet_data = []
    rahu_sidereal = None

    def get_house_number_whole_sign(lon, houses):
        delta_lon = lon - houses[0]
        normalized_delta_lon = delta_lon % 360
        house_number = int(normalized_delta_lon // 30) + 1
        return house_number

    for planet_const, planet_name in planets:
        result, _ = swe.calc_ut(jd, planet_const)
        lon = result[0]
        sidereal_lon = (lon - ayanamsa) % 360
        if planet_name == 'Ra':
            rahu_sidereal = sidereal_lon
        house = get_house_number_whole_sign(sidereal_lon, houses) + 1
        if house > 12:
            house = 1
        sign, sign_degree = get_sign_and_degree(sidereal_lon)
        planet_data.append({
            'name': planet_name,
            'degree': sign_degree,
            'sign': sign,
            'house': house,
        })

    if rahu_sidereal is not None:
        ketu_sidereal = (rahu_sidereal + 180) % 360
        house = get_house_number_whole_sign(ketu_sidereal, houses)
        sign, sign_degree = get_sign_and_degree(ketu_sidereal)
        planet_data.append({
            'name': 'Ke',
            'degree': sign_degree,
            'sign': sign,
            'house': house,
        })

    house_cusps = [round((h - ayanamsa) % 360, 2) for h in houses[:12]]
    ascendant = {
        'degree': round(asc_degree, 2),
        'sign': asc_sign,
        'full_degree': round(ascendant_sidereal, 2),
    }
    return planet_data, house_cusps, ascendant


def kundli_view(request, pk):
    person = get_object_or_404(KundliDetails, pk=pk)
    planet_data, house_cusps, ascendant = get_kundli_data(
        person.birth_date,
        person.birth_time,
        person.latitude,
        person.longitude,
        person.timezone
    )
    context = {
        'person': person,
        'planet_data': planet_data,
        'house_cusps': house_cusps,
        'ascendant': ascendant,
        'house_numbers': list(range(1, 13)),
    }
    return render(request, 'kundli_north_indian.html',context)