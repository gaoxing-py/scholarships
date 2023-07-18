# This is a sample Python script.
import pandas
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from function import *
import json

df_stu_info = pd.read_csv('info/stu_info.csv', encoding='GBK')              # 学生基本信息
df_course_info = pd.read_csv('info/course_info.csv', encoding='GBK')        # 课程基本信息
df_con_info = pd.read_csv('info/contest_info.csv',encoding='utf-8')           # 竞赛信息
df_act_info = pd.read_csv('info/activity_info.csv',encoding='utf-8')          # 活动信息
df_work_info = pd.read_csv('info/work_info.csv')                              # 职务信息

df_stu_grades = pd.read_csv('records/stu_grades.csv', encoding='GBK')            # 学生成绩
df_appr_rec = pd.read_csv('records/demo_appr.csv', encoding='GBK')              # 民主评议结果
df_work_rec = pd.read_csv('records/work_records.csv', encoding='utf-8')       # 社会工作认定
df_tech_award = pd.read_csv('records/tech_award_records.csv', encoding='utf-8')          # 科研类获奖
df_paper = pd.read_csv('records/paper_records.csv',encoding='utf-8')
df_case = pd.read_csv('records/case_records.csv',encoding='utf-8')
df_prize_rec = pd.read_csv('records/prize_records.csv',encoding='utf-8')      # 科创竞赛

# 考试完整信息 姓名/学号/课程名/课程编号/是否必修/成绩 等...
df_exam = pd.merge(pd.merge(df_stu_grades, df_course_info, on="课程编号", how="left"),df_stu_info,on="学号",how='left')
# 民主评议 连接stu_info
df_demo = pd.merge(df_appr_rec,df_stu_info,on="学号",how='left')

points = {
    'tech_award':{

            'hierarchy':{'国家级':6,'教育部':4,'省部级':2,'副省级':1},
            'type':{'自然科学奖':4,'科技进步奖':4,'技术发明奖':4,'哲学社会科学奖':4},
            'level':{'特等奖':1.5,'一等奖':1,'二等奖':0.5,'三等奖':0.3,'青年科学奖/青年成果奖':0.5 },
            'ranking':{1:1,2:0.7,3:0.5,4:0.3,5:0.2,6:0.15,7:0.1,8:0.05}

    },
    'contest':{'hierarchy':{'一级':2,'二级':1,'三级':0.5},
               'type':{'国家级':3,'省级':2,'市级':1.5,'校级':1},
               'level':{'一等奖':1,'二等奖':0.5,'三等奖':0.3}
               },
    'paper':{
        'a':10,'b':5,'c':2,'d':1,'e':0.5,'f':2,
    },
    'case':{'a':3,'b':2,'c':1.5,'d':0.5,'e':1}
}

# 初始界面
st.title("DUT经济管理学院奖学金管理系统")
st.sidebar.title("控制栏")
item=st.sidebar.selectbox('功能列表', ("————","学生信息","评审办法","排名结果"))

if item == "————":
    image_0 = Image.open('image/logo_2.jpg')
    st.image(image_0)
    st.subheader('功能列表')
    st.markdown('●  学生信息：查看学生基本信息、考试成绩、科研成果、社会活动等')
    st.markdown('●  评审规则：修改奖学金名额、评审细则等信息，如更新各项权重等')
    st.markdown('●  排名结果：分专业查看最终奖学金分配结果')

    # st.subheader('欢迎使用！')
    st.markdown('*欢迎使用！本系统仅供参考~*')
    image = Image.open('image/logo.jpg')
    st.image(image)

