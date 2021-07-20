import pandas as pd
#from pandas_ods_reader import read_ods
import ast
import re
import sys
import os

if len(sys.argv) != 2  :
  print('Missing File Name')
  print('Ex: python Event_separator.py your_file.csv')
  sys.exit()
else:
  data_in = sys.argv[1]
print(data_in)
def read_data(data_in):
  if data_in.endswith('.csv'):
    df = pd.read_csv(data_in, skip_blank_lines=True)
    print('Data Loading...')
  else:
    print("Can't read ods file Please give the CSV file")
    sys.exit()
  return df

def get_data0(data):
  res = ast.literal_eval(data)
  return '['+str(res[0])+']'

def get_data1(data):
  res = ast.literal_eval(data)
  return '['+str(res[1])+']'

def get_data2(data):
  res = ast.literal_eval(data)
  return '['+str(res[2])+']'

def get_data3(data):
  res = ast.literal_eval(data)
  return '['+str(res[3])+']'

def start(raw_data):
  raw_data = raw_data.split(',')
  num = re.findall(r'\d+', raw_data[0])
  output = int(ast.literal_eval(str(num))[0])
  return output

def end(raw_data):
  raw_data = raw_data.split(',')
  num = re.findall(r'\d+', raw_data[1])
  output = int(ast.literal_eval(str(num))[0])
  return output

print('Data Loading...')

df = pd.read_csv(data_in, skip_blank_lines=True)


print('Data loaded successfully')
print(df.head(5))
print(df.shape)

def get_drowsy_event_no(df_name):
  df_name.loc[df_name.Total_Drowsiness_events > 1,'Total_Drowsiness_events'] = 1
  df_name.loc[df_name.Drowsiness_TP > 1,'Drowsiness_TP'] = 1
  df_name.loc[df_name.Drowsiness_FP_NoIncident > 1,'Drowsiness_FP_NoIncident'] = 1
  df_name.loc[df_name.Drowsiness_FP_Incident > 1,'Drowsiness_FP_Incident'] = 1
  return df_name

def get_dist_event_no(df_name):
  df_name.loc[df_name.Total_Distraction_events > 1,'Total_Distraction_events'] = 1
  df_name.loc[df_name.Distraction_TP > 1, 'Distraction_TP'] = 1
  df_name.loc[df_name.Distraction_FP_NoIncident > 1, 'Distraction_FP_NoIncident'] = 1
  df_name.loc[df_name.Dristraction_FP_Incident > 1, 'Dristraction_FP_Incident'] = 1
  return df_name

def equal_events_of_drowsy(dataframe):
  your_df = dataframe[(dataframe.Total_Drowsiness_events == dataframe.Drowsiness_TP) | 
                      (dataframe.Total_Drowsiness_events == dataframe.Drowsiness_FP_NoIncident) | 
                      (dataframe.Total_Drowsiness_events == dataframe.Drowsiness_FP_Incident)]
  return your_df

def equal_events_of_dist(dataframe):
  your_dist_df = dataframe[(dataframe.Total_Distraction_events == dataframe.Distraction_TP) | 
                            (dataframe.Total_Distraction_events == dataframe.Distraction_FP_NoIncident) | 
                            (dataframe.Total_Distraction_events == dataframe.Dristraction_FP_Incident)]
  return your_dist_df

def get_dr_result(your_df, value):
    func = [get_data0, get_data1, get_data2, get_data3]
    result_df = pd.DataFrame()
    for i in range(value):
      event_result = your_df.copy(deep=True)
      event_result['Drowsiness'] = event_result.Drowsiness.apply(func[i])
      result_df = pd.concat([result_df, event_result],  ignore_index=True)
    return result_df

def get_di_result(your_df, value):
    func = [get_data0, get_data1, get_data2, get_data3]
    result_df = pd.DataFrame()
    for i in range(value):
      event_result = your_df.copy(deep=True)
      event_result['Distraction'] = event_result.Distraction.apply(func[i])
      result_df = pd.concat([result_df, event_result],  ignore_index=True)
    return result_df

total_drowsy = df[df.Total_Drowsiness_events >= 1]
total_dist   = df[df.Total_Distraction_events >= 1]

all_drowsy_event = total_drowsy.copy(deep=True)
all_dist_event   = total_dist.copy(deep=True)

