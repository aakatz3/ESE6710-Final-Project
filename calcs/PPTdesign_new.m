format long eng;

VIN        = 25;
fs         = 6.78e6;
Coss = 280e-12;
m     = 5;         % L1 = m*L2   
k     = 0.3;       % coil coupling coefficient
omega_s   = 2*pi*fs;

% loads
Rload_tot = 50;
RL_phase  = Rload_tot/2;

% component value calculation 
LMR       = 0.94 * RL_phase / omega_s;
CMR       = 1 / (4 * omega_s^2 * LMR);
Cp_total = 0.61 / (omega_s * RL_phase);
Cpext    = Cp_total - Coss;

LF  = m * LMR;

Ls2 = Rload_tot/(k*omega_s);
Cs2 = 1/((omega_s^2)*Ls2);

RL_phase, Rload_tot, LMR, CMR, Cp_total, Cpext, LF, Ls2, Cs2
