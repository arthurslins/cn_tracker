import streamlit as st
import pandas as pd
import numpy as np
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager

firefoxOptions = Options()
firefoxOptions.add_argument("--headless")
service = Service(GeckoDriverManager().install())

df_cn=pd.read_csv('df_cn.csv')

if st.button('Say hello'):
    st.write('Why hello there') 
    driver = webdriver.Firefox(
    options=firefoxOptions,
    service=service,
    )
    driver.get("https://lol.qq.com/tft/#/rank/tier")
    driver.implicitly_wait(20)
    df_cn=pd.DataFrame([],columns=['Nick','PDL','Jogos'])
    for i in range(0,5):
        cn_list=driver.find_element_by_xpath('//*[@id="appMain"]/div[1]/div/div[2]/div[2]')
        cn_list2=cn_list.text.split('%\n')
        del cn_list2[1::2]
        cn_list3=[]
        for i in range(0,len(cn_list2)):
            cn_list3.append(cn_list2[i].split('\n'))

        for i in range(0,10):
            if cn_list3[i][0].isdigit():
                del cn_list3[i][0]

        for i in range(0,len(cn_list3)):
       
            del cn_list3[i][1]
            del cn_list3[i][3]
        df_cn=pd.concat([df_cn,pd.DataFrame(cn_list3,columns=['Nick','PDL','Jogos'])])
        df_cn.to_csv('df.cn.csv',index=False)
       
        st.dataframe(df_cn)
        next_page=driver.find_element_by_xpath('//*[@id="appMain"]/div[1]/div/div[2]/div[3]/ul/li[9]')
       
        next_page.click()
