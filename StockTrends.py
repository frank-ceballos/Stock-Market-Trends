""" ***************************************************************************
# * File Description:                                                         *
# * Using data downloaded from Yahoo Finace, we construct visual tools        *
# * to confirm stock market trends.                                           *
# *                                                                           *
# * The contents of this script are:                                          *
# * 1. Importing Libraries                                                    *
# * 2. Helper Functions: Use to read data                                     *
# * 3. Read data                                                              *
# * 4a. Visualize Data: Line Plot                                             * 
# * 4b. Visualize Data: Prepare data for Candlestick Chart                    *
# * 4b. Visualize Data: Make Candlestick Chart                                *
# * 5a. Simple Moving Average                                                 *
# * 5b. Exponential Moving Average                                            *
# * 5c. Popular SMA and EMA                                                   *
# * 5d. Candlesticks with Moving Averages                                     *
# * 6a. Candlestick charts, Moving Averages, and Volume: Crunching the numbers*
# * 6b. Candlestick charts, Moving Averages, and Volume: Figure               *
# *                                                                           *
# * --------------------------------------------------------------------------*
# * AUTHORS(S): Frank Ceballos                                                *
# * --------------------------------------------------------------------------*
# * DATE CREATED: Sept 2, 2019                                                *
# * --------------------------------------------------------------------------*
# * NOTES:                                                                    *
# * ************************************************************************"""


###############################################################################
#                          1. Importing Libraries                             #
###############################################################################
# For reading, processing, and visualizing data
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.dates as mdates
import datetime

# To make candlestick charts
from mpl_finance import candlestick_ohlc

# For reading files
from os import listdir


###############################################################################
#                      2. Helper Functions: Use to read data                  #
###############################################################################
def get_data(data_prefix, start_date, end_date):
    """Reads all the files located in the data_prefix directory.
    
    Parameters
    ----------
    
    data_prefix : str
        String object describing path to where the data is located.
                 
    start_date : str
        String object describing the first date to consider
    
    end_date : str
        String object describing the last date to consider
    
    
    Returns
    ----------
    data: dict
        Dictionary object where the keys of the dictionary are the file
        names (without the file extension) and each entry a Pandas
        Dataframe object that contains the data of the file denoted by
        the key.      
    
    Example
    -------
    To read the data between 2014-01-01 and 2018-01-01 contained in the files
    stored in the folder specified by data_prefix: 
        
        # Path to directory where the data is saved
        data_prefix = "C:\\Users\\Pancho\\Documents\\StockMarketData"
    
        # Earliest and latest date to consider
        start_date = "2014-01-01" %"Year-Month-Day"
        end_date   = "2018-01-01"
        
        # Read data
        data = get_data(data_prefix, start_date, end_date)
        
    Author Information
    ------------------
    Frank Ceballos
    LinkedIn: <https://www.linkedin.com/in/frank-ceballos/>
    Date: August, 24, 2019
    """
    
    # Get file names in directory
    file_names = listdir(data_prefix)
            
    # Initiliaze data directory that will contain all the data.
    data = {}
    
    # Get data
    for file_name in file_names:
        # Read data
        df = pd.read_csv(data_prefix + file_name)
        
        # Set mask to select dates
        mask = (df["Date"] > start_date) & (df["Date"] <= end_date)
        
        # Select data between start and end date
        df = df.loc[mask]
        
        # Get timestamps
        dates = [pd.Timestamp(date) for date in df.Date]
        
        # Drop "Date" column
        df = df.drop(["Date"], axis = 1)
        
        # Make dataframe 
        df = pd.DataFrame(df.values, columns = df.columns, index = dates)
        
        # Update dictionary
        data.update({file_name[:-4]: df})
        
    return data
        

###############################################################################
#                               3. Read data                                  #
###############################################################################
# Path to directory where the data is saved
data_prefix = "data\\"

# Define time period to consider
start_date = "2013-01-01"
end_date   = "2017-12-31"

# Use helper function to read data
data = get_data(data_prefix, start_date, end_date)


###############################################################################
#                         4a. Visualize Data: Line Plot                       #
###############################################################################
# Get ADI data
ADI_data = data["01ADI"]

