# 配置导入库目录
import traci
import sys
import time
import os

def getEEBLr(speed, reactionTime, deceleration, safetyFactor):
    return speed*reactionTime+safetyFactor*(speed**2)/2/deceleration


if __name__ == '__main__':
    # 配置调用目录
    try:
        SUMO_HOME = os.environ.get('SUMO_HOME')
    except:
        print('Configure the SUMO environment')
    else:
        sys.path.append(SUMO_HOME+'/tools/')
        sumoBinary = SUMO_HOME+"/bin/sumo-gui"

        #```sumo-gui -c map.sumocfg --start --remote-port 4001 --step-length 0.02```

        #sumoCmd = [sumoBinary, "-c", r'map.sumocfg', "--remote-port", "4001"]

        # 导入traci模块
        #traci.start(sumoCmd)
        # connect server
        traci.init(4001)
        traci.setOrder(0xAABB)



        collisionVehList = set()
        vehInfo = {
                    '0': {'id': '0', 'speed': 5},
                    '1': {'id': '1', 'speed': 25}
                    }
        # collisionTag = False
        step = 0
        while traci.simulation.getMinExpectedNumber() > 0:
            print('>>> step:', step)
            traci.simulationStep()
            step += 1
    