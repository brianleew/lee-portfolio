const functionsModule = require("./functions");


function energyToHome() {
  for (const name in Game.creeps) {
    const creep = Game.creeps[name];

    if (creep.memory.role === 'carry') {
      if (creep.store.getFreeCapacity() > 0 && creep.memory.collecting === true) {
    
        const minerCreep = Game.creeps[creep.memory.minerName];
      
        if (minerCreep) {
          let droppedEnergyPiles = minerCreep.pos.findInRange(FIND_DROPPED_RESOURCES, 3);
    
          if (droppedEnergyPiles.length > 0) {
            let largestEnergyPile = droppedEnergyPiles.reduce((largestPile, currentPile) => {
                return (currentPile.amount > largestPile.amount) ? currentPile : largestPile;
            }, {amount: 0});  // Start with a dummy pile with 0 energy
    
            if (largestEnergyPile.id) {
              if (creep.pickup(largestEnergyPile) === ERR_NOT_IN_RANGE) {
                functionsModule.moveToTarget(creep, largestEnergyPile);
              }
            }
          }
        }
        else {
          console.log(`Carry ${creep.name} could not find associated miner ${creep.memory.minerName}`);
        }
    
      }
      else {
        creep.memory.collecting = false;
        if (creep.store.getUsedCapacity(RESOURCE_ENERGY) === 0) {
          creep.memory.collecting = true;
          creep.memory.excludedContainers = [];
        }
    
        const spawn = Game.spawns['Spawn1'];
    
        if (spawn.store.getFreeCapacity(RESOURCE_ENERGY) > 0) {
          if (creep.transfer(spawn, RESOURCE_ENERGY) === ERR_NOT_IN_RANGE) {
            functionsModule.moveToTarget(creep, spawn);
          }
        }
        
        //else if expansion site exists, transfer energy to expansion site
        // if spawn is full, transfer energy to extension
        if (spawn.store.getFreeCapacity(RESOURCE_ENERGY) === 0) {
          var target = creep.pos.findClosestByPath(FIND_MY_STRUCTURES, { filter: (structure) => {
                return (structure.structureType == STRUCTURE_EXTENSION) &&
                    structure.store.getFreeCapacity(RESOURCE_ENERGY) > 0;
            }
          });
          if(target) {
            // If the creep is not in range to the extension, move towards it
            if(creep.transfer(target, RESOURCE_ENERGY) == ERR_NOT_IN_RANGE) {
              functionsModule.moveToTarget(creep, target);
            }
          }
    
          //else transfer energy to container if exists
          else {
            let container;
            let excludedContainers = creep.memory.excludedContainers || [];
          
            // Find closest container that is not full and not in the excluded list
            container = creep.pos.findClosestByPath(FIND_STRUCTURES, { 
              filter: (s) => s.structureType === STRUCTURE_CONTAINER && !excludedContainers.includes(s.id)
            });
          
            // If that container is full, add it to the excluded list and find the next closest one
            if (container && container.store.getFreeCapacity(RESOURCE_ENERGY) === 0) {
              excludedContainers.push(container.id);
              creep.memory.excludedContainers = excludedContainers;
          
              container = creep.pos.findClosestByPath(FIND_STRUCTURES, { 
                filter: (s) => s.structureType === STRUCTURE_CONTAINER && !excludedContainers.includes(s.id)
              });
            }
          
            if (container) {
              if (creep.transfer(container, RESOURCE_ENERGY) === ERR_NOT_IN_RANGE) {
                functionsModule.moveToTarget(creep, container);
              }
            } else {
              //put it in storage
              let storage = creep.room.storage;
              if (storage) {
                if (creep.transfer(storage, RESOURCE_ENERGY) === ERR_NOT_IN_RANGE) {
                  functionsModule.moveToTarget(creep, storage);
                }
              }
              else {
                creep.memory.excludedContainers = [];  // Reset the excludedContainers list when no container is found
              }
            }
          }
        }
      }
    }
    
    //
    // Iterate over all creeps
    for(let name in Game.creeps) {
      let creep = Game.creeps[name];
      // If this creep is a 'carryOther' and has a target room
      if((creep.memory.role === 'carryOther' && creep.memory.targetRoom) || (creep.memory.role === 'carryOther2' && creep.memory.targetRoom) || (creep.memory.role === 'carryOther3' && creep.memory.targetRoom)) {
        // If creep is in target room and not full, pick up energy
        if(creep.room.name === creep.memory.targetRoom && creep.store.getFreeCapacity() > 0) {

          let droppedEnergy = creep.pos.findClosestByPath(FIND_DROPPED_RESOURCES, {
              filter: (r) => r.resourceType === RESOURCE_ENERGY
          });

          if(droppedEnergy) {
            let pickupResult = creep.pickup(droppedEnergy);
            if(pickupResult === ERR_NOT_IN_RANGE) {
              
              // console.log('Creep position:', creep.pos);
              // console.log('Dropped energy position:', droppedEnergy.pos);
              let moveToResult = creep.moveTo(droppedEnergy);
              // console.log('Result of creep.moveTo:', moveToResult);
              // console.log(creep.name, 'moving to dropped energy');
              creep.memory.excludedContainers = [];

            }
          }
        }
        // If creep is in homeRoom and not empty, transfer energy to container
        else if(creep.room.name === creep.memory.homeRoom && creep.store.getUsedCapacity() > 0) {

          const spawn = Game.spawns['Spawn1'];
          //if spawn is not full, transfer energy to spawn
          if (spawn.store.getFreeCapacity(RESOURCE_ENERGY) > 0) {
            if (creep.transfer(spawn, RESOURCE_ENERGY) === ERR_NOT_IN_RANGE) {
              functionsModule.moveToTarget(creep, spawn);
            }
          }
          //else if expansion site exists, transfer energy to expansion site
          else {
            var target = creep.pos.findClosestByPath(FIND_MY_STRUCTURES, { filter: (structure) => {
                  return (structure.structureType == STRUCTURE_EXTENSION) &&
                      structure.store.getFreeCapacity(RESOURCE_ENERGY) > 0;
              }
            });
            if(target) {
              // If the creep is not in range to the extension, move towards it
              if(creep.transfer(target, RESOURCE_ENERGY) == ERR_NOT_IN_RANGE) {
                functionsModule.moveToTarget(creep, target);
              }
            }
            else {
              let container;
              let excludedContainers = creep.memory.excludedContainers || [];
            
              // Find closest container that is not full and not in the excluded list
              container = creep.pos.findClosestByPath(FIND_STRUCTURES, { 
                filter: (s) => s.structureType === STRUCTURE_CONTAINER && !excludedContainers.includes(s.id)
              });
            
              // If that container is full, add it to the excluded list and find the next closest one
              if (container && container.store.getFreeCapacity(RESOURCE_ENERGY) === 0) {
                excludedContainers.push(container.id);
                creep.memory.excludedContainers = excludedContainers;
            
                container = creep.pos.findClosestByPath(FIND_STRUCTURES, { 
                  filter: (s) => s.structureType === STRUCTURE_CONTAINER && !excludedContainers.includes(s.id)
                });
              }
            
              if (container) {
                if (creep.transfer(container, RESOURCE_ENERGY) === ERR_NOT_IN_RANGE) {
                  functionsModule.moveToTarget(creep, container);
                }
              } else {
                //put it in storage
                let storage = creep.room.storage;
                if (storage) {
                  if (creep.transfer(storage, RESOURCE_ENERGY) === ERR_NOT_IN_RANGE) {
                    functionsModule.moveToTarget(creep, storage);
                  }
                }
                else {
                  creep.memory.excludedContainers = [];  // Reset the excludedContainers list when no container is found
                }
              }
            }
          }
        }
        else {
          // Creep is not in target room or home room, or is in target room but full, find exit and move towards it
          let exitRoom = creep.store.getUsedCapacity() > 0 ? creep.memory.homeRoom : creep.memory.targetRoom;
          let exit = creep.pos.findClosestByRange(creep.room.findExitTo(exitRoom));
          if(exit) {
            functionsModule.moveToTarget(creep, exit);
          }
        }
      }
    }

  }
}


module.exports = {
    energyToHome
};