# Set fontsize
sns.set(font_scale = 1.5)

# Set graph style
sns.set_style({"axes.facecolor": "1.0", "axes.edgecolor": "0.85",  'axes.grid': True, "grid.color": "0.85",
               "grid.linestyle": "-", 'axes.labelcolor': '0.4', "xtick.color": "0.4",
               'ytick.color': '0.4'})

# Set palette
flatui = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]
sns.set_palette(flatui)

# Define time period to consider for figure
start_date = "2015-01-01"
end_date   = "2018-01-01"

# Create figure
f, ax = plt.subplots(figsize=(13, 13), nrows = 2, ncols = 1)

# Plot Analog Devices Open, High, Low, Close, Adj Close
ADI_data.iloc[:, 0:5].plot(fontsize = 14,
                          rot = 45,
                          xlim = (pd.Timestamp(start_date), pd.Timestamp(end_date)),
                          ylim = (40, 100),
                          ax = ax[0])

# Add x and y label
ax[0].set_xlabel("Date", fontsize = 18)
ax[0].set_ylabel("Price ($)", fontsize = 18)


# Plot Analog Devices Volume
ADI_data.iloc[:, 5].plot(fontsize = 14,
                          rot = 45,
                          xlim = (pd.Timestamp(start_date), pd.Timestamp(end_date)),
                          ax = ax[1])

# Add x and y label
ax[1].set_xlabel("Date", fontsize = 18)
ax[1].set_ylabel("Price ($)", fontsize = 18)

# Tight layout
plt.tight_layout()

# Save Figure
plt.savefig("ADI Stock Price Summary.png", dpi = 1080)


###############################################################################
#              4b. Visualize Data: Prepare data for Candlestick Chart         #
###############################################################################
# Get Open, High, Low, Close
ADI_candle   = ADI_data.iloc[:, 0:4] # Analog Devices

# Get dates
dates = ADI_data.index.tolist()
dates = pd.DataFrame(mdates.date2num(dates), columns = ["Date"], index = ADI_data.index)

# Add dates column to OHLC DataFrames
ADI_candle = pd.concat([dates, ADI_candle], axis = 1)


###############################################################################
#                 4b. Visualize Data: Make Candlestick Chart                  #
###############################################################################
# Define time interval to consider
start_date = datetime.date(2015, 5, 18) # Year-Month-Day
end_date   = datetime.date(2015, 7, 10)

# Create figure
f, ax = plt.subplots(figsize=(13, 6.5))

# Plot ADI_OHLC data
candlestick_ohlc(ax, ADI_candle.values.tolist(), 
                 width=.6, 
                 colorup='green',
                 colordown='red')

# Set x and y axis limits
ax.set_xlim([start_date, end_date])
ax.set_ylim([60, 69])

# Set axis labels
ax.set_ylabel("Price ($)", fontsize = 20)

# Rotate tick labels
xlabels = ax.get_xticklabels()
ax.set_xticklabels(xlabels, rotation = 45, fontsize = 14)

# Change x-axis tick label fromat
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

# Send gridlines to back
ax.set_axisbelow(True)

# Tight layout
plt.tight_layout()

# Save Figure
plt.savefig("ADI Candlestick Chart Double Top Pattern.png", dpi = 1080)


###############################################################################
#                          5a. Simple Moving Average                          #
###############################################################################
def get_SMA(close_data, time_period):
    """Computes simple moving average (SMA) for the specified time_period.
    
    Parameters
    ----------
    
    close_data: Pandas Series
        Pandas Series object containing the close data (1-dimensional)
        
    time_period : int
        Number of days to consider for the SMA
    
    Returns
    ----------
    SMA: Pandas Series
        Pandas Series object that contains the simple moving average for the
        close_data.
        
    
    Example
    -------
   To compute a 10-day SMA for the close_data:
           
    # Compute 10-day SMA
    SMA10 = get_SMA(close_data, 10)
        
    Author Information
    ------------------
    Frank Ceballos
    LinkedIn: <https://www.linkedin.com/in/frank-ceballos/>
    
    Date: August, 31, 2019
    """
        
    # List to store moving average results
    SMA = list(range(0, len(close_data) - time_period))
    
    # Compute moving average
    for ii in range(len(SMA)):
        # Previous days index
        index = range(ii, ii + time_period)
        
        # Get data for previous days
        prev_days = close_data.iloc[index]
        
        # Sum previous days
        summation = np.sum(prev_days)
        
        # Get average
        avg = summation/time_period
        
        # Save results to list
        SMA[ii] = avg
         
    # Define column label
    label = f"{time_period}-SMA"
    
    # Get corresponding dates for moving_avg
    dates = close_data.index[time_period:]
    
    # Convert list into Pandas Series
    SMA = pd.Series(SMA, name = label, index = dates)
    
    return SMA



