%[text] Setup
addpath('C:\femm42\mfiles');
openfemm(1);
% showconsole;
file = 'coils_v1_fixed';
circuits = {'TX', 'RX'};
freqs = [0, 6.78e6];
%%
%[text] open document
opendocument([file, '.FEM']);
if not(exist([file, '.ans'], 'file'))
    mi_analyze()
end
opendocument([file, '.ans']);
%%
%[text] Do analysis for both frequencies
%[text] Get circuit info
circuit_results = [];
for freq = freqs
    % Unit is known, make sure this matches
    mi_probdef(freq, 'millimeters', 'axi', 1e-12, 0.001, 30, 0);
    
    mi_purgemesh();
    mi_createmesh();
    mi_analyze(1);
    mo_reload();
    
    for circuit = circuits
        circuit = cell2mat(circuit);
        result = num2cell(mo_getcircuitproperties(circuit));
        [current, voltage, flux] = result{:};
        if current == 0
            inductance = '--';
            impedance = '--';
        else
            inductance = round((flux / current), 4, "significant");
            impedance = round((voltage / current), 4, "significant");
            current = round(current, 4);
        end
        power = voltage * current;
        voltage = round(voltage, 4, "significant");
        flux = round(flux, 4, "significant");
        power = round(power, 4, "significant");
        
        circuit_results = [circuit_results, 
            struct('circuit', circuit, ...
                'frequency',freq, ...
                'current', current, ...
                'voltage', voltage, ...
                'flux', flux, ...
                'inductance', inductance, ...
                'impedance', impedance, ...
                'power', power ...
            )];
    end
end
circuit_results = struct2table(circuit_results) %[output:40c5569d]
writetable(circuit_results, [file, '.csv'])
%%
%[text] Exit FEMM
closefemm;

%[appendix]{"version":"1.0"}
%---
%[metadata:view]
%   data: {"layout":"onright"}
%---
%[output:40c5569d]
%   data: {"dataType":"tabular","outputData":{"columnNames":["circuit","frequency","current","voltage","flux","inductance","impedance","power"],"columns":8,"dataTypes":["cellstr","double","double","double","double","cell","cell","double"],"header":"4×8 table","name":"circuit_results","rows":4,"type":"table","value":[["'TX'","0","0.8000","0.0117 + 0.0000i","2.8530e-06 + 0.0000e+00i","3.5660e-06","0.0146","0.0094 + 0.0000i"],["'RX'","0","0","0.0000 + 0.0000i","1.1190e-06 + 0.0000e+00i","'--'","'--'","0.0000 + 0.0000i"],["'TX'","6780000","0.8000","2.7820e-01 + 1.1840e+02i","2.7790e-06 - 1.7430e-09i","3.4740e-06 - 2.1790e-09i","3.4780e-01 + 1.4800e+02i","0.2226 +94.7100i"],["'RX'","6780000","0","0.0109 +47.3700i","1.1120e-06 - 2.5570e-10i","'--'","'--'","0.0000 + 0.0000i"]]}}
%---
