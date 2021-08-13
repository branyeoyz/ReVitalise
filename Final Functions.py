# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UVOy4ZSPhP-eAANiRSthaa1tKXJee2yO

##Imports
"""

import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing
import numpy as np
from scipy.signal import find_peaks
from scipy.integrate import cumtrapz
from scipy.constants import g
!pip install firebase
!pip install python_jwt
!pip install gcloud
!pip install sseclient
!pip install pycrypto
!pip install requests-toolbelt
!pip install firebase_admin
from firebase import firebase
import csv
import os.path as pth
from statistics import mean
import plotly.graph_objects as go

"""##Firebase"""

from firebase import firebase
import csv
import os.path as pth

firebase = firebase.FirebaseApplication("https://rvcapstone-default-rtdb.asia-southeast1.firebasedatabase.app", None)

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

timestamp = firebase.get('/Data/Timing','')
accx = firebase.get('/Data/Acceleration_X','')
accy = firebase.get('/Data/Acceleration_Y','')
accz = firebase.get('/Data/Acceleration_Z','')
rotx = firebase.get('/Data/Rotation_Roll','')
roty = firebase.get('/Data/Rotation_Pitch','')
rotz = firebase.get('/Data/Rotation_Yaw','')

timestamp_list = []
accx_list = []
accy_list = []
accz_list = []
rotx_list = []
roty_list = []
rotz_list = []

for value in timestamp.values():
    timestamp_list.append(value)
for value in accx.values():
    accx_list.append(value)
for value in accy.values():
    accy_list.append(value)
for value in accz.values():
    accz_list.append(value)
for value in rotx.values():
    rotx_list.append(value)
for value in roty.values():
    roty_list.append(value)
for value in rotz.values():
    rotz_list.append(value)


filename = "session"
filenum = 1
while pth.exists(pth.abspath(filename+str(filenum)+".csv")):
    filenum+=1
