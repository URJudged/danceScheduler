## \file scheduler_test.py
#  \author Judge Lee (jblee@hmc.edu)
#  \date June 4, 2016
#  
#  Tests for the dance scheduler.

from dance_scheduler import *
import random

perfs = [Performer(x) for x in 'abcdefghijklmnopqrstuvwxyz']
print(perfs)
routs = [Routine(x, random.sample(perfs, int(random.triangular(0,26,8))), int(random.uniform(150,300)))
	for x in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
print(perfs)
sched = Scheduler(random.sample(routs, int(random.uniform(0,26))))
# print(perfs)
print(routs)
# print(sched)
# sched.sortRoutines()
# print(perf)
# print(rout)
# print(sched) 