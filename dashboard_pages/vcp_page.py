import datetime
import streamlit as st
def set_up_time_series_plot(ticker, ohlcv_df):
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go
    #import matplotlib.pyplot as plt
    import plotly.io as pio
    #plt.rcParams['figure.figsize'] = [12, 7]
    #plt.rc('font', size=14)

    pio.templates.default = "plotly_dark"

    # creating subplot, 2x1, shared x-axis
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.2, row_heights=[0.7, 0.3])

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
    fig.add_trace(go.Candlestick(x=ohlcv_df['date'], open=ohlcv_df['open'], high=ohlcv_df['high'], low=ohlcv_df['low'],
                                 close=ohlcv_df['close'], name=ticker), row=1, col=1)

    # plot volume bar
    fig.add_trace(go.Bar(x=ohlcv_df['date'], y=ohlcv_df['volume'], name='volume', marker_color=colors), row=2, col=1)
    fig.add_trace(go.Scatter(x=ohlcv_df['date'], y=ohlcv_df['volume'].rolling(50).mean(), name='volume sma(50)',mode='lines'), row=2, col=1)
    return fig


def add_contraction_lines(fig, merged_contractions):
    # plot horizontal lines for contraction
    import datetime
    for idx, con_ in merged_contractions.iterrows():
        constraction_start_dt = datetime.datetime.strptime(con_.start_dt_index, '%Y-%m-%d')
        constraction_end_dt = datetime.datetime.strptime(con_.end_dt_index, '%Y-%m-%d')

        resis_date_on_plot_line_start_index = constraction_start_dt - datetime.timedelta(days=2)
        resis_date_on_plot_line_end_index = constraction_start_dt + datetime.timedelta(days=2)

        fig.add_shape(type='line', x0=resis_date_on_plot_line_start_index,
                      x1=resis_date_on_plot_line_end_index, y0=con_.resis_price, y1=con_.resis_price)

        delta_t_days = (constraction_end_dt - constraction_start_dt).days
        fig.add_annotation(x=resis_date_on_plot_line_start_index, y=con_.resis_price,
                           text=str(round(con_.contraction_pct * 100, 2)) + '%,' + str(delta_t_days), showarrow=True,
                           arrowhead=1)

        support_date_on_plot_line_start_index = constraction_end_dt - datetime.timedelta(days=2)
        support_date_on_plot_line_end_index = constraction_end_dt + datetime.timedelta(days=2)

        fig.add_shape(type='line', x0=support_date_on_plot_line_start_index,
                      x1=support_date_on_plot_line_end_index, y0=con_.support_price,
                      y1=con_.support_price)
    return fig

def clean_up_axis(fig, ticker, date_str):
    generate_title = "TICKER=" + ticker + ",DATE=" + date_str  # + ",volume_slope=" + str(
    # https://plotly.com/python/time-series/#hiding-weekends-and-holidays
    fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"]), ])  # hide weekends
    fig.update_layout(title_text=generate_title)
    fig.update_layout(
        autosize=False,
        width=1000,
        height=600,
        margin=dict(l=0, r=20, t=30, b=20),
        title_text=generate_title
    )
    fig.update_xaxes(showgrid=True, gridwidth=0.01, gridcolor='Black', automargin=False)
    fig.update_yaxes(showgrid=True, gridwidth=0.01, gridcolor='Black', automargin=False)
    fig.update(layout_xaxis_rangeslider_visible=True)
    return fig


def get_contractions_from_vcp_df(vcp_slice):
    import pandas as pd
    # given a vcp slice this function generates the contraction df
    try:
        merged_df = []
        vcp_slice_dict = vcp_slice.to_dict(orient='records')[0]

        num_contractions = vcp_slice_dict['number_of_consolidations']

        for x in range(num_contractions):
            tmp_dict = {"end_dt_index": vcp_slice_dict["MERGEDCONTRACTION_" + str(x) + "_end_dt"],
                        "support_price": vcp_slice_dict["MERGEDCONTRACTION_" + str(x) + "_support_price"],
                        "start_dt_index": vcp_slice_dict["MERGEDCONTRACTION_" + str(x) + "_start_dt"],
                        "resis_price": vcp_slice_dict["MERGEDCONTRACTION_" + str(x) + "_resis_price"],
                        "contraction_pct": vcp_slice_dict["MERGEDCONTRACTION_" + str(x) + "_contraction_pct"]}
            merged_df.append(tmp_dict)
        contractions_df = pd.DataFrame(merged_df)
        return contractions_df

    except Exception as e:
        print(e)
        return pd.DataFrame()


