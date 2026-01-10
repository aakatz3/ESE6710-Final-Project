%[text] Coil transformer characterization
%[text] This doesn't quite work
L1open = 4.18e-6;
L1short = 3.66e-6;
L2open = 4.14e-6;
L2short = 3.66e-6;
Lu = L1open %[output:6d1b5635]
syms lleak;
lleak = double(solve(L1short == 1/sum([1/lleak, 1/Lu]))) %[output:96609133]
n=sqrt(L2short / lleak) %[output:8bd026f1]
nsquare = L2short / (Lu + lleak) %[output:5f7b9a86]
n^2 %[output:88d804c1]
sqrt(nsquare) %[output:12ebe9ab]


%[appendix]{"version":"1.0"}
%---
%[metadata:view]
%   data: {"layout":"onright"}
%---
%[output:6d1b5635]
%   data: {"dataType":"textualVariable","outputData":{"name":"Lu","value":"    4.18000000000000e-006\n"}}
%---
%[output:96609133]
%   data: {"dataType":"textualVariable","outputData":{"name":"lleak","value":"    29.4207692307692e-006\n"}}
%---
%[output:8bd026f1]
%   data: {"dataType":"textualVariable","outputData":{"name":"n","value":"    352.706554908748e-003\n"}}
%---
%[output:5f7b9a86]
%   data: {"dataType":"textualVariable","outputData":{"name":"nsquare","value":"    108.926077699686e-003\n"}}
%---
%[output:88d804c1]
%   data: {"dataType":"textualVariable","outputData":{"name":"ans","value":"    124.401913875598e-003\n"}}
%---
%[output:12ebe9ab]
%   data: {"dataType":"textualVariable","outputData":{"name":"ans","value":"    330.039509301063e-003\n"}}
%---
