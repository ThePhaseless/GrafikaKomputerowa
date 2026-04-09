function Im2 =  linia1(Im1,yp,xp,yk,xk,C)
% na monochromatycznym obrazie kresli linie o jasnosci C  
% od punktu (yp,xp) do punktu (yk, xk)
[Y, X] = size(Im1);
Im2 = Im1;

if (abs(yk-yp) > abs(xk-xp))          % stroma linia                                
    x0 = yp;y0 = xp; x1 = yk;y1 = xk; % zamiana wspolrzednych 
    zamiana =1;                                             
else
    x0 = xp;y0 = yp; x1 = xk;y1 = yk;
    zamiana = 0; 
end
if zamiana==1 temp=X; X=Y; Y=temp; end % zamiana rozmiarow X i Y
if(x0 >x1) % zamiana poczatku i konca linii, zeby zaczynac od lewej
    temp1 = x0; x0 = x1; x1 = temp1;
    temp2 = y0; y0 = y1; y1 = temp2;
end
dx = abs(x1 - x0) ;                % odleglosc x
dy = abs(y1 - y0);                 % odleglosc y
sy = sign(y1 - y0);                % znak przyrostu w kierunku y
x = x0; y = y0;                    % inicjalizacja
if x>0 && x<=X && y>0 && y<=Y  
if (zamiana ==0)                                
        Im2(y,x) = C;               % rysowanie punktu
else 
        Im2(x,y) = C;
end
end
error = 2*dy - dx ;                              % inicjalizacja bledu
for i = 0:dx-1                                   
    error = error + 2*dy;                        % modyfikacja bledu
    if (error >0)                                
        y = y +sy;                             
        error = error - 2*dx;                      
    end
    x = x + 1;                                % zwiekszamy x
  if x>0 && x<=X && y>0 && y<=Y  
    if (zamiana ==0)                                
        Im2(y,x) = C;                % rysowanie punktu
    else                                         
        Im2(x,y) = C;
    end
  end
end
end
