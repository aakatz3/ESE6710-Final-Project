clear; clc;

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


S.YLabelX        = -0.085;  % All ylabels share the same X position 
S.xLabelYOffset  = -0.3;   % move xlabel

S.legendDy = -0.26;          % legend position(+) closer to axes, (-) farther away

% -------- colors --------
C.vds1 = [0.3010 0.7450 0.9330];
C.vds2 = [0.4660 0.6740 0.1880];
C.vg1  = [0.8500 0.3250 0.0980];
C.vg2  = [0.9290 0.6940 0.1250];
C.Vs   = [0.0000 0.4470 0.7410];
C.Is   = [0.8500 0.3250 0.0980];
C.Vr   = [0.4940 0.1840 0.5560];
C.Ir   = [0.6350 0.0780 0.1840];

% -------- read log --------
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

m = isfinite(t) & isfinite(vg1) & isfinite(vg2) & isfinite(vds1) & isfinite(vds2) & ...
    isfinite(Vs) & isfinite(Is) & isfinite(Vr) & isfinite(Ir);

t = t(m);
vg1 = vg1(m); vg2 = vg2(m); vds1 = vds1(m); vds2 = vds2(m);
Vs = Vs(m); Is = Is(m); Vr = Vr(m); Ir = Ir(m);

xLim = [min(t) max(t)];

%% ===================== FIG (a)voltages =====================
[figA, axA] = newFig(S);
plot(axA, t, vds1, "LineWidth", S.lw, "Color", C.vds1); hold(axA,"on");
plot(axA, t, vds2, "LineWidth", S.lw, "Color", C.vds2);
plot(axA, t, vg1,  "LineWidth", S.lw, "Color", C.vg1 );
plot(axA, t, vg2,  "LineWidth", S.lw, "Color", C.vg2 );
ylabel(axA, "Voltage (V)");
styleAxes(axA, S, xLim);
padY(axA, [vds1; vds2; vg1; vg2], 0.1);
tightLegend(axA, {'$v_{ds1}$','$v_{ds2}$','$v_{g1}$','$v_{g2}$'}, S.legendDy); % <-- legend gap
saveEps(figA, fullfile(scriptDir, "Fig_a_voltages.eps"));

%% ===================== FIG (b): Vs =====================
[figB, axB] = newFig(S);
plot(axB, t, Vs, "LineWidth", S.lw, "Color", C.Vs);
ylabel(axB, '$V_s\,(\mathrm{V})$', 'Interpreter','latex');
styleAxes(axB, S, xLim);
padY(axB, Vs, 0.1);
tightLegend(axB, {'$V_s$'}, S.legendDy); % <-- legend gap
saveEps(figB, fullfile(scriptDir, "Fig_b_Vs.eps"));

%% ===================== FIG (c): Is =====================
[figC, axC] = newFig(S);
plot(axC, t, Is, "LineWidth", S.lw, "Color", C.Is);
ylabel(axC, '$I_s\,(\mathrm{A})$', 'Interpreter','latex');
styleAxes(axC, S, xLim);
padY(axC, Is, 0.1);
tightLegend(axC, {'$I_s$'}, S.legendDy); % <-- legend gap
saveEps(figC, fullfile(scriptDir, "Fig_c_Is.eps"));

%% ===================== FIG (d): Vr =====================
[figD, axD] = newFig(S);
plot(axD, t, Vr, "LineWidth", S.lw, "Color", C.Vr);
ylabel(axD, '$V_r\,(\mathrm{V})$', 'Interpreter','latex');
styleAxes(axD, S, xLim);
padY(axD, Vr, 0.1);
tightLegend(axD, {'$V_r$'}, S.legendDy); % <-- legend gap
saveEps(figD, fullfile(scriptDir, "Fig_d_Vr.eps"));

%% ===================== FIG (e): Ir =====================
S.legendDy = -0.12; 
[figE, axE] = newFig(S);
plot(axE, t, Ir, "LineWidth", S.lw, "Color", C.Ir);
xlabel(axE, S.tLabel);
ylabel(axE, '$I_r\,(\mathrm{A})$', 'Interpreter','latex');
styleAxes(axE, S, xLim);
padY(axE, Ir, 0.1);
tightLegend(axE, {'$I_r$'}, S.legendDy); 
axPos = axE.Position;
axPos(2) = axPos(2) + 0.16;   
axPos(4) = axPos(4) - 0.16;   
axE.Position = axPos;
xl = axE.XLabel;
xl.Units = "normalized";
pos = xl.Position;
pos(2) = pos(2) + S.xLabelYOffset;
xl.Position = pos;

saveEps(figE, fullfile(scriptDir, "Fig_e_Ir.eps"));

%% ===================== ylabel alignment =====================
allAxes = [axA, axB, axC, axD, axE];
for ax = allAxes
    yl = ax.YLabel;
    yl.Units = "normalized";
    p = yl.Position;
    p(1) = S.YLabelX;        
    yl.Position = p;
end

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

function tightLegend(ax, labels, dy)
    if nargin < 3, dy = 0; end

    lgd = legend(ax, labels, ...
        "Location","southoutside", ...
        "Orientation","horizontal", ...
        "Interpreter","latex", ...
        "FontSize",8);

    lgd.Box = "off";
    lgd.ItemTokenSize = [15 8];

    lgd.Units = "normalized";
    pos = lgd.Position;
    pos(2) = pos(2) + dy;   
    lgd.Position = pos;
end

function padY(ax, y, ratio)
    y = y(isfinite(y));
    if isempty(y), return; end
    ymin = min(y); ymax = max(y);
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
