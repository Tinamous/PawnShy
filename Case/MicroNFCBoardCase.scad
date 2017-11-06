$fn=60;
curveRadius = 4;
wallWidth = 3;

totalWidth = 36 + 2*wallWidth;
totalHeight = 103+ + 2*wallWidth;

// NB: Uses M2 Screws.

// If the case is an insert for the badger/dymo case
//caseMountingStyle = 0; // Ultimaker Lid
//caseMountingStyle = 1; // Badger
caseMountingStyle = 2; // Have I Been Pwned (main case has holes closer - I measured wrong!)
//caseMountingStyle = 3; // Alternative UM lid for NCF PCB

module rfidReaderHoleChecker() {
    // PCB + underneath aerial.
    cube([35.2,100,1.6]);
    // Making points where the holes are expected to go to test 
    // alignment with actual PCB
    holeHeight = 3;
    holeDiameter = 1.2;

    // PCB holes
    // LHS
    translate([2,0,0]) {
        translate([0,2.5,0]) {
            cylinder(d=holeDiameter, h=holeHeight);
        }
        translate([0,42.5,0]) {
            cylinder(d=holeDiameter, h=holeHeight);
        }
        
    }
    
    // RHS
    translate([33,0,0]) {
        translate([0,2.5,0]) {
            cylinder(d=holeDiameter, h=holeHeight);
        }
        
        translate([0,42.5,0]) {
            cylinder(d=holeDiameter, h=holeHeight);
        }
    }
}

module rfidReader() {
    
    //cube([51,91,16]);
    holeDiameter = 3;
    difference() {
        union() {
            // PCB + underneath aerial.
            cube([35.2,100.2,1.6]);
            // USB socket
            translate([13.5,0,0]) {
                // Buttons are 7mm, USB socked is lower
                // but show it as 7mm to save modelling the buttons also.
                cube([7,5,7]);
            }
            
            // USB Plug
            translate([10.5,-25,-1]) {
                cube([12,25,7]);
            }
            
            
            // Buttons
            translate([8,6,0]) {
                cylinder(d=4, h=5);
            }
            translate([27.5,6,0]) {
                cylinder(d=4, h=5);
            }

            // LEDs
            translate([5,37,0]) {
                cylinder(d=1, h=15);
            }
            translate([31,37,0]) {
                cylinder(d=1, h=15);
            }
        }
        union() {
            // PCB holes
            // LHS
            translate([2,0,0]) {
                translate([0,2.5,0]) {
                    #cylinder(d=holeDiameter, h=20);
                }
                translate([0,42.5,0]) {
                    #cylinder(d=holeDiameter, h=20);
                }
            }
            
            // RHS
            translate([33,0,0]) {
                translate([0,2.5,0]) {
                    #cylinder(d=holeDiameter, h=20);
                }
                translate([0,42.5,0]) {
                    #cylinder(d=holeDiameter, h=20);
                }
            }
        }
    }
}

module GenericBase(xDistance, yDistance, zHeight, zAdjust) {
	    
    // NB: base drops below 0 line by the curve radius so we need to compensate for that
	translate([curveRadius,curveRadius, zAdjust]) {
		minkowski()
		{
			// 3D Minkowski sum all dimensions will be the sum of the two object's dimensions
			cube([xDistance-(curveRadius*2), yDistance-(curveRadius*2), (zHeight /2)]);
			cylinder(r=curveRadius,h= (zHeight/2) + curveRadius);
		}
	}
}

module genericBase2(width, height, depth, cornerDiameter) {
//cornerDiameter = 5;
cornerRadius = cornerDiameter/2;

    translate([cornerDiameter/2,0,0]) {
        cube([width-cornerDiameter, height, depth]);
    }
    
    translate([0,cornerDiameter/2,0]) {
        cube([width, height-cornerDiameter, depth]);
    }
    
    translate([cornerRadius,cornerRadius,0]) {
        cylinder(d=cornerDiameter, h=depth);
    }
    
    translate([width-cornerRadius,cornerRadius,0]) {
        cylinder(d=cornerDiameter, h=depth);
    }
    
