%[text] Mechanical design calcs
u=symunit;
nut = unitConvert(0.126*u.in,u.mm) %[output:03ce8462]
channel=1.8*u.mm %[output:3d6edfd7]
acrylic=6*u.mm %[output:54ce7456]


bracket=5.5*u.mm %[output:5db60bc4]


pcbHolderHeight=nut+channel+acrylic %[output:53707711]
vpa(pcbHolderHeight) %[output:76c815c7]

coilHolderHeight = bracket + acrylic %[output:16869a2c]
vpa(coilHolderHeight) %[output:7e50eba6]

%[appendix]{"version":"1.0"}
%---
%[metadata:view]
%   data: {"layout":"onright"}
%---
%[output:03ce8462]
%   data: {"dataType":"symbolic","outputData":{"name":"nut","value":"\\frac{8001}{2500}\\,{\\textrm{mm}}"}}
%---
%[output:3d6edfd7]
%   data: {"dataType":"symbolic","outputData":{"name":"channel","value":"\\frac{9}{5}\\,{\\textrm{mm}}"}}
%---
%[output:54ce7456]
%   data: {"dataType":"symbolic","outputData":{"name":"acrylic","value":"6\\,{\\textrm{mm}}"}}
%---
%[output:5db60bc4]
%   data: {"dataType":"symbolic","outputData":{"name":"bracket","value":"\\frac{11}{2}\\,{\\textrm{mm}}"}}
%---
%[output:53707711]
%   data: {"dataType":"symbolic","outputData":{"name":"pcbHolderHeight","value":"\\frac{27501}{2500}\\,{\\textrm{mm}}"}}
%---
%[output:76c815c7]
%   data: {"dataType":"symbolic","outputData":{"name":"ans","value":"11.0004\\,{\\textrm{mm}}"}}
%---
%[output:16869a2c]
%   data: {"dataType":"symbolic","outputData":{"name":"coilHolderHeight","value":"\\frac{23}{2}\\,{\\textrm{mm}}"}}
%---
%[output:7e50eba6]
%   data: {"dataType":"symbolic","outputData":{"name":"ans","value":"11.5\\,{\\textrm{mm}}"}}
%---
