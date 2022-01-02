import requests
from bs4 import BeautifulSoup
import time
import configparser
import re

config = configparser.ConfigParser()
config.read('config.ini')
#key = config.read("isThereAnyDeal", "API-key")

def get_comment(game_id, max_num):
    url = "http://steamcommunity.com/app/433850/reviews/?browsefilter=toprated&snr=15_reviews"
    url = "https://steamcommunity.com/app/" + str(game_id) + "/reviews/?browsefilter=toprated&userreviewsoffset=" + str(max_num) + "&filterLanguage=tchinese#scrollTop=0"
    url = "https://steamcommunity.com/app/494430/homecontent/?userreviewscursor=AoIIPuPOp3iCl8kB&userreviewsoffset=10&p=3&workshopitemspage=&readytouseitemspage=2&mtxitemspage=2&itemspage=2&screenshotspage=2&videospage=2&artpage=2&allguidepage=2&webguidepage=2&integratedguidepage=2&discussionspage=2&numperpage=10&browsefilter=toprated&browsefilter=toprated&l=tchinese&appHubSubSection=10&filterLanguage=tchinese&searchText=&maxInappropriateScore=50&forceanon=1"
    i = 3
    a = "https://steamcommunity.com/app/282070/homecontent/?userreviewscursor=AoIIP1AF1XHpo8MB&userreviewsoffset=20&p=3&workshopitemspage=3&readytouseitemspage=3&mtxitemspage=3&itemspage=3&screenshotspage=3&videospage=3&artpage=3&allguidepage=3&webguidepage=3&integratedguidepage=3&discussionspage=3&numperpage=10&browsefilter=toprated&browsefilter=toprated&appid=282070&appHubSubSection=10&appHubSubSection=10&l=tchinese&filterLanguage=tchinese&searchText=&maxInappropriateScore=50&forceanon=1"
    url = 'http://steamcommunity.com/app/282070/homecontent/?userreviewsoffset=' + str(10 * (i - 1)) + '&p=' + str(i) + '&workshopitemspage=' + str(i) + '&readytouseitemspage=' + str(i) + '&mtxitemspage=' + str(i) + '&itemspage=' + str(i) + '&screenshotspage=' + str(i) + '&videospage=' + str(i) + '&artpage=' + str(i) + '&allguidepage=' + str(i) + '&webguidepage=' + str(i) + '&integratedguidepage=' + str(i) + '&discussionspage=' + str(i) + '&numperpage=10&browsefilter=toprated&browsefilter=toprated&appid=282070&appHubSubSection=10&appHubSubSection=10&l=tchinese&filterLanguage=tchinese&searchText=&maxInappropriateScore=50&forceanon=1'
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    comments = soup.find_all("div",class_ = "apphub_CardTextContent")
    for comment in comments :
        date = comment.div.extract()
        print(comment.text)
        #print(date)
def SearchGamebyName(name):
    url = "https://store.steampowered.com/search/?term=" + name
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    game_names = []
    game_links = {}
    for i in range(5):
        game_row = soup.find("span",class_ = "title")
        game_names.append(game_row.text)
        game_links[game_row.text] = game_row.parent.parent.parent.get("href")
        game_row.decompose()
    print(game_links)
    return game_links
def getHistoryPrice(game_id):
    print("0000")
    #url = "https://steamdb.info/app/" + str(game_id)
    #API_key = config["isThereAnyDeal"]["API-key"]
    API_key = "eb1a57f191778cf4dc5d621422ffd49ec56b8317"
    Identifier = requests.get("https://api.isthereanydeal.com/v02/game/plain/?key=" + API_key + "&shop=steam&game_id=app/" + str(game_id)).json()
    plain = Identifier["data"]["plain"]
    print("1111")
    Price = requests.get("https://api.isthereanydeal.com/v01/game/prices/?region=us&shops=steam&key=" + API_key + "&plains=" + plain).json()
    current_cut = Price["data"][plain]["list"][0]["price_cut"]
    steam_url = Price["data"][plain]["list"][0]["url"]
    print("2222")
    Historical_low = requests.get("https://api.isthereanydeal.com/v01/game/lowest/?region=us&shops=steam&key=" + API_key + "&plains=" + plain).json()
    Historical_low_cut = Historical_low["data"][plain]["cut"]
    print("3333")
    html = requests.get(steam_url).text
    soup = BeautifulSoup(html, "html.parser")
    current_price_bg = soup.find("div", "game_purchase_action_bg")
    current_price_div = current_price_bg.find("div", "game_purchase_price price")
    if(not current_price_div):
        current_price_div = current_price_bg.find("div", "discount_original_price")
    current_price = re.search('NT\$ (\d+)',current_price_div.text).group(1)
    struct_time = time.localtime(Historical_low["data"][plain]["added"]) # 轉成時間元組
    timeString = time.strftime("%Y-%m-%d", struct_time) # 轉成字串
    
    print(current_cut)
    print(steam_url)
    print(Historical_low_cut)
    print(current_price)
    print(timeString)
    return [int(current_price), int(current_cut), int(Historical_low_cut), timeString]
if __name__ == "__main__":
    #get_comment(494430,50)

    getHistoryPrice(933110)
    
    #SearchGamebyName("aoe")

    # headers = {    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'}
    # for i in range(1, 6):
    #     url = 'http://steamcommunity.com/app/433850/homecontent/?userreviewsoffset=' + str(10 * (i - 1)) + '&p=' + str(i) + '&workshopitemspage=' + str(i) + '&readytouseitemspage=' + str(i) + '&mtxitemspage=' + str(i) + '&itemspage=' + str(i) + '&screenshotspage=' + str(i) + '&videospage=' + str(i) + '&artpage=' + str(i) + '&allguidepage=' + str(i) + '&webguidepage=' + str(i) + '&integratedguidepage=' + str(i) + '&discussionspage=' + str(i) + '&numperpage=10&browsefilter=toprated&browsefilter=toprated&appid=433850&appHubSubSection=10&l=schinese&filterLanguage=default&searchText=&forceanon=1'
    #     html = requests.get(url, headers=headers).text
    #     soup = BeautifulSoup(html, 'html.parser')  # 如果装了lxml，推荐把解析器改为lxml
    #     reviews = soup.find_all('div', {'class': 'apphub_Card'})    
    #     for review in reviews:
    #         nick = review.find('div', {'class': 'apphub_CardContentAuthorName'})
    #         title = review.find('div', {'class': 'title'}).text
    #         hour = review.find('div', {'class': 'hours'}).text.split(' ')[0]
    #         link = nick.find('a').attrs['href']
    #         comment = review.find('div', {'class': 'apphub_CardTextContent'}).text
    #         print(nick.text, title, hour, link, )
    #         print(comment.split('\n'))
