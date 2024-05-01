

function scoutFunction() {

    for(let name in Game.creeps) {
        let creep = Game.creeps[name];

        // Scout creep behavior
        if (creep.memory.role === 'scout') {
            // If there is a target room set in the creep's memory, try to move to it
            if (creep.memory.targetRoom) {
                // Try to move to the target room
                const exitDir = Game.map.findExit(creep.room, creep.memory.targetRoom);
                const exit = creep.pos.findClosestByPath(exitDir);
                creep.moveTo(exit);
            } else {
                // If there is no target room, pick a random exit and move to it
                const exitDir = Math.floor(Math.random() * 4) + 1;  // random direction between 1 and 4
                const exit = creep.pos.findClosestByPath(exitDir);
                creep.moveTo(exit);
            }
        }

        // Scouting logic
        if (creep.memory.role === 'scout') {
            let rooms = Game.map.describeExits(creep.room.name);
            for (let direction in rooms) {
                let roomName = rooms[direction];
                Game.map.visual.text('⛔', new RoomPosition(25, 25, roomName));
                
                let room = Game.rooms[roomName];
                if (room && !room.controller.safeMode) {
                    let towers = room.find(FIND_STRUCTURES, { filter: s => s.structureType === STRUCTURE_TOWER });
                    if (towers.length === 0) {
                        // Tell attackers to attack this room
                        for(let attackerName in Game.creeps) {
                            let attackerCreep = Game.creeps[attackerName];
                            if (attackerCreep.memory.role === 'attacker') {
                                attackerCreep.memory.targetRoom = roomName;
                            }
                        }
                    }
                    
                    for (let tower of towers) {
                        if (tower.energy === 0) {
                            // Tell attackers to attack this room
                            for(let attackerName in Game.creeps) {
                                let attackerCreep = Game.creeps[attackerName];
                                if (attackerCreep.memory.role === 'attacker') {
                                    attackerCreep.memory.targetRoom = roomName;
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}


module.exports = {
    scoutFunction
};