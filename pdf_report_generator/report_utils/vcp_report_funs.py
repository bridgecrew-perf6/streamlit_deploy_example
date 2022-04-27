def get_factors_df(vcp_slice):
    import pandas as pd

    vcp_slice_dict = vcp_slice.to_dict(orient='records')[0]
    factor_df = pd.DataFrame([[vcp_slice_dict['RSSCORE'], vcp_slice_dict['SCTRSCORE'], vcp_slice_dict['MRSQUARE']],
    [vcp_slice_dict['RSSCORE_SECTOR_MEDIAN'], vcp_slice_dict['SCTRSCORE_SECTOR_MEDIAN'], vcp_slice_dict['MRSQUARE_SECTOR_MEDIAN']],
    [vcp_slice_dict['RSSCORE_SECTOR_RANK'], vcp_slice_dict['SCTRSCORE_SECTOR_RANK'],vcp_slice_dict['MRSQUARE_SECTOR_RANK']]])
    factor_df.columns = ['Relative strength','SCTR','Regression']
    factor_df.index = ['score','sector median', 'rank in sector']
    factor_df = factor_df.round(2)
    factor_df = factor_df.reset_index()
    factor_df = factor_df.rename(columns={'index': ''})
    return factor_df


def get_stock_info(vcp_slice):
    import pandas as pd
    vcp_slice_dict = vcp_slice.to_dict(orient='records')[0]
    stock_info={}
    stock_info["ticker"] = vcp_slice_dict['ticker']
    last_close_price = vcp_slice_dict['adjclose']
    stock_info["adjclose"] = last_close_price
    stock_info['Industry'] = vcp_slice_dict['TR.GICSINDUSTRY']
    stock_info['Industry Group'] = vcp_slice_dict['TR.GICSINDUSTRYGROUP']
    stock_info['Sector'] = vcp_slice_dict['TR.GICSSECTOR']
    stock_info_df = pd.DataFrame(stock_info,index=[0]).T
    stock_info_df.columns =["Stock info"]
    stock_info_df.reset_index(inplace=True)
    stock_info_df = stock_info_df.rename(columns={'index': ''})
    return stock_info_df

def get_vcp_properties_df(vcp_slice,contractions_df):
    import pandas as pd

    vcp_slice_dict = vcp_slice.to_dict(orient='records')[0]
    vcp_property={}
    #last_close_price = vcp_slice_dict['adjclose']
    entry_price = vcp_slice_dict['latest_contraction_price']
    # this is the VCP footprint that MM uses
    vcp_property['footprint'] = str(round(vcp_slice_dict['total_duration'] / 5)) + "W-" + \
                                 str(round(vcp_slice_dict['contraction_ratio'])) + '-' + str(vcp_slice_dict['number_of_consolidations'])+ 'T'

    vcp_property['first detected date'] = vcp_slice_dict['earliest_vcp_scanned_date']
    vcp_property['total duration (days)'] = round(vcp_slice_dict['total_duration'])
    vcp_property['N contractions']= vcp_slice_dict['number_of_consolidations']
    vcp_property["SL"] = contractions_df.iloc[-1]['support_price']
    vcp_property["2R"] = round(entry_price * (1 + 2 * vcp_slice_dict['latest_contraction_pct']), 2)
    vcp_property["4R"] = round(entry_price * (1 + 4 * vcp_slice_dict['latest_contraction_pct']), 2)

    vcp_supplementary={}
    vcp_supplementary["is_break_out_latest_contraction"] = bool(vcp_slice_dict['is_break_out_latest_contraction'])
    vcp_supplementary["is_break_out_first_contraction"] = bool(vcp_slice_dict['is_break_out_first_contraction'])
    vcp_supplementary['SW stage2'] = str(vcp_slice_dict['SW_stage2'])
    vcp_supplementary['MM Trend filtered'] = str(vcp_slice_dict['MM_Stage2Filtered'])
    vcp_supplementary['Volume contraction'] = str(vcp_slice_dict['volume_contraction_condition'])


    vcp_property_df = pd.DataFrame(vcp_property,index=[0]).T
    vcp_property_df.columns =["VCP info"]
    vcp_property_df.reset_index(inplace=True)
    vcp_property_df = vcp_property_df.rename(columns={'index': ''})

    vcp_supplementary_df = pd.DataFrame(vcp_supplementary,index=[0]).T
    vcp_supplementary_df.columns =["Supplementary info"]
    vcp_supplementary_df.reset_index(inplace=True)
    vcp_supplementary_df = vcp_supplementary_df.rename(columns={'index': ''})

    return vcp_property_df, vcp_supplementary_df




