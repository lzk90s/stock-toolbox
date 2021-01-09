import peewee
import os

if not os.path.exists("data"):
    os.mkdir("data")

database = peewee.SqliteDatabase("data/stock.db")
# settings = {'host': 'localhost', 'password': '123456', 'port': 3306, 'user': 'root'}
# database = peewee.MySQLDatabase("stock", **settings)


class BaseModel(peewee.Model):
    class Meta:
        database = database


class StockIndustry(BaseModel):
    update_date = peewee.DateTimeField()
    code = peewee.CharField()
    code_name = peewee.CharField()
    industry = peewee.CharField()
    industry_classification = peewee.CharField()

    class Meta:
        table_name = "t_stock_industry"
        primary_key = peewee.CompositeKey('code')


class StockKData(BaseModel):
    date = peewee.DateTimeField()
    code = peewee.CharField()
    open = peewee.FloatField()
    high = peewee.FloatField()
    low = peewee.FloatField()
    close = peewee.FloatField()
    pre_close = peewee.FloatField()
    volume = peewee.BigIntegerField()
    amount = peewee.BigIntegerField()
    adjust_flag = peewee.BooleanField()
    turn = peewee.FloatField()
    trade_status = peewee.BooleanField()
    pct_chg = peewee.FloatField()
    pe_ttm = peewee.FloatField()
    pe_ttm_inc = peewee.FloatField()

    class Meta:
        table_name = "t_stock_k_data"
        primary_key = peewee.CompositeKey('code', 'date')


def init_tables():
    # sync off
    database.execute_sql(sql="PRAGMA synchronous = OFF;")

    StockIndustry.create_table(fail_silently=True)
    StockKData.create_table(fail_silently=True)
    StockIndustry.truncate_table()
    StockKData.truncate_table()
