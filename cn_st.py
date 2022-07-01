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
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

firefoxOptions = Options()
firefoxOptions.add_argument("--headless")
service = Service(GeckoDriverManager().install())

df_cn=pd.read_csv('df_cn.csv')
df_cn2=pd.read_csv('parcial.csv')
df_cn2.drop('Unnamed: 0',axis=1,inplace=True)
# st.write(df_cn2,unsafe_allow_html=True)

if st.button('Clica para atualizar sa porra'):
    st.write('espera um cado fião') 
    driver = webdriver.Firefox(options=firefoxOptions,
    service=service)
    # driver = webdriver.Chrome()
   
    driver.get("https://lol.qq.com/tft/#/rank/tier")
    # driver.implicitly_wait(20)


    df_cn=pd.DataFrame([],columns=['Nick','PDL','Jogos','link'])
    for i in range(0,10):
        cn_list=driver.find_elements(by=By.CLASS_NAME,value='nickname')
        cn_list2=cn_list[0].text.split('%\n')
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
        url_list=driver.find_elements(by=By.CLASS_NAME,value='nickname')
        urls=[]
        for i in range(0,10):
            url_list[i].click()
            urls.append(driver.current_url)
            driver.back()

        st.write(cn_list3)                           
        df_prev=pd.DataFrame(cn_list3,columns=['Nick','PDL','Jogos'])
        df_prev['link'] = urls
        df_cn=pd.concat([df_cn,df_prev])
        
        
        
       
        
        next_page=driver.find_elements(by=By.CLASS_NAME,value='page-item')
       
        next_page[-2].click()
    df_cn.reset_index(drop=True,inplace=True)
    df_cn.index+=1
    df_cn.to_csv('df.cn.csv',index=False)
    st.dataframe(df_cn)
    @st.cache
    def convert_df(df):
       return df.to_csv().encode('utf-8')


    csv = convert_df(df_cn)

    st.download_button(
       "Press to Download",
       csv,
       "file.csv",
       "text/csv",
       key='download-csv'
    )
