import pytest
import random as r
import torch as tr

import dbfs as dbf
import generate_tasks as gt

@pytest.fixture
def one(): 
  return tr.tensor(1)

@pytest.fixture
def upper(): 
  return tr.tensor(100)

@pytest.fixture
def t(): 
  return tr.tensor(1000)

@pytest.fixture
def get_seed(): return 70

@pytest.fixture
def task_set(get_seed):
  r.seed(get_seed)

  return gt.Task_Set(0.8)

@pytest.fixture
def task_set_list(task_set):
  return task_set.task_set

@pytest.fixture
def LO_task(task_set_list, get_seed):
  r.seed(get_seed)

  while True:
    task = r.choice(task_set_list)
    if task.L == gt.Level.LO: break
  
  return task

@pytest.fixture
def HI_task(task_set_list, get_seed):
  r.seed(get_seed)

  while True:
    task = r.choice(task_set_list)
    if task.L == gt.Level.HI:
      break
  return task

@pytest.fixture
def random_target_u(): 
  return r.choice([0.5, 0.6, 0.7, 0.8, 0.9])

@pytest.fixture
def random_task(random_target_u): 
  return gt.generate_task(random_target_u)

@pytest.fixture
def random_HI_task(random_target_u):
  while True:
    random_HI_task = gt.generate_task(random_target_u)
    if random_HI_task.L == gt.Level.HI: break
  
  return random_HI_task

@pytest.fixture
def random_LO_task(random_target_u):
  while True:
    random_LO_task = gt.generate_task(random_target_u)
    if random_LO_task.L == gt.Level.LO: break
  
  return random_LO_task






''' TEST MAX_REQUESTS FUNCTION '''

def test_max_requests_is_positive_upper_greater_lower(one, upper):
  ''' upper > lower --> k > 0 '''

  assert dbf.max_requests(one, upper, upper - 1) > 0

def test_max_requests_is_1_upper_is_lower(one, upper):
  ''' upper == lower --> k == 1 '''

  assert dbf.max_requests(one, upper, upper) == 1

def test_max_requests_is_zero_upper_less_lower(one, upper):
  ''' upper < lower --> k == 0 '''

  assert dbf.max_requests(one, upper, upper + 4) == 0

def test_max_requests_is_n_plus_1_upper_greater_equal_lower(t):
  ''' upper >= lower --> k == n + 1 '''

  upper = tr.randint(high = t * t, size = (1,))
  lower = tr.randint(high = int(upper), size = (1,))
  T = tr.randint(1, high = t, size = (1,))

  n = tr.floor_divide(upper - lower, T)

  assert dbf.max_requests(T, upper, lower) == n + 1

def test_max_requests_at_nT_and_nT_minus_one_different(t):
  ''' i - j >= T --> k_i != k_j '''

  upper = tr.randint(high = t * t, size = (1,)) 
  lower = tr.randint(high = int(upper), size = (1,))
  T = tr.randint(high = t, size = (1,))
  n = tr.floor_divide(upper - lower, T)

  lower1 = upper - n * T + 1
  lower2 = upper - n * T

  assert dbf.max_requests(T, upper, lower1) != dbf.max_requests(T, upper, lower2) 

def test_max_requests_at_nT_and_n1T_minus_one_same(t):
  ''' i - j < T --> k_i == k_j '''

  upper = tr.randint(high = t * t, size = (1,)) 
  lower = tr.randint(high = int(upper), size = (1,))
  T = tr.randint(high = t, size = (1,))
  n = tr.floor_divide(upper - lower, T)

  lower1 = upper - n * T
  lower2 = upper - (n + 1) * T + 1

  assert dbf.max_requests(T, upper, lower1) == dbf.max_requests(T, upper, lower2)







''' TEST LOWER FUNCTION '''

