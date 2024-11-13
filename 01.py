from flask import Flask, render_template, request, jsonify
import csv
#import folium

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index77x.html')

'''
@app.route('/map', methods=['POST'])
def map():
    # 获取用户提交的地点信息
    location = request.form['location']

    # 使用 Folium 创建地图
    m = folium.Map(location=[25.033, 121.565], zoom_start=12)

    # 在地图上添加标记
    icon = folium.Icon(color='blue')
    tooltip = '<span style="font-size: 10px;">Click me</span>'
    popup_content = f'<div style="white-space: nowrap; font-size: 12px;">{location}</div>'  # 使用 nowrap 让文本横向显示，增加字体大小
    marker = folium.Marker(
        location=[25.033, 121.565],
        popup=folium.Popup(popup_content, max_width=300),  # 设置 max_width 以控制弹出窗口的宽度
        tooltip=tooltip,
        icon=icon
    )
    marker.add_to(m)

    # 将地图保存为 HTML 文件
    m.save('templates/map.html')

    # 返回地图页面
    return render_template('map.html')
'''
'''
@app.route('/get_coords', methods=['POST'])
def get_coords():
    data = request.get_json()
    lat = data['lat']
    lon = data['lon']
    # 在这里您可以对坐标进行处理，例如保存到数据库或进行其他操作
    return jsonify({'message': 'Received coordinates', 'latitude': lat, 'longitude': lon})
'''
if __name__ == '__main__':
    app.run(debug=True)
