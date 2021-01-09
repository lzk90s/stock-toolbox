import pandas as pd
import pandas_profiling
import db

if __name__ == '__main__':
    sql = '''
    select b.code_name , b.industry , a.code, a.open, a.pe_ttm from t_stock_k_data a 
    inner join t_stock_industry b on a.code = b.code where pe_ttm  >=50 and `open` >=30 order by industry
    '''
    data = pd.read_sql_query(sql, db.database)

    data.describe()

    profile = data.profile_report(title='Stock Dataset')
    profile.to_file(output_file='data/stock_report.html')
