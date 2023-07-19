# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# -- coding: utf-8 --
import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
from function import *
import json

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False

df_stu_info = pd.read_csv('info/stu_info.csv', encoding='GBK')                # 学生基本信息
df_course_info = pd.read_csv('info/course_info.csv', encoding='GBK')          # 课程基本信息
df_con_info = pd.read_csv('info/contest_info.csv',encoding='utf-8')           # 竞赛信息
df_act_info = pd.read_csv('info/activity_info.csv',encoding='utf-8')          # 活动信息
df_work_info = pd.read_csv('info/work_info.csv')                              # 职务信息

df_stu_grades = pd.read_csv('records/stu_grades.csv', encoding='GBK')            # 学生成绩
df_appr_rec = pd.read_csv('records/demo_appr.csv', encoding='GBK')               # 民主评议结果
df_work_rec = pd.read_csv('records/work_records.csv', encoding='utf-8')          # 社会工作认定
df_tech_award = pd.read_csv('records/tech_award_records.csv', encoding='utf-8')  # 科研类获奖
df_paper = pd.read_csv('records/paper_records.csv',encoding='utf-8')             # 论文或专著
df_case = pd.read_csv('records/case_records.csv',encoding='utf-8')               # 专利或案例
df_prize_rec = pd.read_csv('records/prize_records.csv',encoding='utf-8')         # 科创竞赛
df_app = pd.read_csv('records/application.csv',encoding='utf-8')                 # 学术直通车申请

# 考试完整信息 姓名/学号/课程名/课程编号/是否必修/成绩 等...
df_exam = pd.merge(pd.merge(df_stu_grades, df_course_info, on="课程编号", how="left"),df_stu_info,on="学号",how='left')
# 民主评议 连接stu_info
df_demo = pd.merge(df_appr_rec,df_stu_info,on="学号",how='left')

# 积分规则
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
item=st.sidebar.selectbox('功能列表', ("————","学生信息","评审办法","排名结果",'申请审核'))

if item == "————":
    st.write('---')
    image_0 = Image.open('image/logo_2.jpg')
    st.image(image_0)
    st.subheader('功能列表')
    st.markdown('该系统用于降低奖学金评定的工作量，高效便捷地完成信息的查看、\
    录入、审核，实现奖学金评选辅助决策，以合理公平客观的方式评选出奖学金获得者。\
    系统实现了对参评学生各项数据的可视化、自动计分并排名，支持对奖学金规则的修改，\
    这极大的简化人工收取奖学金申请表，并手动进行计分排名的奖学金审核步骤。')
    st.markdown(' - **:blue[学生信息]**：查看并修改学生基本信息、考试成绩、科研成果、社会活动等；')
    st.markdown(' - **:blue[评审规则]**：查看并修改奖学金评选细则，如各专业名额、各维度权重等信息等；')
    st.markdown(' - **:blue[排名结果]**：查看最终奖学金评选结果。')
    st.markdown(' - **:blue[申请审批]**：对申请“学术直通车”的学生进行审核。')
    st.write('---')

    st.markdown('*欢迎使用！本系统仅供参考~*')
    image = Image.open('image/logo.jpg')
    st.image(image)

