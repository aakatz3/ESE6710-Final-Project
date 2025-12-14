format long eng;
I1 = 0.8;   

lambda1 = 4.73744e-6 - 1j*3.14733e-9;   % TX flux linkage
lambda2 = 2.09506e-6 - 1j*8.15369e-10;   % RX flux linkage

L = real(lambda1 / I1);    
M = real(lambda2 / I1);

k = abs(M / L);

L,M,k