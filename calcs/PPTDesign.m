%[text] # PPT Design
format long eng;
%%
VIN        = 20;       
Pout_total = 25;       
fs         = 6.78e6;    
Qs         = 1.8;       % resonantQ
k          = 0.2;       % L1 = k * L2
m          = 45;        % Cin design choice ; m= RL/(Cin1||Cin2);45 is the value calculated from the paper  
beta_CB    = 10;        % CB/C2

%half circuit
omega_s = 2*pi*fs;         
Pdc     = Pout_total/2;     
Veff    = 0.5*VIN;          

RL = 0.74 * (Veff^2) / Pdc;  
Rload_pp = 2*RL;             


L2 = 0.94 * RL / omega_s;           % L2a, L2b
C2 = 1 / (4 * omega_s^2 * L2);      % C2a, C2b
C1 = 0.61 / (omega_s * RL);         % C1a, C1b including coss

% output 
Ls = Qs * Rload_pp / omega_s;
Cs = 1 / (Qs * Rload_pp * omega_s);

%design choice
L1 = k * L2;        % L1a , L1b 

Cin_eq = m / (omega_s * RL);

%  n = Cin2 / Cin1
n_opt = 2*k-(k - 2) / (k + 2);

Cin1 = Cin_eq * (1 + n_opt) / n_opt;
Cin2 = Cin_eq * (1 + n_opt);

CB = beta_CB * C2;   

RL, L2, C2, C1, Ls, Cs, L1, Cin1, Cin2, CB %[output:1d486f05] %[output:23d7fa1e] %[output:9738310a] %[output:5a4caab9] %[output:7f683541] %[output:12572688] %[output:1edc8a9c] %[output:8354c02d] %[output:420984a4] %[output:4dc14740]


%[appendix]{"version":"1.0"}
%---
%[metadata:view]
%   data: {"layout":"inline"}
%---
%[output:1d486f05]
%   data: {"dataType":"textualVariable","outputData":{"name":"RL","value":"    5.92000000000000e+000\n"}}
%---
%[output:23d7fa1e]
%   data: {"dataType":"textualVariable","outputData":{"name":"L2","value":"    130.629119073419e-009\n"}}
%---
%[output:9738310a]
%   data: {"dataType":"textualVariable","outputData":{"name":"C2","value":"    1.05458329126989e-009\n"}}
%---
%[output:5a4caab9]
%   data: {"dataType":"textualVariable","outputData":{"name":"C1","value":"    2.41879223685662e-009\n"}}
%---
%[output:7f683541]
%   data: {"dataType":"textualVariable","outputData":{"name":"Ls","value":"    500.281732621604e-009\n"}}
%---
%[output:12572688]
%   data: {"dataType":"textualVariable","outputData":{"name":"Cs","value":"    1.10145365977077e-009\n"}}
%---
%[output:1edc8a9c]
%   data: {"dataType":"textualVariable","outputData":{"name":"L1","value":"    26.1258238146838e-009\n"}}
%---
%[output:8354c02d]
%   data: {"dataType":"textualVariable","outputData":{"name":"Cin1","value":"    324.912390025516e-009\n"}}
%---
%[output:420984a4]
%   data: {"dataType":"textualVariable","outputData":{"name":"Cin2","value":"    395.802366031083e-009\n"}}
%---
%[output:4dc14740]
%   data: {"dataType":"textualVariable","outputData":{"name":"CB","value":"    10.5458329126989e-009\n"}}
%---
