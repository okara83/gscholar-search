#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module searches and parses google scholar search results
 and returns asscociated publications titles and their URLS in an
 structured output format specified by the user.

Example:
        query_list = ['Sehanobish Corzo Kara', 'Learning potentials of
        quantum systems using deep neural networks', '2006.13297' ]

        queryObj = ScholarListener()
        queryObj.querylist = query_list

        # default query result:
        queryObj.scholar_search() #outputs a json file with default title incorporating time and date and query strings
                                  #DOES NOT return any object (list,dict,etc) by default

        # save csv(s) of query results:
        queryObj.save_to_csv = True #this is False by default
        queryObj.scholar_search() #outputs n output csv files each titled as their respective query strings
                                  #DOES NOT return any object (list,dict,etc) by default

        queryObj.return_output_object=True
        queryObj.scholar_search() #Returns results as dict object (i.e. `output_dict`) along with any save options
                                   specified by user

Attributes:
    query_list (list): list of query terms to search
    save_to_json (bool)= Option to save results as json, default = True
    save_to_csv (bool)= Option to save results as csv, default = False
    return_output_object (bool) = Option to output results as dict, default = False

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

"""
__version__ = '0.1'
__author__ = 'Onur Kara'
__email__ = 'okara83@gmail.com'

from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup
import json

class ScholarListener:
    def __init__(self,query_list=None,save_to_json=True,save_to_csv=False,return_output_object=False):
        self.query_list = query_list
        self.return_output_object = return_output_object
        self.save_to_json = save_to_json
        self.save_to_csv = save_to_csv

    def scholar_search(self):
        apikey = "7ff2bdcee22d088ecbb5a04c1bf86246bb70ab43a6e69c7cb5984154b3234a74"
        scraped_time = datetime.now().strftime("%h-%d-%Y")
        output = {}
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
        ql = self.query_list
        for query in ql:
            output_list = []
            url_1 = f'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q={query}&btnG='
            url_2 = f'https://scholar.google.com/scholar?start=10&q={query}&hl=en&as_sdt=0,31'
            url_3 = f'https://scholar.google.com/scholar?start=20&q={query}&hl=en&as_sdt=0,31'
            urls = [url_1,url_2,url_3] # first three search result pages
            for url in urls:
                response=requests.get(url,headers=headers)
                statuscode=response.status_code
                if statuscode != 200:
                    raise Exception(f"requests response for url query: {url} returned {statuscode} response -- check google hasn't blocked your IP")
                    return
                soup=BeautifulSoup(response.content,'lxml')
                links = soup.find_all("h3", class_="gs_rt")
                print(links)
                for j in links:
                    the_url = re.search("href=\"(.*?)\"\s",str(j),re.DOTALL)[1]
                    output_list.append(the_url)
                    prin(the_url)
            output[query] = output_list

        #object output and saving results
        if self.save_to_json == True:
            name_concat_queries = "_".join(self.query_list)
            with open(f"{name_concat_queries}--{scraped_time}","w") as file:
                json.dump(output,file)

        if self.save_to_csv == True:
            import pandas as pd
            for l in output.keys():
                df = pd.DataFrame.from_dict(output[l])
                df.to_csv(f"{l}.csv")

        if self.return_output_object == True:
            return output
        else:
            return
