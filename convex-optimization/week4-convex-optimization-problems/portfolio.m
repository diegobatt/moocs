%% simple_portfolio_data
n = 20;

rng(5,'v5uniform');
pbar = ones(n,1) * 0.03 + [rand(n-1,1); 0] * 0.12;

rng(5,'v5normal');
S = randn(n,n);
S = S'*S;
S = S/max(abs(diag(S)))*.2;
S(:,n) = zeros(n,1);
S(n,:) = zeros(n,1)';
x_unif = ones(n,1)/n;

unif_risk = sqrt(x_unif' * S * x_unif);

%% Optimal risk

cvx_begin
    variable x(n)
    minimize( x' * S * x )
    subject to
        sum(x) == 1
        pbar' * (x - x_unif) == 0
cvx_end

opt_risk = sqrt(x' * S * x);

%% Long-only portfolio risk

cvx_begin
    variable x(n)
    minimize( x' * S * x )
    subject to
        sum(x) == 1
        pbar' * (x - x_unif) == 0
        x >= 0
cvx_end

long_only_risk = sqrt(x' * S * x);

%% Short positions limit portfolio risk

cvx_begin
    variable x(n)
    minimize( x' * S * x )
    subject to
        sum(x) == 1
        pbar' * (x - x_unif) == 0
        sum(max(-x, 0)) <= 0.5
cvx_end

limit_short_risk = sqrt(x' * S * x);