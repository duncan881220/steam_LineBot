import requests
from bs4 import BeautifulSoup
import time
import configparser
import re

config = configparser.ConfigParser()
config.read('config.ini')

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
    for i in range(4):
        game_row = soup.find("span",class_ = "title")
        if(game_row):
            game_names.append(game_row.text)
            game_links[game_row.text] = game_row.parent.parent.parent.get("href")
            game_row.decompose()
    print(game_links)
    return game_links
def getHistoryPrice(game_id):
    API_key = config["isThereAnyDeal"]["API-key"]
    Identifier = requests.get("https://api.isthereanydeal.com/v02/game/plain/?key=" + API_key + "&shop=steam&game_id=app/" + str(game_id)).json()
    plain = Identifier["data"]["plain"]

    Price = requests.get("https://api.isthereanydeal.com/v01/game/prices/?region=us&shops=steam&key=" + API_key + "&plains=" + plain).json()
    current_cut = Price["data"][plain]["list"][0]["price_cut"]
    steam_url = Price["data"][plain]["list"][0]["url"]

    Historical_low = requests.get("https://api.isthereanydeal.com/v01/game/lowest/?region=us&shops=steam&key=" + API_key + "&plains=" + plain).json()
    Historical_low_cut = Historical_low["data"][plain]["cut"]
    
    html = requests.get(steam_url).text
    soup = BeautifulSoup(html, "html.parser")
    current_price_bg = soup.find("div", "game_purchase_action_bg")
    current_price_div = current_price_bg.find("div", "game_purchase_price price")
    if(not current_price_div):
        current_price_div = current_price_bg.find("div", "discount_original_price")

    original_price = re.search('NT\$ (\d+,?\d+)',current_price_div.text).group(1)
    original_price = original_price.replace(",","")

    struct_time = time.localtime(Historical_low["data"][plain]["added"]) # 轉成時間元組
    timeString = time.strftime("%Y-%m-%d", struct_time) # 轉成字串
    return [int(original_price), int(current_cut), int(Historical_low_cut), timeString]
def getGameInfo(game_id):
    headers = {'Accept-Language': 'zh-TW,zh;q=0.9'}
    url = "https://store.steampowered.com/app/" + str(game_id)
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")
    recent_string = "近期評論:  "
    summary_column = soup.find("div", class_ ="summary column")
    tar = summary_column.findChild("span")
    recent_string += tar.text
    tar = tar.find_next("span")
    recent_string += tar.text.replace("\t","").replace("\n","").replace("\r","") + "\n"
    tar = tar.find_next("span")
    recent_string += tar.text.replace("\t","").replace("\n","").replace("\r","") + "\n\n"

    all_string =  "所有評論: "
    summary_column = summary_column.find_next("div")
    tar = summary_column.findChild("span")
    all_string += tar.text
    tar = tar.find_next("span")
    all_string += tar.text.replace("\t","").replace("\n","").replace("\r","") + "\n"
    tar = tar.find_next("span")
    all_string += tar.text.replace("\t","").replace("\n","").replace("\r","") + "\n\n"

    release_date = "發行日期: "
    release_date += soup.find("div", class_ = "date").text + "\n\n"

    tag = soup.find("div", class_ ="glance_tags popular_tags")
    tag = tag.findChild("a")
    tag_string = "標籤: "
    for i in range (5):
        tag_string += tag.text.replace("\t","").replace("\n","").replace("\r","") + " "
        tag = tag.find_next("a")

    return recent_string + all_string + release_date + tag_string




    

    

if __name__ == "__main__":
    #get_comment(494430,50)
    #getHistoryPrice(728530)

    #getGameInfo(924970)

    SearchGamebyName("Persona® 5 Strikers")

