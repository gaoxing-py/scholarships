import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False

# 无资格名单及理由
def check_qualified(df,df_demo_appr):
    # 检查必修不及格的学生
    df = df[(df.是否必修=='是') & (df.考核方式=='score')]
    df['成绩'] = df['成绩'].astype(float)
    df = df[ df.成绩 < 60 ]
    df = df._append(df[(df.是否必修=='是') & (df.考核方式=='T/F') & (df.成绩=='F')])
    df = df[['学号','姓名']]

    df['原因'] = "必修课程不及格"
    df = df.drop_duplicates(subset=['学号'])

    # 检查民主评议不不合格的学生
    df_demo = df_demo_appr[df_demo_appr.民主评议结果=='不合格']
    id_list= df_demo['学号'].tolist()
    for id in id_list:
        if id in df['学号'].tolist():
            df[df.学号==id]['原因'] = '必修课程不及格;民主评议不合格'
            id_list.remove(id)
        if len(id_list)!=0 :
            df_demo['原因'] = '民主评议不合格'
            df_demo=df_demo[['学号','姓名','原因']]
            df = df._append(df_demo)
    return df


# 计算考试加权平均分 imput: df,成绩所在列,学分所在列
def weighted_average(dataframe, value, weight):
    val = dataframe[value]
    wt = dataframe[weight]
    # if val.count()>9:
    #    val=val.sort_values(by=value,ascending=False)[:9]
    return (val * wt).sum() // wt.sum()

# 序数排序法
def ranked_score(df):
    max = df.iloc[:,-1].max()
    df.iloc[:,-1] = 100/max * df.iloc[:,-1]
    return df

# 计算每个分项的得分，返回df格式，包含两列 stu_id,该项分数
def get_study_item(df_exam,major):

    # 筛选出该专业的学生必修课考试记录
    df = df_exam[df_exam.专业 == major]
    df = df[df.是否必修=='是']
    # 专硕 or 学硕
    stu_type = df['类型'].iloc[0]
    if stu_type == '学硕':
        class_num = 9
        score_sum = 20
    else:
        class_num = 6
        score_sum = 18

    df_weighted_grades=pd.DataFrame(columns=['学号','加权平均分'])
    stu_id=df['学号'].unique().tolist()

    # 对每个学生，取其最高的9门 or 6门成绩 计算加权平均分
    for i in stu_id:
        df_i = df[df.学号 == i]
        df_i['成绩'] = df_i['成绩'].apply(pd.to_numeric)
        finished_score= df_i['学分'].sum()
        w = 1
        if finished_score < score_sum:
            if finished_score > score_sum * 0.85:
                w = 0.99
            elif finished_score > score_sum * 0.7:
                w = 0.98
            elif finished_score > score_sum * 0.55:
                w=0.97
            elif finished_score > score_sum * 0.4:
                w=0.96
            elif finished_score > score_sum * 0.25:
                w=0.95
            else:
                w=0.94

        if df_i.shape[0] > class_num:
            df_i.sort_values(by="成绩", inplace=True, ascending=False)
            df_i = df_i.iloc[:class_num]

        df_i = df_i[['成绩','学分']].apply(pd.to_numeric)
        results = (df_i['成绩']*df_i['学分']).sum()/df_i['学分'].sum()*w

        df_weighted_grades.loc[len(df_weighted_grades.index)] = [i,results]
    # 进行序数排序的转换
    return  ranked_score(df_weighted_grades)

def get_research_item(df_research,major):
    df_research = df_research[df_research.专业 == major]
    stu_id=df_research['学号'].unique().tolist()
    df_research_rank=pd.DataFrame(columns=['学号','积分'])
    for i in stu_id:
        df_i = df_research[df_research.学号==i]
        df_i['积分'] = df_i['积分'].apply(pd.to_numeric)
        df_research_rank.loc[len(df_research_rank.index)]=[i,df_i['积分'].sum()]
    return ranked_score((df_research_rank))

def get_contest_item(df_con,major):
    df_con = df_con[df_con.专业 == major]
    stu_id=df_con['学号'].unique().tolist()
    df_con_rank=pd.DataFrame(columns=['学号','竞赛积分'])
    for i in stu_id:
        df_i = df_con[df_con.学号==i]
        df_i['积分'] = df_i['积分'].apply(pd.to_numeric)
        df_con_rank.loc[len(df_con_rank.index)]=[i,df_i['积分'].sum()]
    return ranked_score((df_con_rank))


