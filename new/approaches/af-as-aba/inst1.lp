assumption(a1).
assumption(a2).
assumption(a3).
assumption(a4).
assumption(a5).
assumption(a6).
contrary(a1,a2).
contrary(a1,a3). % a1
contrary(a2,a5). % a2
contrary(a3,a4).
contrary(a3,a5). % a3
contrary(a4,a5). % a4
contrary(a5,a6). % a5
contrary(a6,a6). % a6
contrary(a6,a7).
contrary(a5,a7).

% P a1 <- O a2 <- P a5 <- O a6 <- P a6
% P a1 <- O a3 <- P a5 <- O a6 <- P a6

% P a1 <- O a3 <- a4 <- a5 <- a6 <- a6