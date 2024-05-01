const attackerModule = require("./attacker");
const functionsModule = require("./functions");

const minerCount = 2; // Number of miners you want to spawn
const carryCount = 2; // Number of carry you want to spawn
const builderCount = 1; // Number of builders you want to spawn
const upgraderCount = 1; // Number of upgraders you want to spawn
const energySources = Game.spawns['Spawn1'].room.find(FIND_SOURCES);


function genminer() {


  for (let i = 1; i <= minerCount; i++) {
    const creepName = `miner${i}`;
  
    if (!Game.creeps[creepName]) {
      let sID = i - 1;
      const spawnResult = Game.spawns['Spawn1'].spawnCreep(
        functionsModule.calculatePartsMiner(Game.spawns['Spawn1'].room.energyCapacityAvailable), // Body
        creepName, // Name
        { memory: { role: 'miner', sourceID: energySources[sID].id } } // Memory
      );
    }
  }
  
}

function genCarry() {

  for (let i = 1; i <= carryCount; i++) {
    const creepName = `carry${i}`;
    const minerName = `miner${i}`;  // each carry is associated with a specific miner
  
    if (!Game.creeps[creepName]) {
      const spawnResult = Game.spawns['Spawn1'].spawnCreep(
        functionsModule.calculatePartsCarry(Game.spawns['Spawn1'].room.energyCapacityAvailable),
        creepName,
        { memory: { role: 'carry', minerName } } // include minerName here
      );
    }
  }
  
}

function genBuilder() {

  if (minerCreepCount() > 0 && carryCreepCount() > 0) {


    for (let i = 1; i <= builderCount; i++) {
      const creepName = `builder${i}`;

      if (!Game.creeps[creepName]) {
        const spawnResult = Game.spawns['Spawn1'].spawnCreep(functionsModule.calculatePartsBuilder(Game.spawns['Spawn1'].room.energyCapacityAvailable), creepName);

        if (spawnResult === OK) {
          Game.creeps[creepName].memory.role = 'builder';
        }
      }
  }
  }
}

function genUpgrader() {

  for (let i = 1; i <= upgraderCount; i++) {
    const creepName = `upgrader${i}`;

    if (!Game.creeps[creepName]) {
      const spawnResult = Game.spawns['Spawn1'].spawnCreep(functionsModule.calculatePartsBuilder(Game.spawns['Spawn1'].room.energyCapacityAvailable), creepName);

      if (spawnResult === OK) {
        Game.creeps[creepName].memory.role = 'upgrader';
      }
    }
  }
}

function genTowerManager() {

  if (minerCreepCount() > 1 && carryCreepCount() > 1) {

    //Generate miner creeps if needed
    if (!Game.creeps['towerManager']) {
      const creepName = 'towerManager';
      const spawnResult = Game.spawns['Spawn1'].spawnCreep([CARRY, CARRY, CARRY, CARRY, CARRY, CARRY, CARRY, CARRY, CARRY, CARRY, CARRY, MOVE, MOVE, MOVE, MOVE, MOVE], creepName);

      if (spawnResult === OK) {
        Game.creeps[creepName].memory.role = 'towerManager';
      }
    }
  }
}

function genAttacker() {

  for (let i = 1; i <= minerCount; i++) {
    const creepName = `attacker${i}`;
  
    if (!Game.creeps[creepName]) {
      let sID = i - 1;
      const spawnResult = Game.spawns['Spawn1'].spawnCreep(
        functionsModule.calculatePartsAttacker(Game.spawns['Spawn1'].room.energyCapacityAvailable), // Body
        creepName, // Name
        { memory: { role: 'attacker', sourceID: energySources[sID].id } } // Memory
      );
    }
  }
}

function genScout() {

  for (let i = 1; i <= minerCount; i++) {
    const creepName = `scout${i}`;
  
    if (!Game.creeps[creepName]) {
      let sID = i - 1;
      const spawnResult = Game.spawns['Spawn1'].spawnCreep(
        functionsModule.calculatePartsScout(Game.spawns['Spawn1'].room.energyCapacityAvailable), // Body
        creepName, // Name
        { memory: { role: 'scout', sourceID: energySources[sID].id } } // Memory
      );
    }
  }
}

function countCreepRoles() {
  // Initialize an empty object to store the counts
  let roleCounts = {};
  let total = 0;

  // Iterate over all creeps
  for(let creepName in Game.creeps) {
      let creep = Game.creeps[creepName];
      
      // Get the role of the creep
      let role = creep.memory.role;

      // If the role isn't in the counts object yet, add it with a count of 0
      if(!roleCounts[role]) {
          roleCounts[role] = 0;
         
      }

      // Increment the count for this role
      roleCounts[role]++;
      total++;

  }

  // Log the counts
  for(let role in roleCounts) {
      console.log(`Role ${role}: ${roleCounts[role]}`);
  }


  return "total is " + total;
}

function minerCreepCount() {
  let minerCreepCount = 0;
  for (const creepName in Game.creeps) {
    const creep = Game.creeps[creepName];
    if (creep.memory.role === 'miner') {
      minerCreepCount++;
    }
  }
  return minerCreepCount;
}

function carryCreepCount() {
  let carryCreepCount = 0;
  for (const creepName in Game.creeps) {
    const creep = Game.creeps[creepName];
    if (creep.memory.role === 'carry') {
      carryCreepCount++;
    }
  }
  return carryCreepCount;
}




module.exports = {
    genminer,
    genCarry,
    genAttacker,
    genScout,
    genBuilder,
    genUpgrader,
    genTowerManager,
    countCreepRoles,
    carryCreepCount,
    minerCreepCount
};