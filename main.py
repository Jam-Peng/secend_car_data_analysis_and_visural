import pandas as pd
import numpy as np
import re, os
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties as font
from datetime import datetime

current_date = datetime.now().strftime('%Y-%m-%d')
font_set=font(fname='./font_type/TaipeiSansTCBeta-Regular.ttf')

# 資料預處理
def get_df(csv_path):
    try:
        df=pd.read_csv(csv_path, index_col=0)
    
        df=df.drop(['連結','圖片連結'],axis=1)
        df.columns=['縣市', '車款', '排氣量(L)', '售價(萬)', '里程數(km)', '瀏覽數(次)']
        df['排氣量(L)']=df['排氣量(L)'].apply(lambda x: eval(x.replace('L','').replace('以下','').replace('以上','')))
        df['售價(萬)']=df['售價(萬)'].apply(lambda x: int(eval(x.replace('萬',''))*10000))
        df['里程數(km)']=df['里程數(km)'].apply(lambda x: (x.replace('km','')))
        regex=r'\d{1,}\.\d\w'
        kms=[]
        counter = 0
        for km in df['里程數(km)'].values:
            match=re.fullmatch(regex, km)
            if match != None:
                kms.append(int(eval(match.group().replace('萬',''))*10000))
            else:
                kms.append(eval(km))
            counter += 1
        df['里程數(km)']=kms
        
        file_name=df['車款'].values[0].split()[0]
        if not os.path.exists(f'{current_date}_{file_name}.csv'):
            df.to_csv(f'{current_date}_{file_name}.csv', encoding='utf-8-sig')
        return df
    except Exception as e:
        print(e)

