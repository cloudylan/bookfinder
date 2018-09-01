import tushare as ts
from sqlalchemy import create_engine
import common.stock_configuration as config
import common.datasource as datasource
from sql import StockSQL as sql

start_date = '2015-08-20'
end_date = '2018-08-31'

engine = create_engine('sqlite://%s' % config.db_path)


def get_stock_basic(p_engine):
    basics = ts.get_stock_basics()
    basics.to_csv(config.basics_file_path)
    basics.to_sql('STOCK_BASICS', p_engine, if_exists='append')


def get_historical_data(p_engine):
    print("Get Stock Details.")

    ds = datasource.SqliteDataSource(config.db_path)
    cursor = ds.select(sql.get_basics_by_processed % 'N')
    stock_ids = [item[0] for item in cursor]

    print(stock_ids)

    for s_id in stock_ids:
        get_stock_historical_data(s_id, p_engine)
        ds.update(sql.update_processed % 'Y')
        ds.commit()
        print('Processed: %s' % s_id)


def get_stock_historical_data(stock_id, p_engine):
    stock = ts.get_hist_data(str(stock_id), start=start_date, end=end_date)
    stock.to_csv(config.detail_path % stock_id)
    # fail, replace, append
    stock.to_sql('STOCK_%s' % str(stock_id), p_engine, if_exists='replace')


get_historical_data(engine)
