#!/usr/bin/python3.6m
import os
from ecflow import Defs, Family, Task


for i in reversed(range(1, 53)):
    src = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'run_rapid', 'ens_member.ecf')
    dest = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'run_rapid', 'ensemble_family',
                        f'ens_member_{i}.ecf')
    if not os.path.exists(dest): 
        os.symlink(src, dest)


def create_ensemble_family():
    ensemble_family = Family("ensemble_family" ).add_trigger("prep_task == complete")
    ensemble_family.add_variable("PYSCRIPT", os.path.join(home, 'run_ecflow.py'))
    ensemble_family += [Task(f"ens_member_52").add_variable("JOB_INDEX", 0)]
    ensemble_family += [
        Task(f"ens_member_{j}")
        .add_variable("JOB_INDEX", 52 - j)
        .add_trigger(f"ens_member_{j + 1} == complete") for j in reversed(range(1, 52))
    ]
    return ensemble_family


print("Creating suite definition")
home = os.path.join(os.getenv("HOME"), "host_share", "rapid_run", "ecflow")

defs = Defs()
suite = defs.add_suite('run_rapid')
suite.add_variable("ECF_INCLUDE", home)
suite.add_variable("ECF_FILES", os.path.join(home, 'run_rapid'))
suite.add_variable("ECF_HOME", home)

prep_task = suite.add_task('prep_task')
prep_task.add_variable("PYSCRIPT", os.path.join(home, 'iprep_ecf.py'))
prep_task.add_variable("IO_LOCATION", "/home/michael/host_share/rapid-io_init")
prep_task.add_variable("RUNOFF_LOCATION", "/home/michael/host_share/ecmwf")

suite += create_ensemble_family()
            
print(defs)

print("check trigger expressions")
check = defs.check()
assert len(check) == 0, check

print("Checking job creation: .ecf -> .job0")
print(defs.check_job_creation())

print("Saving definition to file 'run_rapid.def'")
defs.save_as_defs("run_rapid.def")
