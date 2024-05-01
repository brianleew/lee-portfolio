// Require/import another module
const minerModule = require("./miner");
const spawnModule = require("./spawn");
const attackerModule = require("./attacker");
const scoutModule = require("./scout");
const carryModule = require("./carry");
const builderModule = require("./builder");
const rebuilderModule = require("./towerManager");
const upgradeModule = require("./upgrader");
const towerModule = require("./tower");
const functionsModule = require("./functions");
const constructionModule = require("./construction")
const roomDefenseModule = require("./roomDefense")

// if script restarts, set it to false for roomDefense to work properly
if(Memory.initialScanDone === undefined) {
    Memory.initialScanDone = false;
}

module.exports.loop = function () {

    
    if (Game.time % 100 == 0) {
        for(let name in Memory.creeps) {
            if(!Game.creeps[name]) {
                delete Memory.creeps[name];
            }
        }
    }

    //SAFETY Feature
    const controller = Game.spawns['Spawn1'].room.controller;
    if(controller.level < 3) { 
        const room = Game.spawns['Spawn1'].room;
        functionsModule.activateSafeMode(room);
    }
    else {
        const room = Game.spawns['Spawn1'].room;
        functionsModule.activateSafeMode2(room);
    }
    

    // SPAWNING
    spawnModule.genminer();
    spawnModule.genCarry();

    //if there is a miner and carry, spawn others
    if(Object.keys(Game.creeps).filter(creep => Game.creeps[creep].memory.role === 'miner').length > 0 && Object.keys(Game.creeps).filter(creep => Game.creeps[creep].memory.role === 'carry').length > 0) {
        spawnModule.genBuilder();
        spawnModule.genUpgrader();
        //if controller is level 3, spawn a genTowerManager
        if(Game.spawns['Spawn1'].room.controller.level === 3) {
            spawnModule.genTowerManager();
        }
    
        //if controller is level 4, spawn attackers
        if(Game.spawns['Spawn1'].room.controller.level === 4) {
            spawnModule.genAttacker();
            spawnModule.genScout();
        }
    }
    
    //FOR CONSTRUCTION
    constructionModule.setConstructionSite();
    roomDefenseModule.roomDefense();
    
    //FOR WORKING
    minerModule.colletEnergyminers();
    carryModule.energyToHome();
    builderModule.energyToBuild();
    rebuilderModule.energyToReBuild();
    upgradeModule.upgraderDo();



    //make a variable for towers
    var towers = Game.spawns['Spawn1'].room.find(FIND_STRUCTURES, {
        filter: (structure) => {
            return structure.structureType == STRUCTURE_TOWER;
        }
    });
    if (towers.length > 0) {
        towerModule.towerRepair();
    }


    //FOR FIGHTING
    attackerModule.attackerFunction();
    scoutModule.scoutFunction();

    

    return;
}

