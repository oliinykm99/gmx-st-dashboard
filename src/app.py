import streamlit as st

from src.methods import *
from src.fetcher import *
from src.display import *


def home():
    st.set_page_config(page_title="GMX V1 - Dashboard",
                        page_icon="data/gmx_logo.png",
                        layout="wide",
                        initial_sidebar_state='collapsed')

    st.title('GMX V1 - Dashboard')

    # Fetch Required Data
    data = fetch_gmx_data()
    composition_data = fetch_gmx_composition_data()

    current_tvl = "${:,.0f}".format(get_tvl(data, time_col='date', tvl_col='totalValueLockedUSD')[0])
    delta_tvl = "{:.2f}% (24h)".format(get_tvl(data, time_col='date', tvl_col='totalValueLockedUSD')[1])
    current_volume= "${:,.0f}".format(get_cumulative_volume(data, time_col='date', vol_col='cumulativeVolumeUSD')[0])
    delta_volume = "{:.2f}% (24h)".format(get_cumulative_volume(data, time_col='date', vol_col='cumulativeVolumeUSD')[1])
    current_long_open = "${:,.0f}".format(get_open_interest(data, time_col='date', open='dailyLongOpenInterestUSD')[0])
    delta_long_open = "{:.2f}% (24h)".format(get_open_interest(data, time_col='date', open='dailyLongOpenInterestUSD')[1])
    current_short_open = "${:,.0f}".format(get_open_interest(data, time_col='date', open='dailyShortOpenInterestUSD')[0])
    delta_short_open = "{:.2f}% (24h)".format(get_open_interest(data, time_col='date', open='dailyShortOpenInterestUSD')[1])
    current_open = "${:,.0f}".format(get_open_interest(data, time_col='date', open='dailyTotalOpenInterestUSD')[0])
    delta_open = "{:.2f}% (24h)".format(get_open_interest(data, time_col='date', open='dailyTotalOpenInterestUSD')[1])
    metrics = [
        {"label": "Total Value Locked", "value": current_tvl, "delta": delta_tvl, "help": "Total Value Locked in USD"},
        {"label": "Total Volume", "value": current_volume, "delta": delta_volume, "help": "Cumulative Trading Volume"},
        {"label": "Current Total Long Open Interest", "value": current_long_open, "delta": delta_long_open, "help": "Total Daily Long Open Interest in USD"},
        {"label": "Current Total Short Open Interest", "value": current_short_open, "delta": delta_short_open, "help": "Total Daily Short Open Interest in USD"},
        {"label": "Current Total Open Interest", "value": current_open, "delta": delta_open, "help": "Total Daily Open Interest in USD"},
        
        ]
    st.subheader('General Metrics')
    display_metrics(metrics)
    st.markdown('---')
    plot_cols = st.columns(2) 
    with plot_cols[0]:
        plot_general(data, time_col='date',
                            value_col='totalValueLockedUSD', xlabel='',
                            ylabel='USD, $', title='Total Value Locked', 
                            annotate='Historical Total Value Locked in GMX V1 on Arbitrum')
    with plot_cols[1]:
        plot_general_bar(data, time_col='date',
                         value_col='cumulativeVolumeUSD',
                         bar_col='dailyVolumeUSD', xtitle='Total Volume Traded', ytitle='Daily Volume USD', ylabel1='USD, $',
                         ylabel2='', title='Total Volume Traded')
    st.markdown('---')
    plot_cols = st.columns(2) 
    with plot_cols[0]:
        plot_bar_chart(composition_data, time_col='date',
                       column_name='weight', xaxis_title='', yaxis_title='Percent, %',
                       title='GLP Composition', annotate=None)
