$fn=256;
pcb_d=123;
bat_w=65;
bat_l=113;
bat_h = 5.5*2;
pcb_h=1.5;
top_h = 2;
bot_h = 6+bat_h;
max_h = pcb_h+top_h+bot_h;

clearance = 1;
wall_h = 2.54;
wall_w = 1.6;

// Use for DXF/SVG Laser Export
// projection(cut = false)

if (true) {
    case();
} else {
    difference() {
        case();
        pattern();
    }
}
//pcb();
//cover();
//base();
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
       translate([0,0,wall_h])
        cylinder(r=pcb_d/2+clearance+wall_w,h=max_h+clearance*2);

        translate([100+wall_w+clearance,0,0])
        cube(100,center=true);
        translate([-100-wall_w-clearance,0,0])
        cube(100,center=true);
       
       // Battery Expansion
       translate([0,0,bat_h-clearance*2])
                cube([bat_w+clearance*2,bat_l+clearance*2,bat_h+clearance*2],center=true);
       translate([-bat_w/2-clearance+7.1,-bat_l/2-clearance+7.1,bat_h+clearance+wall_h])
                rotate([0,0,45])
                cylinder(10,10,0,$fn=4);
        translate([bat_w/2+clearance-7.1,-bat_l/2-clearance+7.1,bat_h+clearance+wall_h])
                rotate([0,0,45])
                cylinder(10,10,0,$fn=4);
        translate([-bat_w/2-clearance+7.1,bat_l/2+clearance-7.1,bat_h+clearance+wall_h])
                rotate([0,0,45])
                cylinder(10,10,0,$fn=4);
        translate([bat_w/2+clearance-7.1,bat_l/2+clearance-7.1,bat_h+clearance+wall_h])
                rotate([0,0,45])
                cylinder(10,10,0,$fn=4);
       
        // Inner Surface
        difference() {
            translate([0,0,wall_h-2])
           cylinder(r=pcb_d/2+clearance, h=max_h+clearance*3+2);
            translate([100+clearance,0,0])
        cube(100,center=true);
        translate([-100-clearance,0,0])
        cube(100,center=true);
        
        }
        // USB Port
        rotate([0,0,-16])
        translate([0,pcb_d/2+clearance+wall_w/2,bot_h+wall_h])
            cube([10,wall_w*2,5],center=true);
    }
    
    // Battery extension
    difference() {
        translate([0,0,(bat_h+clearance)/2+wall_h])
        cube([bat_w+clearance*2+wall_w*2,bat_l+clearance*2+wall_w*2,bat_h+clearance],center=true);
        translate([0,0,bat_h-2])
        cube([bat_w+clearance*2,bat_l+clearance*2,bat_h+clearance+2],center=true);
        cube([bat_w+wall_w+clearance*4,80,30],center=true);
        cube([49,bat_l+wall_w+clearance*4,30],center=true);
    }

    difference() {
        translate([-bat_w/2-wall_w-clearance+7.1,-bat_l/2-wall_w-clearance+7.1,bat_h+clearance+wall_h])
            rotate([0,0,45])
                cylinder(10,10,0,$fn=4);
        translate([-bat_w/2-wall_w-clearance+7.1+wall_w,-bat_l/2-wall_w-clearance+7.1+wall_w,bat_h+clearance+wall_h])
            rotate([0,0,45])
            cylinder(10,10,0,$fn=4);
        cylinder(30,r=pcb_d/2+clearance);
    }
    difference() {
        translate([bat_w/2+wall_w+clearance-7.1,-bat_l/2-wall_w-clearance+7.1,bat_h+clearance+wall_h])
            rotate([0,0,45])
                cylinder(10,10,0,$fn=4);
        translate([bat_w/2+clearance-7.1,-bat_l/2-clearance+7.1,bat_h+clearance+wall_h])
            rotate([0,0,45])
            cylinder(10,10,0,$fn=4);
        cylinder(30,r=pcb_d/2+clearance);
    }
    difference() {
        translate([-bat_w/2-wall_w-clearance+7.1,bat_l/2+wall_w+clearance-7.1,bat_h+clearance+wall_h])
            rotate([0,0,45])
                cylinder(10,10,0,$fn=4);
        translate([-bat_w/2-wall_w-clearance+7.1+wall_w,bat_l/2+clearance-7.1,bat_h+clearance+wall_h])
            rotate([0,0,45])
            cylinder(10,10,0,$fn=4);
        cylinder(30,r=pcb_d/2+clearance);
    }
    difference() {
        translate([bat_w/2+wall_w+clearance-7.1,bat_l/2+wall_w+clearance-7.1,bat_h+clearance+wall_h])
            rotate([0,0,45])
                cylinder(10,10,0,$fn=4);
        translate([bat_w/2+clearance-7.1,bat_l/2+clearance-7.1,bat_h+clearance+wall_h])
            rotate([0,0,45])
            cylinder(10,10,0,$fn=4);
        cylinder(30,r=pcb_d/2+clearance);
    }

    // Base to PCB Spacers
    pcb_mount(x=1,y=1,h=bot_h+clearance);
    pcb_mount(x=1,y=-1,h=bot_h+clearance);
    pcb_mount(x=-1,y=1,h=bot_h+clearance);
    pcb_mount(x=-1,y=-1,h=bot_h+clearance);
    
    translate([42.5,42,(bat_h+clearance)/2+wall_h])
    cube([8.5,wall_w,bat_h+clearance], true);
    translate([42.5,-42,(bat_h+clearance)/2+wall_h])
    cube([8.5,wall_w,bat_h+clearance], true);
    translate([-42.5,42,(bat_h+clearance)/2+wall_h])
    cube([8.5,wall_w,bat_h+clearance], true);
    translate([-42.5,-42,(bat_h+clearance)/2+wall_h])
    cube([8.5,wall_w,bat_h+clearance], true);
    
    // PCB to Cover Spacers
    if (false) {
        pcb_mount(1,1,top_h+clearance,f=bot_h+pcb_h+clearance);
        pcb_mount(1,-1,top_h+clearance,f=bot_h+pcb_h+clearance);
        pcb_mount(-1,1,top_h+clearance,f=bot_h+pcb_h+clearance);
        pcb_mount(-1,-1,top_h+clearance,f=bot_h+pcb_h+clearance);
    } else {
        //pcb_mount(0,0,top_h+clearance);
        //pcb_mount(1.15,-1,top_h+clearance);
        //pcb_mount(-1.15,1,top_h+clearance);
        //pcb_mount(-1.15,-1,top_h+clearance);
    }
}

