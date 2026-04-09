function H =  Persp(f)
% zwraca macierz jednorodna tranformacji rzutu perspektywicznego
% z uzyciem kamery o osi OZ i o ogniskowej f (konwencja jak na wykladzie) 
H = zeros(4,4);
H(1,1)=1; H(2,2)=1;
H(4,3)=-1/f; H(4,4)=1;
end