elif item=="学生信息":
    view_stu_info = st.sidebar.selectbox('请选择要查看的信息',
                                        ("基本信息", "学习成绩", "科研成果", "科创比赛","社会工作","民主评议"))
    if view_stu_info == "基本信息":
        st.write('---')
        st.subheader('（1） 学生基本信息')
        st.dataframe(df_stu_info)
        #st.bar_chart(data=df_stu_info['性别'].value_counts(),width=400,height=300,use_container_width=False)
        #st.bar_chart(data=df_stu_info['类型'].value_counts(), width=400, height=300, use_container_width=False)
        #st.bar_chart(data=df_stu_info['专业'].value_counts(), width=400, height=300, use_container_width=False)
        st.subheader('（2） 统计数据')
        plt = EDA(df_stu_info)
        st.pyplot(plt)

    elif view_stu_info == "学习成绩":
        st.write('---')
        st.subheader('学生考试成绩')
        st.write(' **:blue[规则说明]**：学术型硕士生学习成绩中取成绩最高的9门必修课,专业型硕士取6门；\
        鼓励广大研究生在第一年完成培养计划中的全部课程，计算中按照个人已修完必修课学分总数占应修完学分总数的比例，乘以加权系数；\
        P/F类型的课程通过即可，不参与分数计算。')

        df_exam = df_exam[['学号', '姓名', '课程编号', '课程名称', '课程类型', '是否必修', '学分', '成绩']]
        st.dataframe(df_exam)

    elif view_stu_info == "科研成果":
        st.write('---')
        st.write(' **:orange[规则说明]**：科研成果包含以下三大类 ↓ ')
        st.write('- **:blue[科研类获奖]**：该项仅包括三大奖和哲学社会科学奖，获奖名次以证书排名为准，积分依照自然排名计算；')
        st.write('- **:blue[科研论文与学术专著]**：如论文署名中包括本人导师或导师组成员，学生可去除且仅可去除一人（此人需为导师或导师组成员）后计算积分;')
        st.write('- **:blue[案例或专利]**：必须本人为第一作者/第一发明人，或导师第一作者/第一发明人、本人第二作者/第二发明人。')
        st.write('---')
        st.write("⬇ 科研类获奖：")
        st.dataframe(df_tech_award[["学号","项目名称","所获奖项","获奖层次","获奖等第","作者排名","积分"]])

        st.write("⬇ 论文或专著：")
        st.dataframe(df_paper[["学号", "论文名称", "载文期刊", "期刊水平", "作者排名","积分"]])

        st.write("⬇ 专利或案例：")
        st.dataframe(df_case[["学号", "专利/案例名称", "专利/案例类型", "作者排名","积分"]])

        # 科研成果类别，选择一种进行添加
        tech_class = st.sidebar.selectbox('添加:',('请选择 ↓','科研类获奖','论文或专著','专利或案例'))

        if tech_class == '科研类获奖':
            with st.sidebar:
                with st.form(key='add_item'):
                    stu_id = st.text_input(label='学号')
                    achi_name = st.text_input(label='项目名称')
                    award = st.selectbox('所获奖项',('自然科学奖','科技进步奖','技术发明奖','哲学社会科学奖'))
                    hi = st.selectbox('获奖层次：',('国家级','教育部','省部级','副省级'))
                    level = st.selectbox('获奖等第：',('特等奖','一等奖','二等奖','三等奖','青年科学奖/青年成果奖'))
                    ranking = st.text_input(label='排名')
                    submit_button = st.form_submit_button(label='添加')

                    if submit_button == True:
                        if stu_id =='' or achi_name=='':
                            st.info('学号和项目名称不能为空！')
                        else:
                            p = points['tech_award']
                            # 计算该项加分
                            score = p['type'][award] * p['hierarchy'][hi] * p['level'][level] * p['ranking'][float(ranking)]
                            new_data = pd.DataFrame([stu_id,achi_name,award,hi,level,ranking,score]).T
                            # 更新到数据表中
                            new_data.to_csv('records/tech_award_records.csv', mode='a', header=False, index=False,
                                        index_label=False)
                            st.dataframe(new_data)
                            st.info("添加成功！")

        elif tech_class == '论文或专著':
            with st.sidebar:
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

                    submit_button = st.form_submit_button(label='添加')
                    if submit_button == True:
                        if stu_id == '' or paper_name == '':
                            st.info('学号和论文名称不能为空！')
                        else:
                            score = calc_paper_score(points['paper'],level,is_inter,count,ranking)
                            new_data = pd.DataFrame([stu_id,paper_name,jour_or_conf,level, ranking,count,score]).T
                            new_data.to_csv('records/paper_records.csv', mode='a', header=False, index=False,
                                        index_label=False)
                            st.dataframe(new_data)
                            st.info("添加成功！")

        elif tech_class == '专利或案例':
            with st.sidebar:
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
                    submit_button = st.form_submit_button(label='添加')
                    if submit_button == True:
                        if stu_id == '' or case_name == '':
                            st.info('学号和案例名称不能为空！')
                        else:
                            score = calc_paper_score(points['case'],level,False,count,ranking)
                            new_data = pd.DataFrame([stu_id,case_name,level,ranking,count,score]).T
                            new_data.to_csv('records/case_records.csv', mode='a', header=False, index=False,
                                        index_label=False)
                            st.dataframe(new_data)
                            st.info("添加成功！")

    elif view_stu_info=="科创比赛":
        st.write('---')
        st.write(' **:orange[规则说明]**')
        st.write('- (1) 科创竞赛类获奖仅面向列表中的奖项计分；')
        st.write('- (2) 不同项目的加分可累加记载，同一项目、不同级别比赛不可以累积计算加分，按照最高级别比赛加分；')
        st.write('- (3) 按照最终实际获奖情况及贡献排名计算项目加分。')
        st.write('---')

        st.dataframe(df_prize_rec)

        with st.sidebar:
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

                con_hi = df_con_info[df_con_info.con_name == contest].iloc[0,-1]  # 从表中找到该比赛的层次

                if submit_button == True and stu_id != '':

                    score = points['contest']['hierarchy'][con_hi]*points['contest']['type'][con_type]*points['contest']['level'][con_level]*(1/float(ranking))
                    st.write("该项积分为：",score)

                    new_data=pd.DataFrame([stu_id,contest,con_type,con_level,con_time,ranking,score]).T
                    new_data.to_csv('records/prize_records.csv',mode='a',header=False,index=False,index_label=False)
                    st.dataframe(new_data)
                    st.info('添加成功!')
                if submit_button==True and stu_id == '':
                    st.info("学号不能为空！")

    elif view_stu_info == "社会工作":
        st.write('---')
        st.write(' **:orange[规则说明]**')
        st.write('该项分为活动加分和职务加分两部分。其中，活动加分指参与各类文艺活动和体育赛事；职务加分指担任学生骨干,\
        例如在学校和学院研究生会、各级党组织、班级等担任一定职务。')
        st.write('---')

        st.dataframe(df_work_rec)
        work_score = pd.read_csv('info/work_info.csv')
        work_list = df_work_info['职务类别'].tolist()

        st.sidebar.write('---')
        with st.sidebar:
            with st.form(key ='add_item'):
                stu_id = st.text_input(label='学号')
                work = st.selectbox('职务',work_list)
                submit_button = st.form_submit_button('添加')
                if submit_button == True:
                    if stu_id == '':
                        st.info('学号不能为空')
                    else:
                        score = work_score[work_score.职务类别==work].iloc[0][1]
                        new_data = pd.DataFrame([stu_id, work,score]).T
                        new_data.to_csv('records/work_records.csv', mode='a', header=False, index=False, index_label=False)
                        st.dataframe(new_data)
                        st.info('添加成功！')

    elif view_stu_info=="民主评议":
        st.write('---')
        st.write(' **:orange[规则说明]**：为推进德智体美劳“五育并举”人才培养体系建设，班级民主评议由班级同学从\
        思想政治、品德修养、集体观念、服务同学、参加学生活动五个维度根据学年行为表现对受评人进行评议。民主评议不合格将不具备参评奖学金的资格。')
        st.write(' **:blue[民主评议不合格：]**')
        st.write('- ① 违反法律法规或学校管理规定并受到纪律处分者；')
        st.write('- ②未按时提交个人学年成长总结者（不论是否参与评议环节）；')
        st.write('- ③未参与民主评议者。')

        st.write('---')
        st.dataframe(df_appr_rec)

