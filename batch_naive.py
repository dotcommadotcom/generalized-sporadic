import sys
import time
import re
import pandas as pd

import generate_tasks as gt
import csv_helper as ch
import search_algorithm as alg

def run_naive_algorithm(dataframe):
  post_tight_results = []

  for _, row in dataframe.iterrows():
    task_set_dict = ch.parse_csv_row_to_dict(row)
    task_set = gt.Task_Set(task_set_dict=task_set_dict)
    start_time = time.time()
    task_set_dict["naive_result"], task_set_dict["naive_task_set"] = alg.naive(task_set)
    end_time = time.time()
    task_set_dict["naive_time"] = end_time - start_time
    post_tight_results.append(task_set_dict)

  post_tight_df = pd.DataFrame(post_tight_results)

  for i, row in post_tight_df.iterrows():
    post_tight_df.loc[i, "lo_tasks_list"] = str(post_tight_df.loc[i, "lo_tasks_list"])
    post_tight_df.loc[i, "hi_tasks_list"] = str(post_tight_df.loc[i, "hi_tasks_list"])
    post_tight_df.loc[i, "naive_task_set"] = repr(post_tight_df.loc[i, "naive_task_set"])

  return post_tight_df

DATABASE_FILEPATH = './db_simulation/' 
DB_LIST = ch.get_csv_filepath(DATABASE_FILEPATH)

if len(sys.argv) < 2:
  print("Error: Provide utilization tag.")
  sys.exit(1)

if __name__ == "__main__":
  for db in DB_LIST:
    utilization_tag = re.search(r"_([0-9]+)_", db).group(1)
    if int(utilization_tag) == int(sys.argv[1]):
      print("running utilization {} file {}".format(utilization_tag, db))
      df = ch.read_csv_to_processed_dataframe(db)
      post_tight_df = run_naive_algorithm(df)
      post_tight_df.to_csv('./db_test_naive/db_{}_naive.csv'.format(utilization_tag), header = True, index = False)
