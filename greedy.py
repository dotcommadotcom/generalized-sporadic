import dbfs
from generate_tasks import task
def greedy(task_set):
    '''
    Inputs:   
    task_set:       type: a list of task object. Indicates the input task set.
    '''
    if dbfs.schedulability_test_thm2(task_set) == False:
        print("Not schedulable under low-criticality mode.")
        return False
    if dbfs.schedulability_test_thm1(task_set) == True:
        print("Already schedualble")
        return True
    t_max = dbfs.calculate_t_max(task_set)
    changed = False
    marked = [False] * len(task_set)
    while not changed:
        # run schedulability tests from 0 to l for low and hi respectively
        for j in range(0, t_max):
            for i in range(j+1, t_max+1):
                if dbfs.calculate_dbf(i, j, task_set) > i:
                    # find the task that maximizes the dbf increase
                    max_diff = 0
                    target = -1
                    for k in range(len(task_set)):
                        if marked[k]:
                            continue
                        diff = dbfs.calculate_dbf(i, j, task_set) - dbfs.calculate_dbf(i-1, j, task_set)
                        if diff > max_diff:
                            max_diff = diff
                            target = k
                    print("Found target:{}".format(target))
                    if target == -1:
                        return False
                    task_set[target].tight_D -= 1
                    if task_set[target].tight_D == task_set[target].WCET_LO:
                        marked[target] = True;
                    changed = True
    return True

