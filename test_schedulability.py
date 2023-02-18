import pytest
import dbfs as dbf
import generate_tasks as gt
import schedulability as s
import random as r
import math as m

@pytest.fixture
def random_u_sum():
  return r.choice([0.5, 0.6, 0.7, 0.8, 0.9])

@pytest.fixture
def random_task(random_u_sum):
  return gt.generate_task(random_u_sum, -1)

@pytest.fixture
def random_LO_task(random_u_sum):
  while True:
    random_LO_task = gt.generate_task(random_u_sum, -1)
    if random_LO_task.L == gt.Level.LO: break
  
  return random_LO_task

@pytest.fixture
def random_HI_task(random_u_sum):
  while True:
    random_HI_task = gt.generate_task(random_u_sum, -1)
    if random_HI_task.L == gt.Level.HI: break
  
  return random_HI_task


@pytest.fixture
def random_task_set(random_u_sum):
  return gt.generate_task_set(random_u_sum, 0.02, 0.25)

@pytest.fixture
def task_set():
  r.seed(69)

  return gt.generate_task_set(0.8, 0.02, 0.25)

@pytest.fixture
def LO_task(task_set):
  r.seed(69)

  while True:
    task = r.choice(task_set)
    if task.L == gt.Level.LO: break
  
  return task

@pytest.fixture
def HI_task(task_set):
  r.seed(69)

  while True:
    task = r.choice(task_set)
    if task.L == gt.Level.HI:
      break
  return task

@pytest.fixture
def unconstrained_task_set(random_u_sum):
  while True:
    unconstrained_task_set = gt.generate_task_set(random_u_sum, 0.02, 0.25)
    if all([task.D > task.T for task in unconstrained_task_set]):
      break

  return unconstrained_task_set

@pytest.fixture
def t():
  return r.randint(0, 1000000)


def test_utilization_close_to_u_sum(random_u_sum, random_task_set):
  assert random_u_sum - s.calculate_utilization(random_task_set) < 0.05

def test_lcmT_maxD_returns_34199401785(task_set):
  assert s.lcmT_maxD(task_set) == 34199401785

def test_U_maxTD_returns_1223(task_set):
  assert s.U_maxTD(task_set) == 1223


def test_t_max_returns_1223(task_set):
  assert s.calculate_t_max(task_set) == 1223

def test_t_max_is_positive(random_task_set):
  assert s.calculate_t_max(random_task_set) >= 0

def test_t_max_is_zero_unconstrained_task_set(unconstrained_task_set):
  assert s.calculate_t_max(unconstrained_task_set) == 0


def test_n_is_10():
  assert s.n(108, 10, 9) == 10


def test_ts_LO_len_less_t(random_task, t):
  assert len(s.ts_LO(random_task, t)) < t

def test_ts_LO_min_is_D(random_task, t):
  assert min(s.ts_LO(random_task, t)) == random_task.tight_D

def test_ts_LO_max_is_nT_D(random_task, t):
  assert max(s.ts_LO(random_task, t)) == random_task.tight_D + s.n(t, random_task.tight_D, random_task.T) * random_task.T

def test_ts_LO_max_less_t(random_task, t):
  assert max(s.ts_LO(random_task, t)) <= t

def test_ts_LO_is_correct(random_task, t):
  assert s.ts_LO(random_task, t) == set(ts for ts in range(t + 1) if ts >= random_task.tight_D and (ts - random_task.tight_D) % random_task.T == 0)

def test_dbf_LO_increases_for_ts_LO(random_task, t):
  assert all([dbf.demand_based_function_LO(random_task, ts) > dbf.demand_based_function_LO(random_task, ts - 1) for ts in s.ts_LO(random_task, t)]) is True

def test_dbf_LO_same_until_next_ts_LO(random_task, t):
  assert all([dbf.demand_based_function_LO(random_task, ts) == dbf.demand_based_function_LO(random_task, ts + random_task.T - 1) for ts in s.ts_LO(random_task, t)]) is True


def test_ts_HI_len_less_t(random_HI_task, t):
  assert len(s.ts_HI(random_HI_task, t)) < t