def NEW_generate_VCP_plot_for_timeslice(ticker, ohlcv_df, vcp_slice):
    import datetime
    near_field_range = -1

    current_scan_date = vcp_slice.iloc[0]['datetime']

    # subset data
    ohlcv_df_tmp = ohlcv_df.reset_index().copy()
    data_end_date = datetime.datetime.strptime(current_scan_date, '%Y-%m-%d')
    subset_ohlcv_df = ohlcv_df_tmp[ohlcv_df_tmp['date'] <= data_end_date]

    fig = set_up_time_series_plot(ticker,subset_ohlcv_df)

    merged_contractions = get_contractions_from_vcp_df(vcp_slice)
    if not merged_contractions.empty:
        fig = add_contraction_lines(fig, merged_contractions)

    fig, clean_up_axis(fig, ticker, current_scan_date)
    # return volume_slope, contraction_slope, merged_contractions, near_field_range
    return fig, near_field_range

def display_vcp_identity(vcp_slice, current_scan_date_str):
    import pandas as pd
    import datetime
    import streamlit as st
    vcp_identity = {}

    vcp_slice_dict = vcp_slice.to_dict(orient='records')[0]
    #print(vcp_slice_dict)
    ticker_ = vcp_slice_dict['ticker']
    vcp_identity['Ticker'] = vcp_slice_dict['ticker']
    vcp_identity['Number of consolidations'] = vcp_slice_dict['number_of_consolidations']
    vcp_identity['Total duration (days)'] = vcp_slice_dict['total_duration']
    vcp_identity['Max consolidation'] = str(round(float(vcp_slice_dict['max_consolidations_pct']) * 100, 2)) + ' %'
    vcp_identity['Max consolidation duration (days)'] = int(vcp_slice_dict['first_contraction_duration'])
    vcp_identity['Latest consolidation'] = str(round(float(vcp_slice_dict['latest_contraction_pct']) * 100, 2)) + ' %'
    vcp_identity['Latest consolidation duration (days)'] = int(vcp_slice_dict['latest_contraction_duration'])
    vcp_identity['Contraction ratio'] = round(vcp_slice_dict['contraction_ratio'], 2)

    vcp_identity = pd.Series(data=vcp_identity).to_frame()
    vcp_identity_title = ticker_ + ' VCP ' + current_scan_date_str
    vcp_identity.columns = [vcp_identity_title]
    st.table(vcp_identity.astype(str))
    pass


def display_vcp_supp_data(vcp_slice):
    import pandas as pd
    import streamlit as st
    vcp_supp_data = {}
    vcp_slice_dict = vcp_slice.to_dict(orient='records')[0]
    vcp_supp_data['MM Basic Filtered'] = vcp_slice_dict['MM_Stage2Filtered']
    vcp_supp_data['Relative Strength'] = vcp_slice_dict['rs_score']
    vcp_supp_data['Stage 2'] = vcp_slice_dict['SW_stage2']
    vcp_supp_data = pd.Series(data=vcp_supp_data).to_frame()
    vcp_supp_data.columns = ["Supplementary Data"]
    st.table(vcp_supp_data.astype(str))
    pass

def display_contractions_df_grid(contractions_df):
    # show contractions
    import streamlit as st
    import pandas as pd
    con_df = contractions_df.copy()

    con_df['duration (days)'] = (pd.to_datetime(contractions_df['end_dt_index']) - pd.to_datetime(contractions_df['start_dt_index']))
    con_df['duration (days)'] = con_df['duration (days)'].apply(lambda x: x.days)
    column_names=['start_dt_index','end_dt_index','duration (days)','contraction_pct','resis_price','support_price']

    con_df = con_df.reindex(columns=column_names)
    con_df['contraction_pct'] = con_df['contraction_pct'].apply(lambda x:str(round(float(x)*100, 2)))
    con_df['resis_price'] = con_df['resis_price'].apply(lambda x: str(round(x, 2)))
    con_df['support_price'] = con_df['support_price'].apply(lambda x: str(round(x, 2)))
    con_df.rename({'start_dt_index':'start_dt','end_dt_index':'end_dt','support_price':"Support",'resis_price':"Resistance", 'contraction_pct':"Contraction %"},inplace=True)

    st.table(con_df)
    pass


