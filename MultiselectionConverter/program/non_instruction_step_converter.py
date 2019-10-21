#!/usr/bin/env python
# coding: utf-8

# In[28]:


import os
import argparse
import pandas as pd
import numpy as np
import datetime as dt
from dateutil.parser import parse


# In[29]:


def changeColumns(x):
    choice = x['Choice']
    correct_answer =  x['Correct Answer']
    correct_answers =  x['Correct Answers']
    selections =  x['Selections']
    input =  x['Input']
    step_name = x['Step Name']
    student_response_type = x['Student Response Type']
    tutor_response_type = x['Tutor Response Type']
    outcome = x['Outcome']
    if selections is not None and selections:
        input = input.split(",")
        if (choice in input and correct_answer == 1) or (choice not in input and correct_answer == 0):
            x['Outcome'] = 'CORRECT'
        else:
            x['Outcome'] = 'INCORRECT'
        x['Step Name'] = step_name + "_" + choice
    elif (student_response_type and student_response_type == 'ATTEMPT'
         and tutor_response_type and tutor_response_type == 'RESULT'
         and step_name and outcome):
        x['Event Type'] = 'assess_instruct'
    elif (student_response_type and student_response_type == 'HINT_REQUEST'
         and tutor_response_type and tutor_response_type == 'HINT_MSG'
         and step_name):
        x['Event Type'] = 'instruct'    
    return x


# In[30]:


map_file_name = ""
data_file_name = ""
command_line_exe = True
#test command 
#Python non_instruction_step_converter.py -dataFile "ds2846_tx_test.txt" -mapFile "ds2846_non_instructional_steps_map.txt"
if command_line_exe:
    parser = argparse.ArgumentParser(description='Convert multi-selection steps into multiple steps and adjust scoring')
    parser.add_argument('-dataFile', type=str, help='data file containing multi-selection steps', required=True)
    parser.add_argument('-mapFile', type=str, help='map file containing mapping information ')
    args, option_file_index_args = parser.parse_known_args()
    data_file_name = args.dataFile
    map_file_name = args.mapFile
else:
    map_file_name = 'ds2846_non_instructional_steps_map.txt'
    data_file_name = 'ds2846_tx_test.txt'


# In[31]:


df_map = pd.read_csv(map_file_name, dtype=str, sep="\t")
new_columns = df_map.columns.tolist()
new_columns.extend(['Choice', 'Correct Answer', 'Event Type'])
df_map_new = pd.DataFrame(columns=new_columns)
for i in range(len(df_map.index)):
    #this_row = pd.Series(df_map.iloc[i, :])
    this_row = df_map.iloc[i, :]
    selections = this_row['Selections'].split(",")
    answers = this_row['Correct Answers'].split(",")
    selections_count = len(selections)
    for j, selection in enumerate(selections):
        new_row = this_row.copy()
        new_row['Choice'] = selection
        if selection in answers:
            new_row['Correct Answer'] = 1
        else:
            new_row['Correct Answer'] = 0
        if j < len(selections) - 1:
            new_row['Event Type'] = "assess"
        else:
            new_row['Event Type'] = "assess_instruct"
        new_row = new_row.to_frame().transpose()
        if df_map_new.empty:
            df_map_new = new_row
        else:
            df_map_new = df_map_new.append(new_row)


# In[32]:


df = pd.read_csv(data_file_name, dtype=str, sep="\t", encoding = "ISO-8859-1")
#save the first line headers bc Python adds number to duplicate column names
infile = open(data_file_name, 'r')
original_headers = infile.readline().strip()
original_headers = original_headers + "\t" + "Event Type" + "\n"


# In[33]:


#find the columns that has Level() in names for mapFile. Assuming mapFile and dataFile has the same names
level_column_names = []
for col in df_map_new.columns:
    if 'Level (' in col:
        level_column_names.append(col)
level_column_names.append('Problem Name')
level_column_names.append('Step Name')
df_combined = pd.merge( df, df_map_new, left_on=level_column_names, right_on=level_column_names, how='left')
df_combined['Selections'] = df_combined['Selections'].fillna(value='')
df_combined['Input'] = df_combined['Input'].fillna(value='')
df_combined['Step Name'] = df_combined['Step Name'].fillna(value='')
df_combined['Student Response Type'] = df_combined['Student Response Type'].fillna(value='')
df_combined['Tutor Response Type'] = df_combined['Tutor Response Type'].fillna(value='')
df_combined['Outcome'] = df_combined['Outcome'].fillna(value='')
df_combined['Input'] = df_combined['Input'].astype(str)
df_combined.apply(changeColumns, axis=1)
df_combined.drop(['Selections', 'Correct Answers', 'Choice', 'Correct Answer'], axis=1, inplace=True)
#make new output file name
out_file_name = os.path.splitext(os.path.basename(data_file_name))[0] + "_converted" + os.path.splitext(os.path.basename(data_file_name))[1]
#write the header
out_file = open(out_file_name, "w")
out_file.write(original_headers)
out_file.close()
with open(out_file_name, 'a', newline='') as f:
    df_combined.to_csv(f, sep='\t', index=False, header=False)


# In[ ]:



