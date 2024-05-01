const functionsModule = require("./functions");


function energyToReBuild() {

    for (const name in Game.creeps) {
      const creep = Game.creeps[name];
        if (creep.memory.role === 'towerManager') {
            if (creep.store.getFreeCapacity() > 0 && creep.memory.collecting === true) {
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
                creep.memory.collecting = false;
                
                // Define target as the closest tower that needs energy
                var target = creep.pos.findClosestByPath(FIND_STRUCTURES, {
                    filter: (s) => s.structureType === STRUCTURE_TOWER && s.store.getFreeCapacity(RESOURCE_ENERGY) > 0
                });
        
                if (creep.store.getUsedCapacity(RESOURCE_ENERGY) === 0) {
                    creep.memory.collecting = true;
                }
                
                if (target) {
                    // Try to transfer energy to it, if it is not in range then move towards it
                    if(creep.transfer(target, RESOURCE_ENERGY) == ERR_NOT_IN_RANGE) {
                        functionsModule.moveToTarget(creep, target);
                    }
                }
            }
        }
    
    }
}

module.exports = {
    energyToReBuild
};