# we want filter vcp to make sense before VCPs before displaying
def in_house_filter_vcp_df(vcp_df):
    inhouse_filtered_vcp_df = vcp_df.copy(deep=True)
    inhouse_filtered_vcp_df = inhouse_filtered_vcp_df[(inhouse_filtered_vcp_df['total_duration']>30) &\
        (inhouse_filtered_vcp_df['first_contraction_pct'] >= 0.15) & (inhouse_filtered_vcp_df['first_contraction_pct'] <= 0.45)  &\
    (inhouse_filtered_vcp_df['latest_contraction_pct'] <= 0.15) &\
    (inhouse_filtered_vcp_df['RSSCORE'] >= 60) &\
    (inhouse_filtered_vcp_df['SCTRSCORE'] >= 60) &\
    (inhouse_filtered_vcp_df['MRSQUARE'] >= 60) &\
    (inhouse_filtered_vcp_df['SW_stage2']==True) & \
    (inhouse_filtered_vcp_df['volume_contraction_condition']) & (inhouse_filtered_vcp_df['latest_contraction_price'] >= 10) & \
    (inhouse_filtered_vcp_df['is_break_out_latest_contraction'] >= True)  & \
        (inhouse_filtered_vcp_df['is_break_out_first_contraction'] >= True)]

    inhouse_filtered_vcp_df = inhouse_filtered_vcp_df.drop('Unnamed: 0',axis=1,errors ='ignore')

    inhouse_filtered_vcp_df.reset_index(inplace=True,drop=True)
    return inhouse_filtered_vcp_df

def app():
    # this page is copied from recent breakout
    import pandas as pd
    import os
    import datetime
    import streamlit as st
    from utils.load_data import load_time_series_data_refintiv
    from utils.load_data import prepare_fullframe_vcp_data

    from utils.vcp_utils import make_multiselect_summary_table

    vcp_full_frame = prepare_fullframe_vcp_data()

    vcp_df_pretty = in_house_filter_vcp_df(vcp_full_frame)
    data, default_ticker = make_multiselect_summary_table(vcp_df_pretty)

    tmp_export_dir = "tmp_dir_" + str(datetime.datetime.today().date())
    st.info(tmp_export_dir)
    if st.button('Click to generate report'):
        from fpdf import FPDF
        pdf = FPDF(orientation='P', unit='mm', format='letter')
        pdf.add_page()
        #pdf.set_font("Courier", "B", 16)
        #from pdf_report_generator.gen_page import setup_titlepage, make_table
        #from fpdf import FPDF
        #pdf = setup_titlepage()
        ########################### build title page ##################
        from pdf_report_generator.gen_page import make_table
        selected_df = pd.DataFrame(data['selected_rows'])[['ticker','total_duration','contraction_ratio','number_of_consolidations']]
        selected_df['contraction_ratio'] = selected_df['contraction_ratio'].round(2)
        selected_df = selected_df.rename(columns={"number_of_consolidations":"N",
                                                  "total_duration":"total days",
                                                  "contraction_ratio":"contraction ratio"})
        selected_df['page'] = list(range(2, selected_df.shape[0]+2))
        st.dataframe(selected_df)
        pdf.ln(10)
        make_table(pdf, selected_df,size=12)
        pdf.set_y(-20)
        #pdf.cell(0, 5, "Information containing any historical information, data or analysis should not be taken as an indication or guarantee of any future performance, analysis, forecast or prediction. Past performance does not guarantee future results", 0, 'C')
        ################################################################

        for data_row in data['selected_rows']:
            vcp_slice = pd.DataFrame(data_row,index=[0])
            from pdf_report_generator.report_utils.vcp_report_funs import make_plots
            from pdf_report_generator.gen_page import build_page

            ticker = vcp_slice['ticker'][0]
            st.write(ticker)
            ohlcv_df = load_time_series_data_refintiv(ticker)
            stockinfo_df, vcp_property_df, vcp_supplementary_df, factors_df, contractions_df, ts_plot_path = make_plots(ticker, vcp_slice, ohlcv_df, tmp_export_dir)
            st.image(ts_plot_path,width=800)
            pdf = build_page(pdf, ticker, ts_plot_path, stockinfo_df, vcp_property_df, vcp_supplementary_df, factors_df, contractions_df)

        import datetime
        export_filename = "vcp_report_"+str(datetime.datetime.today().date())+".pdf"
        pdf.output(export_filename)
        with open(export_filename,"rb") as file:
            btn = st.download_button(
                "Download Report",
                data=file.read(),
                file_name=export_filename,
                mime='application/octet-stream'
            )

    if st.button('Click to clear tmp directory'):
        import shutil
        st.info("removing tmp_dir :: " + tmp_export_dir)
        if os.path.exists(tmp_export_dir):
            shutil.rmtree(tmp_export_dir, ignore_errors=False, onerror=None)