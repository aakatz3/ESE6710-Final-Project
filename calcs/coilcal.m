format long eng;
I1 = 0.8;   

lambda1 =4.86003e-006;% 4.73744e-006-3.14733e-009j;   % TX flux linkage
lambda2 =  2.11619e-006;%2.09506e-006-8.15369e-010j;   % RX flux linkage

L = real(lambda1 / I1);    
M = real(lambda2 / I1);

k = abs(M / L);

L,M,k
