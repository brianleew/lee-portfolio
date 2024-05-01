

function moveToTarget(creep, target) {
    creep.moveTo(target, { 
        visualizePathStyle: { stroke: '#ffffff' },
        ignoreRoads: false,
        swampCost: 10,
        plainCost: 2
    });
}

function activateSafeMode (room) {
    if (room && room.controller && room.controller.my && room.controller.level < 3) {
        const enemies = room.find(FIND_HOSTILE_CREEPS);

        // If there are enemies and we can activate safe mode, do so.
        if (enemies.length > 0 && room.controller.safeModeAvailable > 0 && !room.controller.safeModeCooldown) {
            room.controller.activateSafeMode();
        }
    }
}

function activateSafeMode2 (room) {
    if (room && room.controller && room.controller.my && room.controller.level < 3) {
        //if enemies attack spawn or tower, activate safe mode   WORK IN PROGRESS
        

    }
}

//Dont know if maxEnergy is already defined
// let maxEnergy = room.energyCapacityAvailable
const calculatePartsMiner = (maxEnergy) => {
    let parts = [];
    let pairs = Math.floor(maxEnergy / 150);
    for(let i = 0; i < pairs; i++) {
        parts.push(WORK);
        parts.push(MOVE);
    }
    return parts;
}

const calculatePartsCarry = (maxEnergy) => {
    let parts = [];
    let pairs = Math.floor(maxEnergy / 100);
    for(let i = 0; i < pairs; i++) {
        parts.push(CARRY);
        parts.push(MOVE);
    }
    return parts;
}

const calculatePartsBuilder = (maxEnergy) => {
    let parts = [];
    let pairs = Math.floor(maxEnergy / 200);
    for(let i = 0; i < pairs; i++) {
        parts.push(WORK);
        parts.push(MOVE);
        parts.push(CARRY);
    }
    return parts;
}

const calculatePartsAttacker = (maxEnergy) => {
    let parts = [];
    let pairs = Math.floor(maxEnergy / 150);
    for(let i = 0; i < pairs; i++) {
        parts.push(TOUGH);
        parts.push(TOUGH);
        parts.push(MOVE);
        parts.push(ATTACK);
    }
    return parts;
}

const calculatePartsScout = (maxEnergy) => {
    let parts = [];
    let pairs = Math.floor(maxEnergy / 80);
    for(let i = 0; i < pairs; i++) {
        parts.push(TOUGH);
        parts.push(TOUGH);
        parts.push(TOUGH);
        parts.push(MOVE);
    }
    return parts;
}



module.exports = {
    moveToTarget,
    activateSafeMode,
    activateSafeMode2,
    calculatePartsMiner,
    calculatePartsCarry,
    calculatePartsBuilder,
    calculatePartsAttacker,
    calculatePartsScout
};
