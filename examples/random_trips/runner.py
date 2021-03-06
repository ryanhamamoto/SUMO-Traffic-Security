#!/usr/bin/env python

import os, sys, optparse

# check that sumo load path is set, import python modules from tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


from sumolib import checkBinary  # Checks for the binary in environ vars
import traci


#allow user to run sumo cmd line without visualization tool
def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options


# contains TraCI control loop
def run():
           
    for step in range(simRange):
        
        #increment sim step
        traci.simulationStep() 
        
        #wait until rogue vehicle is deployed
        if step > 20: 
            #make vehicle stop at this intersection
            x, y = traci.junction.getPosition("n2")
            traci.vehicle.rogueNodeException(rogueVehicle, x, y)
            
        if step == 40:
            traci.vehicle.rogueDisableLightRun('1') 
            traci.vehicle.rogueDisableLightRun('2') 
            
        
        if step == 21: 
            traci.vehicle.rogueToggleFollowDistance(rogueVehicle) 
        
        step += 1

    traci.close()
    sys.stdout.flush()


# main entry point
if __name__ == "__main__":
    options = get_options()

    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # traci starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c", "my_config.sumocfg",
                             "--tripinfo-output", "tripinfo.xml"])
    
    #parse command line
    if len(sys.argv) > 1:
        simRange = int(sys.argv[1])
    else:
        simRange = 5000 #default value
           
    if len(sys.argv) > 2:
        rogueVehicle = sys.argv[2]
    else:
        rogueVehicle = 'veh1' #default value
        
    print "running SUMO for", simRange, "steps"
    print "operating on rogue vehicle:", rogueVehicle
    
    run()