    translate([cornerRadius,height-cornerRadius,0]) {
        cylinder(d=cornerDiameter, h=depth);
    }
    
    translate([width-cornerRadius,height-cornerRadius,0]) {
        cylinder(d=cornerDiameter, h=depth);
    }
}

pcbDepth = 2;

module caseOuter() {
holeHeight = 8;
holeSupportDiameter = 6;
holeInnerDiameter = 3.2;
    
    difference() {
        union() {
            //PCB 51,91,16
            //GenericBase(51 + 2*wallWidth, 91+ 2*wallWidth, 16-5+2 + 0.5, 0);
            genericBase2(totalWidth, totalHeight, 10, 8);
        }
        union() {
            // Inner cutout
            translate([wallWidth+1.5, wallWidth, -0.01]) {
                // PCB: 35x100
                // take to 103.
                // but... not here.
                genericBase2(32.5,97,11,4);
                //cube([33, 99, 9]);
            }
            
            // Hollow out PCB
            translate([wallWidth-0.5, wallWidth, 0]) {
                    // Hollow out the same but longer for the PCB
                    // so leaving a ridge for the end of the PCB to sit on
                    // hopefully at the same height as the pcb mounts!
                    cube([37, 102.5, pcbDepth]);               
            }
            
            // Cut through the base for the the badger
            // case to reduce print time, allow ventilation
            // and view the LEDs on the PCB.
            if (caseMountingStyle==1 || caseMountingStyle==2) {
                translate([wallWidth+4.5, wallWidth, -0.1]) {
                    genericBase2(36-10, 97, 11, 8);
                }
            }
            
            // USB input
            translate([11 + (wallWidth + 0.5) - 1,-5,-0.01]) {
                cube([15,10,8]);
            }
        }
    }
    
    
    // Screw posts for the NFC PCB.
    translate([wallWidth+0.5, wallWidth+0.5,pcbDepth]) {                
        mountingPin(2,2.5);
        mountingPin(2,42.5);
    
        mountingPin(33,2.5);
        mountingPin(33,42.5);
    }
    
    
}

// Mouting pin for the FRID reader.
module mountingPin(x,y) {
holeHeight = 10;
holeSupportDiameter = 6;
    
    translate([x,y,0]) {
        cylinder(d=4, h=holeHeight-pcbDepth);
        translate([0,0,-2]) {
            // PCB holes are 1.8mm
            // pin isn't so critical as PCB will be sandwiched between case and enclosure.
            cylinder(d=1.2, h=holeHeight-pcbDepth);
        }
    }
}

// Mounting hole for the RFID reader
module mountingHole(x,y) {
holeHeight = 13.5;
holeSupportDiameter = 6;
holeInnerDiameter = 1.6;
    translate([x,y,0]) {
        difference() {
            union() {
                cylinder(d=holeSupportDiameter, h=holeHeight);
            }
            union() {
                cylinder(d=holeInnerDiameter, h=holeHeight-5);
            }
        }
    }
}

// Mounting hole for the case.
module caseMountingHole(x,y, height, holeSize) {

    translate([x,y,0]) {
        difference() {
            union() {
                cylinder(d=8, h=height);
            }
            union() {
                translate([0,0,-0.01]) {
                    cylinder(d=holeSize, h=height + 0.02);
                }
            }
        }
    }
}

// Top/Bottom (length) of case
module caseMounts(height, holeSize) {
    caseMountingHole(totalWidth/2, totalHeight + 2, height, holeSize);
    caseMountingHole(totalWidth/2, - 2, , height, holeSize);
}

module caseMountConnector(x,y,height) {
    // -3 to allow for hole size and width of cube.
zOffset = 1;
    translate([x, y-3, zOffset ]) {
        cube([22, 6, height-zOffset ]);
    }
}

// Sides to to fit the badger label printer case.
module badgerCaseMounts(height, holeSize) {
    
    echo("totalWidth:", totalWidth);
    
midXHoles = 90/2; // 45
midCase = totalWidth/2; // 57/2 = 28.5
offset = midXHoles - midCase;
//offset2 - midXHoles - 

// 10mm offset for first    
firstMountY = totalHeight - 10;
yDistanceBetweenMounts = 55;
    
