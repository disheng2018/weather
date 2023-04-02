import streamlit as st
import streamlit.components.v1 as components
import requests
from bs4 import BeautifulSoup
import datetime

# 2023年04月01日 15:16:48
# V1.1
# by Zhang, zi cheng

beichen_url = "https://tianqi.moji.com/weather/china/tianjin/beichen-district"
http_headers = { 'Accept': '*/*','Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'}
def get_real_url(url):
    rs = requests.get(url,headers=http_headers, timeout=10)
    return rs.url

def getHTMLdocument(url):
    r = requests.get(url)
    return r.text

def get_weather(url_web):
    try:
        url_web_1 = url_web.replace("today", "weather").replace("aqi", "weather")
        html_document = getHTMLdocument(url_web_1)
        # 选用lxml解析器来解析
        soup = BeautifulSoup(html_document, 'html.parser')

        # 获取城市class
        location = soup.find('em').string
        district = location.split("， ")[0]

        # 获取当天信息class
        ul_today = soup.find('ul', class_ = "days clearfix")

        weather_info = []
        for li in ul_today.find_all("li"):
            today_text = li.text.strip().replace("\n","")
            weather_info.append(today_text)

        # print("({dist}) {w_1} {w_2}[{w_3}] ({w_4})".format(dist = district, w_1 = weather_info[1], w_2 = weather_info[3], w_3 = weather_info[2].replace(" / ", "~"), w_4 = weather_info[4], ))
        if "today" in url_web:
            weather_get = "({dist}) {w_1} {w_2}[{w_3}]".format(dist = district, w_1 = weather_info[1], w_2 = weather_info[3], w_3 = weather_info[2].replace(" / ", "~"))
        else:
            weather_get = "({dist}) {w_1} {w_2}[{w_3}] ({w_4})".format(dist = district, w_1 = weather_info[1], w_2 = weather_info[3], w_3 = weather_info[2].replace(" / ", "~"), w_4 = weather_info[4], )
        return weather_get
    except:
        return "请输入正确的网址"

today = datetime.date.today()
st.markdown("V1.1版`（默认置顶显示北辰区天气）`")
st.markdown("今天的日期：**" + str(today) + "**")

col1, col2 = st.columns(2)


with col1:
    st.code (get_weather(beichen_url))
    web_url = st.text_input("请输入墨迹天气网址：", beichen_url)
    if st.button('手动更新☝的地址后，再获取👇'):
        if web_url:
            if "weather" or "aqi" or "today" in web_url:
                st.code(get_weather(web_url))
            else:
                st.write('请输入正确的网址后再点“获取”！！！')

with col2:
    # embed streamlit docs in a streamlit app
    components.iframe("https://tianqi.moji.com/weather/china", height=400, scrolling=True)

with st.sidebar:
    st.markdown("""
    <<<版本更新>>>

    V1.0: 
    
    1. 置顶默认显示北辰区的天气信息
    
    2. 如果出差等不在北辰的情况
    
    > 2.1 在下面的墨迹天气网页里手动或者利用定位索引到比如“北京”，鼠标悬停在`空气质量处`（如果在手机端，可以长按此处复制当前网页链接）；
    
    > 2.2 如果找不到空气质量就悬浮在`今天`处，但得到的天气信息没有PM2.5指数，因为人家空气太好了，哈哈。
    
    3. 把网址输入到上面的输入框里，点击【获取】即可。

    V2.0: （正在构思）

    直接点击iframe里的元素，获取当前网址，不再手动录入，但是我这个小白还不太会，哈哈哈。
    """)