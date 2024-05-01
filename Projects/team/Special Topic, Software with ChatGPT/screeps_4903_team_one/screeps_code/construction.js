function setConstructionSite() {
    let spawn = Game.spawns['Spawn1'];
    let room = spawn.room;

    //---------------------------------------------------FUNCTIONS----------------------------------------------------------

    // Store the chosen directions in the Memory
    Memory.chosenDirectionsD = Memory.chosenDirectionsD || [];
    function scanDiagonally() {
        let model = {  // 1 = tower/storage/x, 2 = extension, 3 = road
                                 "0,2": 3,
                      "-1,1": 3, "0,1": 2, "1,1": 3, 
            "-2,0":3, "-1,0": 2, "0,0": 1, "1,0": 2, "2,0":3, 
                     "-1,-1": 3,"0,-1": 2,"1,-1": 3,     
                                "0,-2": 3, 
        };
        let directions = [
            {dx: 1, dy: 1},  // Upper-right
            {dx: 1, dy: -1}, // Lower-right
            {dx: -1, dy: -1}, // Lower-left
            {dx: -1, dy: 1}, // Upper-left
        ];
        // Array to hold all valid directions
        let validDirections = [];
        // For each direction
        directions.forEach((dir, index) => {
            if (Memory.chosenDirectionsD.includes(index)) {
                return; // Skip this direction if it was previously chosen
            }
            let canPlace = true;
            for(let [relPos, type] of Object.entries(model)) {
                let [rx, ry] = relPos.split(',').map(Number);
                let x = spawn.pos.x + dir.dx * (rx + 2);
                let y = spawn.pos.y + dir.dy * (ry + 2);
                let terrain = room.lookForAt(LOOK_TERRAIN, x, y);
                if(terrain[0] == 'wall') {
                    canPlace = false;
                    break;
                }
                
            }
            if(canPlace) {
                validDirections.push({direction: dir, index: index});
            } 
        });
        if(validDirections.length === 0) {
            scanCardinally();
            return;
        }
        // Select one valid direction
        let selected = validDirections[Math.floor(Math.random() * validDirections.length)];
        let dir = selected.direction;
        for(let [relPos, type] of Object.entries(model)) {
            let [rx, ry] = relPos.split(',').map(Number);
            let x = spawn.pos.x + dir.dx * (rx + 2);
            let y = spawn.pos.y + dir.dy * (ry + 2);
            if (room.controller.level === 3 && countTowers(room) === 0) {
                // Remember the chosen direction
                Memory.chosenDirectionsD.push(selected.index);
                switch(type) {
                    case 1: room.createConstructionSite(x, y, STRUCTURE_TOWER); break;
                    case 2: room.createConstructionSite(x, y, STRUCTURE_EXTENSION); break;
                    case 3: room.createConstructionSite(x, y, STRUCTURE_ROAD); break;
                }
            } 
            if (room.controller.level === 4 && countStorages(room) === 0) {
                // Remember the chosen direction
                Memory.chosenDirectionsD.push(selected.index);
                switch(type) {
                    case 1: room.createConstructionSite(x, y, STRUCTURE_STORAGE); break;
                    case 2: room.createConstructionSite(x, y, STRUCTURE_EXTENSION); break;
                    case 3: room.createConstructionSite(x, y, STRUCTURE_ROAD); break;
                }
            }
            if (room.controller.level === 4 && countStorages(room) === 1) { 
                // Remember the chosen direction
                Memory.chosenDirectionsD.push(selected.index);
                switch(type) {
                    case 1: room.createConstructionSite(x, y, STRUCTURE_EXTENSION); break;
                    case 2: room.createConstructionSite(x, y, STRUCTURE_EXTENSION); break;
                    case 3: room.createConstructionSite(x, y, STRUCTURE_ROAD); break;
                }
            }
            if (room.controller.level === 5 && countTowers(room) === 1) {
                // Remember the chosen direction
                Memory.chosenDirectionsD.push(selected.index);
                switch(type) {
                    case 1: room.createConstructionSite(x, y, STRUCTURE_TOWER); break;
                    case 2: room.createConstructionSite(x, y, STRUCTURE_EXTENSION); break;
                    case 3: room.createConstructionSite(x, y, STRUCTURE_ROAD); break;
                }
            }
            if (room.controller.level === 5 && countTowers(room) === 2) {
                // Remember the chosen direction
                Memory.chosenDirectionsD.push(selected.index);
                switch(type) {
                    case 1: room.createConstructionSite(x, y, STRUCTURE_EXTENSION); break;
                    case 2: room.createConstructionSite(x, y, STRUCTURE_EXTENSION); break;
                    case 3: room.createConstructionSite(x, y, STRUCTURE_ROAD); break;
                }
            }
            if (room.controller.level === 6) {
                // Remember the chosen direction
                Memory.chosenDirectionsD.push(selected.index);
                switch(type) {
                    case 1: room.createConstructionSite(x, y, STRUCTURE_EXTENSION); break;
                    case 2: room.createConstructionSite(x, y, STRUCTURE_EXTENSION); break;
                    case 3: room.createConstructionSite(x, y, STRUCTURE_ROAD); break;
                }
            }

        }
    }
    function countTowers(room) {
        let towerConstructionSites = room.find(FIND_CONSTRUCTION_SITES, {
            filter: (site) => site.structureType === STRUCTURE_TOWER
        });
    
        let builtTowers = room.find(FIND_STRUCTURES, {
            filter: (structure) => structure.structureType === STRUCTURE_TOWER
        });
    
        // Return the total number of towers (construction sites or built)
        return towerConstructionSites.length + builtTowers.length;
    }
    function countStorages(room) {
        let storageConstructionSites = room.find(FIND_CONSTRUCTION_SITES, {
            filter: (site) => site.structureType === STRUCTURE_STORAGE
        });
    
        let builtStorages = room.find(FIND_STRUCTURES, {
            filter: (structure) => structure.structureType === STRUCTURE_STORAGE
        });
    
        // Return the total number of storages (construction sites or built)
        return storageConstructionSites.length + builtStorages.length;
    }
    let turnoff = false;
    Memory.chosenDirectionsC = Memory.chosenDirectionsC || [];
    function scanCardinally() {
        let model = {  // 1 = tower/storage/x, 2 = extension, 3 = road                 
                         "0,2": 3,
              "-1,1": 3, "0,1": 2, "1,1": 3, 
    "-2,0":3, "-1,0": 2, "0,0": 1, "1,0": 2, "2,0":3, 
             "-1,-1": 3,"0,-1": 2,"1,-1": 3,     
                        "0,-2": 3,  
        };
        let directions = [
            {dx: 0, dy: -1}, // down
            {dx: 0, dy: 1},  // up 
            {dx: 1, dy: 0}, // right
            {dx: -1, dy: 0}, // left
        ];
        // Array to hold all valid directions
        let validDirections = [];
        // For each direction
        directions.forEach((dir, index) => {
            if (Memory.chosenDirectionsC.includes(index)) {
                return; // Skip this direction if it was previously chosen
            }
            let canPlace = true;
            for(let [relPos, type] of Object.entries(model)) {
                let [rx, ry] = relPos.split(',').map(Number);
                let x = spawn.pos.x + dir.dx * 4 + rx;
                let y = spawn.pos.y + dir.dy * 4 + ry;
                let terrain = room.lookForAt(LOOK_TERRAIN, x, y);
                if(terrain[0] == 'wall') {
                    canPlace = false;
                    break;
                }
            }
            if(canPlace) {
                validDirections.push({direction: dir, index: index});
            } 
        });
        if(validDirections.length === 0) {
            console.log('No valid areas for expansion.');
            turnoff = true;
            return;
        }
        // Select one valid direction randomly
        let selected = validDirections[Math.floor(Math.random() * validDirections.length)];
        let dir = selected.direction;
        for(let [relPos, type] of Object.entries(model)) {
            let [rx, ry] = relPos.split(',').map(Number);
            let x = spawn.pos.x + dir.dx * 4 + rx;
            let y = spawn.pos.y + dir.dy * 4 + ry;
            if (room.controller.level === 3 && countTowers(room) === 0) {
                // Remember the chosen direction
                Memory.chosenDirectionsC.push(selected.index);
                switch(type) {
                    case 1: room.createConstructionSite(x, y, STRUCTURE_TOWER); break;
                    case 2: room.createConstructionSite(x, y, STRUCTURE_EXTENSION); break;
                    case 3: room.createConstructionSite(x, y, STRUCTURE_ROAD); break;
                }
            } 
            if (room.controller.level === 4 && countStorages(room) === 0) {
                // Remember the chosen direction
                Memory.chosenDirectionsC.push(selected.index);
                switch(type) {
                    case 1: room.createConstructionSite(x, y, STRUCTURE_STORAGE); break;
                    case 2: room.createConstructionSite(x, y, STRUCTURE_EXTENSION); break;
                    case 3: room.createConstructionSite(x, y, STRUCTURE_ROAD); break;
                }
            }
            if (room.controller.level === 4 && countStorages(room) === 1) { 
                // Remember the chosen direction
                Memory.chosenDirectionsC.push(selected.index);
                switch(type) {
                    case 1: room.createConstructionSite(x, y, STRUCTURE_EXTENSION); break;
                    case 2: room.createConstructionSite(x, y, STRUCTURE_EXTENSION); break;
                    case 3: room.createConstructionSite(x, y, STRUCTURE_ROAD); break;
                }
            }
            if (room.controller.level === 5 && countTowers(room) === 1) {
                // Remember the chosen direction
                Memory.chosenDirectionsC.push(selected.index);
                switch(type) {
                    case 1: room.createConstructionSite(x, y, STRUCTURE_TOWER); break;
                    case 2: room.createConstructionSite(x, y, STRUCTURE_EXTENSION); break;
                    case 3: room.createConstructionSite(x, y, STRUCTURE_ROAD); break;
                }
            }
            if (room.controller.level === 5 && countTowers(room) === 2) {
                // Remember the chosen direction
                Memory.chosenDirectionsC.push(selected.index);
                switch(type) {
                    case 1: room.createConstructionSite(x, y, STRUCTURE_EXTENSION); break;
                    case 2: room.createConstructionSite(x, y, STRUCTURE_EXTENSION); break;
                    case 3: room.createConstructionSite(x, y, STRUCTURE_ROAD); break;
                }
            }
            if (room.controller.level === 6) {
                // Remember the chosen direction
                Memory.chosenDirectionsC.push(selected.index);
                switch(type) {
                    case 1: room.createConstructionSite(x, y, STRUCTURE_EXTENSION); break;
                    case 2: room.createConstructionSite(x, y, STRUCTURE_EXTENSION); break;
                    case 3: room.createConstructionSite(x, y, STRUCTURE_ROAD); break;
                }
            }

        }
    }

    function createContainersIfNeeded(room, numContainersNeeded) {
        room.memory.containersPlanned = room.memory.containersPlanned || 0;
        if ((room.memory.containersPlanned || 0) < numContainersNeeded) {
            let controller = room.controller;
            let minDistance = 3; // Minimum distance from the controller.
            let minContainerDistance = 3; // Minimum distance between containers.
            let searchRadius = minDistance; // Start the search radius from the minimum distance.
            room.memory.containerPositions = room.memory.containerPositions || []; // Store the positions of created containers
            while (room.memory.containersPlanned < numContainersNeeded) {
                let positions = [];
                let terrain = Game.map.getRoomTerrain(room.name);
                for(let dx = -searchRadius; dx <= searchRadius; dx++) {
                    for(let dy = -searchRadius; dy <= searchRadius; dy++) {
                        if(Math.abs(dx) < minDistance && Math.abs(dy) < minDistance) continue; // Ignore positions too close to the controller.
                        let x = controller.pos.x + dx;
                        let y = controller.pos.y + dy;
                        if(!(terrain.get(x, y) & TERRAIN_MASK_WALL)) {
                            let pos = new RoomPosition(x, y, room.name);
                            // Check if there's already a structure or construction site here.
                            let structures = pos.lookFor(LOOK_STRUCTURES);
                            let sites = pos.lookFor(LOOK_CONSTRUCTION_SITES);
                            if(!structures.length && !sites.length) {
                                // Check distance to other containers
                                let tooCloseToOtherContainer = room.memory.containerPositions.some(cPos => pos.getRangeTo(new RoomPosition(cPos.x, cPos.y, room.name)) < minContainerDistance);
                                if (!tooCloseToOtherContainer) {
                                    positions.push(pos);
                                }
                            }
                        }
                    }   
                }
                // Increment the search radius for the next iteration.
                searchRadius++;
                // If we couldn't find any positions, continue with the next iteration.
                if (positions.length === 0) continue;
                // Sort positions by their distance to the controller (ascending).
                positions.sort((a, b) => a.getRangeTo(controller) - b.getRangeTo(controller));
                // Create the construction site at the closest position.
                if (room.createConstructionSite(positions[0], STRUCTURE_CONTAINER) === OK) {
                    room.memory.containersPlanned = (room.memory.containersPlanned || 0) + 1;
                    room.memory.containerPositions.push({x: positions[0].x, y: positions[0].y});
                }
            }

        }
    }
    
    //---------------------------------------------------End of FUNCTIONS---------------------------------------------

    // Container number mapping based on Controller Level
    let numContainersByCL = {
        1: 2,
        2: 4,
        3: 5,
        // add more if needed
    };
    let currentCL = room.controller.level;
    // If the current controller level is in our mapping, create containers as needed.
    if (numContainersByCL[currentCL]) {
        createContainersIfNeeded(room, numContainersByCL[currentCL]);
    }
   
    //------------------LEVEL 2------------------
    if (room.controller.level === 2) {
        
        // Coordinates of the spawn, starting to form diamond shaped construction sites
        let x = spawn.pos.x;
        let y = spawn.pos.y;

        // Positions for extensions around the spawn
        let extensionPositions = [
            [x - 1, y], // left
            [x + 1, y], // right
            [x, y - 1], // above
            [x, y + 1]  // below
        ];

        // Create construction sites for extensions
        for(let pos of extensionPositions) {
            room.createConstructionSite(pos[0], pos[1], STRUCTURE_EXTENSION);
        }

        // Create construction sites for roads surrounding the entire group of structures
        // Calculate positions around the group
        let positionsAround = [
            [x - 2, y], // left
            [x + 2, y], // right
            [x, y - 2], // above
            [x, y + 2], // below
            [x - 1, y - 1], // upper left
            [x + 1, y - 1], // upper right
            [x - 1, y + 1], // lower left
            [x + 1, y + 1], // lower right
        ];

        // Create construction sites for roads at each position around the group
        for(let posAround of positionsAround) {
            // Make sure not to overwrite the spawn or an extension
            let look = room.lookAt(posAround[0], posAround[1]);
            if(!_.some(look, {'type': 'structure'}) && !_.some(look, {'type': 'constructionSite'})) {
                room.createConstructionSite(posAround[0], posAround[1], STRUCTURE_ROAD);
            }
        }
    }

    // Initialize level counters in Memory if they don't exist
    if(!Memory.levelCounters) {
        Memory.levelCounters = {
            3: 0,
            4: 0,
            5: 0,
            6: 0,
        };
    }

    // For level 3
    if (room.controller.level === 3 && Memory.levelCounters[3] < 1) {
        scanDiagonally();
        Memory.levelCounters[3]++;
    }

    // For level 4
    if (room.controller.level === 4 && Memory.levelCounters[4] < 2) {
        scanDiagonally();
        Memory.levelCounters[4]++;
    }

    // For level 5
    if (room.controller.level === 5 && Memory.levelCounters[5] < 2) {
        scanDiagonally();
        Memory.levelCounters[5]++;
    }
    
    // For level 6
    if (room.controller.level === 6 && Memory.levelCounters[6] < 3) {
        scanDiagonally();
        Memory.levelCounters[6]++;
    }
    if (turnoff === true) {
        return;
    }
}

module.exports = {
    setConstructionSite
};