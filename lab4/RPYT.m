function Hmat =  RPYT(roll,pitch,yaw,px,py,pz)
r = roll*pi/180; p = pitch*pi/180; y = yaw*pi/180;
MR = [cos(r), -sin(r), 0; 
      sin(r), cos(r), 0; 
      0, 0, 1];
MP = [cos(p), 0, sin(p); 
      0, 1, 0; 
      -sin(p), 0, cos(p)];
MY = [1, 0, 0;
      0, cos(y), -sin(y); 
      0, sin(y), cos(y)];
Rot = MY*MP*MR;
Hmat = zeros(4,4);
Hmat(1:3,1:3)=Rot;
Hmat(1,4)=px; Hmat(2,4)=py; Hmat(3,4)=pz;
Hmat(4,4)=1;
end