def test_lower_is_869(HI_task, t):
  _, T, _, _, _, tight_D = HI_task.to_tensor()

  T2, tight_D2 = 79, 180

  assert dbf.lower(T, tight_D, t) == T2 * max((1000 - tight_D2)//T2 + 1, 0) == 869

def test_lower_is_positive_ts_is_D(random_task):
  ''' ts >= D --> lower > 0 '''

  _, T, _, _, _, tight_D = random_task.to_tensor()

  assert dbf.lower(T, tight_D, tight_D) > 0

def test_lower_is_zero_ts_less_D(random_task):
  ''' ts < D --> lower == 0 '''

  _, T, _, _, _, tight_D = random_task.to_tensor()

  assert dbf.lower(T, tight_D, tight_D - 1) == 0







''' TEST UPPER_CO FUNCTION '''

def test_upper_CO_is_425(HI_task, t):
  _, T, _, _, D, _ = HI_task.to_tensor()

  T2, D2 = 79, 180

  assert dbf.upper_CO(T, D, t, t // 2) == 1000 - D2 - T2 * max((1000 - 500 - D2)//T2 + 1, 0) == 425
 
def test_upper_CO_less_ts(random_HI_task, t):
  ''' ∀ 0 < ts < t, upper_co < ts '''

  _, T, _, _, D, _ = random_HI_task.to_tensor()

  assert all([dbf.upper_CO(T, D, t, ts) < ts for ts in tr.arange(1, t)])







''' TEST UPPER_UN FUNCTION '''

def test_upper_UN_is_500(LO_task, t):
  _, _, _, _, _, tight_D = LO_task.to_tensor()

  D2 = 180

  assert dbf.upper_UN(tight_D, t, t // 2) == min(500, 1000 - D2) == 500

def test_upper_UN_is_positive_t_greater_D(random_LO_task, one):
  ''' t > D --> upper_un > 0 '''

  _, _, _, _, _, tight_D = random_LO_task.to_tensor()

  assert dbf.upper_UN(tight_D, tight_D + 1, one) > 0







''' TEST DBF FUNCTION '''

def test_dbf_is_35_upper_greater_lower(upper, one):
  ''' upper > lower --> dbf == C * k '''

  assert dbf.demand_based_function(one * 5, one * 15, upper, one - 1) == 35

def test_dbf_is_5_upper_is_lower(upper, one):
  ''' upper == lower --> dbf == C '''

  assert dbf.demand_based_function(one * 5, one * 15, upper, upper) == 5

def test_dbf_is_zero_upper_less_lower(upper, one):
  ''' upper < lower --> dbf == 0 '''

  assert dbf.demand_based_function(one * 5, one * 15, upper, upper + 1) == 0






''' TEST DBF_LO FUNCTION '''

def test_dbf_LO_is_104(LO_task, t):
  _, T, C_LO, _, _, tight_D = LO_task.to_tensor()
  
  T2, C_LO2, tight_D2 = 104, 13, 205

  assert dbf.demand_based_function_LO(C_LO, T, tight_D, t) == C_LO2 * max((1000 - tight_D2)//T2 + 1, 0) == 104

def test_dbf_LO_is_zero_ts_less_D(random_task):
  ''' ts < tight_D --> dbf_LO == 0 '''

  _, T, C_LO, _, _, tight_D = random_task.to_tensor()

  assert dbf.demand_based_function_LO(C_LO, T, tight_D, tight_D - 1) == 0






''' TEST DBF_HI FUNCTION '''

def test_dbf_HI_is_300(HI_task, t):
  _, T, _, C_HI, D, _ = HI_task.to_tensor()

  T2, C_HI2, D2 = 79, 60, 180

  assert dbf.demand_based_function_HI(C_HI, T, D, t, t // 2) == C_HI2 * max((1000 - D2 - 500)//T2 + 1, 0) == 300

def test_dbf_HI_is_zero_t_ts_less_D(random_HI_task, t):
  ''' t - ts - D < 0 --> dbf_HI == 0 '''

  _, T, _, C_HI, D, _ = random_HI_task.to_tensor()

  assert dbf.demand_based_function_HI(C_HI, T, D, t, t - D + 1) == 0






''' TEST DBF_CO FUNCTION '''

def test_dbf_CO_is_60(HI_task, t):
  _, T, _, C_HI, D, tight_D = HI_task.to_tensor()

  T2, C_HI2, D2, tight_D2 = 79, 60, 180, 180
  upper2 = 1000 - D2 - T2 * max((1000 - 500 - D2)//T2 + 1, 0)
  lower2 = T2 * max((500 - tight_D2)//T2 + 1, 0)

  assert dbf.demand_based_function_CO(C_HI, T, D, tight_D, t, t // 2) == C_HI2 * max((upper2 - lower2)//T2 + 1, 0) == 60

def test_dbf_CO_is_zero_t_less_D(random_HI_task):
  ''' t < D --> upper < 0 --> dbf_CO == 0 '''

  _, T, _, C_HI, D, tight_D = random_HI_task.to_tensor()
  t = D - 1
  ts = tr.randint(1, high = t - 1, size = (1,))

  assert dbf.demand_based_function_CO(C_HI, T, D, tight_D, t, ts) == 0

def test_dbf_CO_is_zero_ts_less_condition(random_HI_task):
  ''' t > D and ts <= t - D - (t-D)//T * T --> upper < 0 --> dbf_CO == 0 '''

  _, T, _, C_HI, D, tight_D = random_HI_task.to_tensor()
  t = D + 100
  ts = t - D - (t - D)//T * T

  assert dbf.demand_based_function_CO(C_HI, T, D, tight_D, t, ts) == 0

def test_dbf_CO_is_zero_t_is_D_ts_is_Ds(random_HI_task):
  ''' t == D and ts >= tight_D --> upper == 0 and lower > 0 --> dbf_CO == 0 '''

  _, T, _, C_HI, D, _ = random_HI_task.to_tensor()
  t = D
  tight_D = D // 2
  ts = tight_D

  assert dbf.demand_based_function_CO(C_HI, T, D, tight_D, t, ts) == 0

def test_dbf_CO_is_zero_up_less_low_for_ts(random_HI_task):
  ''' t > D and ts >= (t-D)//T * T + tight_D --> upper < lower --> dbf_CO == 0 '''

  _, T, _, C_HI, D, _ = random_HI_task.to_tensor()
  t = D + 100
  tight_D = D // 2
  ts = tr.floor_divide((t - D), T) * T + tight_D

  assert dbf.demand_based_function_CO(C_HI, T, D, tight_D, t, ts) == 0

def test_dbf_CO_is_zero_up_less_low_for_all(random_HI_task):
  ''' t - D - (t-D)//T * T >= tight_D --> upper < lower --> dbf_CO == 0 '''
  # need to prove, unfinished test

  _, T, _, C_HI, D, _ = random_HI_task.to_tensor()
  t = D + 100
  tight_D = t - D - (t - D)//T * T
  ts = tr.randint(low = 1, high = t, size = (1,)) 

  assert dbf.demand_based_function_CO(C_HI, T, D, tight_D, t, ts) == 0






''' TEST DBF_UN FUNCTION '''

def test_dbf_UN_is_26(LO_task, t):
  _, T, C_LO, _, _, tight_D = LO_task.to_tensor()

  T2, C_LO2, tight_D2 = 79, 13, 180
  upper2 = min(500, 1000 - tight_D2)
  lower2 = T2 * max((500 - tight_D2)//T2 + 1, 0)
  k = max((upper2 - lower2)// T2 + 1, 0)

  assert dbf.demand_based_function_UN(C_LO, T, tight_D, t, t // 2) == int(k * min(C_LO2, 500 - lower2 - (k - 1) * T2 / 2)) == 26

def test_dbf_UN_is_positive_upper_is_positive_lower_is_zero(random_LO_task):
  ''' upper > 0 and lower == 0 --> dbf_UN > 0 '''

  _, T, C_LO, _, D, tight_D = random_LO_task.to_tensor()

  assert dbf.demand_based_function_UN(C_LO, T, tight_D, D + 1, tight_D - 1) > 0

def test_dbf_UN_is_C_LO_upper_lower_is_zero_C_LO_D_min_difference_1(random_LO_task):
  ''' upper == 0 and lower == 0 --> dbf_UN == C_LO '''

  _, T, C_LO, _, D, tight_D = random_LO_task.to_tensor()

  assert dbf.demand_based_function_UN(C_LO, T, tight_D, D, tight_D - 1) == random_LO_task.C_LO

def test_dbf_UN_is_zero_upper_is_negative(random_LO_task, one):
  ''' upper < 0 --> dbf_UN == 0 '''

  _, T, C_LO, _, D, tight_D = random_LO_task.to_tensor()

  assert dbf.demand_based_function_UN(C_LO, T, tight_D, D - 1, one) == 0

def test_dbf_UN_is_zero_upper_is_zero_lower_is_positive(random_LO_task):
  ''' upper == 0 and lower > 0 --> dbf_UN == C_LO '''

  _, T, C_LO, _, D, tight_D = random_LO_task.to_tensor()

  assert dbf.demand_based_function_UN(C_LO, T, tight_D, D, tight_D) == 0






''' TEST SUM_DBF FUNCTION '''

def test_sum_dbf_LO_is_693(task_set, t):
  demand = sum([task.C_LO * max((1000 - task.tight_D)//task.T + 1, 0) for task in task_set.task_set])

  assert dbf.sum_dbf_LO(task_set.to_tensor(), t) == demand == 693

def test_sum_dbf_HI_is_634(task_set, t):
  demand = sum([task.C_HI * max((1000 - task.D - 500)//task.T + 1, 0) for task in task_set.hi_tasks_list])

  assert dbf.sum_dbf_HI(task_set.to_tensor(task_set.hi_tasks_list), t, t//2) == demand == 634

def test_sum_dbf_CO_is_226(task_set, t):
  demand = sum([task.C_HI * max(((1000 - task.D - task.T * max((1000 - 500 - task.D)//task.T + 1, 0)) - (task.T * max((500 - task.tight_D)//task.T + 1, 0)))//task.T + 1, 0) for task in task_set.hi_tasks_list])

  assert dbf.sum_dbf_CO(task_set.to_tensor(task_set.hi_tasks_list), t, t//2) == demand == 226

def test_sum_dbf_UN_is_62(task_set, t):
  upper_list = [min(500, 1000 - task.tight_D) for task in task_set.lo_tasks_list]
  lower_list = [task.T * max((500 - task.tight_D)//task.T + 1, 0) for task in task_set.lo_tasks_list]
  k = [max((upper - lower)// task.T + 1, 0) for upper, lower, task in zip(upper_list, lower_list, task_set.lo_tasks_list)]
  demand = sum([int(k * min(task.C_LO, 500 - lower - (k - 1) * task.T / 2)) for k, lower, task in zip(k, lower_list, task_set.lo_tasks_list)])

  assert dbf.sum_dbf_UN(task_set.to_tensor(task_set.lo_tasks_list), t, t//2) == demand == 62

def test_sum_dbf_is_1211(task_set, t):
  lo = task_set.to_tensor(task_set.lo_tasks_list)
  hi = task_set.to_tensor(task_set.hi_tasks_list)

  assert dbf.sum_dbf(lo, hi, t, t // 2) == 1211