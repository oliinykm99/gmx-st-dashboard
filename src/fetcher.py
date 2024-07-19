import requests
import os
import pandas as pd
import streamlit as st


from dotenv import load_dotenv
load_dotenv()
api = os.getenv("API_KEY")

gmx_url = f'https://gateway-arbitrum.network.thegraph.com/api/{api}/subgraphs/id/DiR5cWwB3pwXXQWWdus7fDLR2mnFRQLiBFsVmHAH9VAs'

@st.cache_data(ttl=86400)
def fetch_gmx_data():
    query = """
        {
    liquidityPoolDailySnapshots(
        first: 500
        orderBy: timestamp
        orderDirection: desc
    ) {
        cumulativeVolumeUSD
        dailyActiveUsers
        dailyLongOpenInterestUSD
        dailyShortOpenInterestUSD
        dailyTotalOpenInterestUSD
        dailyVolumeUSD
        timestamp
        totalValueLockedUSD
    }
    }
    """
    response = requests.post(gmx_url, json={'query': query})
    data = response.json()
    data = data['data']['liquidityPoolDailySnapshots']
    data = pd.DataFrame(data)
    data = data.apply(pd.to_numeric, errors='coerce')
    data['date'] = pd.to_datetime(data['timestamp'].astype(int), unit='s')
    data['total'] = data['dailyLongOpenInterestUSD'] + data['dailyShortOpenInterestUSD']
    data['longPercentage'] = (data['dailyLongOpenInterestUSD'] / data['total']) * 100
    data['shortPercentage'] = (data['dailyShortOpenInterestUSD'] / data['total']) * 100
    data = data.sort_values(by='timestamp')

    return data

@st.cache_data(ttl=86400)
def fetch_gmx_composition_data():
    query = """
        {
      liquidityPoolDailySnapshots(
        first: 365
        orderBy: timestamp
        orderDirection: desc
      ) {
        timestamp
        inputTokens {
          name
          symbol
          
          lastPriceUSD
        }
        inputTokenWeights
        dailyInflowVolumeByTokenUSD
        dailyOutflowVolumeByTokenUSD
      }
    }
    """
    response = requests.post(gmx_url, json={'query': query})
    data = response.json()
    snapshots = data['data']['liquidityPoolDailySnapshots']
    all_tokens_data = []
    for snapshot in snapshots:
        timestamp = snapshot['timestamp']
        for weight, token, inflow, outflow in zip(snapshot['inputTokenWeights'], snapshot['inputTokens'], snapshot['dailyInflowVolumeByTokenUSD'], snapshot['dailyOutflowVolumeByTokenUSD']):
            all_tokens_data.append({
                'timestamp': timestamp,
                'weight': weight,
                'inflowUSD': inflow,
                'outflowUSD': outflow,
                'name': token['name'],
                'symbol': token['symbol'],
                'lastPriceUSD': token['lastPriceUSD']
            })
    data = pd.DataFrame(all_tokens_data)
    data[['timestamp', 'weight', 'inflowUSD', 'outflowUSD', 'lastPriceUSD']] = data[['timestamp', 'weight', 'inflowUSD', 'outflowUSD', 'lastPriceUSD']].apply(pd.to_numeric, errors='coerce')
    data['date'] = pd.to_datetime(data['timestamp'].astype(int), unit='s')
    data = data.sort_values(by='timestamp')
    data['weight'] = data.groupby('timestamp')['weight'].transform(lambda x: 100 * x / x.sum())

    return data

uni_url = f'https://gateway-arbitrum.network.thegraph.com/api/{api}/subgraphs/id/FbCGRftH4a3yZugY7TnbYgPJVEv2LvMT6oF1fxPe9aJM'
@st.cache_data(ttl=86400)
def fetch_uniswapv3_weth():
    query = """
    {
      poolDayDatas(
        first: 365
        orderBy: date
        where: {pool_: {id: "0xc6962004f452be9203591991d15f6b388e09e8d0"}}
        orderDirection: desc
      ) {
        id
        date
        token1Price
      }
    }
    """
    response = requests.post(uni_url, json={'query': query})
    data = response.json()
    
    records = []
    for entry in data['data']['poolDayDatas']:
        date = entry['date']
        pool_id = entry['id']
        pool_id, suffix = pool_id.split('-')
        price_usd = float(entry['token1Price'])
        records.append((date, pool_id, price_usd))
    
    data = pd.DataFrame(records, columns=['timestamp', 'pool', 'price'])
    data['date'] = pd.to_datetime(data['timestamp'].astype(int), unit='s')
    data = data.sort_values(by='timestamp')

    return data