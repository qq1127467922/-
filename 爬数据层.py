import requests
from bs4 import BeautifulSoup
import seaborn as sns
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文字体设置-黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
sns.set(font='SimHei',font_scale=1.5)  # 解决Seaborn中文显示问题并调整字体大小
headers = {
    'cookie':'global_cookie=jps5kg0p7bhqogole2yhj5snw18k4y8rtht; city=tongchuan; passport=username=&password=&isvalid=1&validation=; new_search_uid=c18397714bc48cbef743f943d6dabe45; newhouse_user_guid=B358CB08-96E2-A910-27CD-9EAAB7D2AC45; Integrateactivity=notincludemc; vh_newhouse=1_1578134158_885%5B%3A%7C%40%7C%3A%5Dd4a8b2c4911db0dd39bd63c9f3830239; lastscanpage=0; logGuid=f7d3a814-65b8-41fb-b5ac-434a21e75d46; __utma=147393320.1062291650.1578133067.1578133067.1578318110.2; __utmc=147393320; __utmz=147393320.1578318110.2.2.utmcsr=tongchuan.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; token=4b3e9590851148c7ba9cc3c5b286e7cd; sfut=F25E280D591BDDC22B39B267DE70CA04462FC7EBF909E1DE5A7F4C0A69C4675EEA0256D9A19740D9295A05F1D9AB67836449B5CEC9FB4C310A160EAD6D53C1B3DE56EC65F36A8A6146120FC09070D8AAE58EEC9C883803A863CD5D08ED473209; csrfToken=YXAMinQcxM8Vw25RNfGTLsu2; budgetLayer=1%7Ctongchuan%7C2020-01-06%2021%3A49%3A38; g_sourcepage=esf_fy%5Ewtxq_pc; new_loginid=110779828; login_username=fang3678436687; unique_cookie=U_pq0oqeqrflzd2ugr8hs538osa1tk52huj3s*6; __utmb=147393320.20.10.1578318110',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400',
    'referer':'https://tongchuan.esf.fang.com/'
}
#爬数据
def get_data():
    title_list = []#标题
    price_sum_list = []#总价
    one_price_list = []#单价
    house_type_list = []#户型
    covered_area_list = []#建筑面积
    orientation_list = []#朝向
    floor_list = []#楼层
    decoration_list = []#装修
    region_list = []#区域
    community_list = []#小区
    core_selling_points_list = []#房源亮点
    house_url_list = []
    for i in range(4):
        time.sleep(3)
        count = 0
        url = 'https://tongchuan.esf.fang.com/house/i3{0}/'.format(i+1)
        response = requests.get(url,headers=headers)
        url_xml = BeautifulSoup(response.text,'lxml')
        xml_dl_label = url_xml.find_all('dl',dataflag='bg')
        for dl_label in xml_dl_label:
            count = count + 1
            print('第{0}页第{1}个开始爬取'.format(i+1,count))
            href = dl_label.dd.find('h4',class_='clearfix').find('a',target='_blank').attrs['href']
            num= href.split('_')[0][-1]
            house_info_url = 'https://tongchuan.esf.fang.com' + href
            house_url_list.append(house_info_url)
            print('网址为'+house_info_url)
            time.sleep(3)
            res = requests.get(house_info_url,headers=headers)
            res.encoding = 'utf-8'
            house_info_xml = BeautifulSoup(res.text,'lxml')
            if int(num) == 3:
                title = house_info_xml.find('div',class_='wid1200 clearfix').find('div',class_='tab-cont clearfix').find('div',class_='title rel').find('h1',class_='floatl tit_details').find('span',class_='tit_text').string#获取标题
            else:
                title = house_info_xml.find('h1', class_='title floatl').string  # 获取标题
            title_list.append(title.replace(' ', '').strip())  # 存储标题信息
            print('标题:' + str(title).replace(' ', '').strip())
            xiangqing_label = house_info_xml.find('div',class_='tab-cont-right')
            price_sum = xiangqing_label.find('div',class_='tr-line clearfix zf_new_title').find('div',class_='trl-item_top').find('div',class_='trl-item price_esf sty1').find('i').string#总价
            price_sum_list.append(price_sum)#存储总价
            print('总价:' + str(price_sum))
            house_type = xiangqing_label.find_all('div',class_='tr-line clearfix')[0].find('div',class_='trl-item1 w146').find('div',class_='tt').string#户型
            house_type_list.append(house_type.replace(' ','').strip())#存储户型
            print('户型:' + str(house_type).replace(' ', '').strip())
            covered_area = xiangqing_label.find_all('div',class_='tr-line clearfix')[0].find('div',class_='trl-item1 w182').find('div',class_='tt').string#建筑面积
            covered_area_list.append(covered_area)#存储建筑面积
            print('建筑面积:' + str(covered_area))
            one_price = xiangqing_label.find_all('div',class_='tr-line clearfix')[0].find('div',class_='trl-item1 w132').find('div',class_='tt').string#单价
            one_price_list.append(one_price)#存储单价
            print('单价:' + str(one_price))
            floor = xiangqing_label.find_all('div',class_='tr-line clearfix')[1].find('div',class_='trl-item1 w182').find('div',class_='tt').string#楼层
            floor_list.append(floor)#存储楼层
            print('楼层:' + str(floor))
            orientation = xiangqing_label.find_all('div',class_='tr-line clearfix')[1].find('div',class_='trl-item1 w146').find('div',class_='tt').string#朝向
            orientation_list.append(orientation)#存储朝向
            print('朝向:' + str(orientation))
            decoration = xiangqing_label.find_all('div',class_='tr-line clearfix')[1].find('div',class_='trl-item1 w132').find('div',class_='tt').string#装饰
            decoration_list.append(decoration)#存储装饰
            print('装饰:' + str(decoration))
            region_string = ''
            if int(num) == 3:
                community = xiangqing_label.find('div',style="padding: 23px 0; padding-bottom: 8px;position: relative").find_all('div',class_='trl-item2 clearfix')[0].find('div',class_='rcont').string#小区
                region = xiangqing_label.find('div', style="padding: 23px 0; padding-bottom: 8px;position: relative").find_all('div', class_='trl-item2 clearfix')[1].find('div',class_='rcont').find_all('a',target='_blank')  # 区域
                for region_ in region:
                    region_string = region_string + region_.string.replace('\n','').replace(' ','') + '/'
            else:
                community = xiangqing_label.find('div',style="padding: 23px 0; padding-bottom: 8px;position: relative").find_all('div',class_='trl-item2 clearfix')[0].find('div',class_='rcont').find('div',class_='floatl').find('a',target='_blank').string#小区
                region = xiangqing_label.find('div', style="padding: 23px 0; padding-bottom: 8px;position: relative").find_all('div', class_='trl-item2 clearfix')[1].find('div',class_='rcont').find_all('a',target='_blank')  # 区域
                for region_ in region:
                    if region_.get_text() == '':
                        region_string = '无'
                        break
                    region_string = region_string + region_.get_text().replace('\n','').replace(' ','') + '/'
            community_list.append(community.replace(' ','').strip())#存储小区
            print('小区:' + str(community).replace(' ','').strip())
            region_list.append(region_string.strip().replace('\n','').replace(' ',''))#存储区域
            print('区域:' + str(region_string.strip()).replace('\n','').replace(' ',''))
            # people_label = house_info_xml.find('section',class_='miaoshu').find('section',class_='mBox').find('div',class_='fymsjjr mgX20 mt20').find('div',class_='txt').h3
            # agent_people = people_label.get_text()#代理人
            # agent_people_list.append(agent_people)#存储代理人
            if int(num) == 3:
                core_selling_points_label = house_info_xml.find('div',style="font-size:14px;")
                if (core_selling_points_label):
                    core_selling_points = core_selling_points_label.string
                else:
                    core_selling_points = '无'
            else:
                core_selling_points_label = house_info_xml.find('div',class_='pcont')
                if (core_selling_points_label):
                    core_selling_points = core_selling_points_label.string#房源亮点
                else:
                    core_selling_points = '无'
            core_selling_points_list.append(core_selling_points)
            print('亮点:' + str(core_selling_points))
    df_data = pd.DataFrame({'标题:':title_list,
                            '总价':price_sum_list,
                            '单价':one_price_list,
                            '户型':house_type_list,
                            '建筑面积':covered_area_list,
                            '朝向':orientation_list,
                            '楼层':floor_list,
                            '装饰':decoration_list,
                            '小区':community_list,
                            '区域':region_list,
                            '房源亮点':core_selling_points_list,
                            '网址':house_url_list})
    df_data.to_csv('./房天下二手房数据.csv')
