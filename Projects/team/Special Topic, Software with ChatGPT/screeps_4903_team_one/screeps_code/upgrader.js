const functionsModule = require("./functions");



function upgraderDo() {

    for (const name in Game.creeps) {
        const creep = Game.creeps[name];
  
        if (creep.memory.role === 'upgrader') {
            if (creep.store.getFreeCapacity() > 0 && creep.memory.collecting === true) {
                //get energy from container
                var container = creep.pos.findClosestByPath(FIND_STRUCTURES, {
                    filter: (structure) => {
                        return structure.structureType == STRUCTURE_CONTAINER &&
                            structure.store.getUsedCapacity(RESOURCE_ENERGY) > 0;
                    }
                });
                if (container) {
                    // Try to withdraw energy, if the container is not in range, move towards it
                    if(creep.withdraw(container, RESOURCE_ENERGY) == ERR_NOT_IN_RANGE) {
                        functionsModule.moveToTarget(creep, container);
                    }
                }
                
            }
            else {
                //Locking mechanism
                creep.memory.collecting = false;

                if (creep.store.getUsedCapacity(RESOURCE_ENERGY) === 0) {
                    // collecting = true;
                    creep.memory.collecting = true;
                }

                else {
                    //build controller
                    if (creep.upgradeController(creep.room.controller) === ERR_NOT_IN_RANGE) {
                        creep.upgradeController(creep.room.controller);
                        functionsModule.moveToTarget(creep, creep.room.controller);

                    }

                }
            }
        }
    }


    for (const name in Game.creeps) {
        const creep = Game.creeps[name];
  
        if (creep.memory.role === 'upgrader2') {
            if (creep.store.getFreeCapacity() > 0 && creep.memory.collecting === true) {
                //get energy container

                var container = creep.pos.findClosestByPath(FIND_STRUCTURES, {
                    filter: (structure) => {
                        return structure.structureType == STRUCTURE_CONTAINER &&
                            structure.store.getUsedCapacity(RESOURCE_ENERGY) > 0;
                    }
                });
                if (container) {
                    // Try to withdraw energy, if the container is not in range, move towards it
                    if(creep.withdraw(container, RESOURCE_ENERGY) == ERR_NOT_IN_RANGE) {
                        functionsModule.moveToTarget(creep, container);
                    }
                }
            }
            else {
                //Locking mechanism
                creep.memory.collecting = false;

                if (creep.store.getUsedCapacity(RESOURCE_ENERGY) === 0) {
                    // collecting = true;
                    creep.memory.collecting = true;
                }

                else {
                    //build controller
                    if (creep.upgradeController(creep.room.controller) === ERR_NOT_IN_RANGE) {
                        creep.upgradeController(creep.room.controller);
                        functionsModule.moveToTarget(creep, creep.room.controller);

                    }
                }
            }
        }
    }
}

module.exports = {
    upgraderDo
};