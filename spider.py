import requests
from lxml import etree
import numpy as np
import pandas as pd
import selenium
import time 



# 获取爬取的城市和爬取的页码数
def get_city_page():
    city = input('请输入要爬取的城市：')
    page = int(input('请输入要爬取的页码数：'))
    return city,page
# 构建url_list
def create_url_lis(city,page):
    # 城市对应编码
    city_code_dict = {
        '上海':538, '北京':530, '广州':763, '深圳':765, '天津':531, '武汉':736, '西安':854, 
        '成都':801, '南京':635, '杭州':653, '重庆':551, '厦门':682
    }
    # 定义一个空列表用于存放url
    url_lis = []
    # 根据城市中文名取出对应的城市编码
    city_code = city_code_dict[city]
    # 循环遍历页码数，生成url_lis
    for p in range(page):
        url = 'https://sou.zhaopin.com/?jl={}&kw={}&p={}'.format(city_code,'数据分析',p+1)
        url_lis.append(url)
    return url_lis


# 根据url获取网页源代码
def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'cookie': 'x-zp-client-id=f873b6b9-99ef-46ea-9765-5cd098eb2b67; _uab_collina=165451623563722330196985; at=ced2561a5c194cd8a8f3aa7a6d850833; rt=ffcb2c6f643246ae97f5b45881fd7694; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221089982550%22%2C%22first_id%22%3A%2218138da0c4317-0c28aa3ec9d9a7-57b1a33-1327104-18138da0c44244%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%2218138da0c4317-0c28aa3ec9d9a7-57b1a33-1327104-18138da0c44244%22%7D; ZP_OLD_FLAG=false; sts_deviceid=181395a45735-0763172b75124d-57b1a33-1327104-181395a45743c9; locationInfo_search={%22code%22:%22763%22%2C%22name%22:%22%E5%B9%BF%E5%B7%9E%22%2C%22message%22:%22%E5%8C%B9%E9%85%8D%E5%88%B0%E5%B8%82%E7%BA%A7%E7%BC%96%E7%A0%81%22}; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1654524627,1654565369; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1654565369; ssxmod_itna=iqGxgDyGi=GQN0LxYKBe7u8jUQ0QqKq=FFDl=6DxA5D8D6DQeGTiXqDBiDcinjiD54TDZ7OhvdI01OD3m3rl0exfpDCPGnDBI5bqGDYAODt4DTD34DYDixibkxi5GRD0KDFWqvz19Dm4GWWqDmDGYcYqDgDYQDGLpjD7QDIT6dlGDc3QLevdRBlA0oIi=DjkbD/8xWuj2WHpGl3QnrsExeD0pz0144YDHCFDvoDneRDB6wxBjSITX6+ey99utDg2EKDk5QG7xWl74CehGmDw+ol4hIlZSoi0v5bD+19zzxD=; acw_tc=276077d316545674726624362ef74d4c5ad68525f589cbfbd4efa43a546a61; ZL_REPORT_GLOBAL={%22jobs%22:{%22funczoneShare%22:%22dtl_best_for_you%22%2C%22recommandActionidShare%22:%225720dfd1-7d14-4778-9c73-f326bae43b86-job%22}}'   
    }
    html = requests.get(url,headers = headers).text
    return html

def transform_html(response):
    """
    解析网页源代码，提取想要的信息，并返回信息的dataframe
    response：抓取到的网页源代码
    """
    # 招聘岗位、工作地点、工作经验、学历要求、招聘人数、年龄要求、时间、工资、公司、工作类型、企业类型、企业规模,对于数据的处理可以部署到github中对于github的项目代码我们可以通过url在线访问项目代码
    html = etree.HTML(response)
    # 获取工作名称
    job = html.xpath('//span[@class="iteminfo__line1__jobname__name"]/@title')
    # 获取薪资范围
    salary = html.xpath('//p[@class="iteminfo__line2__jobdesc__salary"]/text()')
    for i in range(len(salary)):
        salary[i] = salary[i].strip('\n').strip(' ').rstrip('\n')
    # 获取地区、经验、学历信息
    location,experience,education = ([] for i in range(3))
    require = html.xpath('//ul[@class="iteminfo__line2__jobdesc__demand"]')
    for req in require:
        try:
            loc = req.xpath('.//li[@class="iteminfo__line2__jobdesc__demand__item"]/text()')[0]
            location.append(loc)
        except:
            location.append(np.nan)
        try:
            exp = req.xpath('.//li[@class="iteminfo__line2__jobdesc__demand__item"]/text()')[1]
            experience.append(exp)
        except:
            experience.append(np.nan)
        try:
            edu = req.xpath('.//li[@class="iteminfo__line2__jobdesc__demand__item"]/text()')[2]
            education.append(edu)
        except:
            education.append(np.nan)

    # 获取职位标签
    job_tag = []
    job_tag_lis = html.xpath('//div[@class="iteminfo__line3__welfare"]')
    for tag in job_tag_lis:
        tag_info = tag.xpath('.//div[@class="iteminfo__line3__welfare__item"]/text()')
        tag_info = str(tag_info)
        job_tag.append(tag_info)

    # 获取公司名称
    company_name = html.xpath('//span[@class="iteminfo__line1__compname__name"]/text()')

    # 获取公司类型、公司规模
    company_type = []
    company_size = []
    company_detail = html.xpath('//div[@class="iteminfo__line2__compdesc"]')
    for company in company_detail:
        try:
            com_type = company.xpath('.//span[@class="iteminfo__line2__compdesc__item"]/text()')[0]
            company_type.append(com_type)
        except:
            company_type.append(np.nan)
        try:
            com_size = company.xpath('.//span[@class="iteminfo__line2__compdesc__item"]/text()')[1]
            company_size.append(com_size)
        except:
            company_size.append(np.nan)

    data_lis = [job,salary,location,experience,education,job_tag,company_name,company_type,company_size]
    # 爬取结果合成一个dataframe
    get_data = pd.DataFrame(columns = ['招聘岗位、工作地点、工作经验、学历要求、招聘人数、年龄要求、时间、工资、公司、工作类型、企业类型、企业规模'])
    for col,data in zip(get_data.columns,data_lis):
        get_data[col] = data
    # 返回数据的dataframe
    return get_data



# 循环爬取每一页的数据，并且合成为一个dataframe
def concat_data(url_lis):
    # 定义字典储存dataframe
    final_df_dict = {}
    for url,num in zip(url_lis,range(len(url_lis))):
        try:
            print('开始爬取第{}页'.format(num+1))
            # 获取网页源代码
            response = get_html(url)
            # 解析网页源代码并且生成一个dataframe
            final_df = transform_html(response)
            # 将dataframe保存到字典里
            final_df_dict[num] = final_df
            print('第{}页爬取完成'.format(num+1))
            # 爬取完成后程序休眠10秒
            time.sleep(10)
        except:
            print('所有页码都爬取完成！总计爬取{}页'.format(num+1))
    concat_df = pd.concat(list(final_df_dict.values()),ignore_index = True)
    return concat_df

# 爬取结果保存到csv，为后续的数据处理进行预处理
def save_df(df,city):
    file_name = '{}work.xls'.format(city)
    path = r'/home/mw/result_data/{}'.format(file_name)
    df.to_csv(path,encoding = 'utf-8',index = False)
    print('{}保存成功'.format(file_name))
    return 