def get_tongchuan_price_sum(data):
    price_sum = data['总价'].values
    x_label = np.linspace(1,len(price_sum),len(price_sum))
    plt.plot(x_label,price_sum)
    plt.title('铜川二手房整体水平')
    plt.show()
#房屋朝向分析饼状图
def get_orientation(data):
    orientation_map = {vol:ii for ii,vol in enumerate(set(data['朝向']))}
    print(orientation_map)
    data['朝向'] = data['朝向'].map(orientation_map)
    orientation_count_data = data.groupby(['朝向'], as_index=False)['朝向'].agg({'cnt': 'count'})
    orientation = orientation_count_data['朝向']
    count = orientation_count_data['cnt']
    plt.pie(count,labels=orientation)
    plt.show()
#热门户型
def get_hot_house_type(data):
    house_type_list = list(set(data['户型']))
    count = []
    for house_type in house_type_list:
        count.append(len(data[data['户型']==house_type]['户型'].values))
    plt.bar(house_type_list, count,width=0.5)
    plt.xticks(rotation=270)
    plt.show()
def set_price_sum(price_string):
    return float(price_string.replace('元/平米',''))
def get_aver_region(data):
    region_list = list(set(data['区域']))
    aver_price_list = []
    for region in region_list:
        aver_price_list.append(sum((data[data['区域']==region]['单价'].values)/(len((data[data['区域']==region]['单价'].values)))))
    plt.bar(region_list, aver_price_list,width=0.5)
    plt.xticks(rotation=270)
    plt.show()