###############################################################################
#                       5b. Exponential Moving Average                        #
###############################################################################
def get_EMA(close_data, time_period):
    """Computes exponential moving average (EMA) for the specified time_period.
    
    Parameters
    ----------
    
    close_data: Pandas Series
        Pandas Series object containing the close data (1-dimensional)
        
    time_period : int
        Number of days to consider for the SMA
    
    Returns
    ----------
    EMA: Pandas Series
        Pandas Series object that contains the exponential moving average for the
        close_data.
        
    
    Example
    -------
   To compute a 10-day EMA for the close_data:
           
    # Compute 10-day EMA
    EMA10 = get_EMA(close_data, 10)
        
    Author Information
    ------------------
    Frank Ceballos
    LinkedIn: <https://www.linkedin.com/in/frank-ceballos/>
    
    Date: August, 31, 2019
    """
    
    # List to store moving average results
    EMA = list(range(0, len(close_data) - time_period))
    
    # Calculate SMA to use as the first EMA
    initial_EMA = get_SMA(close_data, time_period)[0]
    
    # Calculate initial weight
    k = 2.0 / (time_period + 1)

    # Compute EMA
    for ii in range(len(EMA)):
        # Set index
        index = time_period + ii
        
        # Get current Close price
        close_temp = close_data[index]
        
        # Compute current EMA
        if ii == 0:
            EMA_temp = (close_temp - initial_EMA)*k + initial_EMA
        else:
            EMA_temp = (close_temp - EMA[ii-1])*k + EMA[ii-1]


        # Save results to list
        EMA[ii] = EMA_temp
        
    # Define column label
    label = f"{time_period}-EMA"
    
    # Get corresponding dates for moving_avg
    dates = close_data.index[time_period:]
    
    # Convert list into Pandas Series
    EMA = pd.Series(EMA, name = label, index = dates)
    
    return EMA    



###############################################################################
#                           5c. Popular SMA and EMA                           #
###############################################################################
# Analog Devices Close data
close_data = ADI_data.iloc[:, 3]# Column 3 is the close price for Analog Devices

# Get SMA
SMA50  = get_SMA(close_data, 50)
SMA200 = get_SMA(close_data, 200)

# Get EMA
EMA9  = get_EMA(close_data, 9)
EMA20 = get_EMA(close_data, 20)


###############################################################################
#                       5d. Candlesticks with Moving Averages                 #
###############################################################################
# Define time interval to consider
start_date = datetime.date(2015, 5, 18) # Year-Month-Day
end_date   = datetime.date(2015, 7, 10)

# Create figure
f, ax = plt.subplots(figsize=(13, 6.5))

# Plot ADI_OHLC data
candlestick_ohlc(ax, ADI_candle.values.tolist(), 
                 width=.6, 
                 colorup='green',
                 colordown='red')

# Plot 50-day SMA
SMA50.plot(color = ["magenta"], style = ["-"], linewidth = 2.5, ax = ax)

# Plot 200-day SMA
SMA200.plot(color = ["b"], style = ["-"], linewidth = 2.5, ax = ax)

# Plot 9-day EMA
EMA9.plot(color = ["blueviolet"], linewidth = 2.5, style = ["--"], ax = ax)

# Plot 20-day EMA
EMA20.plot(color = ["orange"], linewidth = 2.5, style = ["--"], ax = ax)

# Set x and y axis limits
ax.set_xlim([start_date, end_date])
ax.set_ylim([60, 69])

# Set axis labels
ax.set_ylabel("Price ($)", fontsize = 20)

