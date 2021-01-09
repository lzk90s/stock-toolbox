import datetime

import baostock as bs
import pandas as pd

import db


class StockHelper:
    def __init__(self):
        self.__login()

    def query_stock_industry(self):
        rs = bs.query_stock_industry()
        self.__check_response(rs)

        industry_list = []
        while (rs.error_code == '0') & rs.next():
            industry_list.append(rs.get_row_data())
        result = pd.DataFrame(industry_list, columns=rs.fields)
        return result.to_dict()

    def query_stock_k_data(self, stock_code, start_date, end_date):
        rs = bs.query_history_k_data_plus(stock_code,
                                          "date,code,open,high,low,close,preclose,volume,amount,"
                                          "adjustflag,turn,tradestatus,pctChg,peTTM",
                                          start_date=start_date, end_date=end_date,
                                          frequency="d", adjustflag="3")
        self.__check_response(rs)

        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)
        return result.to_dict()

    def __check_response(self, response):
        if int(response.error_code) != 0:
            raise Exception(response.error_msg)

    def __login(self):
        lg = bs.login()
        self.__check_response(lg)

    def __logout(self):
        bs.logout()


stock_helper = StockHelper()


def get_stock_industry():
    stock_industry = stock_helper.query_stock_industry()
    for idx, code in stock_industry["code"].items():
        data = {
            "code": code,
            "update_date": stock_industry["updateDate"][idx],
            "code_name": stock_industry["code_name"][idx],
            "industry": stock_industry["industry"][idx],
            "industry_classification": stock_industry["industryClassification"][idx]
        }
        db.StockIndustry.insert(data).on_conflict_replace().execute()


def get_latest_n_day_stock_k_data(stock_code, n_days):
    start_date = (datetime.datetime.now() + datetime.timedelta(days=-(n_days + 1))).strftime("%Y-%m-%d")
    end_date = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")

    k_data = stock_helper.query_stock_k_data(stock_code, start_date, end_date)
    if not k_data:
        return []

    tmp_pe_ttm = 0
    for idx, day in k_data["date"].items():
        pe_ttm = float(k_data["peTTM"][idx])
        if tmp_pe_ttm == 0:
            tmp_pe_ttm = pe_ttm
        # 统计周期内的pe ttm增量
        pe_ttm_inc = pe_ttm - tmp_pe_ttm

        data = {
            "date": day,
            "code": k_data["code"][idx],
            "open": k_data["open"][idx],
            "high": k_data["high"][idx],
            "low": k_data["low"][idx],
            "close": k_data["close"][idx],
            "pre_close": k_data["preclose"][idx],
            "volume": k_data["volume"][idx],
            "amount": k_data["amount"][idx],
            "adjust_flag": k_data["adjustflag"][idx],
            "turn": k_data["turn"][idx],
            "trade_status": k_data["tradestatus"][idx],
            "pct_chg": k_data["pctChg"][idx],
            "pe_ttm": k_data["peTTM"][idx],
            "pe_ttm_inc": pe_ttm_inc
        }

        db.StockKData.insert(data).on_conflict_replace().execute()


def collect_stock_data(n_days=7):
    db.init_tables()

    get_stock_industry()

    stock_list = db.StockIndustry.select().order_by("code")

    idx = 0
    for s in stock_list:
        idx = idx + 1
        get_latest_n_day_stock_k_data(s.code, n_days)
        print("[{}] stock = {}, name = {}, industry = {}".format(idx, s.code, s.code_name, s.industry))


if __name__ == '__main__':
    collect_stock_data(30)