#数据处理
def set_data(data):
    def set_covered_area(area_string):
        return float(area_string.replace('平米',''))
    orientation_map = {vol:ii for ii,vol in enumerate(set(data['朝向']))}
    data['朝向'] = data['朝向'].map(orientation_map)
    floor_map = {vol:ii for ii,vol in enumerate(set(data['层']))}
    data['层'] = data['层'].map(floor_map)
    decoration_map = {vol:ii for ii,vol in enumerate(set(data['装饰']))}
    data['装饰'] = data['装饰'].map(decoration_map)
    data['建筑面积'] = data['建筑面积'].apply(set_covered_area)
    house_type_map = {vol:ii for ii,vol in enumerate(set(data['户型']))}
    data['户型'] = data['户型'].map(house_type_map)
    return data
def get_correlation_coefficient(data):
    cols = ['总价', '单价', '户型', '建筑面积', '朝向','层','装饰']
    cm = np.corrcoef(data[cols].values.T)#corrcoef方法按行计算皮尔逊相关系数,cm是对称矩阵
    sns.set(font='SimHei',font_scale=0.9) #font_scale设置字体大小
    sns.set(style='whitegrid', context='notebook')
    hm = sns.heatmap(cm, cbar=True, annot=True,
                     cbar_ax=None,ax=None,
                     square=False,
                     fmt='.2f',
                     linewidths=0.05,
                     annot_kws={'size': 12},
                     yticklabels=cols,
                     xticklabels=cols)
    plt.show()
def train_test(data):
    feature = ['户型', '建筑面积', '朝向','层','装饰']
    x_data = data[feature]
    y_data = data['单价']
    x_train,x_test,y_train,y_test = train_test_split(x_data,y_data,test_size=0.3,random_state=30)
    model = RandomForestRegressor()
    model.fit(x_train,y_train)
    return model,x_test,y_test
if __name__ == '__main__':
    #get_data()
    data = pd.read_csv('房天下二手房数据2.csv',encoding='gbk')
    data['单价'] = data['单价'].apply(set_price_sum)
    data = set_data(data)
    #get_tongchuan_price_sum(data)
    #get_orientation(data)
    #get_hot_house_type(data)
    #get_aver_region(data)
    #get_correlation_coefficient(data)
    model,x_test,y_test = train_test(data)
    y_pred = model.predict(x_test)
    x_label = np.linspace(1,len(y_pred),len(y_pred))
    plt.plot(x_label,y_test)
    plt.plot(x_label,y_pred)
    plt.legend(['真实值','预测值'])
    plt.show()