with open(filename+str(filenum)+'.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(timestamp_list) #row 1 - row 7 accordingly
    writer.writerow(accx_list)
    writer.writerow(accy_list)
    writer.writerow(accz_list)
    writer.writerow(rotx_list)
    writer.writerow(accy_list)
    writer.writerow(accz_list)
    
sessionname = filename + str(filenum)

#mainserviceaccountfile needs to be in the same folder as the code 

if not firebase_admin._apps:
    cred = credentials.Certificate('/content/drive/MyDrive/Colab Notebooks/mainserviceaccount.json') 
    firebase_admin.initialize_app(cred)

db = firestore.client()

#Write the calculated values back to Firebase
session = {
'approach jump count':final_dict.get('Approach')[0],
'block jump count':final_dict.get('Block')[0],
'average approach jump height': final_dict.get('Approach')[1], 
'average block jump height': final_dict.get('Block')[1],
'max approach jump height': final_dict.get('Approach')[2], 
'max approach block jump height': final_dict.get('Block')[2],
'total average jump height': mean(height),
'peak jump height': max(height),
'total jumps': total_jump
}

db.collection('users').document('Bt1OuEGrCKm413CALIqG').collection('trainings').document('week4').collection('sessions').document(str(sessionname)).set(session)


#db.collection('users').document('9qK74YxlBco6S3vEf2DG').add()
#db.collection('users').document('9qK74YxlBco6S3vEf2DG').collection('trainings').document('week1').set()
#db.collection('users').document('9qK74YxlBco6S3vEf2DG').collection('trainings').document('week8').collection('sessions').document('session5').set(session1)

#db.collection('users').document('test').collection('trainings').document(str(sessionname)).set(session)

"""##All Functions"""

def data_processing_NEW(link):
  #time is already in ms
  df = pd.read_csv(link, header=None)
  df_t = df.T

  ls=[]
  #get time stamps
  timezero = df_t[0][0]
  for i in range(len(df_t)):
    ls.append(df_t[0][i]-timezero)
  df_t['Time(s)'] = ls


  df_t.loc[:, 'Time(s)'] /= 1000
  #remove irrelavant columns
  df_t.pop(0)

  # shift column 'Time(s)' to first position
  first_column = df_t.pop('Time(s)')
  df_t.insert(0, 'Time(s)', first_column)

  #rename columns
  df_t.columns = ['Time(s)', 'ax(g)', 'ay(g)', 'az(g)', 'rotX', 'rotY', 'rotZ']

  #create new dataframe without repeated timings
  #take average of repeated readings

  #new_df = pd.DataFrame(data, columns = ['Time(s)', 'ax(g)', 'ay(g)', 'az(g)'])
  new_df = pd.DataFrame()
  to_append=[]
  total = len(df_t)-1
  i=0

  #remove rotational data
  df_t.pop('rotX')
  df_t.pop('rotY')
  df_t.pop('rotZ')

  while i<total:
  #for i in range(len(df)-1):
    if df_t.iloc[i]['Time(s)']<df_t.iloc[i+1]['Time(s)'] and df_t.iloc[i]['Time(s)']>=0:
      new_df = new_df.append(df_t.iloc[i], ignore_index=True)
      i +=1
    else:
      #recalculate
      #append into new dataframe
      new_x = (df_t.iloc[i]['ax(g)'] + df_t.iloc[i+1]['ax(g)'])/2
      new_y = (df_t.iloc[i]['ay(g)'] + df_t.iloc[i+1]['ay(g)'])/2
      new_z = (df_t.iloc[i]['az(g)'] + df_t.iloc[i+1]['az(g)'])/2
      time = df_t.iloc[i]['Time(s)']
      #to_append.append(df.iloc[i]['Time(s)'], new_x, new_y, new_z)
      to_append.extend((time, new_x, new_y, new_z))
      a_series = pd.Series(to_append, index = df.columns)
      #print(a_series)
      new_df = new_df.append(a_series, ignore_index=True)
      #empty list
      to_append=[]
      i+=2

  #convert to Gs
  new_df.loc[:, 'ax(g)'] /= 9.81
  new_df.loc[:, 'ay(g)'] /= 9.81
  new_df.loc[:, 'az(g)'] /= 9.81
  return new_df

def get_jump(new_df):
  y2 = new_df['ax(g)']
  #find index of local minima based on conditions
  indices = find_peaks(y2, height=2, distance=15)
  return indices

def find_takeoff(new_df, elem):
  #find takeoff
  pk_index = new_df.loc[new_df['ax(g)'] == elem].index[0] #retrieves first instance
  dat = new_df.iloc[pk_index-6: pk_index+1,]
  dat = dat.reset_index(drop=True)


  x = []
  y = []
  for i in range(len(dat)-1):
    if dat.loc[i,"ax(g)"]<0.94 and dat.loc[i+1,"ax(g)"]>=0.94:
      x.append(dat.loc[i,"Time(s)"])
      x.append(dat.loc[i+1,"Time(s)"])
      y.append(dat.loc[i,"ax(g)"])
      y.append(dat.loc[i+1,"ax(g)"])
      break
    else:
      pass

  #interpolate acc at take-off
  x_takeoff = np.interp(0.94, x, y)
  return x_takeoff

def find_landing(new_df, elem):
  #find landing
  pk_index = new_df.loc[new_df['ax(g)'] == elem].index[0] #retrieves first instance
  dat = new_df.iloc[pk_index: pk_index+7,]
  dat = dat.reset_index(drop=True)


  x = []
  y = []
  for i in range(len(dat)-1):
    if dat.loc[i,"ax(g)"]>=0.94 and dat.loc[i+1,"ax(g)"]<0.94:
      x.append(dat.loc[i,"Time(s)"])
      x.append(dat.loc[i+1,"Time(s)"])
      y.append(dat.loc[i,"ax(g)"])
      y.append(dat.loc[i+1,"ax(g)"])
      break
    else:
      pass

  #interpolate acc at take-off
  x_landing = np.interp(0.94, x, y)
  return x_landing

def jump_height(new_df, acc_ls):
  #ls contains a list of peak acc identified when counting jumps
  dist_ls=[]
  for elem in acc_ls:
    t_takeoff = find_takeoff(new_df, elem)
    t_landing = find_landing(new_df, elem)
    flight_time = t_landing-t_takeoff
    jump_height = (0.982*flight_time)/8
    dist_ls.append(jump_height)
  return dist_ls

#normalize data
def normalize(df):
    result = df.copy()
    for feature_name in df.columns: #normalize by rows
      if feature_name != "Time": #only normalize accelerations
        max_value = df[feature_name].max()
        min_value = df[feature_name].min()
        result[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
    return result

def ML_processing(new_df, all_acc_ls):
  lst=[]
  for elem in all_acc_ls:
    pk_index = new_df.loc[new_df['ax(g)'] == elem].index[0] #retrieves first instance
    shaped_data = new_df.iloc[pk_index-5: pk_index+20,]
    #we need to only look at x_axis
    df = shaped_data.iloc[:,3]
    df = pd.DataFrame(df)

    #transform dataframe into list to store multiple
    inp_norm = np.array(normalize(df))
    arr = inp_norm.reshape(1,25)
    lst.append(arr)
  
  return lst

def diff_jumps(lst, filename):
  lst_class=[]
  x_test = np.vstack(lst)

  # load the model from drive
  loaded_model = pickle.load(open(filename, 'rb'))
  #put into model for classification
  rfc_predict = loaded_model.predict(x)

  for i in rfc_predict:
    if i == 1:
      lst_class.append('Approach jump')
    else:
      lst_class.append('Block jump')

  from collections import Counter
  dict_class = Counter(lst_class)
  return dict_class,lst_class

def get_jump_stats(jump_dict, class_lst, height):
  count_block = jump_dict.get("Block jump")
  count_approach = jump_dict.get("Approach jump")

  #split into block and approach jumps
  b_lst=[]
  a_lst=[]

  for i in range(len(class_lst)):
    if class_lst[i]=="Block jump":
      b_lst.append(height[i])
    else:
      a_lst.append(height[i])

  #find avg and max block jump height
  if len(b_lst)==0:
    avg_block_height=0
    max_block_height=0
  else:
    avg_block_height = sum(b_lst)/len(b_lst)
    max_block_height = max(b_lst)

  #find avg and max approach jump height
  if len(a_lst)==0:
      avg_approach_height=0
      max_approach_height=0
  else:
    avg_approach_height = sum(a_lst)/len(a_lst)
    max_approach_height = max(a_lst)

  return({"Block":[count_block, avg_block_height, max_block_height], 
          "Approach":[count_approach, avg_approach_height, max_approach_height]})

"""##Final functions to get the required variables"""


get_csv()
#link is the name of the csv file created by get_csv()
data_processing_NEW(link)
new_df = data_processing_NEW(link)
jump_data = get_jump(new_df) 

#find jump height & quantify jumps
total_jump = len(jump_data[0])
all_jump_acc = jump_data[1]["peak_heights"]
height = jump_height(new_df, all_jump_acc)

#differentiate jumps
jump_lst = ML_processing(new_df, all_jump_acc)
#filename: directory where the trained model is saved
jump_dict, class_lst = diff_jumps(jump_lst, filename)
final_dict = get_jump_stats(jump_dict, class_lst, height)

#final_dict - dictionary of stats for different jumps