all_drowsy_event.loc[all_drowsy_event.Total_Distraction_events >= 1,'Total_Distraction_events'] = 0
all_drowsy_event.loc[all_drowsy_event.Distraction_TP >= 1,'Distraction_TP'] = 0
all_drowsy_event.loc[all_drowsy_event.Distraction_FP_NoIncident >= 1,'Distraction_FP_NoIncident'] = 0
all_drowsy_event.loc[all_drowsy_event.Dristraction_FP_Incident >= 1,'Dristraction_FP_Incident'] = 0
all_drowsy_event.loc[all_drowsy_event.Distraction != 0 ,'Distraction'] = 'No Event '

all_dist_event.loc[all_dist_event.Total_Drowsiness_events >= 1,'Total_Drowsiness_events'] = 0
all_dist_event.loc[all_dist_event.Drowsiness_TP >= 1,'Drowsiness_TP'] = 0
all_dist_event.loc[all_dist_event.Drowsiness_FP_NoIncident >= 1,'Drowsiness_FP_NoIncident'] = 0
all_dist_event.loc[all_dist_event.Drowsiness_FP_Incident >= 1,'Drowsiness_FP_Incident'] = 0
all_dist_event.loc[all_dist_event.Drowsiness != 0 ,'Drowsiness'] = 'No Event '

all_drowsy_event.shape, all_dist_event.shape

all_drowsy_event.Total_Drowsiness_events.sum(), all_dist_event.Total_Distraction_events.sum()

all_equal_drowsy_evnt = equal_events_of_drowsy(all_drowsy_event)
all_equal_dist_evnt = equal_events_of_dist(all_dist_event)

all_equal_drowsy_evnt.shape, all_equal_dist_evnt.shape

all_equal_drowsy_evnt.Total_Drowsiness_events.sum(), all_equal_dist_evnt.Total_Distraction_events.sum()

single_drowsy = all_drowsy_event[all_drowsy_event.Total_Drowsiness_events == 1]
drowsy_two = all_equal_drowsy_evnt[all_equal_drowsy_evnt.Total_Drowsiness_events == 2]
drowsy_three = all_equal_drowsy_evnt[all_equal_drowsy_evnt.Total_Drowsiness_events == 3]
drowsy_four = all_equal_drowsy_evnt[all_equal_drowsy_evnt.Total_Drowsiness_events == 4]
drowsy_two.shape, drowsy_three.shape, drowsy_four.shape

single_drowsy_result = single_drowsy.copy(deep=True)
print(single_drowsy_result.shape, )


single_dist = all_dist_event[all_dist_event.Total_Distraction_events == 1]
dist_two = all_equal_dist_evnt[all_equal_dist_evnt.Total_Distraction_events == 2]
dist_three = all_equal_dist_evnt[all_equal_dist_evnt.Total_Distraction_events == 3]
dist_four = all_equal_dist_evnt[all_equal_dist_evnt.Total_Distraction_events == 4]
single_dist.shape, dist_two.shape, dist_three.shape, dist_four.shape

two_drowsy_result = get_dr_result(drowsy_two, 2)
three_drowsy_result = get_dr_result(drowsy_three, 3)
four_drowsy_result = get_dr_result(drowsy_four, 4)

two_dist_result = get_di_result(dist_two, 2)
three_dist_result = get_di_result(dist_three, 3)
four_dist_result = get_di_result(dist_four, 4)

total_drowsy_result = pd.concat([two_drowsy_result, three_drowsy_result, four_drowsy_result],  ignore_index=True)
equal_drowsy_even_res = get_drowsy_event_no(total_drowsy_result)


total_dist_result = pd.concat([two_dist_result, three_dist_result, four_dist_result],  ignore_index=True)
equal_dist_even_res = get_dist_event_no(total_dist_result)

#equal_drowsy_even_res
total_dist_result.shape

equal_dist_even_res

equal_drowsy_even_res.shape, equal_dist_even_res.shape

def not_equal_drowsy_event_df(in_data):

  input_data = in_data.copy(deep=True)
  dataframe = input_data[input_data.Total_Drowsiness_events > 1]
  output_df = dataframe[(dataframe.Total_Drowsiness_events != dataframe.Drowsiness_TP) & 
                          (dataframe.Total_Drowsiness_events != dataframe.Drowsiness_FP_NoIncident) & 
                          (dataframe.Total_Drowsiness_events != dataframe.Drowsiness_FP_Incident)]

  dr_two = output_df[output_df.Total_Drowsiness_events == 2]
  dr_three = output_df[output_df.Total_Drowsiness_events == 3]
  dr_four = output_df[output_df.Total_Drowsiness_events == 4]

  two_dr_result = get_dr_result(dr_two, 2)
  three_dr_result = get_dr_result(dr_three, 3)
  four_dr_result = get_dr_result(dr_four, 4)
  no_match_total = pd.concat([two_dr_result, three_dr_result, four_dr_result],  ignore_index=True)
  final_dr_df = get_drowsy_event_no(no_match_total)

  return final_dr_df

