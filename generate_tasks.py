import random 
import math
from enum import Enum 

class Level(Enum):
    HI = 1
    LO = 2

class task:
    def __init__(self, ID, T, WCET_LO, WCET_HI, D, L, tight_D = -1):
        """
        Args:
                ID:         type: string. The id of the task.
                T:          type: int. The minimum separation time of the task.
                WCET_LO:    type: int. The WCET in low-criticality mode.
                D:          type: int. The deadline of the task.
                L:          type: Level. The criticality level of the task.
                tight_D:    type: int. The tightened deadline of the task. If not assigned, the same as D.
        """
        self.ID = ID
        self.T = T
        self.WCET_LO = WCET_LO
        self.WCET_HI = WCET_HI
        self.D = D
        self.L = L
        if tight_D == -1:
          tight_D = D
        self.tight_D = tight_D

class task_generation:
    def gen_kato_utilizations(self, target_val, min_val, max_val):
        '''
            This function is modified from the function gen_kato_utilizations in class simso.generator.task_generator.
            Inputs: 
                target_val:         type: float. The target sum of the utilization ratio.
                min_val:            type: float. The minimum utilization ratio.
                max_val:            type: float. The maximum utilization ratio.
            Outputs:
                A set of utilization ratios whose sum is the target_val.
        '''
        vals = []
        total_val = 0
        # Classic UUniFast algorithm:
        while total_val < target_val:
            val = random.uniform(min_val, max_val)
            if val + total_val> target_val:
                val = target_val - total_val
            total_val += val
            vals.append(val)
        return vals

    def gen_task(self, utilization, ID):
        '''
            Generates the task based on the utilization ratio
            How do we define the utilization ratio? --> WCET_LO / T based on Easwaran 2013
            Inputs:
                utilization:        type: float. The utilization ratio of the task.
            Output:    
                A task with all parameters initialized.
        '''
        WCET_LO = self.generate_WCET_LO()
        T = math.ceil(WCET_LO/utilization)

        # the operations below randomly generate T and then calculates WCET_LO
        # this may cause the WCET_LO to be 0
        #T = self.generate_T()
        #WCET_LO = math.floor(T * utilization)

        l = self.generate_L()
        if l == Level.LO:
            WCET_HI = WCET_LO
        else:
            WCET_HI = self.generate_WCET_HI(WCET_LO)
        D = self.generate_D(WCET_HI)
        return task(ID, T, WCET_LO, WCET_HI, D, l)

    def generate_WCET_LO(self):
        return random.randrange(5, 30)


    def generate_T(self):
      return random.randrange(5,101)

    def generate_WCET_HI(self, WCET_LO):
      return WCET_LO * random.randrange(2, 5)

    def generate_D(self, WCET_HI):
      #return random.randrange(WCET_HI, 101)
      # enlarge the random range to fit in large WCET_HI values
      return random.randrange(WCET_HI, 301)

    def generate_L(self):
      return random.choice([Level.HI, Level.LO])

    def create_task_set(self, utilization_sum, min_u, max_u):
        utilization_ratios = self.gen_kato_utilizations(utilization_sum, min_u, max_u)
        tasks = []
        counter = 0
        for u in utilization_ratios:
            t = self.gen_task(u, str(counter))
            while t.WCET_LO == 0:
                t = self.gen_task(u, str(counter))
            tasks.append(t)
            counter += 1
        return tasks