elif item=="评审办法":
    st.write("**:blue[Part 1. 各专业名额分配]**")
    st.write("按照国家奖学金相关政策确定各专业获奖名额。")

    x = pd.DataFrame(df_stu_info['专业'].unique(),columns=['专业'])
    x['名额'] = 0

    with open("param/quota.json", "r", encoding='utf-8') as f:
        quota = json.load(f)
        for i in x['专业'].tolist():
            x.名额[x.专业==i]=quota[i]
    st.dataframe(x)
    st.write("**:blue[Part 2. 各维度权重设置]**")

    f_xue = open('param/w_xue.json', 'r', encoding='utf-8')
    f_zhuan = open('param/w_zhuan.json', 'r', encoding='utf-8')
    w_xue = json.loads(f_xue.read())
    w_zhuan = json.loads(f_zhuan.read())

    df_w = pd.DataFrame(columns=['维度','权重（学硕）','权重（专硕）'])
    df_w.loc[0] = ['学习成绩',w_xue['course'],w_zhuan['course']]
    df_w.loc[1]= ['科研成果', w_xue['research'],w_zhuan['research']]
    df_w.loc[2]= ['科创竞赛', w_xue['contest'],w_zhuan['contest']]
    df_w.loc[3]= ['社会工作', w_xue['work'],w_zhuan['work']]
    df_w.loc[4]= ['民主评议', w_xue['appr'],w_zhuan['appr']]
    st.dataframe(df_w)
    f_xue.close()
    f_zhuan.close()

    change_rule = st.sidebar.selectbox('修改规则',('选择修改项 ↓','修改名额','修改权重-学硕','修改权重-专硕'))
    st.sidebar.write('---')
    if change_rule =='修改名额':
        with st.sidebar:
            with st.form(key='change_weight'):
                num_dict={}

                for i in df_stu_info['专业'].unique().tolist():
                    num_dict[i] = st.text_input(label=i)

                submit_button = st.form_submit_button(label='修改')
                if submit_button == True:
                    with open('param/quota.json', 'w', encoding='utf-8') as f:
                        f.write(json.dumps(num_dict, ensure_ascii=False))
                    st.info('修改成功！')
    if change_rule == '修改权重-学硕':
        with st.sidebar:
            with st.form(key='xueshuo'):
                course_1 = st.slider(label="考试成绩",min_value=0.0,max_value=1.0,value=0.2)
                research_1 = st.slider(label="科研成果",min_value=0.0,max_value=1.0,value=0.2)
                contest_1 = st.slider(label="科创竞赛",min_value=0.0,max_value=1.0,value=0.2)
                work_1 = st.slider(label="学生工作",min_value=0.0,max_value=1.0,value=0.2)
                appr_1 = st.slider(label="民主评议",min_value=0.0,max_value=1.0,value=0.2)
                butten_xueshuo = st.form_submit_button(label="提交")
                if butten_xueshuo ==True and (course_1+research_1+contest_1+work_1+appr_1)!=1:
                    st.info("权重不为1！")
                if butten_xueshuo == True and (course_1+research_1+contest_1+work_1+appr_1)==1:
                    weight_xueshuo = {}
                    weight_xueshuo["course"]=course_1
                    weight_xueshuo['research']=research_1
                    weight_xueshuo['contest']=contest_1
                    weight_xueshuo['work']=work_1
                    weight_xueshuo['appr']=appr_1

                    with open('param/w_xue.json', 'w', encoding='utf-8') as f:
                        f.write(json.dumps(weight_xueshuo, ensure_ascii=False))
                    st.info("修改成功！")

    if change_rule == '修改权重-专硕':
        with st.sidebar:
            with st.form(key='zhuanshuo'):
                course_2 = st.slider(label="考试成绩",min_value=0.0,max_value=1.0)
                research_2 = st.slider(label="科研成果",min_value=0.0,max_value=1.0)
                contest_2 = st.slider(label="科创竞赛",min_value=0.0,max_value=1.0)
                work_2 = st.slider(label="学生工作",min_value=0.0,max_value=1.0)
                appr_2 = st.slider(label="民主评议",min_value=0.0,max_value=1.0)

                button_zhuanshuo = st.form_submit_button(label="提交")
                if button_zhuanshuo == True and (course_2+research_2+contest_2+work_2+appr_2)!=1:
                    st.info("权重不为1！")
                if button_zhuanshuo == True and (course_2+research_2+contest_2+work_2+appr_2)==1:
                    weight_zhuanshuo = {}
                    weight_zhuanshuo["course"]=course_2
                    weight_zhuanshuo['research']=research_2
                    weight_zhuanshuo['contest']=contest_2
                    weight_zhuanshuo['work']=work_2
                    weight_zhuanshuo['appr']=appr_2

                    with open('param/w_zhuan.json', 'w', encoding='utf-8') as f:
                        f.write(json.dumps(weight_zhuanshuo, ensure_ascii=False))
                    st.info("修改成功！")

