import requests
import os
import pandas as pd
import streamlit as st


from dotenv import load_dotenv
load_dotenv()
api = os.getenv("API_KEY")

gmx_url = f'https://gateway-arbitrum.network.thegraph.com/api/{api}/subgraphs/id/DiR5cWwB3pwXXQWWdus7fDLR2mnFRQLiBFsVmHAH9VAs'

@st.cache_data
def fetch_gmx_data():
    query = """
        {
    liquidityPoolDailySnapshots(
        first: 1000
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
    data = data.sort_values(by='timestamp')

    return data

def fetch_gmx_composition_data():
    query = """
        {
      liquidityPoolDailySnapshots(
        first: 1000
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
      }
    }
    """
    response = requests.post(gmx_url, json={'query': query})
    data = response.json()
    snapshots = data['data']['liquidityPoolDailySnapshots']
    all_tokens_data = []
    for snapshot in snapshots:
        timestamp = snapshot['timestamp']
        for weight, token in zip(snapshot['inputTokenWeights'], snapshot['inputTokens']):
            all_tokens_data.append({
                'timestamp': timestamp,
                'weight': weight,
                'name': token['name'],
                'symbol': token['symbol'],
                'lastPriceUSD': token['lastPriceUSD']
            })
    data = pd.DataFrame(all_tokens_data)
    data[['timestamp', 'weight','lastPriceUSD']] = data[['timestamp', 'weight','lastPriceUSD']].apply(pd.to_numeric, errors='coerce')
    data['date'] = pd.to_datetime(data['timestamp'].astype(int), unit='s')
    data = data.sort_values(by='timestamp')
    data['weight'] = data.groupby('timestamp')['weight'].transform(lambda x: 100 * x / x.sum())

    return data