def test_ts_HI_min_is_t_D_n_T(random_HI_task, t):
  assert min(s.ts_HI(random_HI_task, t)) == t - random_HI_task.D - s.n(t, random_HI_task.D, random_HI_task.T) * random_HI_task.T 

def test_ts_HI_min_greater_0(random_HI_task, t):
  assert min(s.ts_HI(random_HI_task, t)) >= 0

def test_ts_HI_max_is_t_D(random_HI_task, t):
  assert max(s.ts_HI(random_HI_task, t)) == t - random_HI_task.D

def test_ts_HI_max_less_t(random_HI_task, t):
  assert max(s.ts_HI(random_HI_task, t)) <= t

def test_ts_HI_empty_for_LO_task(random_LO_task, t):
  assert len(s.ts_HI(random_LO_task, t)) == 0

def test_ts_HI_is_correct(random_HI_task, t):
  assert s.ts_HI(random_HI_task, t) == set(ts for ts in range(t + 1) if t - random_HI_task.D >= ts and (t - ts - random_HI_task.D) % random_HI_task.T == 0)

def test_dbf_HI_decreases_for_ts_HI(random_HI_task, t):
  assert all([dbf.demand_based_function_HI(random_HI_task, t, ts) > dbf.demand_based_function_HI(random_HI_task, t, ts + 1) for ts in s.ts_HI(random_HI_task, t)]) is True

def test_dbf_HI_same_since_prev_ts_HI(random_HI_task, t):
  assert all([dbf.demand_based_function_HI(random_HI_task, t, ts) == dbf.demand_based_function_HI(random_HI_task, t, ts - random_HI_task.T + 1) for ts in s.ts_HI(random_HI_task, t)]) is True


def test_ts_CO_len_less_t(random_HI_task, t):
  assert len(s.ts_CO(random_HI_task, t)) < t

def test_ts_CO_min_is_t_D_n_T(random_HI_task, t):
  assert min(s.ts_CO(random_HI_task, t)) == t - random_HI_task.D - s.n(t, random_HI_task.D, random_HI_task.T) * random_HI_task.T + 1

def test_ts_CO_min_greater_0(random_HI_task, t):
  assert min(s.ts_CO(random_HI_task, t)) >= 0

def test_ts_CO_max_is_t_D(random_HI_task, t):
  assert max(s.ts_CO(random_HI_task, t)) == random_HI_task.D + s.n(t, random_HI_task.D, random_HI_task.T) * random_HI_task.T

def test_ts_CO_max_less_t(random_HI_task, t):
  assert max(s.ts_CO(random_HI_task, t)) <= t

def test_ts_CO_empty_for_LO_task(random_LO_task, t):
  assert len(s.ts_CO(random_LO_task, t)) == 0

def test_ts_CO_is_correct(random_HI_task, t):
  assert s.ts_CO(random_HI_task, t) == set(ts for ts in range(t + 1) if t >= random_HI_task.D and dbf.max_requests(random_HI_task.T, dbf.upper(random_HI_task, t, ts), dbf.lower(random_HI_task, ts)) != dbf.max_requests(random_HI_task.T, dbf.upper(random_HI_task, t, ts - 1), dbf.lower(random_HI_task, ts - 1)))

def test_dbf_CO_changes_for_ts_CO(random_HI_task, t):
  assert all([dbf.demand_based_function_CO(random_HI_task, t, ts) != dbf.demand_based_function_CO(random_HI_task, t, ts - 1) for ts in s.ts_CO(random_HI_task, t)]) is True

def test_dbf_CO_same_since_prev_ts_CO(random_HI_task, t):
  ts_values = sorted(s.ts_CO(random_HI_task, t))
  
  assert all([dbf.demand_based_function_CO(random_HI_task, t, ts_values[i]) == dbf.demand_based_function_CO(random_HI_task, t, ts_values[i + 1] - 1) for i in range(len(ts_values) - 1)]) is True




# def test_rule_is_false_t_less_D(random_task):
#   t = random_task.D - 1 if random_task.L == gt.Level.HI else random_task.tight_D - 1
#   ts = r.randint(0, t - 1)

#   assert s.rule(random_task, t, ts) is False

# def test_rule_is_false_upper_less_lower(random_task):
#   t = r.randint(random_task.D + 1, 1000000)