def get_work_item(df_social_work,major):
    df_social_work=df_social_work[df_social_work.专业 == major]
    stu_id = df_social_work['学号'].unique().tolist()
    df_social_result = pd.DataFrame(columns=['学号','活动积分'])
    for i in stu_id:
        df_i = df_social_work[df_social_work.学号 == i]
        df_i['活动积分'] = df_i['活动积分'].apply(pd.to_numeric)
        df_social_result.loc[len(df_social_result.index)]=[i,df_i['活动积分'].sum()]
    return ranked_score(df_social_result)

def get_appr_item():
    pass


def calc_final_score(w,dfs):
    df_all = pd.concat(dfs)
    df_all=df_all.fillna(value=0)

    #df_all['results'] = dfs['加权平均分']*w['course']+ dfs['科研积分'] * w['research'] + \
    #                    dfs['竞赛积分'] * w['contest']+dfs['活动积分']*w['work'] + dfs['民主评议得分']*w['appr']
    return df_all


    # st.write(results)


def EDA(df):

    fig,axes = plt.subplots(1,3,figsize=(16,4),sharex=False,sharey=False)

    # 绘制男女性别比图
    x_1 = [df[df.性别 == '男'].shape[0], df[df.性别 == '女'].shape[0]]
    labels_1 = ['男', '女']
    axes[0].pie(x_1, labels=labels_1,colors=['#DC143C','#FA8072'], explode=(0, 0.2),autopct='%.2f%%')

    # 绘制专硕/学硕比例图
    #data = df['类型'].value_counts()
    x_2 = [df[df.类型 == '学硕'].shape[0], df[df.类型 == '专硕'].shape[0]]
    labels_2 = ['学硕', '专硕']
    axes[1].pie(x_2,labels=labels_2,colors=['#DC143C','#FA8072'], explode=(0, 0.2),autopct='%.2f%%')

    # 绘制个专业人数分布图
    data = df['专业'].value_counts()
    axes[2].bar(df['专业'].unique(),data,color='#F08080')

    plt.xticks(rotation=30)

    return fig

def calc_paper_score(dict,level,is_inter,count,ranking):
    score = 0
    ranking = float(ranking)
    count = float(count)
    if is_inter:
        if (level[0]=='a' and ranking<=6) or (level[0]=='b' and ranking<=5) or \
                (level[0]=='c' and ranking<=4) or level[0]=='d' and ranking<=3:
            if count == 2:
                if ranking==1:
                    score = dict[level[0]]*0.6
                else:
                    score = dict[level[0]] * 0.4
            if count == 3:
                if ranking==1:
                    score = dict[level[0]] * 0.5
                if ranking==2:
                    score = dict[level[0]] * 0.3
                if ranking==3:
                    score = dict[level[0]] * 0.2
            if count == 4:
                if ranking ==1:
                    score = dict[level[0]] * 0.5
                if ranking == 2:
                    score = dict[level[0]] * 0.25
                if ranking == 3:
                    score = dict[level[0]] * 0.15
                if ranking == 4:
                    score = dict[level[0]] * 0.1
            if count == 5:
                if ranking ==1:
                    score = dict[level[0]] * 0.45
                if ranking == 2:
                    score = dict[level[0]] * 0.25
                if ranking == 3:
                    score = dict[level[0]] * 0.15
                if ranking == 4:
                    score = dict[level[0]] * 0.075
                if ranking == 5:
                    score = dict[level[0]] * 0.075
            if count>=6:
                if ranking == 1:
                    score = dict[level[0]] * 0.45
                if ranking == 2:
                    score = dict[level[0]] * 0.25
                if ranking == 3:
                    score = dict[level[0]] * 0.1
                if ranking >=4:
                    score = dict[level[0]] * 0.2/(count-ranking)
    else:
        if count == 2 :
            if ranking == 1 :
                score = dict[level[0]]*0.6
            else:
                score = dict[level[0]]*0.4
        if count ==3:
            if ranking ==1:
                score = dict[level[0]] * 0.5
            elif ranking==2:
                score = dict[level[0]] * 0.3
            else:
                score = dict[level[0]] * 0.2
        if count>=4:
            if ranking ==1:
                score = dict[level[0]] * 0.5
            elif ranking==2:
                score = dict[level[0]] * 0.25
            elif ranking==3:
                score = dict[level[0]] * 0.15
            elif ranking==4:
                score = dict[level[0]] * 0.1
            else:
                score=0
    return score
