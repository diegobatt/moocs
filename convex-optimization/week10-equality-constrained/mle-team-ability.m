% Generate data
run storage/generate_team_data.m
% Generate game incidence sparse matrix
A = sparse(1:m,train(:,1),train(:,3),m,n)
    + sparse(1:m,train(:,2),-train(:,3),m,n);
% Solve system
cvx_begin
    variable a(n)
    maximize(sum(log_normcdf((1/sigma) .* A*a)))
    subject to
        0 <= a <= 1
cvx_end
% Get test predictions
a_ = [1.0;0.0;0.68;0.37;0.79;0.58;0.38;0.09;0.67;0.58]
y_ = sign(a(test(:, 1)) - a(test(:, 2)))
accuracy = sum(y_ == test(:, 3)) / m
dummy_accuracy = sum(train(:, 3) == test(:, 3)) / m
