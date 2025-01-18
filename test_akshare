import streamlit as st
import akshare as ak
import pandas as pd
import datetime
import time

AMOUNT = 10000 #每次交易总金额
MAX_BUY = 3  # 买入股票最大数量
BIG_ORDER_RATIO_THRESHOLD = 25# 大单净比阈值
SELL_RATIO=2 #分多少批次卖出 分2次卖出(测试)
STOP_LOSS_THRESHOLD=0.05 #止损幅度 下跌5%止损


UP_LIMIT_DF = pd.DataFrame(columns=['代码', '名称', '最新价', '涨跌幅', '昨收', '换手率', '流通市值', '涨速', '大单净比'])
def get_ticket_info(retry_count=3, delay=5):
    """
    获取A股实时行情数据，并在发生错误时进行重试。
    
    :param retry_count: 最大重试次数，默认3次
    :param delay: 每次重试间隔时间，单位为秒，默认5秒
    :return: DataFrame 格式的股票数据，或在所有重试失败时返回 None
    """
    attempt = 0
    while attempt < retry_count:
        try:
            # 尝试获取股票实时数据
            df = ak.stock_zh_a_spot_em()
            # 选择所需的列
            selected_columns = df.loc[:, ['代码', '名称', '最新价', '涨跌幅', '昨收', '换手率', '流通市值','涨速']]
            return selected_columns
        except Exception as e:
            # 捕获所有异常
            print(f"尝试获取数据失败，第 {attempt + 1} 次重试，错误信息：{e}")
            attempt += 1
            if attempt < retry_count:
                print(f"等待 {delay} 秒后重试...")
                time.sleep(delay)  # 等待指定时间后重试
            else:
                print("重试次数已用完，获取数据失败。")
                return None

def executeCycle(UP_LIMIT_DF):
    # 上一周期未涨停，这一周期涨停排单
    # UP_LIMIT_DF：记录涨停的票
    # CANDIDATE_DF：这一周期的候选票（需要知道涨停价格，当满足涨停价-1、大单净比>20时，即可）
    # CANDIDATE_LAST_DF：上一周期的票（暂时用不到，不过它是正确的）
    # last_df：上一周期行情数据
    """
    执行周期函数，筛选出符合条件的股票：
    条件：首板第一次涨停，本周期涨停，且大单净比 > 25，最多筛选 3 个股票，非一字涨停板
    """

    # 获取当前周期股票信息
    df = get_ticket_info()
    # 获取主板股票数据
    mainBoarddata = df[df['代码'].str.startswith(('00', '60'))].copy()

    # 计算涨停价：昨收价 * 1.1，四舍五入
    mainBoarddata['涨停价'] = mainBoarddata['昨收'] * 1.1
    mainBoarddata['涨停价'] = mainBoarddata['涨停价'].round(2)
    
    # 筛选出当前价格等于或接近涨停价的股票
    upLimitNow = mainBoarddata[mainBoarddata['最新价'] == mainBoarddata['涨停价']]
    
    # 只关注首板第一次涨停的股票(第一次读取所有涨停票，而不是涨停过的票，正常从头到尾运行的话就没问题)
    first_time_up_limit = upLimitNow[~upLimitNow['代码'].isin(UP_LIMIT_DF['代码'])]
    # 将 stock_individual_fund_flow_rank 按 '代码' 合并到 merged_df 中，添加大单净比_当前列
    stock_individual_fund_flow_rank = ak.stock_individual_fund_flow_rank(indicator="今日")
    stock_individual_fund_flow_rank['今日主力净流入-净占比'] = pd.to_numeric(stock_individual_fund_flow_rank['今日主力净流入-净占比'], errors='coerce') # 检查数据类型
    first_time_up_limit = pd.merge(
        first_time_up_limit, 
        stock_individual_fund_flow_rank[['代码', '今日主力净流入-净占比']], 
        left_on='代码', 
        right_on='代码', 
        how='left'
    )
    # 重命名 '今日主力净流入-净占比' 列为 '大单净比_当前'
    first_time_up_limit.rename(columns={'今日主力净流入-净占比': '大单净比'}, inplace=True)
    if UP_LIMIT_DF.empty:
        UP_LIMIT_DF = first_time_up_limit
    else:
        # 找出 upLimitNow 中不在 UP_LIMIT_DF 的数据，追加到 UP_LIMIT_DF 中
        UP_LIMIT_DF = pd.concat([UP_LIMIT_DF, first_time_up_limit], ignore_index=True)
    # 当前周期的选股逻辑
    if not first_time_up_limit.empty:
            # 选择 df 中代码字段等于 first_time_up_limit 中代码的数据，创建新的 candidate_now_df
            candidate_now_df = pd.merge(first_time_up_limit['代码'], df, on='代码', how='inner')
            candidate_now_df = pd.merge(
                candidate_now_df, 
                stock_individual_fund_flow_rank[['代码', '今日主力净流入-净占比']], 
                left_on='代码', 
                right_on='代码', 
                how='left'
            )
            # 重命名 '今日主力净流入-净占比' 列为 '大单净比_当前'
            candidate_now_df.rename(columns={'今日主力净流入-净占比': '大单净比'}, inplace=True)

            # 给 candidate_now_df 的列名添加 '_当前' 后缀
            candidate_now_df = candidate_now_df.add_suffix('_当前')

            # 选择满足以下条件的数据：
            # 1. 本周期涨停(默认是涨停的了)
            # 2. 本周期的价格高于上一周期价格 (默认不是一字涨停，一字涨停第一个循环就被加到上一周期的候选票中，没有额外做处理操作)
            # 3. 大单净比 > BIG_ORDER_RATIO_THRESHOLD = 20（自己在上面定义）
            candidate_select_df = candidate_now_df[
                (candidate_now_df['大单净比_当前'] > BIG_ORDER_RATIO_THRESHOLD)
            ]

            print("=================================candidate_select_df=================================")
            print(candidate_select_df)
            print("=================================candidate_select_df=================================")
            # 从候选中选择最多 3 个股票
            candidate_select_df = candidate_select_df.head(MAX_BUY)

            # 指定要保存的列
            columns_to_save = ['代码', '名称', '最新价', '涨跌幅', '昨收', '换手率', '流通市值','涨速', '大单净比']
            
            # 选择特定列，并将数据复制到新的 DataFrame
            result_df = candidate_select_df[['代码_当前', '名称_当前', '最新价_当前', '涨跌幅_当前', '昨收_当前', '换手率_当前',
                                             '流通市值_当前', '涨速_当前', '大单净比_当前']].copy()
            print("=================================result_df=================================")
            print(result_df)
            print("=================================result_df=================================")
            # 重命名列名
            result_df.rename(columns={
                '代码_当前': '代码',
                '名称_当前': '名称',
                '最新价_当前': '最新价',
                '涨跌幅_当前': '涨跌幅',
                '昨收_当前': '昨收',
                '换手率_当前': '换手率',
                '流通市值_当前': '流通市值',
                '涨速_当前':'涨速',
                '大单净比_当前': '大单净比'
            }, inplace=True)
            st.write("=================================result_df=================================")
            st.dataframe(result_df)
            st.write("=================================result_df=================================")
            return UP_LIMIT_DF
