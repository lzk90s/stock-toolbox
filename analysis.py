import matplotlib.pyplot as plt
import pandas as pd

import db


def f1():
    sql = '''
        select st.code_name , st.industry , st.code,  kdata.date, kdata.close, kdata.pe_ttm, kdata.pe_ttm_inc from t_stock_k_data kdata 
        inner join t_stock_industry st on st.code = kdata.code where kdata.pe_ttm  >=40 and kdata.`close` >=30 and kdata.pe_ttm_inc > 5
        order by st.industry,st.code,kdata.date
    '''
    data = pd.read_sql_query(sql, db.database)

    data.describe()
    df = data.groupby(["code", "date"]).agg("mean")

    plt.plot(df)
    plt.xlabel('时间')
    plt.ylabel('pe-TTM')
    plt.show()


def f2():
    sql = '''
        select * from (
            select st.code_name, st.industry, st.code, avg(kdata.pe_ttm_inc) as avg_pe_ttm_inc from t_stock_k_data kdata 
            inner join t_stock_industry st on st.code = kdata.code where kdata.pe_ttm  BETWEEN 40 and 1000 and kdata.`close` >=30 group by st.code ) t
        where t.avg_pe_ttm_inc > 5 order by avg_pe_ttm_inc;    
    '''


def f3():
    sql = '''
        select * from (
            select st.code_name, st.industry, st.code, avg(kdata.pe_ttm_inc) as avg_pe_ttm_inc, min(kdata.pe_ttm_inc) as min_pe_ttm_inc from t_stock_k_data kdata 
            inner join t_stock_industry st on st.code = kdata.code where kdata.pe_ttm  BETWEEN 40 and 1000 and kdata.`close` >=30 group by st.code ) t
        where t.avg_pe_ttm_inc > 5  order by avg_pe_ttm_inc;    
    '''


if __name__ == '__main__':
    f2()
