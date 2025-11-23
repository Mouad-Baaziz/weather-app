import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.utils.translation import get_language
from datetime import datetime

def index(request):
    """Main weather app view"""
    return render(request, 'weather/index.html')

def get_weather(request):
    """API endpoint to fetch weather data"""
    city = request.GET.get('city', 'Constantine')
    
    # Get current language from session/cookie
    lang = get_language()
    # Map Django language codes to OpenWeatherMap language codes
    api_lang = 'fr' if lang == 'fr' else 'en'
    
    # Using OpenWeatherMap API (free tier)
    API_KEY = '1eb8e0cdbd8c3c6fb3a718a234e8974e' 
    BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'
    
    try:
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric',
            'lang': api_lang  # Add language parameter
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        
        if response.status_code == 200:
            weather_data = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': round(data['main']['temp']),
                'feels_like': round(data['main']['feels_like']),
                'description': data['weather'][0]['description'].title(),
                'icon': data['weather'][0]['icon'],
                'humidity': data['main']['humidity'],
                'wind_speed': round(data['wind']['speed'] * 3.6),  # Convert to km/h
                'pressure': data['main']['pressure'],
                'visibility': data.get('visibility', 0) // 1000,  # Convert to km
                'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'),
                'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M'),
            }
            return JsonResponse({'success': True, 'data': weather_data})
        else:
            # Translate error messages
            error_msg = 'Ville introuvable' if api_lang == 'fr' else 'City not found'
            return JsonResponse({'success': False, 'error': error_msg})
    
    except Exception as e:
        error_msg = 'Une erreur s\'est produite' if api_lang == 'fr' else 'An error occurred'
        return JsonResponse({'success': False, 'error': error_msg})

def get_forecast(request):
    """API endpoint to fetch 5-day forecast"""
    city = request.GET.get('city', 'Constantine')
    
    # Get current language from session/cookie
    lang = get_language()
    # Map Django language codes to OpenWeatherMap language codes
    api_lang = 'fr' if lang == 'fr' else 'en'
    
    API_KEY = '1eb8e0cdbd8c3c6fb3a718a234e8974e'
    BASE_URL = 'http://api.openweathermap.org/data/2.5/forecast'
    
    # Day name translations
    day_names = {
        'en': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        'fr': ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    }
    
    try:
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric',
            'lang': api_lang  # Add language parameter
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        
        if response.status_code == 200:
            # Get daily forecasts (one per day at noon)
            forecasts = []
            for item in data['list'][::8][:5]:  # Every 8th item (24hrs), max 5 days
                dt = datetime.fromtimestamp(item['dt'])
                # Get day name in the appropriate language
                day_index = dt.weekday()
                day_name = day_names[api_lang][day_index]
                
                forecasts.append({
                    'date': day_name,
                    'temp': round(item['main']['temp']),
                    'description': item['weather'][0]['description'].title(),
                    'icon': item['weather'][0]['icon']
                })
            
            return JsonResponse({'success': True, 'data': forecasts})
        else:
            error_msg = 'Ville introuvable' if api_lang == 'fr' else 'City not found'
            return JsonResponse({'success': False, 'error': error_msg})
    
    except Exception as e:
        error_msg = 'Une erreur s\'est produite' if api_lang == 'fr' else 'An error occurred'
        return JsonResponse({'success': False, 'error': error_msg})