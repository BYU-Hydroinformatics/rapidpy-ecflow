#!/usr/bin/python3.6m
import os
from ecflow import Defs, Family, Task


print("Creating suite definition")
home = os.path.join(os.getenv("HOME"), "host_share", "rapid_run", "ecflow_era")

defs = Defs()
suite = defs.add_suite('run_rapid_era')
suite.add_variable("ECF_INCLUDE", home)
suite.add_variable("ECF_FILES", os.path.join(home, 'run_rapid_era'))
suite.add_variable("ECF_HOME", home)

prep_task = suite.add_task('era_task')
prep_task.add_variable("PYSCRIPT", os.path.join(home, 'run_lsm.py'))
prep_task.add_variable("RAPID_EXEC", '/home/michael/rapid/run/rapid')
prep_task.add_variable("IO_LOCATION", "/home/michael/host_share/rapid-io_init")
prep_task.add_variable("ERA_LOCATION", "/home/michael/host_share/era_data")

print(defs)

print("check trigger expressions")
check = defs.check()
assert len(check) == 0, check

print("Checking job creation: .ecf -> .job0")
print(defs.check_job_creation())

print("Saving definition to file 'run_rapid_era.def'")
defs.save_as_defs("run_rapid_era.def")
