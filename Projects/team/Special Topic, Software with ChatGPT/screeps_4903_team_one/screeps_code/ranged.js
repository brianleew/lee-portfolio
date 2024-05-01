

function moveAround2() {
    for (const name in Game.creeps) {
        const creep = Game.creeps[name];

        if (creep.memory.role === 'AttRangedacRangker') {
            //Do Something
        }
    }
}


module.exports = {
    moveAround2
};