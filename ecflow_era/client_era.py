#!/usr/bin/python3.6m
import ecflow

try:
    ci = ecflow.Client("localhost:2500")
    ci.ping() 

except RuntimeError as e:
    print("ping failed: ", str(e))

try:
    print("Loading definition in 'run_rapid_era.def' into the server")
    ci = ecflow.Client("localhost:2500")

    ci.sync_local()   # get the defs from the server, and place on ci
    defs = ci.get_defs() # retrieve the defs from ci
    if defs is None:
        print("No definition in server, loading defs from disk")
        ci.load("run_rapid_era.def")

    else:
        print("read definition from disk and load into the server")
        ci.replace("/run_rapid_era", "run_rapid_era.def")

    print("Restarting the server. This starts job scheduling")
    ci.restart_server()

    print("Begin the suite named 'run_rapid_era'")
    ci.begin_suite("run_rapid_era")

except RuntimeError as e:
    print("Failed:",   e)
