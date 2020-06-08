% data for online ad display problem
rand('state',0);
n=100;      %number of ads
m=30;       %number of contracts
T=60;       %number of periods

I=10*rand(T,1);  %number of impressions in each period
R=rand(n,T);    %revenue rate for each period and ad
q=T/n*50*rand(m,1);     %contract target number of impressions
p=rand(m,1);  %penalty rate for shortfall
Tcontr=(rand(T,m)>.8); %one column per contract. 1's at the periods to be displayed
for i=1:n
	contract=ceil(m*rand);
	Acontr(i,contract)=1; %one column per contract. 1's at the ads to be displayed
end

%Solve problm taking penalty in mind
cvx_begin
	variable N(n,T)
	revenue = sum(sum(R .* N))
	penalty = max(q' - sum(Acontr .* (N * Tcontr)), 0) * p
	net_rev = revenue - penalty
    maximize(net_rev)
    subject to
		sum(N) == I'
		N >= 0
cvx_end
% Solve problem without caring about penalty
cvx_begin
	variable N_free(n, T)
	revenue_free = sum(sum(R .* N_free))
	penalty_free = max(q' - sum(Acontr .* (N_free * Tcontr)), 0) * p
	net_rev_free = revenue_free - penalty_free
    maximize(revenue_free)
    subject to
		sum(N_free) == I'
		N_free >= 0
cvx_end
 