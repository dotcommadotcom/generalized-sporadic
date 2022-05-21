import pytest
import dbfs as dbf
import generate_tasks as gt
import random as r

def test_lcm():
  assert dbf.lcm([4,5,12,15,30]) == 60

def test_calculate_t_max_returns_60():
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

def test_max_num_requests_always_geq_1():
  T = gt.generate_T()
  D = gt.generate_D(gt.generate_C_Lo(T))
  t = r.randint(0, 100)
  ts = t//2

  assert dbf.max_num_requests(t,ts,D,T) >= 1

def test_dbf_CO():
  assert dbf.demand_based_function_CO(117, 58, 6, 51, 21) == 18

def test_dbf_UN():
  assert dbf.demand_based_function_UN(117, 58, 1, 86, 75) == 1


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

def test_schedulability_test_80_seed_returns_true():
  r.seed(6)

  assert dbf.schedulability_test(gt.create_task_set())

def test_schedulability_test_21_seed_returns_false():
  r.seed(21)

  assert dbf.schedulability_test(gt.create_task_set()) is False

