
module minionStandModel() {
    cube([175, 32, 4]);
}

module ledTapeModel() {
    // TODO: Allow for connecting wires!
    color("red") {
        cube([166, 10, 0.5]);
        for (ledNumber = [0 : 4]) {
            translate([(33.5 * ledNumber) + 16.9+2.5,2.5,0]) {
                cube([5,5,2]);
            }
        }
    }
}



module showModels() {
    translate([2,2,4]) {
        translate([3.8,11,0]) {
            //%ledTapeModel();
        }

        translate([0, 0, 2]) {
            //%minionStandModel();
        }
    }
}

showModels();

height = 10;

difference() {
    union() {
        cube([175+4,32+4, height]);
        
    }
    union() {
        addText();
        
        translate([1.9,1.9,height-4]) {
            // Hollow out the inside for the top 
            // minion stand.
            cube([175.5,32.5, 4.01]) ;
        }
        
        // Hollow out down to the level of nearly full hegith
        // for the leds.
        translate([4,4, height - (4+2)]) {
            cube([175-4,32-4, 2.01]) ;
        }
        
        // Cutout for LEDs
        // 2,2 offset for case outer.
        // 20.5mm to first minion (i.e. first LED).
        // 33.5mm spacing between LEDS.
        // so 33.5/2 (16.7mm) from the tape start
        // to the first LED.
        // 20.5 - 16.7 = 3.8mm offset for the tape start.
        // +0.5 on the depth to allow for a little fudge factor
        // when it's all mounted.
        translate([2 + 3.8, 2 + ((32-10.5)/2), height - (4+2+1.5)]) {
            cube([170,10.5, 2.11]) ;
        }
        
        // Cut out for LED connecting wires.
        translate([2, 2 + ((32-10.5)/2), -0.01]) {
            cube([4,10.5, height + 0.1]) ;
        }
        
        // Mounting holes.
        mountingHoles();
       
    }
}

$fn=80;

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
}

module mountingHole() {
    
    cylinder(d1=3.2, d2=6.2, h=3);
    
    translate([0,0,2.5]) {
        cylinder(d=6.2, h=3);
    }
}

module addText() {
    translate([18,1.2,2]) {
        rotate([90,0,0]) {
            linear_extrude(1.5) {
                #text("';-- Have I Been Pwned", 7, spacing=1.5);
            }
        }
    }
}