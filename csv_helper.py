import csv
import os
import pandas as pd
import numpy as np

import generate_tasks as gt

def parse_task_set_to_dict(task_set):
  return {
          'num_tasks':      task_set.num_tasks,
          't_max':          task_set.t_max,
          'utilization':    task_set.utilization,
          'thm1':           task_set.thm1,
          'thm2':           task_set.thm2,
          'thm3':           task_set.thm3,
          'lo_tasks_list':  task_set.lo_tasks_list,
          'hi_tasks_list':  task_set.hi_tasks_list,
          }

def parse_str_to_bool(bool_string):
  if isinstance(bool_string, bool): return bool_string
  return True if bool_string == 'True' else False if bool_string == 'False' else None

def parse_str_to_tasks(task_set_str):
  task_list = []
  for task_str in task_set_str.strip('[]').split('), '):
    if len(task_str.strip('Task()').split(',')) > 1:
      task_attrs = [int(attr_str) for attr_str in task_str.strip('Task()').split(',')]
      task = gt.Task(*task_attrs)
      task_list.append(task)
  return task_list

def parse_csv_row_to_dict(row):
  return {
          'num_tasks':      int(row["num_tasks"]),
          't_max':          int(row["t_max"]),
          'utilization':    float(row["utilization"]),
          'thm1':           parse_str_to_bool(row["thm1"]),
          'thm2':           parse_str_to_bool(row["thm2"]),
          'thm3':           parse_str_to_bool(row["thm3"]),
          'lo_tasks_list':  parse_str_to_tasks(row["lo_tasks_list"]),
          'hi_tasks_list':  parse_str_to_tasks(row["hi_tasks_list"])
          } 

def is_header_exists(filename):
  if not os.path.exists(filename): return False

  with open(filename + '.csv', 'r') as f:
    reader = csv.reader(f)
    first_row = next(reader)
  
  return all(isinstance(val, str) for val in first_row)

def write_header(filename, header):
  if is_header_exists(filename): return
  
  with open(filename + '.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=header)
    writer.writeheader()

def write_task_sets_to_csv(total_count, filename, header, target_u = 0.5):
  write_header(filename, header)
  task_sets_dict = [parse_task_set_to_dict(gt.Task_Set(target_u)) for _ in range(total_count)]
  
  with open(filename + '.csv', 'a', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=header)

    for ts in task_sets_dict:
      writer.writerow(ts)

def write_target_u_to_csv(total_count, header, target_u_list = []):
  for target_u in target_u_list:
    filename = './db2_{}/db_{}_{}'.format(total_count, int(target_u * 1000), total_count)
    write_task_sets_to_csv(total_count, filename, header, target_u)

def read_csv_to_dataframe(filename, limit = None):
  task_sets_dict_list = []
  if 'csv' not in filename: filename = filename + '.csv'
  
  with open(filename, 'r') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
      task_sets_dict_list.append(parse_csv_row_to_dict(row)) 
      if limit and len(task_sets_dict_list) >= limit:
        break
  
  return pd.DataFrame(task_sets_dict_list)

def read_csv_to_processed_dataframe(filename):
  with open(filename, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    database = [row for row in reader]
  
  df = pd.DataFrame(database)
  df['num_tasks'] = df['num_tasks'].astype(int)
  df['t_max'] = df['t_max'].astype(int)
  df['utilization'] = df['utilization'].astype(float)
  df["thm1"] = df["thm1"].replace("True", True)
  df["thm1"] = df["thm1"].replace("False", False)
  df["thm2"] = df["thm2"].replace("True", True)
  df["thm2"] = df["thm2"].replace("False", False)  
  df["thm3"] = df["thm3"].replace("True", True)
  df["thm3"] = df["thm3"].replace("False", False)

  return df

def get_csv_filepath(filepath):
  return sorted([filepath + file for file in os.listdir(filepath) if file.endswith('.csv')])

def get_filtered_filenames(origin_path, prefix):
  filtered_files = []
  for file in os.listdir(origin_path):
    if file.startswith(prefix) and file.endswith('.csv'):
      filtered_files.append(origin_path + file)
  return filtered_files

def preprocess_data_remove_duplicates(file_names):
  dfs = []
  for file_name in file_names:
    df = pd.read_csv(file_name)  
    df = df.dropna()
    assert not df.isnull().any().any(), "DataFrame contains NaN values"
    dfs.append(df)
  
  combined_df = pd.concat(dfs, ignore_index=True)  
  combined_df.drop_duplicates(inplace=True)  
  combined_df["thm1"] = combined_df["thm1"].astype(bool)
  combined_df["thm2"] = combined_df["thm2"].astype(bool)
  combined_df["thm3"] = combined_df["thm3"].astype(bool)
  # combined_df = combined_df.sample(n=11000)
  return combined_df

COUNT_PER_USUM = 10000
HEADER = ['num_tasks', 't_max', 'utilization', 'thm1', 'thm2', 'thm3', 'lo_tasks_list', 'hi_tasks_list']
# UTARGETS = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.975]
UTARGETS = np.arange(0.3, 0.825, 0.025)
print(UTARGETS)
# USUM = 0.8
# FILENAME = './db2_{}/db_{}_{}'.format(COUNT_PER_USUM, USUM, COUNT_PER_USUM * len(UTARGETS))

# if __name__ == "__main__":
  # print("running..........")
  # write_target_u_to_csv(total_count =   COUNT_PER_USUM, 
  #                       header =        HEADER, 
  #                       target_u_list = UTARGETS)

  # task_sets_db, task_sets_df = read_csv_to_processed_dataframe(FILENAME)

  # print(task_sets_df)