### ========== 近十年 Toyota、Honda、Ford 平均價格趨勢圖 ========== ###
def price_avg():
    try:
        years=list(map(str, toyota_df.loc['2012':'2023'].index.unique()))
        
        all_price_means=[[all_df[df].loc[year:year]['售價(萬)'].mean()//10000 for year in years]\
                     for i,df in enumerate(all_df.keys())]
        
        plt.figure(figsize=(12,6))
        font_set=font(fname='./font_type/TaipeiSansTCBeta-Regular.ttf',size=15)
        colors, labels=['#09c','#ff6347','#3cb371'], ['Toyota','Honda','Ford']
        for i in range(len(all_price_means)):
            plt.plot(years, all_price_means[i], marker='o',linestyle='--',color=colors[i], label=labels[i])
    
        plt.grid(axis='y', alpha=.2)
        plt.title('每年總平均價格趨勢(近十年)', fontproperties=font_set, pad=10, fontsize=15)
        plt.xlabel('年份(車齡)', fontproperties=font_set, fontsize=13)
        plt.ylabel('平均售價(萬)', rotation=0, ha='right', fontproperties=font_set, fontsize=13)
        plt.xticks(np.arange(0,len(years),1))
        plt.yticks(np.linspace(0, 140, 15))
        plt.xlim(0, len(years)-1)
        plt.ylim(0, 140)
        
        plt.legend(loc='best',prop=font_set)
        # plt.savefig('近十年平均價格趨勢', bbox_inches='tight')
        plt.show()
    except Exception as e:
        print(e)

### ========== 30~50萬區間車款的最高、最低與平均售價比 ========== ###
def price_budget():
    try:    
        # 取得 Toyota、Honda、Ford 全部車款(不重複)
        car_models=[price_df['車款'].unique() for i,price_df in enumerate(all_price_dfs)]
    
        # 取得 Toyota、Honda、Ford 最高、最低與平均售價
        t_h_price, t_m_price, t_l_price =[],[],[]
        h_h_price, h_m_price, h_l_price =[],[],[]
        f_h_price, f_m_price, f_l_price =[],[],[]
        t_prices,h_prices,f_prices=[],[],[]
        for i,df in enumerate(all_price_dfs):
            for j,car_model in enumerate(df['車款'].unique()):
                if i == 0:
                    t_h_price.append(np.around(all_price_dfs[i][all_price_dfs[i]['車款']==car_model]['售價(萬)'].max()))
                    t_m_price.append(np.around(all_price_dfs[i][all_price_dfs[i]['車款']==car_model]['售價(萬)'].mean()))
                    t_l_price.append(np.around(all_price_dfs[i][all_price_dfs[i]['車款']==car_model]['售價(萬)'].min()))
                    t_prices.append(t_h_price)
                    t_prices.append(t_m_price)
                    t_prices.append(t_l_price)
                elif i == 1:
                    h_h_price.append(np.around(all_price_dfs[i][all_price_dfs[i]['車款']==car_model]['售價(萬)'].max()))
                    h_m_price.append(np.around(all_price_dfs[i][all_price_dfs[i]['車款']==car_model]['售價(萬)'].mean()))
                    h_l_price.append(np.around(all_price_dfs[i][all_price_dfs[i]['車款']==car_model]['售價(萬)'].min()))
                    h_prices.append(h_h_price)
                    h_prices.append(h_m_price)
                    h_prices.append(h_l_price)
                else:
                    f_h_price.append(np.around(all_price_dfs[i][all_price_dfs[i]['車款']==car_model]['售價(萬)'].max()))
                    f_m_price.append(np.around(all_price_dfs[i][all_price_dfs[i]['車款']==car_model]['售價(萬)'].mean()))
                    f_l_price.append(np.around(all_price_dfs[i][all_price_dfs[i]['車款']==car_model]['售價(萬)'].min()))
                    f_prices.append(f_h_price)
                    f_prices.append(f_m_price)
                    f_prices.append(f_l_price)
    
        # 重組車款的刻度 
        for i,cars in enumerate(car_models):
            if i == 0:
                t_ytick=[' '.join(car.split()[1:]) for car in cars]
            elif i == 1:
                h_ytick=[' '.join(car.split()[1:]) for car in cars]
            else:
                f_ytick=[' '.join(car.split()[1:]) for car in cars]
    
        # 繪圖
        labels=['最高','平均','最低']
        colors=['#09c','#ff6347','#3cb371']
        
        plt.figure(figsize=(20,16))
        font_set=font(fname='./font_type/TaipeiSansTCBeta-Regular.ttf',size=16)
        for i in range(3):
            plt.scatter(t_prices[i], t_ytick, s=90, color=colors[i], label=labels[i])
        
        plt.grid(axis='both', alpha=.4)
        plt.title('Toyota 30~50萬區間車款的最高、最低與平均售價比', fontproperties=font_set, pad=12, fontsize=20)
        plt.xlabel('售價(萬)', fontproperties=font_set, fontsize=17)
        plt.ylabel('車款', rotation=0, ha='right', fontproperties=font_set, fontsize=17)
        plt.xticks(np.arange(300000,510000,20000),fontsize=15)
        plt.yticks(fontsize=15)
        plt.xlim(300000-20000,515000)
        plt.ylim(-1, len(car_models[0])-.5)
        plt.legend(loc='best',prop=font_set)
        # plt.savefig('Toyota 30~50萬區間車款的最高、最低與平均售價比', bbox_inches='tight')
        
        plt.figure(figsize=(20,10))
        font_set=font(fname='./font_type/TaipeiSansTCBeta-Regular.ttf',size=16)
        for i in range(3):
            plt.scatter(h_prices[i], h_ytick, s=90, color=colors[i], label=labels[i])
        
        plt.grid(axis='both', alpha=.4)
        plt.title('Honda 30~50萬區間車款的最高、最低與平均售價比', fontproperties=font_set, pad=12, fontsize=20)
        plt.xlabel('售價(萬)', fontproperties=font_set, fontsize=17)
        plt.ylabel('車款', rotation=0, ha='right', fontproperties=font_set, fontsize=17)
        plt.xticks(np.arange(300000,510000,20000),fontsize=15)
        plt.yticks(fontsize=15)
        plt.xlim(300000-20000,515000)
        plt.ylim(-1, len(car_models[1])-.5)
        plt.legend(loc='best',prop=font_set)
        # plt.savefig('Honda 30~50萬區間車款的最高、最低與平均售價比', bbox_inches='tight')
        
        plt.figure(figsize=(20,10))
        font_set=font(fname='./font_type/TaipeiSansTCBeta-Regular.ttf',size=16)
        for i in range(3):
            plt.scatter(f_prices[i], f_ytick, s=90, color=colors[i], label=labels[i])
        
        plt.grid(axis='both', alpha=.4)
        plt.title('Ford 30~50萬區間車款的最高、最低與平均售價比', fontproperties=font_set, pad=12, fontsize=20)
        plt.xlabel('售價(萬)', fontproperties=font_set, fontsize=17)
        plt.ylabel('車款', rotation=0, ha='right', fontproperties=font_set, fontsize=17)
        plt.xticks(np.arange(300000,510000,20000),fontsize=15)
        plt.yticks(fontsize=15,fontproperties=font_set)
        plt.xlim(300000-20000,515000)
        plt.ylim(-1, len(car_models[2])-.5)
        plt.legend(loc='best',prop=font_set)
        
        # plt.savefig('Ford 30~50萬區間車款的最高、最低與平均售價比', bbox_inches='tight')
        plt.show()
    except Exception as e:
        print(e)

### ========== 10-15萬公里數的前5款數量(30~50萬區間) ========== ###
def km_amount():
    try:    
        # 三個品牌里程數10-15萬的車款
        all_km_cars=[dfs[dfs['里程數(km)'].between(100000,150000)]['車款'].unique() for i,dfs in enumerate(all_price_dfs)]
    
        # 統計三個品牌10-15萬里程數的前5車款
        t_km_amount,h_km_amount,f_km_amount=[],[],[]
        for i,dfs in enumerate(all_price_dfs):
            for car in all_km_cars[i][:5]:
                if i == 0:
                    t_km_amount.append(len(dfs[dfs['車款']==car]))
                elif i == 1:
                    h_km_amount.append(len(dfs[dfs['車款']==car]))
                else:
                    f_km_amount.append(len(dfs[dfs['車款']==car]))
    
        # 繪圖
        fig=plt.figure(figsize=(21,20))
        font_set=font(fname='./font_type/TaipeiSansTCBeta-Regular.ttf',size=14)
        colors=['#dc143c','#ffd700','#3cb371','#1e90ff','#ff69b4'][::-1]
        
        for i in range(3):
            if i == 0:
                fig.add_subplot(311)
                plt.barh(all_km_cars[i][:5], t_km_amount,  color=colors, label=t_km_amount, height=.5)
                plt.title('Toyota 10-15(萬)里程數的前 5 款車數量比', fontproperties=font_set, pad=12, fontsize=21)
            elif i == 1:
                fig.add_subplot(312)
                plt.barh(all_km_cars[i][:5][::-1], h_km_amount[::-1],  color=colors, label=h_km_amount, height=.5)
                plt.title('Honda 10-15(萬)里程數的前 5 款車數量比', fontproperties=font_set, pad=12, fontsize=21)
            else:
                fig.add_subplot(313)
                plt.barh(all_km_cars[i][:5], f_km_amount,  color=colors, label=f_km_amount, height=.5)
                plt.title('Ford 10-15(萬)里程數的前 5 款車數量比', fontproperties=font_set, pad=12, fontsize=21)
        
            plt.grid(axis='x', alpha=.4)
            
            plt.xlabel('數量(輛)', fontproperties=font_set, fontsize=19)
            plt.ylabel('車款', rotation=0, ha='right', fontproperties=font_set, fontsize=19)
            plt.xticks(fontsize=15)
            plt.yticks(fontsize=15,fontproperties=font_set)
            plt.ylim(-.7, len(all_km_cars[0][:5])-.3)
            plt.subplots_adjust(wspace=.2, hspace=.5)
            plt.legend(loc='best',prop=font_set)
        # plt.savefig('三個品牌里程數10-15(萬)的前5款數量(30~50萬)', bbox_inches='tight')
        plt.show()
    except Exception as e:
        print(e)


### ========== 10-15(萬)里程數中1.8cc的車款數量 ========== ###
def cc_amount():
    try:
        # 找出符合的所有車款
        all_cc_cars=[need_cc_df['車款'].unique() for i,need_cc_df in enumerate(need_cc_dfs)]
        
        # 統計符合的每個車款數量
        t_cc_amount,h_cc_amount=[],[]
        for i,need_cc_df in enumerate(need_cc_dfs):
            for cc_car in all_cc_cars[i]:
                if i == 0:
                    t_cc_amount.append(len(need_cc_df[need_cc_df['車款']==cc_car]))
                else:
                    h_cc_amount.append(len(need_cc_df[need_cc_df['車款']==cc_car]))
        # 繪圖
        fig=plt.figure(figsize=(12,10))
        font_set=font(fname='./font_type/TaipeiSansTCBeta-Regular.ttf',size=12)
        colors=['#dc143c','#ffd700','#3cb371','#1e90ff','#9932cc','#ff69b4'][::-1]
        colors2=['#dc143c','#ffd700','#3cb371'][::-1]
        
        for i in range(2):
            if i == 0:
                fig.add_subplot(211)
                plt.barh(all_cc_cars[i][::-1], t_cc_amount[::-1],  color=colors, label=t_cc_amount[::-1], height=.5)
                plt.title('Toyota 10-15(萬)里程數中 1.8cc 的車款數量', fontproperties=font_set, pad=12, fontsize=15)
            else:
                fig.add_subplot(212)
                plt.barh(all_cc_cars[i][::-1], h_cc_amount[::-1],  color=colors2, label=h_cc_amount[::-1], height=.2)
                plt.title('Honda 10-15(萬)里程數中 1.8cc 的車款數量', fontproperties=font_set, pad=12, fontsize=15)
                
                
            plt.grid(axis='x', alpha=.4)
            plt.xlabel('數量(輛)', fontproperties=font_set, fontsize=13)
            plt.ylabel('車款', rotation=0, ha='right', fontproperties=font_set, fontsize=13)
            plt.xticks(fontsize=13)
            plt.yticks(fontsize=13, fontproperties=font_set)
            plt.ylim(-.7, len(all_cc_cars[i])-.3)
        
            plt.legend(loc='best',prop=font_set)
            
        plt.subplots_adjust(hspace=.3)
        # plt.savefig('10-15(萬)里程數中排氣量符合需求的車款數量', bbox_inches='tight')
        plt.show()
    except Exception as e:
        print(e)


### ========== 根據以上條件找到 toyota 和 honda 各有一款車款在符合需求上 ========== ###
def area_amount():
    try: 
        # 取得 Toyota Corolla Altis 和 Honda Civic 另存 Dataframe
        result_car_dfs=[[]]*2
        for i,cc_df in enumerate(need_cc_dfs):
            if i==0:
                result_car_dfs[i]=cc_df[cc_df['車款']=='Toyota Corolla Altis']
            else:
                result_car_dfs[i]=cc_df[cc_df['車款']=='Honda Civic']
        
        # 找出兩款車的所在縣市
        countys=[result_car_df['縣市'].unique() for result_car_df in result_car_dfs]
        
        # 統計兩台車每個縣市的數量
        for i,result_car_df in enumerate(result_car_dfs):
            if i==0:
                t_county_amounts=[len(result_car_df[result_car_df['縣市']==county]) for j,county in enumerate(countys[i])]
            else:
                h_county_amounts=[len(result_car_df[result_car_df['縣市']==county]) for j,county in enumerate(countys[i])]
        
        # 將縣市分區域重新統計
        # 北北基宜
        t_nn_count=t_county_amounts[0]+t_county_amounts[5]+t_county_amounts[11]+t_county_amounts[13]
        # 桃竹苗
        t_ns_count=t_county_amounts[4]+t_county_amounts[9]
        # 中彰投
        t_cn_count=t_county_amounts[2]+t_county_amounts[7]+t_county_amounts[14]
        # 雲嘉南
        t_cs_count=t_county_amounts[6]+t_county_amounts[8]+t_county_amounts[10]+t_county_amounts[12]
        # 高屏
        t_s_count=t_county_amounts[1]+t_county_amounts[3]
        new_t_counts=[t_nn_count, t_ns_count, t_cn_count, t_cs_count, t_s_count]
        
        # 北北基宜
        h_nn_count=h_county_amounts[1]+t_county_amounts[4]
        # 桃竹苗
        h_ns_count=h_county_amounts[3]+h_county_amounts[5]+h_county_amounts[8]+h_county_amounts[10]
        # 中彰投
        h_cn_count=h_county_amounts[0]+h_county_amounts[3]
        # 雲嘉南
        h_cs_count=h_county_amounts[7]+h_county_amounts[9]
        # 高屏
        h_s_count=h_county_amounts[6]+h_county_amounts[11]
        new_h_counts=[h_nn_count, h_ns_count, h_cn_count, h_cs_count, h_s_count]
        
        # 繪圖
        font_set=font(fname='./font_type/TaipeiSansTCBeta-Regular.ttf',size=12)
        new_countys=['北北基','桃竹苗','中彰投','雲嘉南','高屏區']
        colors=['#09c','#f55','#0c6','#f90','#c5c']
        
        plt.figure(figsize=(10,6))
        plt.title('Toyota Corolla Altis 各縣市的總數量佔比', fontproperties=font_set, pad=20, fontsize=15)
        pie_var=plt.pie(new_t_counts, 
                        radius=1.6, 
                        labels=new_countys,
                        colors=colors, 
                        autopct='%2.2f%%',
                        wedgeprops={'linewidth':3,'edgecolor':'w','width':.4},
                        counterclock = True,
                        pctdistance = 0.55,  
                       )
        
        for text in pie_var[1]:    
            text.set_fontproperties(font_set)
        plt.axis('equal')
        plt.legend(loc='best', prop=font_set, facecolor ='#f5f5f5')
        # plt.savefig('Toyota_Corolla_Altis各縣市的車子總數量比率', bbox_inches='tight')
        
        plt.figure(figsize=(10,6))
        plt.title('Honda Civic 各縣市的總數量佔比', fontproperties=font_set, pad=20, fontsize=15)
        pie_var2=plt.pie(new_h_counts, 
                        radius=1.6, 
                        labels=new_countys,
                        colors=colors, 
                        autopct='%2.2f%%',
                        wedgeprops={'linewidth':3,'edgecolor':'w','width':.4},
                        counterclock = True,
                        pctdistance = 0.55,  
                       )
        
        for text in pie_var2[1]:    
            text.set_fontproperties(font_set)
        plt.axis('equal')
        plt.legend(loc='best', prop=font_set, facecolor ='#f5f5f5')
        # plt.savefig('Honda_Civic各縣市的車子總數量比率', bbox_inches='tight')
        
        plt.show()
    except Exception as e:
        print(e)



if __name__ == '__main__':
    # 取資料來源 Toyota、Honda、Ford
    toyota_path, honda_path, ford_path='data_source/Toyota.csv','data_source/Honda.csv','data_source/Ford.csv'
    toyota_df=get_df(toyota_path)
    honda_df=get_df(honda_path)
    ford_df=get_df(ford_path)
    
    all_df={'t_ten_year':toyota_df.loc['2012':'2023'],'h_ten_year':honda_df.loc['2012':'2023'],\
            'f_ten_year':ford_df.loc['2012':'2023']}
        
    # 取得近十年 Toyota、Honda、Ford 預算30~50萬區間的車款
    all_price_dfs=[all_df[df][all_df[df]['售價(萬)'].between(300000,500000)] for i,df in enumerate(all_df.keys())]
    
    # 篩選預算30~50萬區間排氣量(L)=1.8的車輛
    cc_dfs=[price_df[price_df['排氣量(L)']==1.8]  for i,price_df in enumerate(all_price_dfs)\
            if len(price_df[price_df['排氣量(L)']==1.8]) != 0]
    
    # 篩選後再進行篩選10-15萬公里數
    need_cc_dfs=[cc_df[cc_df['里程數(km)'].between(100000,150000)] for i,cc_df in enumerate(cc_dfs)]
    
    # 繪圖
    price_avg()
    price_budget()
    km_amount()
    cc_amount()
    area_amount()