    echo("offset:", offset);

    // Raise the mouting points up 1mm
    translate([0,0,-0.01]) {
        // 90mm between 8 axis mounts
        // Top 2 (furthest from USB
        caseMountingHole(midCase + midXHoles, firstMountY, height, holeSize);
        caseMountConnector(totalWidth, firstMountY, height);
        
        caseMountingHole(midCase - midXHoles, firstMountY, height, holeSize);
        caseMountConnector(midCase - midXHoles+2.5, firstMountY, height);
        
        // 55mm gap on y axis
        caseMountingHole(midCase + midXHoles, firstMountY-yDistanceBetweenMounts, height, holeSize);
        caseMountConnector(totalWidth, firstMountY-yDistanceBetweenMounts, height);
        
        caseMountingHole(midCase - midXHoles, firstMountY-yDistanceBetweenMounts, height, holeSize);
        caseMountConnector(midCase - midXHoles+2.5, firstMountY-yDistanceBetweenMounts, height);
    }
}

module haveIBeenPwnedCaseMounts(height, holeSize) {
         
midXHoles = 90/2; // 45
midCase = totalWidth/2; // 57/2 = 28.5
offset = midXHoles - midCase;
//offset2 - midXHoles - 

// 10mm offset for first    
firstMountY = totalHeight - 10;
yDistanceBetweenMounts = 50;
    
    echo("offset:", offset);

    // Raise the mouting points up 1mm
    translate([0,0,-0.01]) {
        // 90mm between 8 axis mounts
        // Top 2 (furthest from USB
        caseMountingHole(midCase + midXHoles, firstMountY, height, holeSize);
        caseMountConnector(totalWidth, firstMountY, height);
        
        caseMountingHole(midCase - midXHoles, firstMountY, height, holeSize);
        caseMountConnector(midCase - midXHoles+2.5, firstMountY, height);
        
        // 55mm gap on y axis
        caseMountingHole(midCase + midXHoles, firstMountY-yDistanceBetweenMounts, height, holeSize);
        caseMountConnector(totalWidth, firstMountY-yDistanceBetweenMounts, height);
        
        caseMountingHole(midCase - midXHoles, firstMountY-yDistanceBetweenMounts, height, holeSize);
        caseMountConnector(midCase - midXHoles+2.5, firstMountY-yDistanceBetweenMounts, height);
    }
}

module alternativeLidMounts(height, holeSize) {
midXHoles = 24; //90/2; // 45
midCase = totalWidth/2; // 57/2 = 28.5
offset = midXHoles - midCase;

// 10mm offset for first    
firstMountY = totalHeight - 10;
yDistanceBetweenMounts = 85;
    
    echo("offset:", offset);

    // Raise the mouting points up 1mm
    translate([0,0,0]) {
        // 90mm between 8 axis mounts
        // Top 2 (furthest from USB
        caseMountingHole(midCase + midXHoles, firstMountY, height, holeSize);        
        caseMountingHole(midCase - midXHoles, firstMountY, height, holeSize);
        caseMountingHole(midCase + midXHoles, firstMountY-yDistanceBetweenMounts, height, holeSize);
        caseMountingHole(midCase - midXHoles, firstMountY-yDistanceBetweenMounts, height, holeSize);
    }
}

// +0.5 to allow a gap around the wall
translate([wallWidth +0.5, wallWidth +0.5 ,0]) {
    //color("red") {
       %rfidReader();
       //% rfidReaderDrillTemplate();
    
        // Printable flat to check that the holes
        // are in the expected place.
       //rfidReaderHoleChecker();
    //}
}




caseOuter();

mountHeight = 10;
mountHoleSize = 4.2;

if (caseMountingStyle  ==  0) {
    caseMounts(mountHeight, mountHoleSize);
} else if (caseMountingStyle == 1) {
    badgerCaseMounts(mountHeight, mountHoleSize);
} else if (caseMountingStyle == 2) {
    haveIBeenPwnedCaseMounts(mountHeight, mountHoleSize);
} else if (caseMountingStyle == 3) {
    alternativeLidMounts(mountHeight, mountHoleSize);
}