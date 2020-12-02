def calculate_covered_ratio(input_df,
                                   label_column,
                                   list_DoW,
                                   list_Time,
                                   list_DoW_Time = None,
                                   list_sorted_DoW = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']):
    

    df = input_df.reset_index(drop=True)
    df['Time'] = df['Datetime'].dt.time.astype('str')
    df['DoW'] = df['Datetime'].dt.day_name()
    df['DoW-Time'] = df['DoW'] + '_' + df['Time']
    df['value'] =  0
    df['value'].iloc[df[label_column] ==  True]  = 1

    df['isin_list_DoW'] = df['DoW'].isin(list_DoW)
    df['isin_list_Time'] = df['Time'].isin(list_Time)

    df_interest = df[df[label_column] ==  True].reset_index(drop=True)

    df_prob_DoW = df[['DoW', 'value']].groupby(['DoW']).mean()

    df_covered_DoW = df_interest[['DoW', 'value']].groupby(['DoW']).count()
    df_covered_DoW['value'] = df_covered_DoW['value']/len(df_interest)

    df_prob_Time = df[['Time', 'value']].groupby(['Time']).mean()

    df_covered_Time = df_interest[['Time', 'value']].groupby(['Time']).count()
    df_covered_Time['value'] = df_covered_Time['value']/len(df_interest)



    return df_prob_DoW, df_prob_Time, df_covered_DoW, df_covered_Time, df_interest