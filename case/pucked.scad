$fn=256;
pcb_d=123;
pcb_h=1.5;
top_h = 2;
bot_h = 6;
max_h = pcb_h+top_h+bot_h;

clearance = 1;
wall_h = 1.2;
wall_w = 1.6;

difference() {
case();
pattern();
}
//cover();
//electronics();
//battery();

module pattern() {
  translate([17,-72,-.79]) {
    for (j = [1:1:6]) {
        translate([0,19.2*j]) {
            tri_hept();
            for (i = [1:1:1]) {
                tri_hept(24.2*i);
            }
        }
    }
}
}

module tri_hept(x=0,y=0,flip=false,dupe=false) {
    translate([-5,6,0])
    rotate(52)
    cylinder(d=6,h=4,center=true,$fn=5);
    translate([-5,13,0])
    rotate(-52)
    cylinder(d=6,h=4,center=true,$fn=5);

    translate([-17,-3.6,0])
    rotate(52)
    cylinder(d=6,h=4,center=true,$fn=5);
    translate([-17,3.5,0])
    rotate(-52)
    cylinder(d=6,h=4,center=true,$fn=5);
    
    translate([-29.2,6.1,0])
    rotate(52)
    cylinder(d=6,h=4,center=true,$fn=5);
    translate([-29.2,13.1,0])
    rotate(-52)
    cylinder(d=6,h=4,center=true,$fn=5);
    
    
    mirror([flip?1:0,0,0])
    translate([flip && flip?x:-x,y,0])
    cylinder(d=10,h=4,center=true,$fn=7);
    mirror([flip?0:1,0,0])
    translate([-2.1+x*(flip?-1:1),-9.7+y,0])
    cylinder(d=10,h=4,center=true,$fn=7);
    mirror([flip?0:1,0,0])
    translate([-2.1+x*(flip?-1:1),9.7+y,0])
    cylinder(d=10,h=4,center=true,$fn=7);
    if (!dupe) {
        tri_hept(x=x+10,y=y,flip=!flip,dupe=true);
    }
}


module case() {    
   difference() {
       // Outter surface
        cylinder(r=pcb_d/2+clearance+wall_w,h=max_h+clearance*2+wall_h);

        translate([100+wall_w+clearance,0,0])
        cube([100,100,40],center=true);
        translate([-100-wall_w-clearance,0,0])
        cube([100,100,40],center=true);
        
        // Inner Surface
        difference() {
            translate([0,0,wall_h])
           cylinder(r=pcb_d/2+clearance, h=max_h+clearance*3);
            translate([100+clearance,0,0])
        cube([100,100,40],center=true);
        translate([-100-clearance,0,0])
        cube([100,100,40],center=true);
        
        }
        rotate([0,0,-16])
        translate([0,pcb_d/2+clearance+wall_w/2,bot_h+wall_h+clearance-1.5])
            cube([10,wall_w*2,5],center=true);
    }

    pcb_mount(x=1,y=1);
    pcb_mount(x=1,y=-1);
    pcb_mount(x=-1,y=1);
    pcb_mount(x=-1,y=-1);
}

module battery(w=34,l=50,h=5,show=false) {
    if (show) {
        translate([0,0,h/2+wall_h])
        cube([w,l,h],center=true);
    }
    difference() {
        translate([0,0,h/8+wall_h])
        cube([w+clearance*2+wall_w,l+clearance*2+wall_w,h/4],center=true);
        translate([0,0,h/2+wall_h])
        cube([w+clearance*2,l+clearance*2,h],center=true);
        
    }
}

module pcb_mount(x,y) {
    translate([37*x,40.5*y,wall_h]) {
        difference() {
            cylinder(d1=16,d2=10,h=bot_h+clearance);
            translate([0,0,bot_h+clearance-6]) cylinder(d=4,h=6+clearance);
        }
    }
}

module cover() {
  color("grey", 0.3)
    translate([0,0,max_h+wall_h+clearance*2])
    cylinder(r=pcb_d/2+clearance+wall_w,h=3);
}


// Inner Assembly Clearence Bounds
module electronics() {
    translate([0,0,wall_h+bot_h+clearance]) {
        difference() {
        union() {
            pcb();
            //top();
            //bottom();
        }
        translate([100,0,0])
        cube([100,200,40],center=true);
        translate([-100,0,0])
        cube([100,200,40],center=true);
        }
    }
}
module pcb() {
    // PCB Board
    difference() {
        color("green",1)
        cylinder(d=pcb_d, h=pcb_h);
    
        pcb_hole(x=1,y=1);
        pcb_hole(x=-1,y=1);
        pcb_hole(x=1,y=-1);
        pcb_hole(x=-1,y=-1);
}
}

module top() {   
// Top Bounds
difference() {
    color("cyan",.2)
    translate([0,0,pcb_h]) {
        cylinder(d=pcb_d,h=top_h);
        pcb_hole(x=1,y=1,h=top_h,c=2);
        pcb_hole(x=1,y=-1,h=top_h,c=2);
        pcb_hole(x=-1,y=1,h=top_h,c=2);
        pcb_hole(x=-1,y=-1,h=top_h,c=2);
    }
}
}

module bottom() {
// Bottom Bounds
difference() {
    color("magenta",.2 )
    translate([0,0,-bot_h]) {
        cylinder(d=pcb_d, h=bot_h);
    
        pcb_hole(x=1,y=1,h=bot_h,c=2);
        pcb_hole(x=1,y=-1,h=bot_h,c=2);
        pcb_hole(x=-1,y=1,h=bot_h,c=2);
        pcb_hole(x=-1,y=-1,h=bot_h,c=2);
    }
}
}
module pcb_hole(x, y, h=pcb_h, c=0) {
    translate([37*x,40.5*y,-clearance])
        cylinder(d=4.6+c,h=h+clearance*2);
}