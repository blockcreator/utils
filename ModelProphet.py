import matplotlib.pyplot as plt
import pandas as pd
from fbprophet import Prophet
from fbprophet.plot import add_changepoints_to_plot
from fbprophet.plot import seasonality_plot_df
import datetime


class ModelProphet():
    def __init__(self, input_df_holidays=None, holiday_country='US'):
        # if input_df is not None:
        #     self.df = input_df
        # else:
        #     self.df = pd.read_csv(ruleFilePath)
        
        if input_df_holidays is not None:
            
            # init model
            self.model = Prophet(
                interval_width=0.95,
                growth='linear',  #or 'logistic''
                yearly_seasonality=True, 
                weekly_seasonality=True,
                daily_seasonality=True, 
                seasonality_mode='multiplicative',
                holidays=input_df_holidays,
                #changepoint_range=0.8
                )
        else:
            self.model = Prophet(
                interval_width=0.95,
                growth='linear',  #or 'logistic''
                yearly_seasonality=True, 
                weekly_seasonality=True,
                daily_seasonality=True, 
                seasonality_mode='multiplicative',
                #changepoint_range=0.8
                )
            self.model.add_country_holidays(holiday_country)

        return None

    def generate_history_df(self, input_df, history_datetime_range):
        if history_datetime_range is None:
            dateRange = [datetime.datetime(year=2019, month=1, day=1, hour=0, minute=0),
                    datetime.datetime(year=2019, month=1, day=1, hour=23, minute=59)]
        else:
            dateRange = history_datetime_range

        # self.history_df = input_df.query('(ds >= @dateRange[0]) and (ds <= @dateRange[-1])')
        print(dateRange)
        self.history_df = input_df[(input_df['ds'] >= dateRange[0]) & (input_df['ds'] <= dateRange[-1])]

        return None
    
    def fit_model(self):
        self.model.fit(self.history_df)

        return None
    
    def predict(self, period_to_forecast=7, freq_to_forecast = 'D', include_history=True):
        self.future_df = self.model.make_future_dataframe(
            periods=period_to_forecast,
            freq=freq_to_forecast ,
            include_history=include_history)
        
        self.forecast_df = (self.model.predict(self.future_df)
                .assign(ds = lambda x : pd.to_datetime(x["ds"]))
                )
        
        return None


        # inferred_freq = pd.infer_freq(input_df.index)
        # idx_datetime_range_span = pd.date_range(start = dateRange[0], end = dateRange[-1], freq = inferred_freq)
        # assert inferred_freq not None, 'Inferred frequency should not be None!'
    def return_plot_forecast(self):
        fig = self.model.plot(self.forecast_df)
        # a = add_changepoints_to_plot(fig.gca(), self.model, self.forecast_df)
        return fig

    def return_plot_components(self):
        return self.model.plot_components(self.forecast_df)


    def extract_trend(self, includeBound=False):

        if includeBound == True:
            return self.forecast_df[['ds', 'trend', 'trend_lower', 'trend_upper']]
        else:
            return self.forecast_df[['ds', 'trend']]

    def extract_seasonality(self, name='weekly'):
        
        if name == 'daily':
            weekly_start = 0
            # Compute weekly seasonality for a Sun-Sat sequence of dates.
            datetimes = (pd.date_range(start='2017-01-01', periods=4*24, freq='15T'))
            df_w = seasonality_plot_df(self.model, datetimes)
            seas = self.model.predict_seasonal_components(df_w)
            time_name = datetimes.time
            # day_name = days.day_name()

            df_seasonality = pd.DataFrame({'time': time_name,
                                        'daily': seas['daily'],
                                        'daily_lower': seas['daily_lower'],
                                        'daily_upper': seas['daily_upper']
                                        })
        elif name == 'weekly':
            weekly_start = 0
            # Compute weekly seasonality for a Sun-Sat sequence of dates.
            days = (pd.date_range(start='2017-01-01', periods=7) +
                    pd.Timedelta(days=weekly_start))
            df_w = seasonality_plot_df(self.model, days)
            seas = self.model.predict_seasonal_components(df_w)
            day_of_week = days.day_name()

            df_seasonality = pd.DataFrame({'day_of_week': day_of_week,
                                        'weekly': seas['weekly'],
                                        'weekly_lower': seas['weekly_lower'],
                                        'weekly_upper': seas['weekly_upper']
                                        })
            
        elif name == 'yearly':
            yearly_start = 0
            # Compute weekly seasonality for a Sun-Sat sequence of dates.
            days = (pd.date_range(start='2017-01-01', periods=365) +
                    pd.Timedelta(days=yearly_start))
            df_w = seasonality_plot_df(self.model, days)
            seas = self.model.predict_seasonal_components(df_w)
            day_of_week = days.day_name()
            month_name = days.month_name()
            day_of_year = days.dayofyear

            df_seasonality = pd.DataFrame({'day_of_year': day_of_year,
                                        'month_name': month_name,
                                        'day_of_week': day_of_week,
                                        'yearly': seas['yearly'],
                                        'yearly_lower': seas['yearly_lower'],
                                        'yearly_upper': seas['yearly_upper']
                                        })

        return df_seasonality