module battery(w=bat_w,l=bat_l,h=bat_h) {
    color("yellow", 0.5)
    translate([0,0,h/2+wall_h+clearance/2])
    cube([w,l,h],center=true);
}

module pcb_mount(x,y,h,f=0) {
    translate([37*x,40.5*y,wall_h+f]) {
        difference() {
            cylinder(d=5,h=h);
            translate([0,0,-1]) cylinder(d=3.2,h=h+2);
        }
    }
}

module cover() {
  color("grey", 0.3)
    translate([0,0,max_h+wall_h+clearance*2])
    cylinder(r=pcb_d/2+clearance+wall_w,h=wall_h*2);
}

module base() {
  color("blue", 0.3)
    difference() {
        cylinder(r=pcb_d/2+     clearance+wall_w,h=wall_h);
    
        translate([100+wall_w+clearance,0,0])
            cube([100,100,40],center=true);
        translate([-100-wall_w-clearance,0,0])
            cube([100,100,40],center=true);
    }
}


// Inner Assembly Clearence Bounds
module electronics() {
    translate([0,0,wall_h+bot_h+clearance]) {
        difference() {
        union() {
            pcb();
            top();
            bottom();
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
    color("green",0.8)
    difference() {
        translate([0,0,wall_h+bot_h+clearance])
        cylinder(d=pcb_d, h=pcb_h);
        
        translate([100,0,0])
            cube([100,100,40],center=true);
        translate([-100,0,0])
            cube([100,100,40],center=true);
    
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