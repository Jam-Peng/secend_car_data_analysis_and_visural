
<div align="center">

# 國產二手車資料分析及視覺化
</div>

###  Preview :

<table width="100%"> 
<tr>
<td width="50%">      
&nbsp; 
<br>
<img src="./public/project_home.jpg">
</td> 
</tr>
</table>

#

## 專案說明
- 使用爬蟲與視覺化工具取得 8891 中古車網資料，將資料做清理與整合並製成圖表做分析。
- <a href="https://drive.google.com/file/d/12MLlj9-V30H9OGr7XbKIy55qCCZtEmCs/view?usp=sharing" target="_blank">線上專案說明</a>

### 分析動機
在二手車市場比較每個車款的售價和受大眾關注的車輛從中找符合預算的自用車。<br>

### 資料來源
8891 中古車網。<br>
https://auto.8891.com.tw/<br>


#
### 使用環境
- `Python3.9`。

### 使用技術
- 8891 中古車網是一個動態的網頁，所以選用 `selenium` 撰寫腳本自動模擬使用者操作取的所有相關資料。
- 使用 `threading` 多線程編程工具，同時執行取得多筆資料提高效率，節省時間。
- 使用 `queue` 套件在執行多線程的環境中將資料做存放與取出。


### 使用套件
- `selenium`
- `bs4`
- `pandas`
- `nunpy`
- `pymysql`
- `dotenv`
- `threading`
- `queue`
- `matplotlib`
- `os`
- `re`
- `time`


### 工具使用 - my_app file
- `scraping_tools.py` - 執行自動化開啟 chrome 瀏覽器。
- `get_data_tosql.py` - 爬取資料後進行第一次的資料整理並儲存到資料庫中。
- `get_sql_tocsv.py` - 從資料庫中取回需要的資料，進行第二次資料清理與整合，將資料儲存成 csv 檔方便後續處理資料使用和查閱。
