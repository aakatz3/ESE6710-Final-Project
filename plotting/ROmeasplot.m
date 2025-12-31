clear; clc;

csvFile = "measurementsROUT.csv";
simFile = "simRosweep.log.txt";

scriptDir = fileparts(mfilename('fullpath'));   % script folder
outDir = scriptDir;

LW = 1.2;

%% ---------------- Load MEAS data ----------------
Tmeas = readtable(csvFile);
getcol = @(T,n) getColumnByNames(T,n);

Ro_m   = getcol(Tmeas, ["ROUT"]);
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

Ro_s   = getcol(Tsim, ["ro"]);
Vout_s = getcol(Tsim, ["vout","Vout"]);
Pout_s = getcol(Tsim, ["poutavg","Pout"]);
Vds_s  = getcol(Tsim, ["vds1max","Vdsmax"]);
Pin_s  = abs(getcol(Tsim, ["pinavg","Pin"]));

eff_s  = (Pout_s ./ Pin_s) * 100;

%% ---------------- Sort by R_o ----------------
[Ro_m, im] = sort(Ro_m);
Vout_m = Vout_m(im); Pout_m = Pout_m(im);
eff_m  = eff_m(im);  Vds_m  = Vds_m(im);

[Ro_s, is] = sort(Ro_s);
Vout_s = Vout_s(is); Pout_s = Pout_s(is);
eff_s  = eff_s(is);  Vds_s  = Vds_s(is);

xmin = min([Ro_m; Ro_s]);
xmax = max([Ro_m; Ro_s]);

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

setYlimRule = @(ax,y) ylim(ax, [0.92*min(y) 1.08*max(y)]);

legendLoc = 'northwest';

%% ---------------- Plot & export ----------------
makeOneFig(Ro_s,Vout_s,Ro_m,Vout_m, ...
    '$R_o\ (\Omega)$', '$V_{\mathrm{out}}\ \mathrm{(V)}$', ...
    'fig_Ro_Vout', LW, figW, figH, applyStyle, setYlimRule, outDir, legendLoc);

makeOneFig(Ro_s,Pout_s,Ro_m,Pout_m, ...
    '$R_o\ (\Omega)$', '$P_{\mathrm{out}}\ \mathrm{(W)}$', ...
    'fig_Ro_Pout', LW, figW, figH, applyStyle, setYlimRule, outDir, legendLoc);

makeOneFig(Ro_s,eff_s,Ro_m,eff_m, ...
    '$R_o\ (\Omega)$', '$\eta\ \mathrm{(\%)}$', ...
    'fig_Ro_Eff', LW, figW, figH, applyStyle, setYlimRule, outDir, legendLoc);

makeOneFig(Ro_s,Vds_s,Ro_m,Vds_m, ...
    '$R_o\ (\Omega)$', '$V_{\mathrm{ds,max}}\ \mathrm{(V)}$', ...
    'fig_Ro_Vdsmax', LW, figW, figH, applyStyle, setYlimRule, outDir, legendLoc);

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

    fig = figure('Color','w','Units','inches','Position',[1 1 figW figH]);
    ax = axes(fig);
    hold(ax,'on');
    grid(ax,'off');

    h1 = plot(ax, xs, ys, '-',  'LineWidth', LW);
    h2 = plot(ax, xm, ym, '-',  'LineWidth', LW);

    applyStyle(ax);
    setYlimRule(ax, [ys(:); ym(:)]);

    xlabel(ax, xlab, 'Interpreter','latex', 'FontSize',9);
    ylabel(ax, ylab, 'Interpreter','latex', 'FontSize',9);

    legend(ax, [h1 h2], {'Simulation','Measurement'}, ...
        'Interpreter','latex', ...
        'FontSize',8, ...
        'Box','off', ...
        'Location', legendLoc);

    set(fig,'Renderer','painters');
    print(fig, fullfile(outDir, fname), '-depsc2', '-painters');

end

