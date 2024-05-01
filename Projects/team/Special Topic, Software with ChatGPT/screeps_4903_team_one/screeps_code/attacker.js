
//make attacked creep move to flag named Attack!
const functionsModule = require("./functions");

function attackerFunction() {
    
    for(let name in Game.creeps) {
        let creep = Game.creeps[name];

        // Attacker creep behavior
        if (creep.memory.role === 'attacker') {
            // If there is a target room set in the creep's memory, go there and attack
            if (creep.memory.targetRoom) {
                if (creep.room.name !== creep.memory.targetRoom) {
                    // Not in the target room, move towards it
                    const exitDir = Game.map.findExit(creep.room, creep.memory.targetRoom);
                    const exit = creep.pos.findClosestByPath(exitDir);
                    creep.moveTo(exit);
                } else {
                    // In the target room, find targets and attack
                    let targets = creep.room.find(FIND_HOSTILE_STRUCTURES, {
                        filter: (structure) => {
                            return structure.structureType === STRUCTURE_SPAWN ||
                                structure.structureType === STRUCTURE_WALL ||
                                structure.structureType === STRUCTURE_RAMPART;
                        }
                    });
                    
                    targets.sort((a, b) => a.hits - b.hits); // Sort by lowest hits first
                    
                    if (targets.length > 0) {
                        if (creep.attack(targets[0]) === ERR_NOT_IN_RANGE) {
                            creep.moveTo(targets[0]);
                        }
                    }
                }
            } else {
                // If there is no target room, defend home base
                let hostileCreeps = creep.room.find(FIND_HOSTILE_CREEPS);
                if (hostileCreeps.length > 0) {
                    if (creep.attack(hostileCreeps[0]) === ERR_NOT_IN_RANGE) {
                        creep.moveTo(hostileCreeps[0]);
                    }
                }
            }
        }
    }
}




module.exports = {
    attackerFunction
};