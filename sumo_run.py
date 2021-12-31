import traci
import time
import traci.constants as tc
import pytz
import datetime
from random import randrange
import pandas as pd


def getdatetime():
        utc_now = pytz.utc.localize(datetime.datetime.utcnow())
        currentDT = utc_now.astimezone(pytz.timezone("Europe/Paris"))
        DATIME = currentDT.strftime("%Y-%m-%d %H:%M:%S")
        return DATIME




#traci.init(8873)
# launch sumo with the senario
sumoCmd = ["sumo-gui", "-c", "environement/Config_highway.sumocfg"]
print('Run ' + ' '.join(sumoCmd))
traci.start(sumoCmd)

packVehicleData = []


while traci.simulation.getMinExpectedNumber() > 0:
       
        traci.simulationStep();

        vehicles=traci.vehicle.getIDList(); # get list of vehicles from the simulation
        print(vehicles)
# for each vehicle we'll get the cooredinates, speed , lane ....
        for i in range(0,len(vehicles)):

                
                vehid = vehicles[i]
                x, y = traci.vehicle.getPosition(vehicles[i])
                coord = [x, y]
                lon, lat = traci.simulation.convertGeo(x, y)
                gpscoord = [lon, lat]
                spd = round(traci.vehicle.getSpeed(vehicles[i])*3.6,2)
                edge = traci.vehicle.getRoadID(vehicles[i])
                lane = traci.vehicle.getLaneID(vehicles[i])
                displacement = round(traci.vehicle.getDistance(vehicles[i]),2)
                turnAngle = round(traci.vehicle.getAngle(vehicles[i]),2)

                #Packing of all the data for export to CSV/XLSX
                vehList = [getdatetime(), vehid, coord, gpscoord, spd, edge, lane, displacement, turnAngle]
                
                
                print("Vehicle: ", vehicles[i], " at datetime: ", getdatetime())
                print(vehicles[i], " >>> Position: ", coord, " | GPS Position: ", gpscoord, " |", \
                                       " Speed: ", round(traci.vehicle.getSpeed(vehicles[i])*3.6,2), "km/h |", \
                                      #Returns the id of the edge the named vehicle was at within the last step.
                                       " EdgeID of veh: ", traci.vehicle.getRoadID(vehicles[i]), " |", \
                                      #Returns the id of the lane the named vehicle was at within the last step.
                                       " LaneID of veh: ", traci.vehicle.getLaneID(vehicles[i]), " |", \
                                      #Returns the distance to the starting point like an odometer.
                                       " Distance: ", round(traci.vehicle.getDistance(vehicles[i]),2), "m |", \
                                      #Returns the angle in degrees of the named vehicle within the last step.
                                       " Vehicle orientation: ", round(traci.vehicle.getAngle(vehicles[i]),2), "deg |", \
                                      
                       )

                idd = traci.vehicle.getLaneID(vehicles[i]) # get lane id of the vehicle

                
        
                
                


                ##----------MACHINE LEARNING CODES/FUNCTIONS HERE----------##


                ##---------------------------------------------------------------##


                ##----------CONTROL Vehicles----------##

                #***SET FUNCTION FOR VEHICLES***
                #REF: https://sumo.dlr.de/docs/TraCI/Change_Vehicle_State.html
                NEWSPEED = 15 # value in m/s (15 m/s = 54 km/hr)
                if vehicles[i]=='veh2':
                        traci.vehicle.setSpeedMode('veh2',0)
                        traci.vehicle.setSpeed('veh2',NEWSPEED)
                        


                ##------------------------------------------------------##


traci.close()

#Generate Excel file
#columnnames = ['dateandtime', 'vehid', 'coord', 'gpscoord', 'spd', 'edge', 'lane', 'displacement', 'turnAngle']
#dataset = pd.DataFrame(vehList, index=None, columns=columnnames)
#dataset.to_excel("C:\\Users\\Bolbol\\Desktop\\Projet RL\\environement\\output.xlsx", index=False)
#time.sleep(5)


