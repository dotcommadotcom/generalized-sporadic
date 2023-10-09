import dbfs as dbf

def schedulability_test_thm1(task_set):
  if task_set.t_max == 0: return False

  return not any(dbf.sum_dbf(task_set, i, j) > i  for i in range(2, task_set.t_max + 1) for j in range(1, i))

def schedulability_test_thm2(task_set):
  if task_set.t_max == 0: return False

  return not any(dbf.sum_dbf_LO(task_set, i) > i for i in range(1, task_set.t_max + 1))

def schedulability_test_thm3(task_set):
  if task_set.t_max == 0: return False

  return not any(dbf.sum_dbf_HI(task_set, i, 0) > i for i in range(1, task_set.t_max + 1))