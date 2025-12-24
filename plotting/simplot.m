clear; clc;

% -------- paths --------
scriptDir = fileparts(mfilename("fullpath"));
fAll = fullfile(scriptDir, "simdata.log.txt");

% -------- global style --------
S.figW = 3.50;  
S.figH = 1.15; 
S.fs   = 8;
S.lw   = 1.0;
S.font = "Times New Roman";
S.tScale = 1;
S.tUnit  = "s";
S.tLabel = "Time (" + S.tUnit + ")";

% -------- colors --------
C.vds1 = [0.3010 0.7450 0.9330];
C.vds2 = [0.4660 0.6740 0.1880];
C.vg1  = [0.8500 0.3250 0.0980];
C.vg2  = [0.9290 0.6940 0.1250];
C.Vs   = [0.0000 0.4470 0.7410];
C.Is   = [0.8500 0.3250 0.0980];
C.Vr   = [0.4940 0.1840 0.5560];
C.Ir   = [0.6350 0.0780 0.1840];


opts = detectImportOptions(fAll, "FileType","text");
opts.VariableNamingRule = "preserve";
T = readtable(fAll, opts);

% -------- extract waveforms --------
t    = T.("time") * S.tScale;

vg1  = T.("V(gbottom)");
vg2  = T.("V(gtop)");
vds1 = T.("V(n_bot_mid)");
vds2 = T.("V(n_top_mid)");

Vs   = T.("V(n_top_mid)-V(n_bot_mid)");
Is   = T.("I(Lspri)");

Vr   = T.("V(sec_r)-V(sec_bot)");  
Ir   = T.("I(Cssec)");              

% -------- time range --------
m = isfinite(t) & isfinite(vg1) & isfinite(vg2) & isfinite(vds1) & isfinite(vds2) & ...
    isfinite(Vs) & isfinite(Is) & isfinite(Vr) & isfinite(Ir);

t = t(m);
vg1 = vg1(m); vg2 = vg2(m); vds1 = vds1(m); vds2 = vds2(m);
Vs = Vs(m); Is = Is(m); Vr = Vr(m); Ir = Ir(m);

xLim = [min(t) max(t)];

%% ===================== FIG (a): 4 voltages =====================
[fig, ax] = newFig(S);
plot(ax, t, vds1, "LineWidth", S.lw, "Color", C.vds1); hold(ax,"on");
plot(ax, t, vds2, "LineWidth", S.lw, "Color", C.vds2);
plot(ax, t, vg1,  "LineWidth", S.lw, "Color", C.vg1 );
plot(ax, t, vg2,  "LineWidth", S.lw, "Color", C.vg2 );
xlabel(ax, S.tLabel);
ylabel(ax, "Voltage (V)");
styleAxes(ax, S, xLim);
padY(ax, [vds1; vds2; vg1; vg2], 0.1);
tightLegend(ax, {'$v_{ds1}$','$v_{ds2}$','$v_{g1}$','$v_{g2}$'});
saveEps(fig, fullfile(scriptDir, "Fig_a_voltages.eps"));

%% ===================== FIG (b): Vs =====================
[fig, ax] = newFig(S);
plot(ax, t, Vs, "LineWidth", S.lw, "Color", C.Vs);
xlabel(ax, S.tLabel);
ylabel(ax, '$V_s\,(\mathrm{V})$', 'Interpreter','latex');
styleAxes(ax, S, xLim);
padY(ax, Vs, 0.1);
tightLegend(ax, {'$V_s$'});
saveEps(fig, fullfile(scriptDir, "Fig_b_Vs.eps"));

%% ===================== FIG (c): Is =====================
[fig, ax] = newFig(S);
plot(ax, t, Is, "LineWidth", S.lw, "Color", C.Is);
xlabel(ax, S.tLabel);
ylabel(ax, '$I_s\,(\mathrm{A})$', 'Interpreter','latex');
styleAxes(ax, S, xLim);
padY(ax, Is, 0.1);
tightLegend(ax, {'$I_s$'});
saveEps(fig, fullfile(scriptDir, "Fig_c_Is.eps"));

%% ===================== FIG (d): Vr =====================
[fig, ax] = newFig(S);
plot(ax, t, Vr, "LineWidth", S.lw, "Color", C.Vr);
xlabel(ax, S.tLabel);
ylabel(ax, '$V_r\,(\mathrm{V})$', 'Interpreter','latex');
styleAxes(ax, S, xLim);
padY(ax, Vr, 0.1);
tightLegend(ax, {'$V_r$'});
saveEps(fig, fullfile(scriptDir, "Fig_d_Vr.eps"));

%% ===================== FIG (e): Ir =====================
[fig, ax] = newFig(S);
plot(ax, t, Ir, "LineWidth", S.lw, "Color", C.Ir);
xlabel(ax, S.tLabel);
ylabel(ax, '$I_r\,(\mathrm{A})$', 'Interpreter','latex');
styleAxes(ax, S, xLim);
padY(ax, Ir, 0.1);
tightLegend(ax, {'$I_r$'});
saveEps(fig, fullfile(scriptDir, "Fig_e_Ir.eps"));

disp("✓ Saved EPS: Fig_a_voltages / Fig_b_Vs / Fig_c_Is / Fig_d_Vr / Fig_e_Ir");

%% ===================== local helper functions =====================
function [fig, ax] = newFig(S)
    fig = figure("Units","inches","Position",[1 1 S.figW S.figH], ...
                 "Color","w","Renderer","painters");
    ax = axes(fig);
    grid(ax,"on"); box(ax,"on"); hold(ax,"off");
end

function styleAxes(ax, S, xLim)
    set(ax, "FontName",S.font, "FontSize",S.fs, "LineWidth",0.75, ...
            "TickDir","in", "Box","on");
    xlim(ax, xLim);
end

function tightLegend(ax, labels)
    lgd = legend(ax, labels, ...
        "Location","northeast", ...
        "Box","on", ...
        "Interpreter","latex", ...
        "FontSize",6);
    lgd.Color = "white";
    lgd.EdgeColor = "black";
    lgd.Units = "normalized";
    pos = lgd.Position;
    pos(1) = 0.99 - pos(3);   
    pos(2) = 0.98 - pos(4);   
    lgd.Position = pos;
end

function padY(ax, y, ratio)
    y = y(isfinite(y));
    if isempty(y)
        return;
    end
    ymin = min(y);
    ymax = max(y);
    if ymin == ymax
        dy = max(abs(ymin),1);
    else
        dy = ymax - ymin;
    end
    pad = ratio * dy;
    ylim(ax, [ymin - pad, ymax + pad]);
end

function saveEps(fig, outPath)
    print(fig, outPath, "-depsc2", "-painters");
end