def vcp_plot_for_report(ohlcv_df, vcp_slice):
    # this is leaned down to display better data
    from utils.vcp_plottings import add_contraction_lines
    from utils.vcp_utils import get_contractions_from_vcp_df
    current_scan_date = vcp_slice.iloc[0]['datetime']
    ticker = vcp_slice.iloc[0]['ticker']
    # subset data
    ohlcv_df_tmp = ohlcv_df.reset_index().copy()

    def clean_up_axis(fig, ticker, date_str, use_title=True, range_slide_on=True):
        if use_title:
            generate_title = "TICKER=" + ticker + ",DATE=" + date_str  # + ",volume_slope=" + str(
        else:
            generate_title = ""
        # https://plotly.com/python/time-series/#hiding-weekends-and-holidays
        fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"]), ])  # hide weekends
        fig.update_layout(title_text=generate_title)
        fig.update_layout(
            autosize=True,
            width=1000,
            height=600,
            margin=dict(l=20, r=50, t=50, b=20),
            title_text=generate_title,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        fig.update_xaxes(showgrid=True, gridwidth=0.01, gridcolor='Black', automargin=False)
        fig.update_yaxes(showgrid=True, gridwidth=0.01, gridcolor='Black', automargin=False)
        fig.update(layout_xaxis_rangeslider_visible=range_slide_on)
        return fig

    def simple_plot(ticker, ohlcv_df_tmp):
        from utils import vcp_plottings

        from plotly.subplots import make_subplots
        import plotly.graph_objects as go
        import plotly.io as pio

        pio.templates.default = "plotly_dark"

        # creating subplot, 2x1, shared x-axis
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.01, row_heights=[0.8, 0.2])

        #####################
        #####################
        colors = []
        INCREASING_COLOR = "GREEN"
        DECREASING_COLOR = "RED"
        for i in range(len(ohlcv_df.close)):
            if i != 0:
                if ohlcv_df.close[i] > ohlcv_df.close[i - 1]:
                    colors.append(INCREASING_COLOR)
                else:
                    colors.append(DECREASING_COLOR)
            else:
                colors.append(DECREASING_COLOR)
        # plot candles
        fig.add_trace(
            go.Candlestick(x=ohlcv_df['date'], open=ohlcv_df['open'], high=ohlcv_df['high'], low=ohlcv_df['low'],
                           close=ohlcv_df['close'], name=ticker), row=1, col=1)

        # plot volume bar
        fig.add_trace(go.Bar(x=ohlcv_df['date'], y=ohlcv_df['volume'], name='volume', marker_color=colors), row=2,
                      col=1)
        fig.add_trace(go.Scatter(x=ohlcv_df['date'], y=ohlcv_df['volume'].rolling(50).mean(), name='volume sma(50)',
                                 mode='lines'), row=2, col=1)
        return fig

    fig = simple_plot(ticker, ohlcv_df_tmp)
    merged_contractions = get_contractions_from_vcp_df(vcp_slice)
    if not merged_contractions.empty:
        fig = add_contraction_lines(fig, merged_contractions)

    fig, clean_up_axis(fig, ticker, current_scan_date,range_slide_on=False)
    return fig



def make_plots(ticker, vcp_slice, ohlcv_df, export_dir):
    import os
    import datetime
    import pandas as pd
    from utils.vcp_utils import get_contractions_from_vcp_df
    from pdf_report_generator.report_utils.graph_conversion import export_plotly_2_png

    factors_df = get_factors_df(vcp_slice)
    stockinfo_df = get_stock_info(vcp_slice)
    contractions_df = get_contractions_from_vcp_df(vcp_slice)
    vcp_property_df, vcp_supplementary_df = get_vcp_properties_df(vcp_slice, contractions_df)

    from pathlib import Path
    Path(export_dir).mkdir(exist_ok=True)

    fig = vcp_plot_for_report(ohlcv_df, vcp_slice)
    ts_plot_path = export_plotly_2_png(fig,ticker+".html", export_dir)

    # cosmetics for contractions dataframe
    contractions_df = contractions_df[['start_dt_index','end_dt_index',"support_price","resis_price","contraction_pct"]]
    contractions_df['contraction_pct'] = (contractions_df['contraction_pct']*100).round(2)
    contractions_df['duration'] = (pd.to_datetime(contractions_df['end_dt_index'])-pd.to_datetime(contractions_df['start_dt_index'])).apply(lambda x: x.days)
    contractions_df = contractions_df.rename(columns={'start_dt_index':'start', 'end_dt_index': 'end','support_price':"support","resis_price":"resis", "contraction_pct":'%'})
    return stockinfo_df, vcp_property_df, vcp_supplementary_df, factors_df, contractions_df, ts_plot_path




if __name__ == "__main__":
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    # *************************************************
    # =================== prepare_fullframe_vcp_data =============#
    import os
    import pandas as pd

    local_dir = r"/Downloaded_data"
    VCP_DF_PATH = os.path.join(local_dir, "LIVEVCP.csv")
    STOCKBASIS_DF_PATH = os.path.join(local_dir, "STOCKBASIS.csv")

    # this is load VCP without streamlit
    import pandas as pd

    vcp_df = pd.read_csv(VCP_DF_PATH)
    vcp_df = vcp_df.drop(['RSSCORE', 'SCTRSCORE', 'MRSQUARE'], axis=1, errors='ignore')

    # this is load STOCKBASIS without streamlit
    import pandas as pd

    stockbasis_df = pd.read_csv(STOCKBASIS_DF_PATH, index_col=[0])

    vcp_full_frame = vcp_df.join(stockbasis_df, on=['ticker'], how='inner')

    # ============================== OHLCV dic load ============================#
    ticker = "ACHC"
    from utils.load_data import convert_single_equity_2_df

    OHLCV_PICKLE = os.path.join(local_dir, "OHLCVDICT.pickle")
    ts_df = pd.read_pickle(OHLCV_PICKLE)
    ticker_specific_df = convert_single_equity_2_df(ts_df, ticker)
    ticker_specific_df.reset_index(inplace=True)

    ohlcv_df = ticker_specific_df

    vcp_slice = vcp_full_frame[vcp_full_frame["ticker"] == ticker]

    export_dir="hello"
    stockinfo_df, vcp_property_df, vcp_supplementary_df, factors_df, contractions_df, ts_plot_path = make_plots(vcp_slice, ohlcv_df, export_dir)

    stockinfo_df.to_pickle("stockinfo_df.pkl")
    vcp_property_df.to_pickle('vcp_property_df.pkl')
    vcp_supplementary_df.to_pickle("vcp_supplementary_df.pkl")
    factors_df.to_pickle('factors_df.pkl')
    contractions_df.to_pickle('contractions_df.pkl')