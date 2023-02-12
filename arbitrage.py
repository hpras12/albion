import streamlit as st
import pandas as pd
import numpy as np
import json, requests

st.set_page_config(layout="wide")
st.title('Albion Arbitrage')
run_button = st.button('Refresh Opportunities')

if run_button:
    with st.spinner('Wait for it...'):
        # Detect arbitrage opportunities within the Royal cities in Albion online


        # # V2:  From To City:
        # items = requests.get('https://raw.githubusercontent.com/broderickhyman/ao-bin-dumps/master/formatted/items.json').json()

        # from_city = 'Bridgewatch'
        # to_city = 'Lymhurst'
        # for item in items:
        #     from_data = requests.get('https://www.albion-online-data.com/api/v2/stats/prices/'+item['UniqueName']+'?locations='+from_city+'&qualities=1').json()
        #     tmp_buy_price = from_data[0]['sell_price_min']
        #     to_data = requests.get('https://www.albion-online-data.com/api/v2/stats/prices/'+item['UniqueName']+'?locations='+from_city+'&qualities=1').json()
        #     tmp_sell_price = to_data[0]['buy_price_max']
            
        #     if (tmp_sell_price-tmp_buy_price)>0:
        #         print(item['UniqueName'])
        #         print('BUY@' + str(tmp_buy_price) + '  SELL@' + str(tmp_sell_price))
        #         print("Spread of: " + str(tmp_sell_price-tmp_buy_price) + ' per unit')




        strategy = [];

        # Lets get the list of cities:
        royal_cities = ['Martlock','Fort Sterling','Thetford','Bridgewatch','Lymhurst']




        item_ids = ['T1_ROCK','T2_ROCK','T3_ROCK','T4_ROCK','T5_ROCK','T6_ROCK','T7_ROCK','T8_ROCK']
        item_ids += ['T1_WOOD','T2_WOOD','T3_WOOD','T4_WOOD','T5_WOOD','T6_WOOD','T7_WOOD','T8_WOOD']
        item_ids += ['T1_FIBER','T2_FIBER','T3_FIBER','T4_FIBER','T5_FIBER','T6_FIBER','T7_FIBER','T8_FIBER']
        item_ids += ['T1_ORE','T2_ORE','T3_ORE','T4_ORE','T5_ORE','T6_ORE','T7_ORE','T8_ORE']
        item_ids += ['T1_HIDE','T2_HIDE','T3_HIDE','T4_HIDE','T5_HIDE','T6_HIDE','T7_HIDE','T8_HIDE']


        for item_id in item_ids:
            print('ANALYSIS FOR: '+item_id)
            best_buy_price = 9999999
            best_buy_city = ''

            best_sell_price = 0
            best_sell_city = ''
            for royal_city in royal_cities:
                r = requests.get('https://www.albion-online-data.com/api/v2/stats/prices/'+item_id+'?locations='+royal_city+'&qualities=1').json()
                tmp_buy_price = r[0]['sell_price_min']
                if tmp_buy_price == 0: tmp_buy_price=99999999
                tmp_sell_price = r[0]['buy_price_max']
            #     print('BUY@' + str(tmp_buy_price) + '  SELL@' + str(tmp_sell_price))


                if r[0]['sell_price_min'] < best_buy_price:best_buy_price = tmp_buy_price;best_buy_city= royal_city
                if r[0]['buy_price_max'] > best_sell_price:best_sell_price = tmp_sell_price;best_sell_city = royal_city
                    
        #     print("Buy asset from: " + best_buy_city + ' for a price of: ' + str(best_buy_price))
        #     print("Sell asset to: " + best_sell_city + ' for a price of: ' + str(best_sell_price))
        #     print("Spread of: " + str(best_sell_price-best_buy_price) + ' per unit')
            raw_profit = (best_sell_price-best_buy_price)*999
        #     print('For an investment of 100 units you get: '+str(raw_profit))
            fees = 100*best_sell_price*0.105
        #     print('Fees: ' + str(fees))
        #     print('After tax and setup fee of 10.5%: ' + str(raw_profit-fees))
        #     print('ROI: ' + str((raw_profit-fees)/(100*best_buy_price)*100))
        #     print('\n\n')
            
            strategy.append([item_id,best_buy_city,best_buy_price,best_sell_city,best_sell_price,best_sell_price-best_buy_price,raw_profit,fees,raw_profit-fees,(raw_profit-fees)/(999*best_buy_price)*100])
            
        df = pd.DataFrame(strategy,columns=['Item','BuyCity','BuyPrice','SellCity','SellPrice','Spread','RawProfit','Fees','NetIncome','ROI'])
        df = df.sort_values(by=['ROI'], ascending=False)
            

    st.write(df)