elif item=='排名结果':
    st.markdown('国家奖学金排名及名额分配结果')

    # 获取所有专业的名称
    major_list = df_stu_info['专业'].unique().tolist()
    major = st.sidebar.selectbox("选择专业", major_list)

    # 分专业计算各个分项的分值
    # 计算考试成绩的序数排名
    df=df_exam[df_exam.专业==major]

    df_test = get_study_item(df_exam,major)

    # 计算科研成果的序数排名
    df_award = pd.merge(df_tech_award,df_stu_info,how='left',on="学号")[['学号','专业','积分']]
    df_paper = pd.merge(df_paper, df_stu_info, how='left', on="学号")[['学号', '专业', '积分']]
    df_case = pd.merge(df_case, df_stu_info, how='left', on="学号")[['学号', '专业', '积分']]
    dfs= [df_award,df_paper,df_case]
    df_tech = pd.concat(dfs)   # 加一下说是论文/专利还是啥
    # st.dataframe(df_tech)
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

    df_elim = check_qualified(df,df_demo)
    for i in df_elim['学号'].tolist():
        df_final =df_final.drop(df_final[df_final.学号==i].index)


    df_final=df_final.sort_values(by='results', ascending=False)
    df_final['是否获奖'] = '否'

    with open("param/quota.json", "r", encoding='utf-8') as f:
        quota = json.load(f)

    for i in range(int(quota[major])):
        df_final.iloc[i,-1]='是'

    st.dataframe(df_final[['姓名','学号','性别','导师','类型','加权平均分','积分','竞赛积分','活动积分','民主评议得分','results','是否获奖']])
    st.write('**:blue[拟获奖学金的学生名单：]** ')
    roster = ''
    for i in df_final[df_final['是否获奖']=='是']['姓名'].tolist():
        roster =roster+ '  ' + i
    st.markdown(roster)



    st.write('**:blue[无资格名单及原因：]** ')
    st.dataframe(df_elim)

    # st.sidebar.write('---')
    # audit = st.sidebar.button(label='学术直通车申请审核')
