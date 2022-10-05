

clear all
close all
clc

s = serialport("COM5", 115200);

n = 15000; % with 250Hz -
counter = 1;

mx = zeros(0, n);
my = zeros(0, n);
mz = zeros(0, n);


flush(s)
while(1)
    if s.NumBytesAvailable > 0
        data = strsplit(readline(s),' ');
        mx(counter) = data(7);
        my(counter) = data(8);
        mz(counter) = data(9);
        
        fprintf("%d %d %d %d\n",counter, mx(counter), my(counter), mz(counter))
        counter = counter + 1;
    end
    if counter == n
        break;
    end
end

clear s; % Dirty way uzavření portu

width = max([mx my mz])+5;
osax = [-width 0 0; width 0 0];
osay = [0 -width 0; 0 width 0];
osaz = [0 0 -width; 0 0 width];

figure(1)
plot3(mx, my, mz, '*', osax, osay, osaz, 'k')
axis equal
grid on
xlabel('X');
ylabel('Y');
zlabel('Z');
title('Magnetometer 3D data')

figure(2)
set(gcf, 'Position', [10 10 1550 400])
subplot(1,3,1)
plot(mx,my,'*r', osax,osay,'k') % XY projection
axis equal
grid on
xlabel('X')
ylabel('Y')
title('XY projection')

subplot(1,3,2) 
plot(mx,mz,'*g', osax,osay,'k') % XZ projection
axis equal
grid on
xlabel('X')
ylabel('Z')
title('XZ projection')

subplot(1,3,3)
plot(my,mz,'*b', osax,osay,'k') % YZ projection
axis equal
grid on
xlabel('Y')
ylabel('Z')
title('YZ projection')

% Návrh offsetů:
x_offset = (max(mx)+min(mx))/2; 
y_offset = (max(my)+min(my))/2; 
z_offset = (max(mz)+min(mz))/2; 

% Zjištění "kulatosti" - jestli se jedná o hard iron nebo soft iron trouble
% měla by to být koule, protože v okolí magnetometru nemám žadný soft iron
xr = abs(max(mx)-min(mx))/2; 
yr = abs(max(my)-min(my))/2; 
zr = abs(max(mz)-min(mz))/2; 
r = (xr+yr+zr)/3;

fprintf("\nPrůměr: %.1f; x: %.1f, y: %.1f, z: %.1f\n", r, xr, yr, zr);
fprintf("Odchylky: x: %.2f, y: %.2f, z: %.2f\n", xr/r*100-100,yr/r*100-100,zr/r*100-100);

mx_o = mx-x_offset;
my_o = my-y_offset;
mz_o = mz-z_offset;

fprintf("\nOffsety: x: %.1f, y: %.1f, z: %.1f\n", x_offset, y_offset, z_offset);


% Vy kreslení po offsetu:

figure(3)
plot3(mx_o, my_o, mz_o, '*', osax, osay, osaz, 'k')
axis equal
grid on
xlabel('X');
ylabel('Y');
zlabel('Z');
title('Magnetometer 3D data')

figure(4) 
set(gcf, 'Position', [10 10 1550 400])
subplot(1,3,1)
plot(mx_o,my_o,'*r', osax,osay,'k') % XY projection
axis equal
grid on
xlabel('X')
ylabel('Y')
title('XY projection')

subplot(1,3,2) 
plot(mx_o,mz_o,'*g', osax,osay,'k') % XZ projection
axis equal
grid on
xlabel('X')
ylabel('Z')
title('XZ projection')

subplot(1,3,3)
plot(my_o,mz_o,'*b', osax,osay,'k') % YZ projection
axis equal
grid on
xlabel('Y')
ylabel('Z')
title('YZ projection')

figure(5) % Jeden graf i s kružnicí
t = 0:pi/50:2*pi;
xx = sin(t)*r;
yy = cos(t)*r;
plot(osax, osay, 'k', mx_o, my_o, '*r', mx_o, mz_o, '*g', my_o, mz_o, '*b', xx, yy, '--k');
title("All projections comparison with ideal circle (sphere)");
grid on;
axis equal;