elif item=="学生信息":

    view_stu_info = st.sidebar.selectbox('请选择要查看的信息',
                                        ("基本信息", "学习成绩", "科研成果", "科创比赛","社会工作","民主评议"))
    if view_stu_info=="基本信息":
        st.write('---')
        st.subheader('（1） 学生基本信息')
        st.dataframe(df_stu_info)
        #st.bar_chart(data=df_stu_info['性别'].value_counts(),width=400,height=300,use_container_width=False)
        #st.bar_chart(data=df_stu_info['类型'].value_counts(), width=400, height=300, use_container_width=False)
        #st.bar_chart(data=df_stu_info['专业'].value_counts(), width=400, height=300, use_container_width=False)
        st.subheader('（2） 统计数据')
        plt = EDA(df_stu_info)
        st.pyplot(plt)

    elif view_stu_info=="学习成绩":
        st.write('---')
        st.subheader('学生考试成绩')
        df_exam = df_exam[['学号','姓名','课程编号','课程名称','课程类型','是否必修','学分','成绩']]
        st.dataframe(df_exam)

    elif view_stu_info=="科研成果":
        st.write("⬇ 科研类获奖：")
        st.dataframe(df_tech_award[["学号","项目名称","所获奖项","获奖层次","获奖等第","作者排名","积分"]])

        st.write("⬇ 论文或专著：")
        st.dataframe(df_paper[["学号", "论文名称", "载文期刊", "期刊水平", "作者排名","积分"]])

        st.write("⬇ 专利或案例：")
        st.dataframe(df_case[["学号", "专利/案例名称", "专利/案例类型", "作者排名","积分"]])

        tech_class = st.sidebar.selectbox('添加:',('请选择 ↓','科研类获奖','论文或专著','专利或案例'))

        if tech_class == '科研类获奖':
            with st.form(key='add_item'):
                stu_id = st.text_input(label='学号')
                achi_name = st.text_input(label='项目名称')
                award = st.selectbox('所获奖项',('自然科学奖','科技进步奖','技术发明奖','哲学社会科学奖'))  # 这一块需要修改
                hi =st.selectbox('获奖层次：',('国家级','教育部','省部级','副省级'))
                level = st.selectbox('获奖等第：',('特等奖','一等奖','二等奖','三等奖','青年科学奖/青年成果奖'))
                ranking = st.text_input(label='排名')
                submit_butten = st.form_submit_button(label='添加')
                if submit_butten == True:
                    if stu_id =='' or achi_name=='':
                        st.info('学号和项目名称不能为空！')
                    else:
                        p=points['tech_award']
                        score = p['type'][award] * p['hierarchy'][hi] * p['level'][level] * p['ranking'][float(ranking)]
                        st.write(score)
                        new_data = pd.DataFrame([stu_id,achi_name,award,hi,level,ranking,score]).T
                        new_data.to_csv('records/tech_award_records.csv', mode='a', header=False, index=False,
                                        index_label=False)
                        st.dataframe(new_data)
                        st.info("添加成功！")


        elif tech_class == '论文或专著':
            with st.form(key='add_item'):
                stu_id = st.text_input(label='学号')
                paper_name = st.text_input(label='论文名称')
                jour_or_conf = st.text_input(label='载文期刊/会议')
                level = st.selectbox('期刊水平：',
                                     ('a.国际A*/TOP5类论文/中国社会科学',
                                      'b.国际A/TOP10类论文/国内TOP论文',
                                      'c.国际B/国内A',
                                      'd.国际C/国内B',
                                      'e.国内C',
                                      'f.学术专著'))
                is_inter = st.checkbox('Yes --是否为国际期刊/会议')
                count = st.text_input(label='作者数')
                ranking = st.text_input(label='排名')
                # count_list= [ i+1  for i in range(4)]
                # ranking = st.radio('排名',count_list)

                submit_butten = st.form_submit_button(label='添加')
                if submit_butten == True:
                    if stu_id == '' or paper_name == '':
                        st.info('学号和论文名称不能为空！')
                    else:
                        score = calc_paper_score(points['paper'],level,is_inter,count,ranking)
                        #score = p['type'][award] * p['hierarchy'][hi] * p['level'][level] * p['ranking'][float(ranking)]
                        st.write(score)
                        new_data = pd.DataFrame([stu_id,paper_name,jour_or_conf,level, ranking,count,score]).T
                        new_data.to_csv('records/paper_records.csv', mode='a', header=False, index=False,
                                        index_label=False)
                        st.dataframe(new_data)
                        st.info("添加成功！")

        elif tech_class == '专利或案例':
            with st.form(key='add_item'):
                stu_id = st.text_input(label='学号')
                case_name = st.text_input(label='案例/专利名称')
                level = st.selectbox('种类：',
                                     ('a.全国百优重点案例',
                                      'b.入选哈佛、毅伟案例库的案例',
                                      'c.全国百优案例',
                                      'd.入选全国MBA共享中心案例库的案例',
                                      'e.专利'))
                count = st.text_input(label='作者数')
                ranking = st.text_input(label='排名')
                submit_butten = st.form_submit_button(label='添加')
                if submit_butten == True:
                    if stu_id == '' or case_name == '':
                        st.info('学号和案例名称不能为空！')
                    else:
                        score = calc_paper_score(points['case'],level,False,count,ranking)
                        #score = p['type'][award] * p['hierarchy'][hi] * p['level'][level] * p['ranking'][float(ranking)]
                        st.write(score)
                        new_data = pd.DataFrame([stu_id,case_name,level,ranking,count,score]).T
                        new_data.to_csv('records/case_records.csv', mode='a', header=False, index=False,
                                        index_label=False)
                        st.dataframe(new_data)
                        st.info("添加成功！")

    elif view_stu_info=="科创比赛":
        # df_prize_rec = pd.merge(df_prize_rec,df_stu_info,how='left',on='学号')
        st.dataframe(df_prize_rec)

        with st.form(key='add_item'):
            stu_id = st.text_input(label='学号')
            contest_list = pd.read_csv('info/contest_info.csv')
            # contest_list=contest_list[contest_list.con_type==con_level]['con_name'].tolist()
            contest = st.selectbox('比赛名称',contest_list)
            con_type = st.selectbox('获奖类别',('国家级','省级','市级','校级'))
            con_level = st.selectbox('获奖等级',('一等奖','二等奖','三等奖'))
            ranking = st.selectbox('排名系数',('1','2','3','4','5','6'))
            con_time=st.text_input(label='获奖时间(yyyy年mm月):')
            submit_button = st.form_submit_button(label='添加')

            # st.dataframe(df_con_info)
            st.write(contest)
            con_hi = df_con_info[df_con_info.con_name == contest].iloc[0,-1]  # 从表中找到该比赛的层次

            if submit_button==True and stu_id!='':

                score = points['contest']['hierarchy'][con_hi]*points['contest']['type'][con_type]*points['contest']['level'][con_level]*(1/float(ranking))
                st.write("该项积分为：",score)

                new_data=pd.DataFrame([stu_id,contest,con_type,con_level,con_time,ranking,score]).T
                #st.dataframe(new_data)
                #st.dataframe(new_data[,1:])
                new_data.to_csv('records/prize_records.csv',mode='a',header=False,index=False,index_label=False)
                st.dataframe(new_data)
                # df_prize_record.loc[len(df_prize_record.index)]=new_data
                # df_prize_rec = df_prize_rec._append(new_data)

                #  ↑ 但是还没有更新到表中

                st.info('添加成功!')
            if submit_button==True and stu_id=='':
                st.info("学号不能为空！")

    elif view_stu_info=="社会工作":
        st.dataframe(df_work_rec)
        #with st.form(key='add_item'):
        work_score = pd.read_csv('info/work_info.csv')

        work_list = df_work_info['职务类别'].tolist()

        # add = st.sidebar.button(label='添加')
        #if add ==True:
        with st.form(key ='add_item'):
            stu_id = st.text_input(label='学号')
            work = st.selectbox('职务',work_list)
            submit_butten = st.form_submit_button('添加')
            if submit_butten == True:
                if stu_id == '':
                    st.info('学号不能为空')
                else:
                    score = work_score[work_score.职务类别==work].iloc[0][1]
                    new_data = pd.DataFrame([stu_id, work,score]).T
                    new_data.to_csv('records/work_records.csv', mode='a', header=False, index=False, index_label=False)
                    st.dataframe(new_data)
                    st.info('添加成功！')

    elif view_stu_info=="民主评议":
        st.dataframe(df_appr_rec)