def display_factor_radar_chart():
    import streamlit as st
    import plotly.graph_objects as go
    fig = go.Figure(data=go.Scatterpolar(
        r=[1, 5, 2, 2, 3],
        theta=['Momentum', 'Quality', 'Value', 'Size',
               'Low vol'],
        fill='toself'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True
            ),
        ),
        showlegend=True,
    height = 600,
    )
    st.plotly_chart(fig)
    pass


def display_stat_data(static_data_df):
    import streamlit as st
    import pandas as pd
    st.dataframe(static_data_df.T)
    st.write("## Description")
    static_data_dict = static_data_df.to_dict()
    vcp_identity = pd.Series(data=static_data_dict).to_frame()
    vcp_identity_title = "TEST"
    vcp_identity.columns = [vcp_identity_title]
    st.table(vcp_identity.astype(str))
    pass

def make_pertty_vcp_summary(vcp_df):
    import pandas as pd
    vcp_df_pretty = pd.DataFrame()
    vcp_df_pretty['ticker'] = vcp_df['ticker']
    vcp_df_pretty['scanned date'] = vcp_df['datetime']
    vcp_df_pretty['total duration (days)'] = vcp_df['total_duration'].astype('int32')
    vcp_df_pretty['First contraction (%)'] = round(vcp_df['first_contraction_pct'].astype('float')*100,1)
    vcp_df_pretty['First contraction_duration (days)'] = vcp_df['first_contraction_duration'].astype('int32')
    vcp_df_pretty['Latest contraction (%)'] = round(vcp_df['latest_contraction_pct'].astype('float')*100,1)
    vcp_df_pretty['latest contraction duration (days)'] = vcp_df['latest_contraction_duration'].astype('int32')
    vcp_df_pretty['SW stage2'] = vcp_df['SW_stage2'].astype('str')
    vcp_df_pretty['MM Stage2Filtered'] = vcp_df['MM_Stage2Filtered'].astype('str')
    vcp_df_pretty['Volume contraction'] = vcp_df['volume_contraction_condition'].astype('str')
    vcp_df_pretty['Relative Strength Score'] = round(vcp_df['rs_score'],0)
    return vcp_df_pretty

# we want filter vcp to make sense before VCPs before displaying
def in_house_filter_vcp_df(vcp_df):
    inhouse_filtered_vcp_df = vcp_df.copy(deep=True)
    inhouse_filtered_vcp_df = inhouse_filtered_vcp_df[(inhouse_filtered_vcp_df['total_duration']>30) &\
        (inhouse_filtered_vcp_df['first_contraction_pct'] >=0.2) & (inhouse_filtered_vcp_df['first_contraction_pct'] <= 0.45)  &\
    (inhouse_filtered_vcp_df['latest_contraction_pct'] <= 0.15) &\
    (inhouse_filtered_vcp_df['rs_score'] >= 60) &\
    (inhouse_filtered_vcp_df['SW_stage2']==True) & \
    (inhouse_filtered_vcp_df['volume_contraction_condition']) & (inhouse_filtered_vcp_df['latest_contraction_price'] >= 10)]

    inhouse_filtered_vcp_df.reset_index(inplace=True)
    return inhouse_filtered_vcp_df

