close all; clear; clc;

scriptDir = fileparts(mfilename("fullpath"));
epsDir = [scriptDir, '/eps/ads'];
mkdir(epsDir)

LW = 1;

%% ---------------- figure style ----------------
figW = 3.45;
figH = 2.25;



setYlimRule = @(ax,y) ylim(ax, [0.8*min(y) 1.2*max(y)]);


%% ---------------- Load MEAS data ----------------
ads = sparameters('data/rf_tank/ads.s2p');

freqsads = ads.Frequencies;
f=figure("Position",[100,100,600,600],Color='W');
plt = smithplot();
ax = f.CurrentAxes;
hold(ax,"on");
a=smithplot(ads,1,1);
% a.FontName = 'Roboto';
legend(ax,'off');
% fontname('Roboto');
a.ClipData = false;
a.FontSize = 10;
exportgraphics(ax,fullfile(epsDir, 's11.eps'),'ContentType','vector');

f=figure("Position",[100,100,400,400]);
ax=axes(f);

rfplot(ax,ads,2,1,"db");
xlim(ax,[1,10])
ylim(ax,[-80,10])
hold on
yyaxis right
rfplot(ax,ads,2,1,"angle")
ylabel('Phase (°)');
ylim([-225,135])
yticks(-360:45:180)
% applyStyle(ax);
legend(ax,'off');
yyaxis left;
% fontname('Roboto');
exportgraphics(ax,fullfile(epsDir, 's21.eps'),'ContentType','vector');

f=figure("Position",[100,100,400,400]);
ax=axes(f);
rfplot(ax,ads,1,2,"db");
xlim(ax,[1,10])
ylim(ax,[-80,10])
hold on
yyaxis right
rfplot(ax,ads,1,2,"angle")
ylabel('Phase (°)');
ylim([-225,135])
yticks(-360:45:180)
% applyStyle(ax);
legend(ax,'off');
yyaxis left;
% fontname('Roboto');
exportgraphics(ax,fullfile(epsDir, 's12.eps'),'ContentType','vector');

f=figure("Position",[100,100,600,600],Color='W');
plt = smithplot();
ax = f.CurrentAxes;
hold(ax,"on");
a=smithplot(ads,2,2);
a.ClipData = false;
a.FontSize = 10;
legend(ax,'off');
exportgraphics(ax,fullfile(epsDir, 's22.eps'),'ContentType','vector');

%% ---------------- Plot & export ----------------
% makeOneFig(f_MR,power_MR, ...
%     '$f\ (\mathrm{MHz})$', '$P_{MR}\ \mathrm{(dBm,\ relative)}$', ...
%     'fig_f_p_mr', LW, figW, figH, applyStyle, setYlimRule, outDir, legendLoc);


disp("EPS figures exported to the script folder successfully.");



function makeOneFig(x, y, xlab, ylab, fname, ...
                    LW, figW, figH, applyStyle, setYlimRule, outDir, legendLoc)

    fig = figure('Color','w','Units','inches','Position',[1 1 figW figH]);
    ax = axes(fig);
    hold(ax,'on');
    grid(ax,'on');

    h1 = plot(ax, x, y, '-', 'LineWidth', LW);
    % h2 = plot(ax, xm, ym, '-', 'LineWidth', LW);

    applyStyle(ax);
    % setYlimRule(ax, [ys(:); ym(:)]);

    xlabel(ax, xlab, 'Interpreter','latex', 'FontSize',9);
    ylabel(ax, ylab, 'Interpreter','latex', 'FontSize',9);

    % legend(ax, [h1 h2], {'Simulation','Measurement'}, ...
    %     'Interpreter','latex', ...
    %     'FontSize',8, ...
    %     'Box','off', ...
    %     'Location', legendLoc);
    
    exportgraphics(ax,fullfile(outDir, [fname, '.eps']))
    % set(fig,'Renderer','painters');
    % print(fig, fullfile(outDir, fname), '-depsc2', '-vector');
end