elif item=="评审办法":
    st.write("Part 1. 各专业名额分配")
    st.write("按照国家奖学金相关政策，按照3%的比例进行名额分配。其他未尽事宜等待后续通知，如有需要可以自行修改，输入各专业对应的人数即可。")
    x = pd.DataFrame(df_stu_info['专业'].value_counts())
    x['名额'] = x['count']*0.05
    st.dataframe(x)
    with st.form(key='change_weight'):
        guanke = st.text_input(label='管理科学与工程：')
        jinrong = st.text_input(label='金融：')
        dashujv = st.text_input(label='大数据技术与应用：')
        jingji = st.text_input(label='产业经济学：')
        submit_button = st.form_submit_button(label='修改')
        if submit_button == True:
            st.info('这一块的代码还没写:(')

    st.write("Part 2. 各维度权重设置")
    st.write("学硕：")
    with st.form(key='xueshuo'):
        course_1 = st.slider(label="考试成绩",min_value=0.0,max_value=1.0,value=0.2)
        research_1 = st.slider(label="科研成果",min_value=0.0,max_value=1.0,value=0.2)
        contest_1 = st.slider(label="科创竞赛",min_value=0.0,max_value=1.0,value=0.2)
        work_1 = st.slider(label="学生工作",min_value=0.0,max_value=1.0,value=0.2)
        appr_1 = st.slider(label="民主评议",min_value=0.0,max_value=1.0,value=0.2)
        butten_xueshuo=st.form_submit_button(label="提交")
        if butten_xueshuo ==True and (course_1+research_1+contest_1+work_1+appr_1)!=1:
            st.info("权重不为1！")
        if butten_xueshuo ==True and (course_1+research_1+contest_1+work_1+appr_1)==1:
            weight_xueshuo={}
            weight_xueshuo["course"]=course_1
            weight_xueshuo['research']=research_1
            weight_xueshuo['contest']=contest_1
            weight_xueshuo['work']=work_1
            weight_xueshuo['appr']=appr_1

            st.write(weight_xueshuo)

            with open('param/w_xue.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(weight_xueshuo, ensure_ascii=False))

            st.info("修改成功！")

    st.write("专硕：")
    with st.form(key='zhuanshuo'):
        course_2 = st.slider(label="考试成绩",min_value=0.0,max_value=1.0,value=0.2)
        research_2 = st.slider(label="科研成果",min_value=0.0,max_value=1.0,value=0.2)
        contest_2 = st.slider(label="科创竞赛",min_value=0.0,max_value=1.0,value=0.2)
        work_2 = st.slider(label="学生工作",min_value=0.0,max_value=1.0,value=0.2)
        appr_2 = st.slider(label="民主评议",min_value=0.0,max_value=1.0,value=0.2)
        butten_zhuanshuo=st.form_submit_button(label="提交")
        if butten_zhuanshuo ==True and (course_2+research_2+contest_2+work_2+appr_2)!=1:
            st.info("权重不为1！")
        if butten_zhuanshuo ==True and (course_2+research_2+contest_2+work_2+appr_2)==1:
            weight_zhuanshuo={}
            weight_zhuanshuo["course"]=course_2
            weight_zhuanshuo['research']=research_2
            weight_zhuanshuo['contest']=contest_2
            weight_zhuanshuo['work']=work_2
            weight_zhuanshuo['appr']=appr_2
            st.info("修改成功！")

else:
    st.markdown('国家奖学金排名及名额分配结果')

    # 获取所有专业的名称
    major_list = df_stu_info['专业'].unique().tolist()
    major = st.sidebar.selectbox("选择专业", major_list)

    # 分专业计算各个分项的分值
    # 计算考试成绩的序数排名
    df_test = get_study_item(df_exam,major)

    # 计算科研成果的序数排名
    df_award = pd.merge(df_tech_award,df_stu_info,how='left',on="学号")[['学号','专业','积分']]
    df_paper = pd.merge(df_paper, df_stu_info, how='left', on="学号")[['学号', '专业', '积分']]
    df_case = pd.merge(df_case, df_stu_info, how='left', on="学号")[['学号', '专业', '积分']]
    dfs= [df_award,df_paper,df_case]
    df_tech = pd.concat(dfs)   # 加一下说是论文/专利还是啥
    st.dataframe(df_tech)
    df_research_rank = get_research_item(df_tech,major)

    # 计算科创竞赛的序数排名
    df_con = pd.merge(df_prize_rec,df_stu_info,how='left',on="学号")
    df_con_rank = get_contest_item(df_con,major)

    # 计算社会活动的序数排名
    df_work = pd.merge(df_work_rec, df_stu_info, how='left', on="学号")
    df_work_rank = get_work_item(df_work, major)

    # 计算民主评议得分
    df_demo = df_demo[df_demo.专业 == major]
    max = df_demo.iloc[:, 2].max()
    df_demo.iloc[:, 2] = 100 / max * df_demo.iloc[:,2]

    #dfs=[df_test,df_research_rank,df_con_rank,df_work_rank,df_demo]
    # df_all = pd.concat(dfs)

    # st.dataframe(df_test)
    # st.dataframe(df_research_rank)
    # st.dataframe(df_con_rank)
    # st.dataframe(df_work_rank)
    # st.dataframe(df_demo)
    # st.dataframe(df_all)

    df_final = pd.merge(df_demo,df_test,how='left',on="学号")
    df_final = pd.merge(df_final, df_research_rank, how='left', on="学号")
    df_final = pd.merge(df_final, df_con_rank, how='left', on="学号")
    df_final = pd.merge(df_final, df_work_rank, how='left', on="学号")
    df_final = df_final.fillna(value=0)
    # st.dataframe(df_final)

    if df_final.loc[1,'类型'] == "学硕":

        with open("param/w_xue.json", "r", encoding='utf-8') as f:
            weight_xueshuo = json.load(f)

            df_final['results'] = df_final['加权平均分']*weight_xueshuo['course']+ \
                                  df_final['积分'] * weight_xueshuo['research'] + \
                              df_final['竞赛积分'] * weight_xueshuo['contest']+\
                              df_final['活动积分']*weight_xueshuo['work'] + \
                              df_final['民主评议得分']*weight_xueshuo['appr']
    #    results = calc_final_score(weight_xueshuo,dfs)
    else:
    #    results = calc_final_score(weight_zhuanshuo,dfs)

        with open("param/w_zhuan.json", "r", encoding='utf-8') as f:
            weight_zhuanshuo = json.load(f)
            df_final['results'] = df_final['加权平均分'] * weight_zhuanshuo['course'] + \
                              df_final['积分'] * weight_zhuanshuo['research'] + \
                              df_final['竞赛积分'] * weight_zhuanshuo['contest'] + \
                              df_final['活动积分'] * weight_zhuanshuo['work'] + \
                              df_final['民主评议得分'] * weight_zhuanshuo['appr']

    df_elim = check_qualified(df_exam,df_demo)

    df_final=df_final.sort_values(by='results', ascending=False)
    df_final['是否获奖'] = '否'

    for i in range(2):
        df_final.iloc[i,-1]='是'

    st.dataframe(df_elim)
    st.dataframe(df_final)
