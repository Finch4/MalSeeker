import itertools

from selenium import webdriver
import time
import re
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
from dash.dependencies import Input, Output
import plotly.express as px

from ipycytoscape import cytoscape

def find(string):
    # findall() has been used
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]


driver = webdriver.Chrome("chromedriver.exe")

elements = [
            #{'data': {'id': 'ca', 'label': 'Canada'}}, -> Format
            #{'data': {'source': 'ca', 'target': 'on'}},
        ]

# &tbs=qdr:s - results of the previous second
# &tbs=qdr:n - results of the previous minute
# &tbs=qdr:h - results of the previous hour
# &tbs=qdr:d - results of the previous day
# &tbs=qdr:w -results of the previous week
# &tbs=qdr:m - results of the previous month
# &tbs=qdr:y - results of the previous year

driver.get("https://www.bing.com/search?q=site%3ayoutube.com+intitle%3afree+hack+download&count=100&tbs=qdr%3ad&first=1&FORM=PERE")
time.sleep(2)
url_titles = driver.find_elements_by_class_name("b_results")
pages = len(driver.find_elements_by_class_name("sb_pagF"))
report = open("MalSeekerReport","w")

youtube_urls = []
more_urls = []
wrap_youtube_urls = []
warp_more_urls = []
combination_list = \
    [

    ]

def find_urls():
    for i in range(1, 100):
        try:
            url = driver.find_element_by_xpath(f"/html/body/div[1]/main/ol/li[{i}]/div[1]/h2/a").get_attribute("href")
            description_urls = find(driver.find_element_by_xpath(f"/html/body/div[1]/main/ol/li[{i}]/div[2]/p").text)
            report.write \
    (f"""
    Url: {url}
    Description [Only Urls]: {description_urls}
    """)
            youtube_urls.append(url)
            if not (description_urls in more_urls):
                more_urls.append(description_urls)

        except:
            pass


    driver.get("https://www.bing.com/search?q=site%3ayoutube.com+intitle%3afree+hack+download&count=100&tbs=qdr%3ad&first=51&FORM=PERE")
    time.sleep(2)
    for i in range(1, 100):
        try:
            url = driver.find_element_by_xpath(f"/html/body/div[1]/main/ol/li[{i}]/div[1]/h2/a").get_attribute("href")
            description_urls = find(driver.find_element_by_xpath(f"/html/body/div[1]/main/ol/li[{i}]/div[2]/p").text)
            report.write \
(f"""
Url: {url}
Description [Only Urls]: {description_urls}
""")
            youtube_urls.append(url)
            if not (description_urls in more_urls):
                more_urls.append(description_urls)
        except:
            pass

    return youtube_urls, more_urls

more_urlsz = find_urls()[1]

for i in more_urls:
    list_youtube_urls = []
    list_more_urls = []
    if len(i) > 1:
        for y in i:
            if len(y) == 0:
                continue
            else:
                driver.get(
                    f"https://www.bing.com/search?q={y}&count=100&tbs=qdr%3ad&first=51&FORM=PERE")
                time.sleep(2)
                for i in range(1, 100):
                    try:
                        list_youtube_urls.append(driver.find_element_by_xpath(f"/html/body/div[1]/main/ol/li[{i}]/div[1]/h2/a").get_attribute(
                            "href"))
                        list_more_urls.append(find(driver.find_element_by_xpath(f"/html/body/div[1]/main/ol/li[{i}]/div[2]/p").text))
                    except:
                        pass
    else:
        if len(i) == 0:
            continue
        else:
            driver.get(
                f"https://www.bing.com/search?q={i}&count=100&tbs=qdr%3ad&first=51&FORM=PERE")
            time.sleep(2)
            for i in range(1, 100):
                try:
                    list_youtube_urls.append(
                        driver.find_element_by_xpath(f"/html/body/div[1]/main/ol/li[{i}]/div[1]/h2/a").get_attribute(
                            "href"))
                    list_more_urls.append(
                        find(driver.find_element_by_xpath(f"/html/body/div[1]/main/ol/li[{i}]/div[2]/p").text))
                except:
                    pass
    wrap_youtube_urls.append(list_youtube_urls)
    warp_more_urls.append(list_more_urls)



app = dash.Dash(__name__)

for combination in itertools.zip_longest(youtube_urls, more_urls, wrap_youtube_urls, warp_more_urls):
    combination_list.append(combination)

for url,murl,wurls,wmurls in combination_list:
    i = 0
    if len(str(url)) < 1 or url == None:
        elements.append({'data': {'id': f'{url}{i}', 'label': f'Something went wrong'}})
    else:
        elements.append({'data': {'id': f'{url}', 'label': f'First Url: {url}'}})
    if len(str(murl)) < 1 or murl == None or murl == []:
        elements.append({'data': {'id': f'{murl}{i}', 'label': f'No First Layers Urls'}})
        elements.append({'data': {'source': f'{url}', 'target': f'{murl}{i}'}})
    else:
        elements.append({'data': {'id': f'{murl}', 'label': f'First Layer Urls: {murl}'}})
        elements.append({'data': {'source': f'{url}', 'target': f'{murl}'}})
    if len(str(wurls)) < 1 or wurls == None or wurls == []:
        elements.append({'data': {'id': f'{wurls}{i}', 'label': f"No Second Layers Urls"}})
        elements.append({'data': {'source': f'{url}', 'target': f'{wurls}{i}'}})
    else:
        elements.append({'data': {'id': f'{wurls}', 'label': f'Second Layer Urls: {wurls}'}})
        elements.append({'data': {'source': f'{url}', 'target': f'{wurls}'}})
    if len(str(wmurls)) < 1 or wmurls == None or str(wurls).__contains__("[],") or str(wurls).__contains__("[]"):
        elements.append({'data': {'id': f'{wmurls}{i}', 'label': f'No More Urls Found With The Second Layers Urls'}})
        elements.append({'data': {'source': f'{url}', 'target': f'{wmurls}{i}'}})
    else:
        elements.append({'data': {'id': f'{wmurls}', 'label': f' More Urls Found Searching With The Second Layer Urls{wmurls}'}})
        elements.append({'data': {'source': f'{url}', 'target': f'{wmurls}'}})


    i += 1








app.layout = html.Div(children=[
    html.P("Dash Cytoscape:"),
    cyto.Cytoscape(
        id='cytoscape',
        elements=elements,
        layout={'name': 'breadthfirst', "minNodeSpacing":200, "edgeLengthVal":200},
        style={'width': '1920px', 'height': '1080px'},

    )
])



app.run_server(debug=False)
