function towerRepair() {
    var towers = Game.spawns['Spawn1'].room.find(FIND_STRUCTURES, {
        filter: (structure) => {
            return structure.structureType == STRUCTURE_TOWER;
        }
    });
    
    if (towers.length > 0) {
        for (let tower of towers) {
            // Find hostile creeps
            let hostileCreeps = tower.pos.findInRange(FIND_HOSTILE_CREEPS, 50);
            
            // If there are hostile creeps, attack them
            if (hostileCreeps.length > 0) {
                let closestCreep = tower.pos.findClosestByRange(hostileCreeps);
                tower.attack(closestCreep);
            }
            else {
                // Get the controller level
                let controllerLevel = Game.spawns['Spawn1'].room.controller.level;
                
                // Calculate the target hits based on the controller level
                let targetHits = Math.pow(10, controllerLevel);
                
                // Find damaged ramparts first
                let damagedRampart = tower.pos.findClosestByRange(FIND_STRUCTURES, {
                    filter: (structure) => {
                        return structure.structureType === STRUCTURE_RAMPART && structure.hits < targetHits;
                    }
                });

                if (damagedRampart) {
                    tower.repair(damagedRampart);
                }
                else {
                    // If no damaged ramparts, find other damaged structures excluding walls
                    var closestDamagedStructure = tower.pos.findClosestByRange(FIND_STRUCTURES, {
                        filter: (structure) => {
                            // Exclude walls and ramparts
                            return structure.structureType !== STRUCTURE_WALL && structure.structureType !== STRUCTURE_RAMPART;
                        }
                    });
                    
                    // If there are damaged structures, repair them
                    if (closestDamagedStructure) {
                        tower.repair(closestDamagedStructure);
                    }
                    else {
                        // If no other damaged structures, find damaged walls
                        var closestDamagedWall = tower.pos.findClosestByRange(FIND_STRUCTURES, {
                            filter: (structure) => {
                                // Include only walls with hits < targetHits
                                return structure.structureType === STRUCTURE_WALL && structure.hits < targetHits && structure.hits < 300000000;
                            }
                        });

                        // If there are damaged walls, repair them
                        if (closestDamagedWall) {
                            tower.repair(closestDamagedWall);
                        }
                    }
                }
            }
        }
    }
}

module.exports = {
    towerRepair
};