# Rotate tick labels
xlabels = ax.get_xticklabels()
ax.set_xticklabels(xlabels, rotation = 45, fontsize = 14)

# Change x-axis tick label fromat
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

# Send gridlines to back
ax.set_axisbelow(True)

# Show legend
plt.legend()

# Tight layout
plt.tight_layout()

# Save Figure
plt.savefig("ADI Candlestick Chart With Averages.png", dpi = 1080)


###############################################################################
#  6a. Candlestick charts, Moving Averages, and Volume: Crunching the numbers #
###############################################################################
# Path to directory where the data is saved
data_prefix = "data\\"

# Define time period to consider when reading the data
start_date = "2013-01-01"
end_date   = "2019-08-01"

# Use helper function to read data
data = get_data(data_prefix, start_date, end_date)

# Get ADI data
ADI_data = data["01ADI"]

# Get Open, High, Low, Close
ADI_candle   = ADI_data.iloc[:, 0:4] # Analog Devices

# Get dates
dates = ADI_data.index.tolist()
dates = pd.DataFrame(mdates.date2num(dates), columns = ["Date"], index = ADI_data.index)

# Add dates column to OHLC DataFrames
ADI_candle = pd.concat([dates, ADI_candle], axis = 1)

# Analog Devices Close data
close_data = ADI_data.iloc[:, 3]# Column 3 is the close price for Analog Devices

# Get SMA
SMA50  = get_SMA(close_data, 50)
SMA200 = get_SMA(close_data, 200)

# Get EMA
EMA9  = get_EMA(close_data, 9)
EMA20 = get_EMA(close_data, 20)


###############################################################################
#          6b. Candlestick charts, Moving Averages, and Volume: Figure        #
###############################################################################
# Set fontsize
sns.set(font_scale = 1.5)

# Set graph style
sns.set_style({"axes.facecolor": "1.0", "axes.edgecolor": "0.85",  'axes.grid': True, "grid.color": "0.85",
               "grid.linestyle": "-", 'axes.labelcolor': '0.4', "xtick.color": "0.4",
               'ytick.color': '0.4'})


# Define time period to consider for figure
start_date = "2016-07-01"
end_date   = "2017-4-01"

# Create figure
f, ax = plt.subplots(figsize=(13, 13), nrows = 2, ncols = 1)

# Plot ADI_OHLC data
candlestick_ohlc(ax[0], ADI_candle.values.tolist(), 
                 width=.6, 
                 colorup='green',
                 colordown='red')

# Plot 50-day SMA
SMA50.plot(color = ["magenta"], style = ["-"], linewidth = 2.5, ax = ax[0])

# Plot 200-day SMA
SMA200.plot(color = ["b"], style = ["-"], linewidth = 2.5, ax = ax[0])

# Plot 9-day EMA
EMA9.plot(color = ["blueviolet"], linewidth = 2.5, style = ["--"], ax = ax[0])

# Plot 20-day EMA
EMA20.plot(color = ["orange"], linewidth = 2.5, style = ["--"], ax = ax[0])

# Set x and y axis limits
ax[0].set_xlim([start_date, end_date])
ax[0].set_ylim([54, 85])

# Set axis labels
ax[0].set_ylabel("Price ($)", fontsize = 20)

# Rotate tick labels
xlabels = ax[0].get_xticklabels()
ax[0].set_xticklabels(xlabels, rotation = 45, fontsize = 14)

# Change x-axis tick label fromat
ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

# Send gridlines to back
ax[0].set_axisbelow(True)

# Show legend
ax[0].legend()


# Plot Analog Devices Volume
ADI_data.iloc[:, 5].plot(fontsize = 14,
                          rot = 45,
                          xlim = (pd.Timestamp(start_date), pd.Timestamp(end_date)),
                          ax = ax[1])

# Add x and y label
ax[1].set_xlabel("Date", fontsize = 18)
ax[1].set_ylabel("Price ($)", fontsize = 18)

# Show legend
ax[1].legend()

# Tight layout
plt.tight_layout()

# Save Figure
plt.savefig("ADI Candlestick Chart, Averages, and Volume.png", dpi = 1080)

