from flask import Flask, render_template, request, jsonify
import pandas as pd
import random

app = Flask(__name__)

# 讀取EXCEL
try:
    cities_df = pd.read_excel('stations.xlsx', sheet_name='cities')
    stations_df = pd.read_excel('stations.xlsx', sheet_name='stations')
    places_df = pd.read_excel('places.xlsx', sheet_name='dot')
    data_df = pd.read_excel('data.xlsx')
except Exception as e:
    print("Error reading Excel file:", e)

# 將數據轉換為字典
cities_data = []
for _, city_row in cities_df.iterrows():
    city_id = city_row['id']
    city_name = city_row['name']
    city_stations = stations_df[stations_df['city_id'] == city_id]['name'].tolist()
    city_places = places_df[places_df['city_id'] == city_id][['名稱', '類別']].dropna().to_dict(orient='records')
    cities_data.append({
        'id': city_id,
        'name': city_name,
        'stations': city_stations,
        'places': city_places
    })

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/advice', methods=['POST'])
def advice():
    station = request.form['station']
    startst = request.form['startst'] 
    country_id = request.form['country']
    recommendations = request.form['recommendations'].split(',') if request.form['recommendations'] else []
    # 打印起点火车站

    valid_places_df = places_df.dropna()  # 去除NaN值

    if country_id == "all":
        # 如果縣市選擇了“都可以”
        if recommendations:
            # 有選擇景點類型
            valid_places_df = valid_places_df[valid_places_df['類別'].isin(recommendations)]
        places = valid_places_df.sample(n=min(30, len(valid_places_df))).to_dict(orient='records')
        country = "所有縣市"
    else:
        country_id = int(country_id)
        country = next((city['name'] for city in cities_data if city['id'] == country_id), "未知縣市")
        places = next((city['places'] for city in cities_data if city['id'] == country_id), [])

        # 如果选择了县市，且没有选择景点类型
        if recommendations:
            # 有選擇景點類型
            places = [place for place in places if place['類別'] in recommendations]
        else:
            # 沒有選擇景點類型，顯示所有景點
            places = [place for place in places if pd.notna(place['名稱'])]

    # 确保推荐的景点数不超过30个
    if len(places) > 30:
        places = random.sample(places, 30)

    return render_template('advice.html', startst=startst, country=country, places=places, recommendations=recommendations)

@app.route('/road', methods=['POST'])
def road():
    selected_places = request.form.getlist('places')
    return render_template('road.html', selected_places=selected_places)

@app.route('/data')
def get_cities():
    return jsonify({"cities": cities_data})

@app.route('/stations')
def get_stations():
    country_id = request.args.get('country')
    stations = next((city['stations'] for city in cities_data if city['id'] == int(country_id)), [])
    return jsonify({"stations": stations})

@app.route('/search')
def search():
    query = request.args.get('q')
    results = data_df[data_df['name'].str.contains(query, case=False, na=False)]['name'].tolist()
    return jsonify(results)

@app.route('/place-info/<place_name>', methods=['GET'])
def place_info(place_name):
    place_info = places_df[places_df['名稱'] == place_name].to_dict(orient='records')
    if not place_info:
        return "Place not found", 404

    place_info = [{k: (v if pd.notna(v) else '') for k, v in place.items()} for place in place_info]

    return render_template('place_info.html', place=place_info[0])

@app.route('/travel', methods=['POST'])
def travel():
    country = request.form.get('country')
    station = request.form.get('station')
    address = request.form.get('address')

    return render_template('travel.html', country=country, station=station, address=address)    

@app.route('/index77x', methods=['POST'])
def index77x():
    start_station = request.form.get('start_station')
    destination = request.form.get('destination')

    return render_template('index77x.html', start_station=start_station, destination=destination)

@app.route('/retrain', methods=['GET', 'POST'])
def retrain():
    if request.method == 'POST':
        start_station = request.form.get('station')
        destination = request.form.get('destination')

        return render_template('index77x.html', start_station=start_station, destination=destination)

    return render_template('retrain.html')

@app.route('/repin')
def repin():
    return render_template('repin.html')

@app.route('/readvice', methods=['POST'])
def readvice():
    #station = request.form['station']
    #startst = request.form['startst'] 
    country_id = request.form['country']
    recommendations = request.form['recommendations'].split(',') if request.form['recommendations'] else []
    # 打印起点火车站

    valid_places_df = places_df.dropna()  # 去除NaN值

    if country_id == "all":
        # 如果縣市選擇了“都可以”
        if recommendations:
            # 有選擇景點類型
            valid_places_df = valid_places_df[valid_places_df['類別'].isin(recommendations)]
        places = valid_places_df.sample(n=min(30, len(valid_places_df))).to_dict(orient='records')
        country = "所有縣市"
    else:
        country_id = int(country_id)
        country = next((city['name'] for city in cities_data if city['id'] == country_id), "未知縣市")
        places = next((city['places'] for city in cities_data if city['id'] == country_id), [])

        # 如果选择了县市，且没有选择景点类型
        if recommendations:
            # 有選擇景點類型
            places = [place for place in places if place['類別'] in recommendations]
        else:
            # 沒有選擇景點類型，顯示所有景點
            places = [place for place in places if pd.notna(place['名稱'])]

    # 确保推荐的景点数不超过30个
    if len(places) > 30:
        places = random.sample(places, 30)

    return render_template('readvice.html', country=country, places=places, recommendations=recommendations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
