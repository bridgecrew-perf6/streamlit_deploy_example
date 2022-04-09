path = r"C:\Users\tclyu\Dropbox\thomas_home\active_portfolio_management\data\universe\refinitiv_Russell3000_20220302.csv"
import pandas as pd

df = pd.read_csv(path)
df.columns = df.columns.str.replace(r'TR.', '')
print(df)
print('hello')
df.set_index(['TICKERSYMBOL'],inplace=True)
print(df.loc['C'][['ISIN','COMMONNAME','GICSINDUSGROUP','GICSSECTOR','IPODATE']])
df
static_data_df = pd.DataFrame({"ISIN":        "US1729674242",
"COMMONNAME":        "Citigroup Inc",
"GICSINDUSGROUP":            "Banks",
"GICSSECTOR":           "Financials",
"IPODATE":              "1986-10-30"}, index=[0]).T
print(static_data_df)