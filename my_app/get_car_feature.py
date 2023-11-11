from scraping_tools import get_chrome
from bs4 import BeautifulSoup
import time, os
import pandas as pd


# 當前頁面的評價
def get_car_feature(url):
    chrome=None
    datas=[]
    try:
        chrome=get_chrome(url, hide=True)
        if chrome is not None:
            soup=BeautifulSoup(chrome.page_source,'lxml')
            ul=soup.find(id="ratingComment")
            lis=ul.find_all('li',class_="nsc-list-li clearfix")[:-1]

            for li in lis:
                data=[]
                for td in li.find('table',class_="nsc-table-box").find('tbody').find_all('td'):
                    try:
                        data.append(eval(td.text.split('：')[1]))
                    except:
                        data.append(None)
                datas.append(data)
            return datas
        else:
            print('chrome 取得失敗')
    except Exception as e:
        print(e)
    finally:
        if chrome is not None:
            chrome.quit()
    return datas


# 總頁數
def get_pages(url):
    chrome=None
    try:
        chrome=get_chrome(url)
        soup=BeautifulSoup(chrome.page_source,'lxml')
        ul=soup.find(id="ratingComment")
        li=ul.find_all('li',class_="nsc-list-li clearfix")[-1]
        pages=eval(li.find('span',class_="pc-tp-nm").text)
        
        return pages
    except Exception as e:
        print(e)
    finally:
        if chrome is not None:
            chrome.quit()


# 建立目錄將資料儲存指定路徑
def makeDirs(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            print('建立新目錄,進行資料抓取中...')
        else:
            print('目錄已存在,進行資料抓取中...')
    except Exception as e:
        print(e)


# 取得每一頁score 儲存 csv
def save_csv(url, pages):
    datas=[]
    for page in range(1,pages+1):
        page_url=f'{url}?page={page}'
        data=get_car_feature(page_url)
        print(f'第{page}頁 - 有{len(data)}筆資料')
        
        if len(data) != 0:
            datas += data
        time.sleep(1)
        
    df=pd.DataFrame(datas, columns=columns)
    df.to_csv(f'{dir_path}/{file_name}.csv',encoding='utf-8-sig')
    print('檔案儲存成功')


if __name__=='__main__':
    columns=['內裝','外觀','操控','動力','空間','舒適度']
    
    toyota_url='https://c.8891.com.tw/toyota/corolla-altis/Comment.html'
    pages=get_pages(toyota_url)
    time.sleep(3)
    file_name='toyota_scores'
    dir_path = '../feature_score'
    makeDirs(dir_path)
    save_csv(toyota_url, pages)


    honda_url='https://c.8891.com.tw/honda/civic/Comment.html'
    pages=get_pages(honda_url)
    time.sleep(3)
    file_name='honda_scores'
    dir_path = '../feature_score'
    makeDirs(dir_path)
    save_csv(honda_url, pages)


