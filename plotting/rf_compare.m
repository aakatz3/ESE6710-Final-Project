scriptDir = fileparts(mfilename("fullpath"));
epsDir = [scriptDir, '/eps/rf']
mkdir(epsDir)
ads = sparameters('data/rf_tank/ads.s2p')
awr = sparameters('data/rf_tank/awr.s2p')
meas = sparameters('data/rf_tank/TUNEDCOILS1.S2P')
S11ads=rfparam(ads,1,1);
S11meas=rfparam(meas,1,1);

freqsads = ads.Frequencies;
freqsmeas = meas.Frequencies;
f=figure("Position",[100,100,400,450]);
plt = smithplot();
ax = f.CurrentAxes;
hold(ax,"on");


% a=smithplot(ax,freqsads,S11ads);%,"LegendLabels",{'Simulation S11'});
% b=smithplot(ax,freqsmeas,S11meas);%,"LegendLabels",{'Measured S11'});
smithplot(meas,1,1,"LegendLabels",{'S11, Measured'})
smithplot(ads,1,1,"LegendLabels",{'S11, ADS Simulation'});
% c=smithplot(awr,1,1,'--',"LegendLabels", {'AWR Simulation S11'})
legend(ax,"Location","southoutside")
figure
rfplot(ads)
hold on
rfplot(meas)

figure;

exportgraphics(ax,[epsDir, '/s11.eps'])


%% CLEAN THIS

figure
nexttile

tiledlayout("horizontal")
nexttile
plot(ads.Frequencies,abs(x))
nexttile
plot(ads.Frequencies,rad2deg(angle(x)))
nexttile
tiledlayout("vertical")
nexttile
plot(ads.Frequencies,abs(x))
nexttile
plot(ads.Frequencies,rad2deg(angle(x)))
nexttile
rfplot(ads,1,1)
rfplot(ads,1,1,"abs")

ads_z = zparameters(ads)

ads_z.Parameters(1,1)
ads_z.Parameters(:,1,1)
aaaa=ads_z.Parameters
doc zparameters
clear x
clear aaaa
ads_z11 = rfparam(ads_z,1,1);
figure
tiledlayout('vertical')
nexttile

plot(ads_z.Frequencies,abs(rfparam(ads_z,1,1)))
plot(ads_z.Frequencies,db(rfparam(ads_z,1,1)))
nexttile
plot(ads_z.Frequencies,rad2deg(angle(rfparam(ads_z,1,1))))
nexttile(1)
hold on
meas_z = zparameters(meas)
plot(meas_z.Frequencies,db(rfparam(meas_z,1,1)))
xline(6.78e6)
nexttile
nexttile(2)
hold on
plot(meas_z.Frequencies,rad2deg(angle(rfparam(meas_z,1,1))))
%-- 1/12/2026 04:43 PM --%

