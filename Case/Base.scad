module showMainBody() {
    import("MainBody.stl");
}


difference() {
    union() {   
        cube([199, 96, 15]);

        translate([2.25, 2.25,0]) {
            cube([199-4.5, 96-4.5, 23]);
        }
        
        // Add a support for a phone.
        
        //translate([(199-80)/2,-10,24]) { - center - NFC reader issues.
        translate([10,-10,24]) {
            rotate([-55, 0, 0]) {
                cube([80, 20, 2]);
            }
        }
    }
    union() {
        
        // Main body cutout, but only down to 
        // 4mm to allow for a little pocket for the battery
        translate([3.75, 3.75,4]) {
            cube([199-7.5, 96-7.5, 25]);
        }
        
        // Battery cutout.
        translate([199-149-5.75, 6,1]) {
            #cube([151, 83.5, 25]);
        }
        
        // back cable cutout.
                // Power cable for the Pi.
        translate([179/2, 90, 15]) {
            #cube([5,15,15]);
        }
    }
}


translate([0,0,25]) {
    %showMainBody();
}