else :
    st.write('---')
    st.write('**:blue["学术直通车"申请人名单：]** ')
    st.dataframe(df_app)
    app_list = df_app['学号'].tolist()
    stu_app_id = st.sidebar.selectbox('查看申请人信息',app_list)
    st.write('---')
    st.write('申请人：'+ str(stu_app_id) )
    if st.button(label='通过'):
        # x.名额[x.专业==i]=quota[i]
        df_app.状态[df_app.学号==stu_app_id]='通过'
        #st.dataframe(df_app)
        st.info('修改成功!')
        df_app.to_csv('records/application.csv',index=False,encoding='utf-8')

    if st.button(label='不通过'):
        df_app.状态[df_app.学号 == stu_app_id] = '不通过'
        st.info('修改成功!')
        df_app.to_csv('records/application.csv', index=False,encoding='utf-8')
        #st.dataframe(df_app)

    st.write('**:blue[（1）学习成绩]** ')
    grades = df_exam[(df_exam.学号 ==stu_app_id) & (df_exam.是否必修=='是')]
    st.dataframe(grades)
    # if grades[grades.考核方式=='score']['成绩'].apply(pd.to_numeric).values.all() >= 60 :
    #    st.write("**:green[学习成绩满足要求。]**")

    st.write('**:blue[（2）科研成果]** ')
    st.dataframe(df_prize_rec[df_prize_rec.学号 == stu_app_id])
    st.dataframe(df_paper[df_paper.学号 == stu_app_id])

    st.write('**:blue[（3）民主评议]** ')
    if df_demo[df_demo.学号==stu_app_id]['民主评议结果'].iloc[0]!='不合格':
        st.write("民主评议结果"+df_demo[df_demo.学号==stu_app_id]['民主评议结果'].iloc[0]+",**:green[满足要求！]**")
    else:
        st.write("**:red[民主评议结果不合格，未达到要求。]**")







