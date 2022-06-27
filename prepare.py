'''
These functions will prepare acquired store data and german energy data for time series analysis.
'''
import pandas as pd
import acquire
import matplotlib.pyplot as plt
import seaborn as sns

def store_data_prep():
    '''
    This function pulls store data in using a puprpose built acquire.py script 
    and then creates a timedate index as well as some additional columns
    '''
    # Acquires and then converts date to datetime and sets it as index
    df = acquire.acquire_store_data()
    df.sale_date = pd.to_datetime(df.sale_date, format='%a, %d %b %Y %H:%M:%S %Z')
    df = df.set_index('sale_date')
    
    # Plots out the two indicated distributions
    plt.figure(figsize = (15,5))
    plt.subplot(121)
    plt.title('Distribution of Sale Amounts')
    plt.xlabel('Quantity Sold')
    sns.histplot(df.sale_amount)
    plt.subplot(122)
    plt.title('Distribution of Item Prices')
    plt.xlabel('Item Price, $')
    sns.histplot(df.item_price, bins=10)
    plt.show()

    # Adding columns
    df['month'] = df.index.month
    df['day_of_week'] = df.index.day_name()
    df['sales_total'] = df.sale_amount * df.item_price

    return df

def OPS_data_prep():
    df = acquire.OPS_acquire()
    df.Date = pd.to_datetime(df.Date, format='%Y-%m-%d')
    df = df.set_index('Date')

    for col in df.columns:
        print(f'Count of days of {col} at a given energy level (x-axis):')
        sns.histplot(df[col])
        plt.show()
        print('----------\n')

    df['month'] = df.index.month
    df['year'] = df.index.year

    df = df.fillna(value=0)
    df['Wind+Solar'] = df.Wind + df.Solar
    df['Non-Renewable'] = df.Consumption - df['Wind+Solar']

    df_monthly = df.resample('M').mean()

    plt.figure(figsize = (12,6))
    plt.subplot(121)
    df.Consumption.plot(label='Electricity Consumed')
    df.Wind.plot(label='Wind Generation')
    df.Solar.plot(label='Solar Generation')
    df['Wind+Solar'].plot(label='Total Renewable Generation')
    df['Non-Renewable'].plot(label='Non-Renewable Generation Required')
    plt.title('German Energy Generation and Consumption, Daily')
    plt.xlabel("Date")
    plt.legend()
    plt.subplot(122)
    df_monthly.Consumption.plot(label='Electricity Consumed')
    df_monthly.Wind.plot(label='Wind Generation')
    df_monthly.Solar.plot(label='Solar Generation')
    df_monthly['Wind+Solar'].plot(label='Total Renewable Generation')
    df_monthly['Non-Renewable'].plot(label='Non-Renewable Generation Required')
    plt.title('German Energy Generation and Consumption, Monthly')
    plt.xlabel("Date")
    plt.legend()
    plt.show()

    return df
