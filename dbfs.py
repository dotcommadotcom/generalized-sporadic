from functools import lru_cache

CACHE_SIZE = 10000

def set_cache_size(length, t_max):
  global CACHE_SIZE
  CACHE_SIZE = length * t_max * t_max

# @lru_cache(maxsize=CACHE_SIZE)
def max_requests(T, upper, lower):
  return max(0, (upper - lower)//T + 1)

# @lru_cache(maxsize=CACHE_SIZE)
def lower(task, ts):
  return task.T * max_requests(task.T, ts, task.tight_D) 

# @lru_cache(maxsize=CACHE_SIZE)
def upper_CO(task, t, ts):
  return t - task.D - task.T * max_requests(task.T, t - ts, task.D)

# @lru_cache(maxsize=CACHE_SIZE)
def upper_UN(task, t, ts):
  return min(ts, t - task.tight_D)

# @lru_cache(maxsize=CACHE_SIZE)
def demand_based_function(C, T, upper, lower):
  return  C * max_requests(T, upper, lower)

# @lru_cache(maxsize=CACHE_SIZE)
def demand_based_function_LO(task, ts):
  return demand_based_function(task.C_LO, task.T, upper = ts, lower = task.tight_D)

def demand_based_function_HI(task, t, ts):
  return demand_based_function(task.C_HI, task.T, upper = t - task.D, lower = ts)

# @lru_cache(maxsize=CACHE_SIZE)
def demand_based_function_CO(task, t, ts):
  return demand_based_function(task.C_HI, task.T, upper_CO(task, t, ts), lower(task, ts))

def demand_based_function_UN(task, t, ts):
  k = max_requests(task.T, upper_UN(task, t, ts), lower(task, ts))

  return int(min(task.C_LO, ts - lower(task, ts) - (k - 1) * task.T / 2) * k)

def sum_dbf_LO(task_set, ts):
  set_cache_size(task_set.num_tasks, task_set.t_max)

  return sum([demand_based_function_LO(task, ts) for task in task_set.task_set.values()])

def sum_dbf_HI(task_set, t, ts):
  set_cache_size(task_set.num_tasks, task_set.t_max)

  return sum([demand_based_function_HI(task, t, ts) for task in task_set.hi_tasks_list])

def sum_dbf_CO(task_set, t, ts):
  set_cache_size(task_set.num_tasks, task_set.t_max)

  return sum([demand_based_function_CO(task, t, ts) for task in task_set.hi_tasks_list])

def sum_dbf_UN(task_set, t, ts):
  set_cache_size(task_set.num_tasks, task_set.t_max)

  return sum([demand_based_function_UN(task, t, ts) for task in task_set.lo_tasks_list])

def sum_dbf(task_set, t, ts):
  set_cache_size(task_set.num_tasks, task_set.t_max)

  demand_sum = 0
  for task in task_set.task_set.values():
    if task.C_LO < task.C_HI:
      demand_sum += demand_based_function_HI(task, t, ts) + demand_based_function_CO(task, t, ts)
    else:
      demand_sum += demand_based_function_UN(task, t, ts)
    demand_sum += demand_based_function_LO(task, ts) 

  return demand_sum