import cbrapi as cbr
cbr.get_currencies_list()
df = cbr.get_time_series(symbol = 'USD', first_date = '2019-01-01', last_date = '2020-12-31', period = 'M')
df = plot(title = 'График курсаUSD/RUB')