% "Hacked" together from Yiyu's plot scripts
csvFiles = {"measurementsfrequency.csv", "measurementsduty.csv", "measurementsROUT.csv", "measurementsvin.csv"};

Pout_m = [];
Pin_m = [];

%% ---------------- Load MEAS data ----------------
for csvFile = csvFiles
    Tmeas = readtable(csvFile{1});
    
    
    Pout_m = [Pout_m; getColumnByNames(Tmeas, ["P_OUT","Pout","POUT"])];
    Pin_m  = [Pin_m; getColumnByNames(Tmeas, ["P_IN","Pin","PIN"])];
    
    

end
clear Tmeas
eff_m  = (Pout_m ./ Pin_m) * 100;

% extract nominal condition
T_freq = readtable(csvFiles{1});
lookup = T_freq.FREQ == 6.78e6;
T_freq.EFF = T_freq.P_OUT ./ T_freq.P_IN * 100;

Pout_nom = T_freq.P_OUT(lookup)
Pout_min = min(Pout_m)
Pout_max = max(Pout_m)
eff_nom = T_freq.EFF(lookup)
eff_min = min(eff_m)
eff_max = max(eff_m)


%% =========================================================
function x = getColumnByNames(T, names)
    vars = string(T.Properties.VariableNames);
    hit = "";
    for k = 1:numel(names)
        idx = find(strcmpi(vars, string(names(k))), 1);
        if ~isempty(idx)
            hit = vars(idx);
            break;
        end
    end
    if hit == ""
        error("Cannot find column: %s | Available: %s", ...
              strjoin(names,", "), strjoin(vars,", "));
    end
    x = double(T.(hit));
end
