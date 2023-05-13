import pytest
import random as r

import generate_tasks as gt 

@pytest.fixture
def get_seed():
  return 70

@pytest.fixture
def min_u():
  return 0.02

@pytest.fixture
def max_u():
  return 0.25

@pytest.fixture
def utilization(min_u, max_u):
  return r.uniform(min_u, max_u)

@pytest.fixture
def target_u():
  return 0.7

@pytest.fixture
def get_seed():
  return 70

@pytest.fixture
def random_task(utilization):
  return gt.generate_task(utilization)

@pytest.fixture
def random_task_set(target_u):
  return gt.Task_Set(target_u)

@pytest.fixture
def task_set(get_seed, target_u):
  r.seed(get_seed)

  return gt.Task_Set(target_u)

@pytest.fixture
def unconstrained_task_set(target_u):
  while True:
    unconstrained_task_set = gt.Task_Set(target_u)
    if all([task.D > task.T for task in unconstrained_task_set.task_set]):
      break

  return unconstrained_task_set

def test_canary():
  assert True

''' TEST TASK ATTRIBUTES AND ASSUMPTIONS '''

def test_level_HI_or_LO():
  assert isinstance(gt.generate_L(), gt.Level)

def test_C_LO_greater_than_5_inclusive():
  assert gt.generate_C_LO() >= 5

def test_C_LO_less_than_25_inclusive():
  assert gt.generate_C_LO() <= 25

def test_C_LO_is_13(get_seed):
  r.seed(get_seed)

  assert gt.generate_C_LO() == 8

def test_C_HI_is_C_LO_when_L_is_LO():
  C_LO = gt.generate_C_LO()

  assert gt.generate_C_HI(C_LO, gt.Level.LO) == C_LO

def test_C_HI_greater_than_10_inclusive():
  C_LO = gt.generate_C_LO()

  assert gt.generate_C_HI(C_LO, gt.Level.HI) >= 10

def test_C_HI_less_than_100_inclusive():
  C_LO = gt.generate_C_LO()
  
  assert gt.generate_C_HI(C_LO, gt.Level.HI) <= 100

def test_C_HI_is_57(get_seed):
  r.seed(get_seed)

  assert gt.generate_C_HI(25, gt.Level.HI) == 57

def test_D_greater_than_C_HI_inclusive():
  C_HI = gt.generate_C_HI(gt.generate_C_LO(), gt.Level.HI)
  
  assert gt.generate_D(C_HI) >= C_HI

def test_D_less_than_500_inclusive():
  C_HI = gt.generate_C_HI(gt.generate_C_LO(), gt.Level.HI)
  
  assert gt.generate_D(C_HI) <= 500

def test_T_minimum_is_100(max_u):
  assert gt.generate_T(5, max_u) == 20

def test_T_maximum_known_is_1500(min_u):
  assert gt.generate_T(25, min_u) == 1250

def test_T_greater_than_C_HI(max_u):
  C_LO = gt.generate_C_LO()
  C_HI = gt.generate_C_HI(C_LO, gt.Level.HI)
  
  assert gt.generate_T(C_LO, max_u) >= C_HI

def test_task_C_LO_less_than_C_HI_inclusive(random_task):
  assert random_task.C_LO < random_task.C_HI if random_task.L == gt.Level.HI else random_task.C_LO == random_task.C_HI

def test_task_C_HI_less_than_T_inclusive(random_task):
  assert random_task.C_HI <= random_task.T 

def test_task_max_C_HI_equal_min_T(random_task, max_u):
  random_task.C_HI = 4 * random_task.C_LO
  random_task.T = gt.generate_T(random_task.C_LO, max_u)

  assert random_task.C_HI == random_task.T

''' TEST TASK SET METHODS '''

def test_utilizations_greater_than_0_exclusive(random_task_set, target_u):
  assert min(random_task_set.generate_kato_utilizations(target_u)) > 0

def test_utilizations_less_than_maxu_inclusive(random_task_set, target_u, max_u):
  assert max(random_task_set.generate_kato_utilizations(target_u)) < max_u + 0.00001

def test_utilizations_sum_equal_target_sum(random_task_set, target_u):
  assert sum(random_task_set.generate_kato_utilizations(target_u)) == pytest.approx(target_u)

def test_task_set_utilization_approximately_target_u(random_task_set, target_u):
  assert target_u - random_task_set.utilization < 0.05

def test_lcmT_maxD_returns_134523906(task_set):
  assert task_set.lcmT_maxD() == 134523906

def test_U_maxTD_returns_114(task_set):
  assert task_set.U_maxTD() == 114
  
def test_t_max_returns_114(task_set):
  assert task_set.calculate_t_max() == 114

def test_t_max_is_positive(random_task_set):
  assert random_task_set.calculate_t_max() >= 0

def test_t_max_is_zero_unconstrained_task_set(unconstrained_task_set):
  assert unconstrained_task_set.calculate_t_max() == 0

''' TEST TASK SET '''
def test_task_set_not_empty(random_task_set):
  assert random_task_set.num_tasks > 0

def test_task_set_lo_is_lo(random_task_set):
  assert all([task.L == gt.Level.LO for task in random_task_set.lo_tasks_list])

def test_task_set_hi_is_hi(random_task_set):
  assert all([task.L == gt.Level.HI for task in random_task_set.hi_tasks_list])

''' TEST VALID TASK SETS GENERATOR '''

def test_valid_task_sets_t_max_greater_0(target_u):
  task_set = gt.generate_valid_task_set(target_u)

  assert task_set.t_max > 0


