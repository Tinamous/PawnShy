// This enclosuren holds the RFID sensor and the Raspberry Pi.
// The MinionStandLEDHolder sits on top.

module showLedHolder() {
    translate([10,60,110]) {
        import("MinionStandlEDHolder.stl");
    }
}

module slopingBox(length, width, height, offset) {
    hull() {
        cube([length+20,width+offset, 8]);

        translate([10,offset,height]) {
            cube([length,width, 0.1]);
        }
    }
}

module hollowSlopingBox() {
    difference() {
        union() {
            slopingBox(175+4, 32+4,110, 60);
        }
        union() {
            translate([2, 2, 0]) {
                slopingBox(175, 32,108.5, 60);
            }
        }
    }
}

module mountingHoles() {
    translate([10, 8, -0.1]) {
        mountingHole();
    }
    
    translate([10, 36-8, -0.1]) {
        mountingHole();
    }
    
    translate([179/2, 8, -0.1]) {
        mountingHole();
    }
    
    translate([179/2, 36-8, -0.1]) {
        mountingHole();
    }
    
    translate([179-10, 8, -0.1]) {
        mountingHole();
    }
    
    translate([179-10, 36-8, -0.1]) {
        mountingHole();
    }
    
    // Cut out for LED connecting wires.
    translate([2, 2 + ((32-10.5)/2), -0.01]) {
        cube([4,10.5, 10 + 0.1]) ;
    }
}

module mountingHole() {
    cylinder(d=3.2, h=10);
}

$fn=60;

module rfidHolderHole() {
    cylinder(d=8, h=18);
    translate([0,0,18]) {
        cylinder(d=2.8,d2=8, h=3);
    }
}

// Holes are in the wrong place for the 
// RFID holder used for the "Do Not Hack" badger.
module rfidHolder() {
length = 97;
    
    translate([length-10, 0,0]) {
       rfidHolderHole(); 
    }
    
    translate([length-10, 90,0]) {
        rfidHolderHole();
    }
    
    translate([length-60, 0,0]) {
        rfidHolderHole();
    }
    
    translate([length-60, 90,0]) {
        rfidHolderHole();
    }
    
    translate([0, 16, 0]) {
        cube([length, 57, 18]);
    }
}

/*
module raspberryPi() {
    cube([88, 59, 25]);
    translate([3,3,-5]) {
        
        cylinder(d=3.2, h=35);
        
        // TODO: Add other Pi Mounting holes...
    }
}
*/

// Show a model of the Raspberry Pi to check sizing
module raspberryPi() {
    
    // Rasberry Pi main body
    cube([56, 80, 30]); // 65mm + USB/Ethernet port.
    
    // USB Connections
    translate([56-35,-53,5]) {
        cube([35, 53, 30]);
    }
    
    translate([5,80,30]) {
        //cube([12, 20, 20]);
    }
    
    // With connectors and supports.
//    cube([56, 80, 45]);
    
    // 4 Pin power connector (connect printer power when running 24V into Pi Power Hat)
    translate([3,80-25,30]) {
  //      cube([12, 4, 20]);
    }
    
    // Holes.
    translate([0,80-65,-10]) {
        piScrewHoles(3.2);
    }
}

module piScrewHoles(d) {
h = 40;
    translate([3.5,3.5,0]) {
        cylinder(d=d,h=h);
    }
    translate([52.5,3.5,0]) {
        cylinder(d=d,h=h);
    }
    translate([52.5,61.5,0]) {
        cylinder(d=d,h=h);
    }
    translate([3.5,61.5,0]) {
        cylinder(d=d,h=h);
    }
}

difference() {
    union() {
        hollowSlopingBox();
    }
    union() {
        translate([10,60,108]) {
           mountingHoles();
        }
        
        translate([40,22,5]) {
            rotate([59.5,0,0]) {
                #rfidHolder();
            }
        }
        
        translate([100,94,70]) {
            rotate([90,90,0]) {
                #raspberryPi();
            }
        }
        
        // Power cable for the Pi.
        translate([179/2, 90, 0]) {
            #cube([5,15,5]);
        }
    }
}


%showLedHolder();