def build_vcp_summary_table(vcp_df_pretty):
    from st_aggrid import AgGrid
    from st_aggrid.shared import GridUpdateMode
    from st_aggrid.grid_options_builder import GridOptionsBuilder

    gb = GridOptionsBuilder.from_dataframe(vcp_df_pretty)
    gb.configure_pagination()
    gb.configure_side_bar()
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True,min_column_width=100)
    gb.configure_selection(selection_mode="single", use_checkbox=True)
    gridOptions = gb.build()
    selected_data = AgGrid(vcp_df_pretty,
                           width='1000',
                           #theme='dark',
                fit_columns_on_grid_load=True,
                  gridOptions=gridOptions,
                  enable_enterprise_modules=True,
                  allow_unsafe_jscode=True,
                  update_mode=GridUpdateMode.SELECTION_CHANGED)
    default_ticker = vcp_df_pretty['ticker'][0]
    return selected_data, default_ticker

@st.cache(ttl=36000,allow_output_mutation=True,suppress_st_warning=True,hash_funcs={"_thread.RLock": lambda _: None})
def prepare_vcp_df(vcp_df):
    print("********************  RUNNING PREPARE VCP")
    inhouse_filtered_vcp_df = in_house_filter_vcp_df(vcp_df)
    vcp_df_pretty = make_pertty_vcp_summary(inhouse_filtered_vcp_df)
    return vcp_df_pretty


def app():
    import pandas as pd
    import os
    import datetime
    import streamlit as st
    from utils.load_data import load_time_series_data_refintiv, load_vcp_df
    vcp_df = load_vcp_df()
    vcp_df_pretty = prepare_vcp_df(vcp_df)
    #vcp_df = load_vcp_df()
    #inhouse_filtered_vcp_df = in_house_filter_vcp_df(vcp_df)
    #print('*********************',inhouse_filtered_vcp_df.shape,vcp_df.shape)
    #vcp_df_pretty = make_pertty_vcp_summary(inhouse_filtered_vcp_df)
    data, default_ticker = build_vcp_summary_table(vcp_df_pretty)

    if not data['selected_rows']:
        ticker = default_ticker
    else:
        ticker = data['selected_rows'][0]['ticker']

    ohlcv_df = load_time_series_data_refintiv(ticker)

    current_scan_date_str = str(datetime.datetime(day=10, month=1, year=2009).date())

    vcp_slice = vcp_df[vcp_df["ticker"] == ticker]
    contractions_df = get_contractions_from_vcp_df(vcp_slice)
    fig, near_field = NEW_generate_VCP_plot_for_timeslice(ticker, ohlcv_df, vcp_slice)
    fig.update_layout(width=1200, height=900)
    st.plotly_chart(fig, width=1200, height=900)
    #st.plotly_chart(fig)


    st.write("## VCP pattern recognition")
    display_vcp_identity(vcp_slice, current_scan_date_str)
    display_vcp_supp_data(vcp_slice)

    st.write("## Contractions info")
    display_contractions_df_grid(contractions_df)






if __name__ == "__main__":
    import os
    import pandas as pd
    abs_path = os.path.join(r"C:\Users\tclyu\PycharmProjects\exodus\hardcore_vcp","HARDCORE_VCP_2009-10-01.csv")
    vcp_df = pd.read_csv(abs_path)

    #df.astype('int32').dtypes
    vcp_df_pretty = pd.DataFrame()
    vcp_df_pretty['ticker'] = vcp_df['ticker']
    vcp_df_pretty['scanned date'] = vcp_df['datetime']
    vcp_df_pretty['total duration (days)'] = vcp_df['total_duration'].astype('int32')
    vcp_df_pretty['First contraction (%)'] = round(vcp_df['first_contraction_pct'].astype('float')*100,1)
    vcp_df_pretty['First contraction_duration (days)'] = vcp_df['first_contraction_duration'].astype('int32')
    vcp_df_pretty['Latest contraction (%)'] = round(vcp_df['latest_contraction_pct'].astype('float')*100,1)
    vcp_df_pretty['latest contraction duration (days)'] = vcp_df['latest_contraction_duration'].astype('int32')
    vcp_df_pretty['SW stage2'] = vcp_df['SW_stage2'].astype('str')
    vcp_df_pretty['MM Stage2Filtered'] = vcp_df['MM_Stage2Filtered'].astype('str')
    vcp_df_pretty['Volume contraction'] = vcp_df['volume_contraction_condition']
    vcp_df_pretty['Relative Strength Score'] =  round(vcp_df['rs_score'],0)
    print('here')

