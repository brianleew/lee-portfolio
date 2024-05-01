const functionsModule = require("./functions");



function energyToBuild() {

  for (const name in Game.creeps) {
    const creep = Game.creeps[name];

    if (creep.memory.role === 'builder' ) {
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

        else {
          //get energy dropped on ground
          var droppedEnergy = creep.pos.findClosestByPath(FIND_DROPPED_RESOURCES);
          if (droppedEnergy) {
            //pickup energy
            if(creep.pickup(droppedEnergy) == ERR_NOT_IN_RANGE) {
              functionsModule.moveToTarget(creep, droppedEnergy);
            }

          }
        }
      } 
      else {
        //Locking mechanism
        // var collecting = false;
        creep.memory.collecting = false;

        // create a const for construction sites that focuses on extensions and then everything else
        const target = creep.pos.findClosestByPath(FIND_CONSTRUCTION_SITES);
        if (creep.store.getUsedCapacity(RESOURCE_ENERGY) === 0) {
          creep.memory.collecting = true;
        }
        if (target) {
          if (creep.build(target) === ERR_NOT_IN_RANGE) {
            functionsModule.moveToTarget(creep, target);
            creep.build(target);
          }
        }
        
        else {
          //build controller
          if (creep.upgradeController(creep.room.controller) === ERR_NOT_IN_RANGE) {
            functionsModule.moveToTarget(creep, creep.room.controller);
            creep.upgradeController(creep.room.controller);
          }
        }
      }
    }
  }
}

module.exports = {
    energyToBuild
};