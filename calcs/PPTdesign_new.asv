%[text] New Calculation
format long eng;

VIN        = 25;
fs         = 6.78e6;
Coss = 300e-12;
m     = 5;         % L1 = m*L2   
k     = 0.3;       % coil coupling coefficient
omega_s   = 2*pi*fs;

% loads
Rload_tot = 50;
RL_phase  = Rload_tot/2;

% component value calculation 
LMR       = 0.94 * RL_phase / omega_s;
CMR       = 1 / (4 * omega_s^2 * LMR);
TwoCMR = 2*CMR;
Cp_total = 0.61 / (omega_s * RL_phase);
Cpext    = Cp_total - Coss;

LF  = m * LMR;

Ls2 = Rload_tot/(k*omega_s);
Cs2 = 1/((omega_s^2)*Ls2);
HalfCS2 = Cs2 / 2;

RL_phase, Rload_tot, LMR, CMR, TwoCMR, Cp_total, Cpext, LF, Ls2, Cs2, HalfCS2 %[output:1d93e6e0] %[output:48341e1a] %[output:657f6a49] %[output:1406963f] %[output:25e4598c] %[output:0558a9d8] %[output:618b75d6] %[output:81803653] %[output:89052846] %[output:32223de2] %[output:2327e0c5]

%[appendix]{"version":"1.0"}
%---
%[metadata:view]
%   data: {"layout":"inline"}
%---
%[output:1d93e6e0]
%   data: {"dataType":"textualVariable","outputData":{"name":"RL_phase","value":"    25.0000000000000e+000\n"}}
%---
%[output:48341e1a]
%   data: {"dataType":"textualVariable","outputData":{"name":"Rload_tot","value":"    50.0000000000000e+000\n"}}
%---
%[output:657f6a49]
%   data: {"dataType":"textualVariable","outputData":{"name":"LMR","value":"    551.643239330316e-009\n"}}
%---
%[output:1406963f]
%   data: {"dataType":"textualVariable","outputData":{"name":"CMR","value":"    249.725323372710e-012\n"}}
%---
%[output:25e4598c]
%   data: {"dataType":"textualVariable","outputData":{"name":"TwoCMR","value":"    499.450646745419e-012\n"}}
%---
%[output:0558a9d8]
%   data: {"dataType":"textualVariable","outputData":{"name":"Cp_total","value":"    572.770001687647e-012\n"}}
%---
%[output:618b75d6]
%   data: {"dataType":"textualVariable","outputData":{"name":"Cpext","value":"    272.770001687647e-012\n"}}
%---
%[output:81803653]
%   data: {"dataType":"textualVariable","outputData":{"name":"LF","value":"    2.75821619665158e-006\n"}}
%---
%[output:89052846]
%   data: {"dataType":"textualVariable","outputData":{"name":"Ls2","value":"    3.91236339950579e-006\n"}}
%---
%[output:32223de2]
%   data: {"dataType":"textualVariable","outputData":{"name":"Cs2","value":"    140.845082382208e-012\n"}}
%---
%[output:2327e0c5]
%   data: {"dataType":"textualVariable","outputData":{"name":"HalfCS2","value":"    70.4225411911041e-012\n"}}
%---
