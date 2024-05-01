const functionsModule = require("./functions");


// Define a function to send miners to collect energy
function colletEnergyminers() {
  //Loop through all creeps
  for(var name in Game.creeps) {

    const creep = Game.creeps[name];

    // if creep is a miner
    if (creep.memory.role == 'miner') {
      var source = Game.getObjectById(creep.memory.sourceID);
      if (creep.harvest(source) == ERR_NOT_IN_RANGE) {
          functionsModule.moveToTarget(creep, source);
      }


    }
    
    if(creep.memory.role == 'miner2' || creep.memory.role == 'miner3') {
      // If creep is in target room, mine energy
      if(creep.room.name === creep.memory.targetRoom) {
        let source = creep.pos.findClosestByPath(FIND_SOURCES);
        if(creep.harvest(source) === ERR_NOT_IN_RANGE) {
          functionsModule.moveToTarget(creep, source);
        }
      } 
      else {
        // Creep is not in target room, find exit and move towards it
        let exit = creep.pos.findClosestByPath(creep.room.findExitTo(creep.memory.targetRoom));
        if(exit) {
          functionsModule.moveToTarget(creep, exit);
        }
      }
    }
  }
}

module.exports = {
  colletEnergyminers,
};