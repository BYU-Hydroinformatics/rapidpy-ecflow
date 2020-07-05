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
    ensemble_family = Family("ensemble_family").add_trigger("prep_task == complete")
    ensemble_family.add_variable("PYSCRIPT", os.path.join(home, 'run_ecflow.py'))
    ensemble_family.add_variable("RAPID_EXEC", '/home/michael/rapid/run/rapid')
    ensemble_family.add_variable("EXEC_DIR", '/home/michael/execute')
    ensemble_family.add_variable("SUBPROCESS_DIR", '/home/michael/subprocess_logs')
    ensemble_family += [Task(f"ens_member_52").add_variable("JOB_INDEX", 0)]
    ensemble_family += [
        Task(f"ens_member_{j}")
        .add_variable("JOB_INDEX", 52 - j) for j in reversed(range(1, 52))
        # .add_trigger(f"ens_member_{j + 1} == complete") for j in reversed(range(1, 52))
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
prep_task.add_variable("IO_LOCATION", "/home/michael/host_share/japan-io")
prep_task.add_variable("RUNOFF_LOCATION", "/home/michael/host_share/ecmwf")

suite += create_ensemble_family()

plain_table_task = suite.add_task('plain_table_task')
plain_table_task.add_trigger("ensemble_family == complete")
plain_table_task.add_variable("PYSCRIPT", os.path.join(home, 'spt_extract_plain_table.py'))
plain_table_task.add_variable("OUT_LOCATION", "/home/michael/host_share/japan-io/output")
plain_table_task.add_variable("LOG_FILE", os.path.join(home, 'run_rapid/ecf_out/plain_table.log'))
plain_table_task.add_variable("NCES_EXEC", "/home/michael/miniconda3/envs/ecflow/bin/nces")

store_day_one = suite.add_task('store_day_one')
store_day_one.add_trigger("ensemble_family == complete")
store_day_one.add_variable("PYSCRIPT", os.path.join(home, 'day_one_forecast.py'))
store_day_one.add_variable("IO_LOCATION", "/home/michael/host_share/japan-io")
store_day_one.add_variable("ERA_LOCATION", "/home/michael/host_share/era5_data/era5_runoff_2001to2015")
store_day_one.add_variable("FORECAST_RECORDS_DIR", "/home/michael/host_share/japan-io")
store_day_one.add_variable("LOG_DIR", os.path.join(home, 'run_rapid/ecf_out'))

print(defs)

print("check trigger expressions")
check = defs.check()
assert len(check) == 0, check

print("Checking job creation: .ecf -> .job0")
print(defs.check_job_creation())

print("Saving definition to file 'run_rapid.def'")
defs.save_as_defs("run_rapid.def")