def not_equal_dist_event_df(in_data):
  input_data = in_data.copy(deep=True)
  dataframe = input_data[input_data.Total_Distraction_events > 1]
  output_df = dataframe[(dataframe.Total_Distraction_events != dataframe.Distraction_TP) & 
                          (dataframe.Total_Distraction_events != dataframe.Distraction_FP_NoIncident) & 
                          (dataframe.Total_Distraction_events != dataframe.Dristraction_FP_Incident)]

  dr_two = output_df[output_df.Total_Distraction_events == 2]
  dr_three = output_df[output_df.Total_Distraction_events == 3]
  dr_four = output_df[output_df.Total_Distraction_events == 4]

  two_di_result = get_di_result(dr_two, 2)
  three_di_result = get_di_result(dr_three, 3)
  four_di_result = get_di_result(dr_four, 4)
  no_match_total = pd.concat([two_di_result, three_di_result, four_di_result],  ignore_index=True)
  final_di_df = get_dist_event_no(no_match_total)

  return final_di_df

no_match_dr_re = not_equal_drowsy_event_df(all_drowsy_event)
no_match_di_re = not_equal_dist_event_df(all_dist_event)


single_drowsy
final_drowsy_result = pd.concat([single_drowsy, equal_drowsy_even_res, no_match_dr_re],  ignore_index=True)
final_drowsy_result.shape

single_dist
final_dist_result = pd.concat([single_dist, equal_dist_even_res, no_match_di_re],  ignore_index=True)
final_dist_result.shape

no_match_dr_re.shape, no_match_di_re.shape

final_df = pd.concat([final_drowsy_result, final_dist_result],  ignore_index=True)


#final_df.tail()

#final_df['Date&Time'] = pd.to_datetime(final_df['Date&Time'])

#final_df.sort_values(by =['Date&Time'], inplace = True, ascending= True)

#final_df.tail()

only_drowsy_events = final_df[final_df.Total_Drowsiness_events == 1]
only_dist_events   = final_df[final_df.Total_Distraction_events == 1]

print('Total drowsy and distraction events is :')
print(only_drowsy_events.shape, only_dist_events.shape)

# Expected output
print('Sum of total events is :')
print([(only_drowsy_events.Total_Drowsiness_events.sum() + only_dist_events.Total_Distraction_events.sum())])

only_drowsy_events['START_FRAME'] = only_drowsy_events.Drowsiness.apply(start)
only_drowsy_events['END_FRAME'] = only_drowsy_events.Drowsiness.apply(end)
only_dist_events['START_FRAME'] = only_dist_events.Distraction.apply(start)
only_dist_events['END_FRAME'] = only_dist_events.Distraction.apply(end)

final_df = pd.concat([only_drowsy_events, only_dist_events], ignore_index=True)

final_df['NEW_REMARKS'] = ''

final_df['Date&Time'] = pd.to_datetime(final_df['Date&Time'])

final_df.sort_values(by =['Date&Time'], inplace = True, ascending= True)

data1 = 'Event_separated-' +  data_in
cwd = os.getcwd()
Output_folder = os.path.join(cwd,"output_csv")
try:
    os.makedirs(Output_folder)
except:
    pass

csv1 =  os.path.join(Output_folder, data1)

Name_of_csv = csv1

print('data_in :', data_in)
final_df.to_csv(Name_of_csv, index= False)

print(final_df.shape)
print('Total_Drowsiness_events and Total_Distraction_events in the original csv is :')
print(df.Total_Drowsiness_events.sum(), df.Total_Distraction_events.sum())
print('Total_Drowsiness_events and Total_Distraction_events in Auto_edited_CSV is :')
print(final_df.Total_Drowsiness_events.sum(), final_df.Total_Distraction_events.sum())

# Expected output
print('Total_Drowsy and Distraction_events in original csv is :')
print([(df.Total_Drowsiness_events.sum()) + (df.Total_Distraction_events.sum())])

# Actual output
print('Total_Drowsy and Distraction events in the Auto_edited_CSV is : ')
print([(final_df.Total_Drowsiness_events.sum()) + (final_df.Total_Distraction_events.sum())])

print('Event separated Output_folder created successfully')
print('Completed successfully')