#   while True:
#     ts = r.randint(random_task.D, t - 1)
#     if dbf.upper(random_task, t, ts) < dbf.lower(random_task, ts): break
    
#   assert s.rule(random_task, t, ts) is False


# def test_ts_CO_dbf_CO(random_task): 
#   random_task.L = gt.Level.HI
#   t = 1000
#   result = []
#   answer = []
#   before = -1
#   for i in range(t):
#     if dbf.max_requests(random_task.T, dbf.upper(random_task, t, i), dbf.lower(random_task, i)) != before and dbf.upper(random_task, t, i) >= dbf.lower(random_task, i):
#       answer.append(i)
#     before = dbf.max_requests(random_task.T, dbf.upper(random_task, t, i), dbf.lower(random_task, i))

#   result.extend(ts_CO(t, random_task.T, random_task.D, random_task.tight_D))
  
#   assert result == answer

# # def test_schedulability_test_thm1(task_set):
# #   assert dbf.schedulability_test_thm1(task_set) is True

# # def test_schedulability_test_thm2(task_set):
# #   assert dbf.schedulability_test_thm2(task_set) is True

# # def test_schedulability_test_thm3(task_set):
# #   assert dbf.schedulability_test_thm3(task_set) is True

# def test_LO_task_upper_greater_than_lower(random_task):
#   random_task.L = gt.Level.LO
#   ts = random_task.D - 1
#   t = random_task.D
  
#   assert dbf.upper(random_task, t, ts) >= dbf.lower(random_task, ts)

# def test_ts_LO():
#   assert [i for i in dbf.ts_LO(120, 13, 49)] == [49, 62, 75, 88, 101, 114] 

# def test_ts_LO_dbf_LO(random_task): 
#   t = 1000
#   result = []
#   answer = []
#   before = -1
#   for i in range(t):
#     if dbf.max_requests(random_task.T, i, random_task.tight_D) != before:
#       answer.append(i)
#     before = dbf.max_requests(random_task.T, i, random_task.tight_D)

#   result.extend(dbf.ts_LO(t, random_task.T, random_task.tight_D))

#   assert result == answer[1:]

# def test_ts_HI():
#   assert [i for i in dbf.ts_HI(120, 13, 49)] == [6, 19, 32, 45, 58, 71]

# def test_ts_HI_dbf_HI(random_task): 
#   t = 1000
#   result = []
#   answer = []
#   before = -1
#   for i in range(t, -1, -1):
#     if dbf.max_requests(random_task.T, t - random_task.D, i) != before:
#       answer.append(i)
#     before = dbf.max_requests(random_task.T, t - random_task.D, i)

#   result.extend(dbf.ts_HI(t, random_task.T, random_task.D))

#   assert sorted(result) == sorted(answer[1:])

# def test_ts_CO():
#   t, T, D, C_LO, C_HI, L, tight_D = 120, 13, 14, 1, 5, gt.Level.HI, 14
#   task = gt.Task(-1, T, D, C_LO, C_HI, L, tight_D)
#   answer = []
#   before = -1
#   for i in range(t):
#     if dbf.max_requests(task.T, dbf.upper(task, t, i), dbf.lower(task, i)) != before and dbf.upper(task, t, i) >= dbf.lower(task, i):
#       answer.append(i)
#     before = dbf.max_requests(task.T, dbf.upper(task, t, i), dbf.lower(task, i))

#   result = [i for i in ts_CO(t, T, D, tight_D)]

#   assert result == answer

# def test_ts_CO_dbf_CO(random_task): 
#   random_task.L = gt.Level.HI
#   t = 1000
#   result = []
#   answer = []
#   before = -1
#   for i in range(t):
#     if dbf.max_requests(random_task.T, dbf.upper(random_task, t, i), dbf.lower(random_task, i)) != before and dbf.upper(random_task, t, i) >= dbf.lower(random_task, i):
#       answer.append(i)
#     before = dbf.max_requests(random_task.T, dbf.upper(random_task, t, i), dbf.lower(random_task, i))

#   result.extend(ts_CO(t, random_task.T, random_task.D, random_task.tight_D))
  
#   assert result == answer

# def test_ts_UN():
#   assert [i for i in ts_UN(120, 13, 49, 15)] == [13, 15, 26, 28, 39, 41, 52, 54, 65, 67, 78, 80, 91, 93, 104, 106]

