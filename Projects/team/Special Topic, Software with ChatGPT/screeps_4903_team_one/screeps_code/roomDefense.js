function roomDefense(){
    
    let spawn = Game.spawns['Spawn1']; 
    let room = spawn.room;

    function scanExits() {
        delete Memory.ramparts;
        delete Memory.walls;
        delete Memory.wallas;
        // If ramparts and walls aren't in memory, initialize them
        if (!Memory.ramparts) {
            Memory.ramparts = [];
        }
        if (!Memory.walls) {
            Memory.walls = [];
        }
        if (!Memory.wallas) {
            Memory.wallas = [];
        }
        // Find all exits in the room
        let catExits = {};

        let exitUP = room.find(FIND_EXIT_TOP);
        let adjustedExitUP = exitUP.map(pos => {
            return new RoomPosition(pos.x, pos.y + 2, pos.roomName);
        });
        if(adjustedExitUP.length > 0){
            catExits.up = adjustedExitUP;
        }
    
        let exitDOWN = room.find(FIND_EXIT_BOTTOM);
        let adjustedExitDOWN = exitDOWN.map(pos => {
            return new RoomPosition(pos.x, pos.y - 2, pos.roomName);
        });
        if(adjustedExitDOWN.length > 0){
            catExits.down = adjustedExitDOWN;
        }

        let exitLEFT = room.find(FIND_EXIT_LEFT);
        let adjustedExitLEFT = exitLEFT.map(pos => {
            return new RoomPosition(pos.x + 2, pos.y, pos.roomName); 
        });
        if(adjustedExitLEFT.length > 0){
            catExits.left = adjustedExitLEFT;
        }

        let exitRIGHT = room.find(FIND_EXIT_RIGHT);
        let adjustedExitRIGHT = exitRIGHT.map(pos => {
            return new RoomPosition(pos.x - 2, pos.y, pos.roomName); 
        });
        if(adjustedExitRIGHT.length > 0){
            catExits.right = adjustedExitRIGHT;
        }
        
        console.log(`catExits: ${catExits}}`);
        
        let ramparts = [];
        let walls = [];
        let wallas = [];
        
        let highestPosLEFT = adjustedExitLEFT.reduce((highest, pos) => (pos.y < highest.y) ? pos : highest); 
        let lowestPosLEFT = adjustedExitLEFT.reduce((lowest, pos) => (pos.y > lowest.y) ? pos : lowest); 
        let extendedExitLEFT = [
            new RoomPosition(highestPosLEFT.x, highestPosLEFT.y - 2, highestPosLEFT.roomName), // one above
            new RoomPosition(highestPosLEFT.x, highestPosLEFT.y - 1, highestPosLEFT.roomName), // one above
            new RoomPosition(highestPosLEFT.x - 1, highestPosLEFT.y - 2, highestPosLEFT.roomName), // one to the left
            new RoomPosition(lowestPosLEFT.x, lowestPosLEFT.y + 1, lowestPosLEFT.roomName), // one below
            new RoomPosition(lowestPosLEFT.x, lowestPosLEFT.y + 2, lowestPosLEFT.roomName), // one below
            new RoomPosition(lowestPosLEFT.x - 1, lowestPosLEFT.y + 2, lowestPosLEFT.roomName), // one to the left
        ];
        console.log(`Extended exit left: ${extendedExitLEFT}`);

        let highestPosRIGHT = adjustedExitRIGHT.reduce((highest, pos) => (pos.y < highest.y) ? pos : highest); 
        let lowestPosRIGHT = adjustedExitRIGHT.reduce((lowest, pos) => (pos.y > lowest.y) ? pos : lowest); 
        let extendedExitRIGHT = [
            new RoomPosition(highestPosRIGHT.x, highestPosRIGHT.y - 2, highestPosRIGHT.roomName), // one above
            new RoomPosition(highestPosRIGHT.x, highestPosRIGHT.y - 1, highestPosRIGHT.roomName), // one above
            new RoomPosition(highestPosRIGHT.x + 1, highestPosRIGHT.y - 2, highestPosRIGHT.roomName), // one to the left
            new RoomPosition(lowestPosRIGHT.x, lowestPosRIGHT.y + 1, lowestPosRIGHT.roomName), // one below
            new RoomPosition(lowestPosRIGHT.x, lowestPosRIGHT.y + 2, lowestPosRIGHT.roomName), // one below
            new RoomPosition(lowestPosRIGHT.x + 1, lowestPosRIGHT.y + 2, lowestPosRIGHT.roomName), // one to the left
        ];
        console.log(`Extended exit right: ${extendedExitRIGHT}`);

        let highestPosUP = adjustedExitUP.reduce((highest, pos) => (pos.x > highest.x) ? pos : highest); 
        let lowestPosUP = adjustedExitUP.reduce((lowest, pos) => (pos.x < lowest.x) ? pos : lowest); 

        let extendedExitUP = [
            new RoomPosition(lowestPosUP.x - 1, lowestPosUP.y, lowestPosUP.roomName), 
            new RoomPosition(lowestPosUP.x - 2, lowestPosUP.y, lowestPosUP.roomName), 
            new RoomPosition(lowestPosUP.x - 2, lowestPosUP.y - 1, lowestPosUP.roomName), 
            new RoomPosition(highestPosUP.x + 1, highestPosUP.y, highestPosUP.roomName), 
            new RoomPosition(highestPosUP.x + 2, highestPosUP.y, highestPosUP.roomName), 
            new RoomPosition(highestPosUP.x + 2, highestPosUP.y - 1, highestPosUP.roomName), 
        ];
        console.log(`Extended exit up: ${extendedExitUP}`);

        let highestPosDOWN = adjustedExitDOWN.reduce((highest, pos) => (pos.x > highest.x) ? pos : highest); 
        let lowestPosDOWN = adjustedExitDOWN.reduce((lowest, pos) => (pos.x < lowest.x) ? pos : lowest); 
        let extendedExitDOWN = [
            new RoomPosition(lowestPosDOWN.x - 1, lowestPosDOWN.y, lowestPosDOWN.roomName), 
            new RoomPosition(lowestPosDOWN.x - 2, lowestPosDOWN.y, lowestPosDOWN.roomName), 
            new RoomPosition(lowestPosDOWN.x - 2, lowestPosDOWN.y + 1, lowestPosDOWN.roomName), 
            new RoomPosition(highestPosDOWN.x + 1, highestPosDOWN.y, highestPosDOWN.roomName), 
            new RoomPosition(highestPosDOWN.x + 2, highestPosDOWN.y, highestPosDOWN.roomName), 
            new RoomPosition(highestPosDOWN.x + 2, highestPosDOWN.y + 1, highestPosDOWN.roomName), 
        ];
        console.log(`Extended exit down: ${extendedExitDOWN}`);

        // similar structure to catExits but we are going to process it differently
        let newExits = {
            'LEFT': extendedExitLEFT,
            'RIGHT': extendedExitRIGHT,
            'UP': extendedExitUP,
            'DOWN': extendedExitDOWN,
        };
        // Process each category of exit in newExits
        for(let cat in newExits) {
            let newExitsInCategory = newExits[cat];
            
            // Remove the category if no coordinates are present
            if(newExitsInCategory.length === 0) {
                delete newExits[cat];
                continue;
            }

            // Remove swamp positions
            newExits[cat] = newExitsInCategory.filter(exita => {
                let terraina = room.lookForAt(LOOK_TERRAIN, exita);
                return terraina[0] !== 'swamp';
            });

            // Remove wall positions
            newExits[cat] = newExits[cat].filter(exita => {
                let terraina = room.lookForAt(LOOK_TERRAIN, exita);
                return terraina[0] !== 'wall';
            });

            if(newExits[cat].length >= 1) {
                wallas = wallas.concat(newExits[cat]);
                delete newExits[cat];
                continue;
            }
            
        }

        // Process each category of exit
        for(let category in catExits) {
            let exitsInCategory = catExits[category];
            // Remove the category if no coordinates are present
            if(exitsInCategory.length === 0) {
                delete catExits[category];
                continue;
            }
            
            // Remove swamp positions
            catExits[category] = exitsInCategory.filter(exit => {
                let terrain = room.lookForAt(LOOK_TERRAIN, exit);
                return terrain[0] !== 'swamp';
            });

            // Remove wall positions
            catExits[category] = catExits[category].filter(exit => {
                let terrain = room.lookForAt(LOOK_TERRAIN, exit);
                return terrain[0] !== 'wall';
            });

            // If only 1 exit remains, add it to ramparts
            if(catExits[category].length === 1) {
                ramparts.push(catExits[category][0]);
                delete catExits[category];
                continue;
            }

            // If 2 or more exits remain, add one to ramparts and the rest to walls
            if(catExits[category].length >= 2) {
                ramparts.push(catExits[category][0]);
                walls = walls.concat(catExits[category].slice(1));
                delete catExits[category];
                continue;
            }
        }
        // At the end of the scanExits function, update the memory
        Memory.ramparts = ramparts;
        Memory.walls = walls;
        Memory.wallas = wallas;
    }
    
    if(!Memory.initialScanDone && room.controller.level === 1) {
        scanExits();
        Memory.initialScanDone = true;
    }
    if(room.controller.level >= 2) {
        // Process walls reverse order better for deleting memory array
        for(let i = Memory.wallas.length - 1; i >= 0; i--) {
            let walla = Memory.wallas[i];
            room.createConstructionSite(walla.x, walla.y, STRUCTURE_WALL);           
            //remove from memory
            Memory.wallas.splice(i, 1);
        }
    }
    if(room.controller.level >= 2) {
        // Process walls reverse order better for deleting memory array
        for(let i = Memory.walls.length - 1; i >= 0; i--) {
            let wall = Memory.walls[i];
            room.createConstructionSite(wall.x, wall.y, STRUCTURE_WALL);           
            //remove from memory
            Memory.walls.splice(i, 1);
        }
    }
    if(room.controller.level >= 2) {
        // Process walls reverse order better for deleting memory array
        for(let i = Memory.ramparts.length - 1; i >= 0; i--) {
            let rampart = Memory.ramparts[i];
            room.createConstructionSite(rampart.x, rampart.y, STRUCTURE_RAMPART);
            //remove from memory
            Memory.ramparts.splice(i, 1);
        }
    }
    if(Memory.walls.length === 0 && Memory.ramparts.length === 0 && Memory.wallas.length === 0) {
        return;
    }
}
module.exports = {
    roomDefense
};