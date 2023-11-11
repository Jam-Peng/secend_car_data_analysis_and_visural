from scraping_tools import get_chrome, get_element, time
from bs4 import BeautifulSoup
from threading import Thread
from queue import Queue
import pymysql, os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
sql_host = os.getenv('SQL_HOST')
sql_port = eval(os.getenv('SQL_PORT'))
sql_uesr = os.getenv('SQL_USER')
sql_pwd = os.getenv('SQL_PWD')

# 取得當前頁面所有資料
def get_car_data(url, page):
    global model, cc 
    chrome = None
    
    datas = []
    try:
        chrome = get_chrome(url, hide=True)
        if chrome is not None:
            soup = BeautifulSoup(chrome.page_source, 'lxml')
            cars = soup.find(id="search-result").find_all('a')
            print(f'第{page}頁 - 共{len(cars)}筆資料')

            for car in cars:
                data = []
                
                titles = car.find('span',class_="ib-it-text").text.split()
                # 重組titles資料 - 車款 model / 排氣量 cc
                cc = titles[-1]
                model = ' '.join(titles[:-2])

                price, year, km = car.find('div',class_="ib-row ib-extra").text.split()
                county = car.find('span',class_="ib-ii-item").text.strip()
                view = car.find('div',class_="ib-info-im").text.split()[-1].split('次')[0]
                link = 'https://auto.8891.com.tw'+car.get('href')
                img_link = car.find('img').get('data-src')

                data = [year, county, model, cc, price, km, view, link, img_link]
                datas.append(data)
        else:
            print('取得 chrome 失敗')
    except Exception as e:
        print(e)    
    finally:
        if chrome is not None:
            chrome.quit()

    if len(datas) == 0:
        print('取得資料失敗')
    else:
        q.put(datas)

    return datas

# 開啟資料庫
def open_db():
    global conn, cursor
    try:
        conn=pymysql.connect(host=sql_host, port=sql_port,\
                             user=sql_uesr, password=sql_pwd, db=db_name, charset='utf8mb4')
        cursor=conn.cursor()
    except Exception as e:
        print(e)

# 建立資料表
def create_table():
    car_table=f"""
    CREATE TABLE if not exists {table_name}(
        year int,
        county varchar(128),
        model varchar(128),
        cc varchar(128),
        price varchar(128),
        km varchar(128),
        view varchar(128),
        link varchar(255),
        img_link varchar(255)
    )"""
    cursor.execute(car_table)
    conn.commit()

# 寫入資料庫
def insert_data_tosql(data):
    try:
        insert_data=f"""
        INSERT INTO {table_name} VALUES({data[0]}, '{data[1]}', '{data[2]}', '{data[3]}',\
                                        '{data[4]}', '{data[5]}', '{data[6]}', '{data[7]}', '{data[8]}')"""
        
        cursor.execute(insert_data)
        conn.commit()
    except Exception as e:
        print(e)

# 檢查資料是否在資料庫
def data_exists(year, model, link):
    try:
        select_data=f"""SELECT * FROM {table_name} WHERE year='{year}' AND model='{model}' AND link='{link}'"""
        cursor.execute(select_data)
        result=cursor.fetchall()
        if len(result) != 0:
            return True
    except Exception as e:
        print(e)
    return False

# 儲存資料到資料庫
def save_data_tosql():
    global conn, cursor, df_datas
    try:
        open_db()
        create_table()

        counter = 0
        print('資料寫入中....')
        for data in df_datas:
            if not data_exists(data[0], data[2], data[-2]):
                insert_data_tosql(data)
                counter += 1

        time.sleep(2)
        df_datas = []
    except Exception as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()
            print('資料庫關閉')


if __name__=='__main__':
# ================================================================== #
    threads = []
    max_thread = 10       
    counter = 0
    datas = []
    q = Queue()
    model, cc = None, None

# ==========================  查詢車款頁數  ========================== #
    key = input('請輸入要查詢的車款：')
    index_url = 'https://auto.8891.com.tw/'

    chrome = get_chrome(index_url)
    time.sleep(2)

    element = get_element(chrome, xpath='/html/body/div[5]/div/div[4]/div/div[1]/div[2]/form/div[1]/input')
    element.clear()
    time.sleep(2)
    element.send_keys(f'{key}\n')
    time.sleep(2)

    soup = BeautifulSoup(chrome.page_source, 'lxml')
    pages=eval(soup.find_all('button',class_="_page_1skvm_295")[-2].text)
    print(f'{key}車款，共{pages}頁')

    chrome.quit()

# ==========================  進行資料查找  ========================== #
    if input('是否要執行？(y/n)')=='y':
        print('資料加載中，請稍後....')
        for page in range(1, pages+1):
            page_url = f'https://auto.8891.com.tw/?page={page}&key={key}'

            threads.append(Thread(target=get_car_data, args=(page_url, page)))

            counter += 1
            if counter % max_thread == 0:
                for t in threads:
                    t.start()

                for t in threads:
                    t.join()

                threads = []
                counter = 0
            time.sleep(2)

    for t in threads:
        t.start()

    for t in threads:
        t.join()        

# ============================  輸出值  ============================ #      
    print(f'共有{q.qsize()}筆資料') 

    for i in range(q.qsize()):
        datas.extend(q.get())

# ===========================  清理資料  =========================== # 
    columns = 'year,county,model,cc,price,km,view,link,img_link'.split(',')
    df = pd.DataFrame(datas, columns=columns)

    # 更換年為數字型別 
    df['year']=df['year'].apply(lambda x:eval(x.replace('年','').replace('前','')))

    # 刪除價錢為電洽的資料
    df.drop(df[df['price']=='電洽'].index, inplace=True)

    df=df.sort_values('year')


# =======================  資料儲存到資料庫  ======================= #
    conn, cursor = None, None
    db_name = 'pre_owned_car'
    table_name = key

    df_datas = []
    df_datas.extend(df.values)
    save_data_tosql()
    
 