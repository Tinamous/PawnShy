$fn=100;

ledSpacing = 33.25;
minionDiameter = 26.5;

// Expected to sit on-top of the LED. Not to be around the LED
ledDiameter = 6; //4.2;

blockLength = 175;
blockWidth = 32;
blockHeight = 4;


difference() {
    union() {
        cube([175, blockWidth, blockHeight]);
    }
    union() {
        // 20mm to first Minion.
        translate([20.5, blockWidth/2,0]) {
            // Space for 5 minions
            for (minionNumber = [0 : 4]) {
                
                translate([ledSpacing * minionNumber,0, blockHeight-2.3]) {
                    cylinder(d=minionDiameter, h=3.1);
                }
                
                translate([ledSpacing * minionNumber,0, -0.01]) {
                    #cylinder(d=ledDiameter, h=blockHeight+0.02);
                }
            }
        }
    }
}