import torch as tr

@tr.jit.script
def max_requests(T, upper, lower):
  return tr.max(tr.floor_divide(upper - lower, T) + 1, tr.tensor(0))

@tr.jit.script
def lower(T, tight_D, ts):
  return T * max_requests(T, ts, tight_D) 

@tr.jit.script
def upper_CO(T, D, t, ts):
  return t - D - T * max_requests(T, t - ts, D)

@tr.jit.script
def upper_UN(tight_D, t, ts):
  return tr.min(ts, t - tight_D)

@tr.jit.script
def demand_based_function(C, T, upper, lower):
  return  C * max_requests(T, upper, lower)

@tr.jit.script
def demand_based_function_LO(C_LO, T, tight_D, ts):
  return demand_based_function(C_LO, T, upper = ts, lower = tight_D)

@tr.jit.script
def demand_based_function_HI(C_HI, T, D, t, ts):
  return demand_based_function(C_HI, T, upper = t - D, lower = ts)

@tr.jit.script
def demand_based_function_CO(C_HI, T, D, tight_D, t, ts):
  return demand_based_function(C_HI, T, upper_CO(T, D, t, ts), lower(T, tight_D, ts))

@tr.jit.script
def demand_based_function_UN(C_LO, T, tight_D, t, ts):
  k = max_requests(T, upper_UN(tight_D, t, ts), lower(T, tight_D, ts))

  return tr.trunc(tr.min(C_LO, ts - lower(T, tight_D, ts) - (k - 1) * T / 2) * k).int()

@tr.jit.script
def sum_dbf_LO(task_set_tensor, ts):
  T, C_LO, tight_D = task_set_tensor[:, 1], task_set_tensor[:, 2], task_set_tensor[:, 5]

  return tr.sum(tr.stack([demand_based_function_LO(C_LO[i], T[i], tight_D[i], ts) for i in tr.arange(len(T))]), dim=0)
  
@tr.jit.script
def sum_dbf_HI(task_set_tensor, t, ts):
  T, C_HI, D = task_set_tensor[:, 1], task_set_tensor[:, 3], task_set_tensor[:, 4]

  return tr.sum(tr.stack([demand_based_function_HI(C_HI[i], T[i], D[i], t, ts) for i in tr.arange(len(T))]), dim=0)

@tr.jit.script
def sum_dbf_CO(task_set_tensor, t, ts):
  T, C_HI, D, tight_D = task_set_tensor[:, 1], task_set_tensor[:, 3], task_set_tensor[:, 4], task_set_tensor[:, 5]

  return tr.sum(tr.stack([demand_based_function_CO(C_HI[i], T[i], D[i], tight_D[i], t, ts) for i in tr.arange(len(T))]), dim=0)

@tr.jit.script
def sum_dbf_UN(task_set_tensor, t, ts):
  T, C_HI, tight_D = task_set_tensor[:, 1], task_set_tensor[:, 3], task_set_tensor[:, 5]

  return tr.sum(tr.stack([demand_based_function_UN(C_HI[i], T[i], tight_D[i], t, ts) for i in tr.arange(len(T))]), dim=0)

@tr.jit.script
def sum_dbf(task_set_lo, task_set_hi, t, ts):
  return sum_dbf_LO(task_set_lo, ts) + sum_dbf_LO(task_set_hi, ts) + sum_dbf_HI(task_set_hi, t, ts) + sum_dbf_CO(task_set_hi, t, ts) + sum_dbf_UN(task_set_lo, t, ts)