# def test_ts_UN_dbf_UN(random_task): 
#   random_task.L = gt.Level.LO
#   t = 1000
#   result = []
#   answer = []
#   before = -1
#   for i in range(t):
#     if dbf.max_requests(random_task.T, dbf.upper(random_task, t, i), dbf.lower(random_task, i)) != before and dbf.upper(random_task, t, i) >= dbf.lower(random_task, i):
#       answer.append(i)
#     before = dbf.max_requests(random_task.T, dbf.upper(random_task, t, i), dbf.lower(random_task, i))

#   result.extend(ts_UN(t, random_task.T, random_task.D, random_task.tight_D))
  
#   assert result == answer[1:]






# def test_ts_list(task_set):
#   assert dbf.ts_list(500, task_set) == {0, 132, 263, 264, 392, 394, 395, 18, 405, 407, 154, 155, 284, 285, 287, 33, 296, 299, 44, 430, 176, 307, 439, 185, 187, 190, 70, 71, 454, 456, 204, 78, 468, 214, 88, 216, 345, 219, 220, 346, 94, 95, 351, 483, 489, 108, 109, 237, 238, 375, 380, 125}

# # def test_ts_list_random(random_task_set): 
# #   t = 100
# #   result = set()
# #   answer = set()
# #   before = 0
# #   for i in range(1, t):
# #     if dbf.sum_dbf(random_task_set, t, i) > 0 and dbf.sum_dbf(random_task_set, t, i) != before:
# #       answer.add(i)        
      
# #     before = dbf.sum_dbf(random_task_set, t, i)
      

# #   result = dbf.ts_list(t, random_task_set)

# #   assert len(result) == len(answer)

# # def test_ts_HI():
# #   assert [i for i in dbf.ts_HI(120, 13, 49)] == [6, 19, 32, 45, 58, 71]

# # def test_ts_HI_dbf_HI(random_task): 
# #   t = 1000
# #   result = []
# #   answer = []
# #   before = -1
# #   for i in range(t, -1, -1):
# #     if dbf.max_requests(random_task.T, t - random_task.D, i) != before:
# #       answer.append(i)
# #     before = dbf.max_requests(random_task.T, t - random_task.D, i)

# #   result.extend(dbf.ts_HI(t, random_task.T, random_task.D))

# #   assert sorted(result) == sorted(answer[1:])

# # def test_ts_CO():
# #   assert [i for i in dbf.ts_CO(120, 13, 49, 15)] == [7, 20, 33, 46, 59, 72]

# # def test_ts_CO_dbf_CO(random_task): 
# #   random_task.L = gt.Level.HI
# #   t = 1000
# #   result = []
# #   answer = []
# #   before = -1
# #   for i in range(t):
# #     if dbf.max_requests(random_task.T, dbf.upper(random_task, t, i), dbf.lower(random_task, i)) != before and dbf.upper(random_task, t, i) >= dbf.lower(random_task, i):
# #       answer.append(i)
# #     before = dbf.max_requests(random_task.T, dbf.upper(random_task, t, i), dbf.lower(random_task, i))

# #   result.extend(dbf.ts_CO(t, random_task.T, random_task.D, random_task.tight_D))
  
# #   assert result == answer

# # def test_ts_UN():
# #   assert [i for i in dbf.ts_UN(120, 13, 49, 15)] == [13, 15, 26, 28, 39, 41, 52, 54, 65, 67, 78, 80, 91, 93, 104, 106]

# # def test_ts_UN_dbf_UN(random_task): 
# #   random_task.L = gt.Level.LO
# #   t = 1000
# #   result = []
# #   answer = []
# #   before = -1
# #   for i in range(t):
# #     if dbf.max_requests(random_task.T, dbf.upper(random_task, t, i), dbf.lower(random_task, i)) != before and dbf.upper(random_task, t, i) >= dbf.lower(random_task, i):
# #       answer.append(i)
# #     before = dbf.max_requests(random_task.T, dbf.upper(random_task, t, i), dbf.lower(random_task, i))

# #   result.extend(dbf.ts_UN(t, random_task.T, random_task.D, random_task.tight_D))
  
# #   assert result == answer[1:]

