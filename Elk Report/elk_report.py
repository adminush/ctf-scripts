import re
import time
import requests
import sys, requests, urllib
from selenium import webdriver
import win32com.client as win32
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def DashboardReport():
    login = f"http://{domain}"
    driver = webdriver.Firefox()
    driver.get(login)
    time.sleep(6)
    driver.find_element("name", "username").send_keys(creds[0])
    time.sleep(1)
    driver.find_element("name", "password").send_keys(creds[1])
    #driver.find_element("type", "submit").click()
    driver.find_element(By.CSS_SELECTOR, '[data-test-subj="loginSubmit"]').click()
    time.sleep(6)
    driver.get(f"http://{domain}/app/dashboards#/view/987203d0-c011-11ee-9072-2b4e7ef329f0?_g=(filters:!())")
    time.sleep(6)
    driver.find_element(By.CSS_SELECTOR, '[data-test-subj="dashboardFullScreenMode"]').click()
    driver.fullscreen_window()
    time.sleep(15)
    driver.find_element(By.TAG_NAME, "body").screenshot("test1.png")
    time.sleep(1)
    driver.close()

def TxtReport():
    requests.packages.urllib3.disable_warnings()

    file = open("users.txt", "w")

    searchUrl = "https://***.***.***.***/******/_search?pretty" # elk api search
    # Запрос по выгрузке уникальных УЗ, которые подключались по VPN из-за границы в течении недели
    searchData = '{"query": {"bool": {"must_not": [ {"match": {"geo.country_name": "***"}}],"must": [ {"match": {"***": "***"}}], "filter": [ {"range": {"@timestamp": {"gte": "now-7d/d", "lte": "now/d"}}}]}}, "aggs": {"user": {"terms": {"field": "user.keyword","size": 4000}}}, "_source": ["user", "geo.country_name"]}' # request to api elk
    searchHeaders = {"Content-Type": "application/json"}

    requestApiElasticUsers = requests.get(searchUrl, auth=(apiCreds[0], apiCreds[1]), verify=False,
                                          data=searchData,
                                          headers=searchHeaders) # auth api elk
    requestResultUser = requestApiElasticUsers.text

    ip = []
    users = []
    lines = []
    lines2 = []
    inputs = []
    country = []
    city = ["-"] * 1000

    lines = requestResultUser.split('\n')

    file.write("УЗ, Количество действий, Последний IP адрес, Страна, Город\n")

    for i in range(len(lines)):

        regularUserUniq = re.search(r'(?<=(["]|[(]))(([A-z]{1,4}[.][A-z]{1,})|([A-z]{1,}[.][A-z]{1,4})|([A-z]{3,})|(sd[\]{1,2}[A-z]{1,4}[.][A-z]{1,})|([A-z]{1,4}[.][A-z]{1,}[@]\S{1,}))(?=(["]{1,3}[,])|([)]["][,]))', lines[i])
        regularUserInputs = re.search(r'(?<=[\"]doc_count[\"] \: ).{1,}', lines[i])

        if (regularUserUniq != None):
            users.append(regularUserUniq[0])
        if (regularUserInputs != None):
            inputs.append(regularUserInputs[0])

    for i in range(len(users)):

        searchData2 = '{"query": {"bool": {"must":[{"match": {"user": "' + users[
            i] + '"}},{"match": {"***": "***"}}],"must_not":[{"match": {"geo.country_name": "***"}}]}},"_source": ["geo.country_name", "geo.city_name", "source"],"size": 1}'

        requestResultMoreInfo = requests.get(searchUrl, auth=(apiCreds[0], apiCreds[1]), verify=False,
                                             data=searchData2,
                                             headers=searchHeaders)
        
        requestResultUser = requestResultMoreInfo.text
        
        lines2 = requestResultUser.split('\n')

        for j in range(len(lines2)):
            
            regularUserIp = re.search(r'\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}', lines2[j])
            regularUserCountry = re.search(r'(?<=["]country_name["]\s[:]\s["])[A-z\']{1,}', lines2[j])
            regularUserCity = re.search(r'(?<=["]city_name["]\s[:]\s["])[A-z\']{1,}', lines2[j])

            if (regularUserIp != None):
                ip.append(regularUserIp[0])
            if (regularUserCountry != None):
                country.append(regularUserCountry[0])
            if (regularUserCity != None):
                city[i] = regularUserCity[0]

        file.write(users[i] + "," + inputs[i] + "," + ip[i] + "," + country[i] + "," + city[i] + "\n")

    file.close()

def EmailShare():
    file_path = "C:\\***\\" # path for files

    olApp = win32.Dispatch('Outlook.Application')
    olNS = olApp.GetNameSpace('MAPI')

    # construct email item object
    mailItem = olApp.CreateItem(0)
    mailItem.Subject = 'Отчет Сервера мониторинга ELK'

    mailItem.BodyFormat = 1
    mailItem.HTMLBody = "<html><body><p>ELK (Elasticsearch)</p><img src='cid:test1.png'></body></html>"
    mailItem.Attachments.Add(file_path + "test1.png")
    mailItem.Attachments.Add(file_path + "users.txt")
    mailItem.To = '***@***.***' # mail on Outlook
    mailItem.Sensitivity = 2
    mailItem.Display()
    mailItem.Save()
    mailItem.Send()

if __name__ == "__main__":
    domain = "***.***.***.***"
    apiCreds = ["***", "***"] # elasticsearch api creds
    creds = ["***", "***"] # kibana creds
    DashboardReport()
    TxtReport()
    EmailShare()
