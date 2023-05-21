import pytest
import random as r

import generate_tasks as gt 

@pytest.fixture
def get_seed():
  return 70

@pytest.fixture
def random_target_u():
  return r.choice([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])

@pytest.fixture
def get_seed():
  return 70

@pytest.fixture
def random_task():
  return gt.generate_task()

@pytest.fixture
def random_task_set(random_target_u):
  return gt.Task_Set(random_target_u)

@pytest.fixture
def task_set():
  task_set_dict = {'num_tasks': 6, 
                   't_max': 261, 
                   'utilization': 0.6964358021917052, 
                   'thm1': None, 
                   'thm2': None, 
                   'thm3': None, 
                   'lo_tasks_list': [gt.Task(0, 414, 13, 13, 300, 300), gt.Task(3, 115, 14, 14, 267, 267), gt.Task(5, 94, 7, 7, 172, 172)], 
                   'hi_tasks_list': [gt.Task(1, 122, 23, 46, 312, 312), gt.Task(2, 108, 18, 37, 107, 107), gt.Task(4, 132, 15, 50, 233, 233)]}
  
  return gt.Task_Set(task_set_dict = task_set_dict)

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

def test_C_HI_gt_10_lt_100_inclusive():
  C_LO = gt.generate_C_LO()
  
  assert 10 <= gt.generate_C_HI(C_LO, gt.Level.HI, 4) <= C_LO * 4

def test_C_HI_is_57(get_seed):
  r.seed(get_seed)

  assert gt.generate_C_HI(25, gt.Level.HI, 4) == 57

def test_D_gt_C_HI_lt_500_inclusive():
  C_HI = gt.generate_C_HI(gt.generate_C_LO(), gt.Level.HI)
  
  assert C_HI <= gt.generate_D(C_HI) <= 500

def test_T_gt_C_HI_lt_500_inclusive():
  C_LO = gt.generate_C_LO()
  C_HI = gt.generate_C_HI(C_LO, gt.Level.HI)
  
  assert C_HI <= gt.generate_T(C_HI) <= 500

def test_task_C_LO_less_than_C_HI_inclusive(random_task):
  assert random_task.C_LO < random_task.C_HI if random_task.L == gt.Level.HI else random_task.C_LO == random_task.C_HI

def test_task_C_HI_less_than_D_inclusive(random_task):
  assert random_task.C_HI <= random_task.D

def test_task_C_HI_less_than_T_inclusive(random_task):
  assert random_task.C_HI <= random_task.T 

''' TEST TASK SET METHODS '''

def test_task_set_utilization_approximately_target_u(random_task_set, random_target_u):
  assert random_target_u - random_task_set.utilization < 0.05

def test_lcmT_maxD_returns_391689852(task_set):
  assert task_set.lcmT_maxD() == 391689852

def test_U_maxTD_returns_261(task_set):
  assert task_set.U_maxTD() == 261
  
def test_t_max_returns_261(task_set):
  assert task_set.calculate_t_max() == 261

def test_t_max_is_positive(random_task_set):
  assert random_task_set.calculate_t_max() > 0

''' TEST TASK SET '''

def test_task_set_not_empty(random_task_set):
  assert random_task_set.num_tasks > 0

def test_task_set_num_tasks_is_length(random_task_set):
  assert random_task_set.num_tasks == len(random_task_set.task_set)

def test_task_set_t_max_pos(random_task_set):
  assert random_task_set.t_max > 0

def test_task_set_lo_is_lo(random_task_set):
  assert all([task.L == gt.Level.LO for task in random_task_set.lo_tasks_list])

def test_task_set_hi_is_hi(random_task_set):
  assert all([task.L == gt.Level.HI for task in random_task_set.hi_tasks_list])


