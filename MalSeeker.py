import requests
import datetime
import json
import re
import sys
import codecs
from serpwow.google_search_results import GoogleSearchResults



def find(string):
    # findall() has been used
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]




# create the serpwow object, passing in our API key -> https://app.serpwow.com/login
serpwow = GoogleSearchResults("YOUR_API_KEY")

# set up a dict for the search parameters
params = {
  "q" : "site:youtube.com intitle:free hack download", # You can write whatever you want, like: bitcoin miner free download or credit card money adder free download
  "num" : "100",
  "time_period" : "last_week" # Or last_day or last_year, see the website for more params
}

# retrieve the search results as JSON
result = serpwow.get_json(params)




file_data = open("report.txt","w", encoding="utf-8")
description_urls_file = open("description_urls.txt", "w", encoding="utf-8")

for i in result["organic_results"]:
    urls = find(i["snippet"])
    data = \
        f"""
            -------------------------------------
        Title: {i["title"]}
        Url: {i["link"]}
        Description [Only Found Urls]: {urls}
        Date: {i["rich_snippet"]["top"]["extensions"][0]}
        Author: {i["rich_snippet"]["top"]["extensions"][1]}
        \n
        """
    file_data.write(str(data))
    if len(urls) > 0:
        description_urls_file.write(f"{urls}\n")
        try:
            for x in urls:
                params = {
                    "q": f"{x}"
                }
                # retrieve the search results as JSON
                result = serpwow.get_json(params)
                if  len(result["organic_results"]) > 0:
                    for z in result["organic_results"]:
                        urls = find(z["snippet"])
                        data = \
                            f"""
                                    -------------------------------------
                                Query: {result["search_parameters"]["q"]}
                                Title: {z["title"]}
                                Url: {z["link"]}
                                Domain: {z["domain"]}
                                Description: {z["snippet"]}
                                More Urls: {urls}
                                \n
                                """
                        file_data.write(str(data))
                        description_urls_file.write(f"{urls}\n")
        except:
            continue

description_urls_file.close()
file_data.close()
