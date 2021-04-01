# 配置导入库目录
import traci
import sys
import time
import os
import sumolib

def getEEBLr(speed, reactionTime, deceleration, safetyFactor):
    return speed*reactionTime+safetyFactor*(speed**2)/2/deceleration
    #from sumolib.miscutils import getFreeSocketPort
    #port = sumolib.miscutils.getFreeSocketPort()
    
'''def isPedestrianBeenHit(vehPos, pedPos, vehLength, vehWidth):
    #if 机动车从东向西
    vehUp = vehPos[1] + vehWidth / 2
    vehDown = vehPos[1] - vehWidth / 2
    vehRight = vehPos[0] + 1
    vehLeft = vehPos[0] - vehLength - 1
    return True if pedPos[0]>vehLeft and pedPos[0]<vehRight and pedPos[1]>vehDown and pedPos[1]<vehUp else False'''


if __name__ == '__main__':
    # 配置调用目录
    try:
        SUMO_HOME = os.environ.get('SUMO_HOME')
    except:
        print('Configure the SUMO environment')
    else:
        sys.path.append(SUMO_HOME+'/tools/')
        sumoBinary = SUMO_HOME+"/bin/sumo-gui"
        sumoCmd = [sumoBinary, "-c", r'map.sumocfg']
        # 导入traci模块
        #traci.start(sumoCmd)
        # connect server
        #traci.init(4001)
        #traci.setOrder(0xAABB)
        #connection1 = traci.start(sumoCmd, port=4001)

        #traci.setOrder(1)
        #connection2 = traci.connect(port=4001, numRetries=10, host="localhost")

        #connection2.setOrder(2)

        # 导入traci模块
        traci.start(sumoCmd)
        collisionVehList = set()
        
        vehInfo = {
                    '3': {'id': '3', 'speed': 6},
                    '1': {'id': '1', 'speed': 10},
                    #'4': {'id': '4', 'speed': 10}
                    }
        # collisionTag = False
        step = 0
        while traci.simulation.getMinExpectedNumber() > 0:
            print('>>> step:', step)
            try:
                for veh in vehInfo.values():
                    traci.vehicle.setSpeedMode(veh['id'], 0)                # Disable speed model
                    traci.vehicle.setLaneChangeMode(veh['id'], 0)           # Disable lane change
                    traci.vehicle.setSpeed(veh['id'], veh['speed'])         # Set fixed speed
                    traci.vehicle.moveToXY(vehID="1", lane=1)               # change lane
                    #traci.vehicle.moveToXY(vehID="0", lane=1)
                traci.person.setSpeed('ped0', 2)
                #traci.person.moveToXY('ped0', x=586.89, y=788.29)

            except:
                pass
            traci.simulationStep()
            # collisionTag = True if traci.simulation.getCollidingVehiclesNumber() > 0 else False
            if traci.simulation.getCollidingVehiclesNumber() > 0:
                collisionVeh = set(traci.simulation.getCollidingVehiclesIDList())
                collisionVehList.update(collisionVeh)
                for keys in vehInfo:
                    if keys in collisionVeh:
                        vehInfo[keys]['speed'] = 0
                        traci.vehicle.setColor(keys, (255, 0, 0))
                time.sleep(0.1)
            print('Accident vehicle:', collisionVehList)
            
'''            if step > 100:
                if isPedestrianBeenHit(traci.vehicle.getPosition('0'), traci.person.getPosition('ped0'), traci.vehicle.getLength('0'), traci.vehicle.getWidth('0')):
                    collisionTag = True
                    collisionVeh = set(['0'])
                    print('事故车辆：', collisionVeh)
                    for keys in vehInfo:
                        if keys in collisionVeh:
                            vehInfo[keys]['speed'] = 0
                            traci.vehicle.setColor(keys, (255, 0, 0))
                            time.sleep(10)
                            traci.close()

            step += 1'''