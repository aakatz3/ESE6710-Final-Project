close all; clear; clc;

csvFile = "measurementsfrequency.csv";
simFile = "simfresweep.log.txt";

scriptDir = fileparts(mfilename('fullpath'));
outDir = [scriptDir, '/eps/freq'];
mkdir(outDir);

LW = 1.2;

%% ---------------- Load MEAS data ----------------
Tmeas = readtable(csvFile);
getcol = @(T,n) getColumnByNames(T,n);

fs_m   = getcol(Tmeas, ["FREQ"]) / 1e6;
Vout_m = getcol(Tmeas, ["V_OUT","Vout","VOUT"]);
Pout_m = getcol(Tmeas, ["P_OUT","Pout","POUT"]);
Vds_m  = getcol(Tmeas, ["V_DS_A_max","vdsmax","V_DS"]);
Pin_m  = getcol(Tmeas, ["P_IN","Pin","PIN"]);

eff_m  = (Pout_m ./ Pin_m) * 100;

%% ---------------- Load SIM data ----------------
opts = detectImportOptions(simFile,"FileType","text");
opts.Delimiter = '\t';
opts.ConsecutiveDelimitersRule = "join";
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";
Tsim = readtable(simFile, opts);

fs_s   = getcol(Tsim, ["fstest"]) / 1e6;
Vout_s = getcol(Tsim, ["vout","Vout"]);
Pout_s = getcol(Tsim, ["poutavg","Pout"]);
Vds_s  = getcol(Tsim, ["vds1max","Vdsmax"]);
Pin_s  = abs(getcol(Tsim, ["pinavg","Pin"]));

eff_s  = (Pout_s ./ Pin_s) * 100;

%% ---------------- Sort by fs ----------------
[fs_m, im] = sort(fs_m);
Vout_m = Vout_m(im); Pout_m = Pout_m(im);
eff_m  = eff_m(im);  Vds_m  = Vds_m(im);

[fs_s, is] = sort(fs_s);
Vout_s = Vout_s(is); Pout_s = Pout_s(is);
eff_s  = eff_s(is);  Vds_s  = Vds_s(is);

%% ---------------- X-axis range (fixed: 6.25–7 MHz) ----------------
xmin = 6.7e6;
xmax = 6.9e6;

%% ---------------- figure style ----------------
figW = 3.45;
figH = 2.25;

applyStyle = @(ax) set(ax, ...
    'Box','on', ...
    'LineWidth',0.75, ...
    'FontName','Times New Roman', ...
    'FontSize',8.5, ...
    'XLim',[xmin xmax], ...
    'TickDir','out', ...
    'TickLength',[0.018 0.018], ...
    'Layer','top', ...
    'TickLabelInterpreter','latex');

setYlimRule = @(ax,y) ylim(ax, [0.8*min(y) 1.2*max(y)]);

legendLoc = 'northwest';

xlab = 'f_s (MHz)';

%% ---------------- Plot & export ----------------
makeOneFig(fs_s,Vout_s,fs_m,Vout_m, ...
    xlab, 'V_{out} (V)',...
    'fig_fs_Vout', LW, figW, figH, applyStyle, setYlimRule, outDir, legendLoc);

makeOneFig(fs_s,Pout_s,fs_m,Pout_m, ...
    xlab, 'P_{out} (W)', ...
    'fig_fs_Pout', LW, figW, figH, applyStyle, setYlimRule, outDir, legendLoc);

makeOneFig(fs_s,eff_s,fs_m,eff_m, ...
    xlab, '\eta (%)', ...
    'fig_fs_Eff', LW, figW, figH, applyStyle, setYlimRule, outDir, legendLoc);

makeOneFig(fs_s,Vds_s,fs_m,Vds_m, ...
    xlab,  'V_{ds,max} (V)', ...
    'fig_fs_Vdsmax', LW, figW, figH, applyStyle, setYlimRule, outDir, legendLoc);

disp("EPS figures exported to the script folder successfully.");

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

function makeOneFig(xs, ys, xm, ym, xlab, ylab, fname, ...
                    LW, figW, figH, applyStyle, setYlimRule, outDir, legendLoc)

    fig = figure('Units','inches','Position',[1 1 figW figH]);
    ax = axes(fig, 'Box','on');
    hold(ax,'on');
    grid(ax,'on');
    
    xmin = min([xm]);
    xmax = max([xm]);

    xlim(ax,[xmin,xmax]);

    h1 = plot(ax, xs, ys, '-',  'LineWidth', LW);
    h2 = plot(ax, xm, ym, '-',  'LineWidth', LW);

    % applyStyle(ax);
    setYlimRule(ax, [ys(:); ym(:)]);

    xlabel(ax, xlab);%, 'Interpreter','latex', 'FontSize',9);
    ylabel(ax, ylab);%, 'Interpreter','latex', 'FontSize',9);

    legend(ax, [h1 h2], {'Simulation','Measurement'}, ...
        ...'Interpreter','latex', ...
        'FontSize',8, ...
        'Box','off', ...
        'Location', legendLoc);
    
    
    exportgraphics(ax,fullfile(outDir, [fname, '.eps']));

end