# Streamlit 应用程序

st.title("打板生成器")
if st.button("点击开始"):
    while True:
        dateTime = datetime.datetime.now()
        now = dateTime.time()
        current_day = dateTime.weekday()  # 获取当前星期几，星期一是0，星期天是6
        begin = 1
        # 判断是否为工作日（周一到周五）
        if current_day >= 0 and current_day <= 4:  # 工作日
            # 早上9:25开始执行
            if now >= datetime.time(9, 25) and now <= datetime.time(11, 30):
                # 每天早上执行一次，重置所有外部参数
                if begin != 0:
                    begin = 0

                    UP_LIMIT_DF = pd.DataFrame(columns=['代码', '名称', '最新价', '涨跌幅', '昨收', '换手率', '流通市值', '涨速', '大单净比'])
                    CANDIDATE_DF = pd.DataFrame(columns=['代码', '名称', '最新价', '涨跌幅', '昨收', '换手率', '流通市值', '涨速', '大单净比'])
                    CANDIDATE_LAST_DF = pd.DataFrame(columns=['代码', '名称', '最新价', '涨跌幅', '昨收', '换手率', '流通市值', '涨速', '大单净比'])
                    # 记录上一周期行情数据
                    last_df = pd.DataFrame(columns=['代码', '名称', '最新价', '涨跌幅', '昨收', '换手率', '流通市值', '涨速', '大单净比'])
                st.write(f"runing morning...{now}")
                UP_LIMIT_DF = executeCycle(UP_LIMIT_DF)
            # time.sleep(2)  # 休息
            # 下午1:00开始执行
            elif now >= datetime.time(13, 0) and now <= datetime.time(15, 0):
                st.write(f"runing morning...{now}")
                UP_LIMIT_DF = executeCycle(UP_LIMIT_DF)
            else:
                # 非交易时间段，休息一段时间（例如 5 分钟），避免过于频繁的检查，并且更新为新的一天
                if now <= datetime.time(9, 25) or now >= datetime.time(15, 0):
                    if begin != 1:
                        begin = 1
                st.write("rest...")
                time.sleep(300)  # 休息
        else:
            # 如果是非工作日（周六和周日），退出程序
            st.write("Non-trading day. Resting until Monday morning.(非工作日休息，请等工作日再启动)")
            break
            # 如果是非工作日（周六和周日），程序休眠直到下一个工作日
            # 休眠 24 小时 * 60 分钟 * 60 秒 = 86400 秒，直到第二天
            # time.sleep(86400)

    
