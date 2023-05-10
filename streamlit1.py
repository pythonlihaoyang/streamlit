import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']

df=pd.read_csv('datas.csv')#总表


def pie():#画饼图
                       
    fig = plt.figure()

    education_counts=df['education'].value_counts()#相同元素个数 

    education_counts_index=education_counts.index.tolist()#regio地域列的index转化为列表    转换成 .to_dict字典

    education_counts_data=[i/sum(education_counts.tolist()) for i in education_counts.tolist()]#regio列 不同地域个数统计

    a=plt.pie(

            education_counts_data,
            
            autopct='%1.1f%%',
            shadow=True, 
            startangle=90,
            explode=[i*0.2 for i in education_counts_data],
            wedgeprops={'width':0.6,'edgecolor':'k'}
            
            )

    plt.legend(labels=education_counts_index,title='学历',frameon=False,
            loc='center',fontsize=8, bbox_to_anchor=(-0.1, 0.5),
            )

    st.pyplot(fig)


# 设置网页信息 
st.set_page_config(page_title="招聘大数据分析", page_icon=":bar_chart:", layout="wide")

side = ["首页","学历可视化","工资可视化","面议工资分析","招聘行业可视化","招聘企业可视化"]


st.sidebar.title("招聘数据进行分析可视化")

la = st.sidebar.selectbox("请选择",side)


if la=="首页":
    st.title('毕业设计LHY-对招聘网站的二万条数据进行爬取-进行数据可视化')

    st.warning('节选1000条数据集展示：')

    st.dataframe(df.head(1000))

    st.warning('节选spider自定义封装函数代码展示：')
    code='''
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
    return get_data'''

    st.code(code, language='python')




if la=="学历可视化":
    st.title('分析目前招聘市场对于学历的要求实际情况')
    st.warning('对抓取到的200000条招聘信息进行分析可视化！')
    pie()
    st.header('可视化代码展示！')
    code = '''
    def pie():#画饼图
        education_counts=df['education'].value_counts()#相同元素个数                     转换成 .to_dict字典

        fig = plt.figure()

        education_counts_index=education_counts.index.tolist()#regio地域列的index转化为列表

        education_counts_data=[i/sum(education_counts.tolist()) for i in education_counts.tolist()]#regio列 不同地域个数统计

        a=plt.pie(

                education_counts_data,
                
                autopct='%1.1f%%',
                shadow=True, 
                startangle=90,
                explode=[i*0.2 for i in education_counts_data],
                wedgeprops={'width':0.6,'edgecolor':'k'}
                
                )


        plt.legend(labels=education_counts_index,title='学历',frameon=False,
                loc='center',fontsize=8, bbox_to_anchor=(-0.1, 0.5),)


        st.pyplot(fig)
    '''
    st.code(code, language='python')
   

if la=="工资可视化":

    st.title('对招聘工作的工资进行数据可视化')
    fig1 = plt.figure()

    moneys=df['wage'].value_counts().head(26)


    moneys_index=moneys.index.to_list()#相同工作工资的金额


    moneys_data=moneys.to_list()#存储相同工资的工作个数

    plt.title('工资情况可视化图')

    plt.grid(axis='x',which='major')#对x轴生成虚线

    plt.xlabel('相同工资统计')

    plt.barh(width=moneys_data,y=moneys_index,color='blue')#生成横向条形图



    st.pyplot(fig1)

    st.header('可视化代码展示！')
    code = '''
     fig1 = plt.figure()

    moneys=df['wage'].value_counts().head(26)


    moneys_index=moneys.index.to_list()#相同工作工资的金额


    moneys_data=moneys.to_list()#存储相同工资的工作个数

    plt.title('工资情况可视化图')

    plt.grid(axis='x',which='major')#对x轴生成虚线

    plt.xlabel('相同工资统计')

    plt.barh(width=moneys_data,y=moneys_index,color='blue')#生成横向条形图



    st.pyplot(fig1)
    '''
    st.code(code, language='python')


