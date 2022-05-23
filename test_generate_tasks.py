from generate_tasks import task, task_generation

def print_task_set(task_set):
  for t in task_set:
    print("ID:{}, WCET_LO:{}, WCET_HI:{}, T:{}, D:{}".format(t.ID, t.WCET_LO, t.WCET_HI, t.T, t.D))

def cal_real_u_sum(task_set):
  sum = 0
  for t in task_set:
    sum += t.WCET_LO/t.T
  return sum

if __name__ == '__main__':
  G = task_generation()
  for u_sum in [0.5, 0.6, 0.7, 0.8, 0.9]:
    task_set = G.create_task_set(u_sum, 0.02, 0.25)
    print("------- Current utilization sum: {}---------".format(u_sum))
    print_task_set(task_set)
    print("Real utilization sum: {}".format(cal_real_u_sum(task_set)))

'''
# the unit tests of the prebious generate_tasks.py
import pytest
import generate_tasks as gt
import random as r

def test_min_sep_between_5_and_100():
  assert gt.generate_T() >= 5 and gt.generate_T() <= 100

def test_LO_computation_time_is_integer():
  assert isinstance(gt.generate_C_Lo(5), int)

def test_LO_computation_time_for_5_between_1_and_2():
  assert gt.generate_C_Lo(5) >= 1 and gt.generate_C_Lo(5) <= 2

def test_LO_computation_time_for_100_between_2_and_25():
  assert gt.generate_C_Lo(100) >= 2 and gt.generate_C_Lo(100) <= 25

def test_HI_computation_time_for_13_between_26_and_52():
  assert gt.generate_C_Hi(13) >= 26 and gt.generate_C_Hi(13) <= 52

def test_deadline_for_34_between_34_and_100():
  assert gt.generate_D(34) >= 34 and gt.generate_D(34) <= 100

def test_level_HI_or_LO():
  assert isinstance(gt.generate_L(), gt.Level)

def test_utilization_bound_in_list():
  assert gt.generate_utilization_bound() in [0.5, 0.6, 0.7, 0.8, 0.9]

def test_is_utilization_valid_returns_true():
  assert gt.is_utilization_valid([1, 1, 4], [4, 4, 8], 1)

def test_is_utilization_valid_returns_false():
  assert gt.is_utilization_valid([1, 1, 4], [4, 4, 7], 1) is False

def test_is_utilization_valid_error_different_lengths():
  with pytest.raises(AssertionError, match = "Input lists must be the same length."):
    gt.is_utilization_valid([1], [4, 4, 8], 1)

def test_calculate_utilization_is_1():
  assert gt.calculate_utilization([1, 1, 4], [4, 4, 8]) == 1

def unpack_task_set(task_set):
  CLos = []
  CHis = []
  Ds = []
  Ts = []
  Ls = []

  for task in task_set:
    CLo, CHi, _, D, T, L = task
    CLos.append(CLo)
    CHis.append(CHi)
    Ds.append(D)
    Ts.append(T)
    Ls.append(L)
    
  return CLos, CHis, Ds, Ts, Ls

def test_create_task_set_utilization_less_than_1():
  _, CHis, _, Ts, _ = unpack_task_set(gt.create_task_set())

  assert gt.is_utilization_valid(CHis, Ts, 1)

def test_create_task_set_CHi_less_than_deadline():
  _, CHis, Ds, _, _ = unpack_task_set(gt.create_task_set())

  assert [CHi <= D for (CHi, D) in zip(CHis, Ds)]

def test_create_task_set_CHi_less_than_min_separation():
  _, CHis, _, Ts, _ = unpack_task_set(gt.create_task_set())

  assert [CHi <= T for (CHi, T) in zip(CHis, Ts)]
'''