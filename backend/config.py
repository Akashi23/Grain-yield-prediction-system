filename = './data/finalized_model.sav'
filename_scaler = './data/finalized_scaler.sav'
path_to_data = './data/dataset.csv'
features_for_train = [
        'year', 'month', 'region', 'crop', 'maxtempC', 'maxtempF',
        'mintempC', 'mintempF', 'avgtempC', 'avgtempF',
        'totalSnow_cm', 'sunHour', 'uvIndex_x', 'day', 
        'tempC', 'tempF', 'windspeedMiles', 
        'windspeedKmph', 'winddirDegree', 'winddir16Point', 
        'weatherCode', 'weatherDesc', 'precipMM', 'precipInches', 
        'humidity', 'visibility', 'visibilityMiles', 'pressure', 
        'pressureInches', 'cloudcover', 'HeatIndexC', 'HeatIndexF', 
        'DewPointC', 'DewPointF', 'WindChillC', 'WindChillF', 'WindGustMiles', 
        'WindGustKmph', 'FeelsLikeC', 'FeelsLikeF', 'uvIndex_y', 'soil']