if la=="面议工资分析":


    st.title('对于面议招聘类型的可视化')


    st.warning('结论：经过可视化我们发现，对那些工作的工资需要面议的情况下，对学历要求普遍的有所降低。')


    df_mianyi = df.drop(df[df['wage']!='面议'].index)#删除不是面议的行组成新的datafame

    mianyi_conts=df_mianyi['education'].value_counts().to_list()#相同学历的个数列表


    mianyi_index=df_mianyi['education'].value_counts().index.to_list()#相同学历个数的index


    fig2 = plt.figure()

    plt.title('面议工资情况可视化图')

    plt.grid(axis='x',which='major')#对x轴生成虚线

    plt.xlabel('相同工资统计')

    plt.ylabel('在同等的工资需要面议情况下，对学历要求。')

    plt.barh(width=mianyi_conts,y=mianyi_index,color='red')#生成横向条形图



    st.pyplot(fig2)

    st.header('可视化代码展示！')

    code = '''
    st.title('对于面议招聘类型的可视化')


    st.warning('经过可视化我们发现，对那些需要工资面议的工作，对于学历要求普遍的不是很高的标准')


    df_mianyi = df.drop(df[df['wage']!='面议'].index)#删除不是面议的行组成新的datafame

    mianyi_conts=df_mianyi['education'].value_counts().to_list()#相同学历的个数列表


    mianyi_index=df_mianyi['education'].value_counts().index.to_list()#相同学历个数的index


    fig2 = plt.figure()

    plt.title('面议工资情况可视化图')

    plt.grid(axis='x',which='major')#对x轴生成虚线

    plt.xlabel('相同工资统计')

    plt.barh(width=mianyi_conts,y=mianyi_index,color='red')#生成横向条形图



    st.pyplot(fig2)
            '''
    st.code(code, language='python')


if la=="招聘行业可视化":

    df_hangye=df['trade'].value_counts().head(26).to_list()#相同行业工作机会的个数


    df_hangye_data=df['trade'].value_counts().head(26).index.to_list()#相同行业个数的index


    print(df_hangye_data)
    fig3 = plt.figure()

    plt.title('招聘行业可视化图')

    plt.grid(axis='x',which='major')#对x轴生成虚线

    plt.xlabel('相同行业统计')

    plt.barh(width=df_hangye,y=df_hangye_data,color='green')#生成横向条形图



    st.pyplot(fig3)

    st.header('可视化代码展示！')
    code = '''

    df_hangye=df['trade'].value_counts().to_list()#相同行业工作机会的个数


    df_hangye_data=df['trade'].value_counts().index.to_list()#相同行业个数的index

    fig3 = plt.figure()

    plt.title('招聘行业可视化图')

    plt.grid(axis='x',which='major')#对x轴生成虚线

    plt.xlabel('相同行业统计')

    plt.barh(width=df_hangye,y=df_hangye_data,color='yellow')#生成横向条形图



    st.pyplot(fig3)

    '''
    st.code(code, language='python')
    

if la=="招聘企业可视化" :  


    df_qiye=df['nature'].value_counts().to_list()#个数



    df_qiyed_ata=df['nature'].value_counts().index.to_list()#相同企业个数的index


    fig4 = plt.figure()

    plt.title('招聘企业可视化图')

    plt.grid(axis='x',which='major')#对x轴生成虚线

    plt.xlabel('相同企业统计')

    plt.barh(width=df_qiye,y=df_qiyed_ata,color='black')#生成横向条形图


    st.pyplot(fig4)

    st.header('可视化代码展示！')

    code = '''
    df_qiye=df['nature'].value_counts().to_list()#个数



    df_qiyed_ata=df['nature'].value_counts().index.to_list()#相同企业个数的index


    fig4 = plt.figure()

    plt.title('招聘企业可视化图')

    plt.grid(axis='x',which='major')#对x轴生成虚线

    plt.xlabel('相同企业统计')

    plt.barh(width=df_qiye,y=df_qiyed_ata,color='black')#生成横向条形图


    st.pyplot(fig4)
    '''

    st.code(code, language='python')
