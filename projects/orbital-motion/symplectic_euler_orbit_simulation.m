%Hamiltonian Motion
g = 9.67*10^(-11);
M = 5.972*10^24;
m = 5;
x0 =[0;160000];
p0 =[200000;200000];
T = 40;
Tao = 0.0001;
step = floor(T/Tao);

% arrays
x(:,1) = x0;
p(:,1) = p0;
Ha(1) = 0;
%funktions
dx = @(p) p/m;
dp = @(x) -g*(m*M)./(norm(x).^3).*x;
H = @(p,x) (norm(p)^2)/(2*m)-g*m*M/(norm(x));

%loop symplectic Euler
for k=1:step
    p(:,k+1) = p(:,k) + Tao*(dp(x(:,k)));
    x(:,k+1) = x(:,k) + Tao*(dx(p(:,k+1)));
    Ha(k+1) = H(p(:,k),x(:,k));
end


%time
T=0:Tao:T;

%plot
close all;
pbaspect([1 1 1]);
plot(x(1,:),x(2,:));
hold on;
figure;
plot(T,Ha);
