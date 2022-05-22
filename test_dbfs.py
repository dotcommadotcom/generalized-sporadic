import pytest
import dbfs as dbf
import generate_tasks as gt
import random as r

def test_canary():
  assert True

def test_lcm():
  assert dbf.lcm([4,5,12,15,30]) == 60

def test_calculate_t_max_returns_160():
  r.seed(36)
  
  assert dbf.calculate_t_max(gt.create_task_set()) == 160

def test_calculate_t_max_always_returns_nonnegative():
  assert dbf.calculate_t_max(gt.create_task_set()) > 0

def test_demand_based_function():
  assert dbf.demand_based_function(7, 4, 6, 4) == 4

def test_demand_based_function_always_nonnegative():
  T = gt.generate_T()
  C = gt.generate_C_Lo(T)
  D = gt.generate_D(C)

  assert dbf.demand_based_function(r.randrange(5, 101), C, D, T) >= 0

def test_max_num_requests():
  assert dbf.max_num_requests(75,63,15,4) == 3

def test_dbf_CO():
  assert dbf.demand_based_function_CO(117, 58, 3, 6, 51, 21) == 18

def test_dbf_UN():
  assert dbf.demand_based_function_UN(117, 58, 1, 86, 75) == 1

def test_total_dbf_HI_with_80_seed():
  r.seed(80)
  t = r.randint(100, 150)
  ts = t//2
  task_set = gt.create_task_set()

  assert dbf.total_dbf_HI(t, ts, task_set) == 6

def test_total_dbf_HI_with_15_seed():
  r.seed(15)
  t = r.randint(100, 150)
  ts = t//2
  task_set = gt.create_task_set()

  assert dbf.total_dbf_HI(t, ts, task_set) == 28

def test_total_dbf_LO_with_80_seed():
  r.seed(80)
  t = r.randint(100, 150)
  ts = t//2
  task_set = gt.create_task_set()

  assert dbf.total_dbf_LO(ts, task_set) == 26

def test_total_dbf_LO_with_15_seed():
  r.seed(15)
  t = r.randint(100, 150)
  ts = t//2
  task_set = gt.create_task_set()

  assert dbf.total_dbf_LO(ts, task_set) == 11

def test_total_dbf_CO_with_80_seed():
  r.seed(80)
  t = r.randint(100, 150)
  ts = t//2
  task_set = gt.create_task_set()

  assert dbf.total_dbf_CO(t, ts, task_set) == 33

def test_total_dbf_CO_with_15_seed():
  r.seed(15)
  t = r.randint(100, 150)
  ts = t//2
  task_set = gt.create_task_set()

  assert dbf.total_dbf_CO(t, ts, task_set) == 46

def test_total_dbf_UN_with_80_seed():
  r.seed(80)
  t = r.randint(100, 150)
  ts = t//2
  task_set = gt.create_task_set()

  assert dbf.total_dbf_UN(t, ts, task_set) == 29

def test_total_dbf_UN_with_15_seed():
  r.seed(15)
  t = r.randint(100, 150)
  ts = t//2
  task_set = gt.create_task_set()

  assert dbf.total_dbf_UN(t, ts, task_set) == 0

def test_calculate_dbf_with_80_seed():
  r.seed(80)
  t = r.randint(100, 150)
  ts = t//2
  task_set = gt.create_task_set()

  assert dbf.calculate_dbf(t, ts, task_set) == 94

def test_calculate_dbf_with_15_seed():
  r.seed(15)
  t = r.randint(100, 150)
  ts = t//2
  task_set = gt.create_task_set()

  assert dbf.calculate_dbf(t, ts, task_set) == 85

def test_schedulability_test_15_seed_returns_true():
  r.seed(15)

  assert dbf.schedulability_test(gt.create_task_set())

def test_schedulability_test_21_seed_returns_false():
  r.seed(21)

  assert dbf.schedulability_test(gt.create_task_set()) is False

