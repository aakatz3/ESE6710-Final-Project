ads = sparameters('data/rf_tank/ads.s2p')
meas = sparameters('data/rf_tank/TUNEDCOILS1.S2P')
S11ads=rfparam(ads,1,1);
S11meas=rfparam(meas,1,1);

freqsads = ads.Frequencies;
freqsmeas = meas.Frequencies;
f=figure("Position",[100,100,200,250]);
plt = smithplot();
ax = f.CurrentAxes;
hold(ax,"on");


% a=smithplot(ax,freqsads,S11ads);%,"LegendLabels",{'Simulation S11'});
% b=smithplot(ax,freqsmeas,S11meas);%,"LegendLabels",{'Measured S11'});
a=smithplot(ads,1,1,"LegendLabels",{'Simulation S11'});
b=smithplot(meas,1,1,"LegendLabels",{'Measured S11'})
legend(ax,"Location","southoutside")
figure



% smithplot(ax,ads,1,1,"LegendLabels",{'ads S11'})
