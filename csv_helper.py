import csv
import os
import pandas as pd

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
  task_sets_dict = [parse_task_set_to_dict(gt.generate_valid_task_set(target_u)) for _ in range(total_count)]
  
  with open(filename + '.csv', 'a', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=header)

    for ts in task_sets_dict:
      writer.writerow(ts)

def write_target_u_to_csv(total_count, header, target_u_list = []):
  for target_u in target_u_list:
    filename = 'task_sets_{}_{}'.format(int(target_u * 1000), total_count)
    write_task_sets_to_csv(total_count, filename, header, target_u)

def read_csv_to_dataframe(filename, limit = None):
  task_sets_dict_list = []
  with open(filename + '.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
      task_sets_dict_list.append(parse_csv_row_to_dict(row)) 
      if limit and len(task_sets_dict_list) >= limit:
        break
  
  return pd.DataFrame(task_sets_dict_list)

TOTAL_COUNT = 10000
HEADER = ['num_tasks', 't_max', 'utilization', 'thm1', 'thm2', 'thm3', 'lo_tasks_list', 'hi_tasks_list']
UTARGETS = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.975]

if __name__ == "__main__":
  write_target_u_to_csv(total_count =   TOTAL_COUNT, 
                        header =        HEADER, 
                        target_u_list = UTARGETS)