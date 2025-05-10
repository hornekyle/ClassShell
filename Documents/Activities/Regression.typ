#import "../../Tooling/Typst/activity.typ":formatter

#show: doc => formatter(
	title:[Regression Derivations],
	doc,
	)

Several logic paths may be followed to derive the same linear system of equations for regression of the polynomial $p(x;c_j)$ which best matches as set of data $x_m , y_m$. Three of these derivations are given below without commentary. Care should be taken to understand reasoning behind the decisions made in each.

#grid(columns:(1fr,1fr),
[
= Projected Error Rejection

$
exists {x_m} in 𝔻^M, {y_m} in ℝ^M | m in [0,M) subset ℤ \
{p_m} = [x_m^j]{c_j} | {c_j} in ℝ^N; N in [1,∞) subset ℤ
$
$
{ϵ_m} = {p_m}-{y_m} & = [x_m^j]{c_j}-{y_m}={0} \
[x_m^j]^T [x_m^j]{c_j} & = [x_m^j]^T {y_m} \
[x_m^i][x_m^j]{c_j} & = [x_m^i]{y_m} \
[sum_m x_m^(i+j)]{c_j} & = {sum_m x_m^i y_m} \
$
],[
= Least Squares Error Minimization

$
exists x_m & in 𝔻, y_m in ℝ | m in [0,M) subset ℤ \
p(x;c_j) & = sum_j [c_j x^j] | c_j in ℝ; j in [0,N) subset ℤ \
ϵ_m (c_j) & = p(x_m;c_j)-y_m \
R(c_j) & = sum_m [ϵ_m^2 (c_j)] = sum_m [(p(x_m;c_j)-y_m)^2] \
(partial R) / (partial c_i) & = sum_m [2 (p(x_m;c_j)-y_m) (partial p)/(partial c_i) (x_m;c_j)] \ 
(partial p) / (partial c_i) & = sum_j [partial/(partial c_i) (c_j x^j)] = sum_j [δ_(i j) x^j] = x^i \
(partial R) / (partial c_i) & = 2 sum_m [x_m^i sum_j [c_j x_m^j] - x_m^i y_m] = 0 \
& arrow [sum_m x_m^(i+j)]{c_j} = {sum_m x_m^i y_m}
$
])
= Weighted Residuals

$
exists x_m & in 𝔻, y_m in ℝ | m in [0,M) subset ℤ \
p(x;c_j) & = sum_j [c_j ϕ_j (x)] | ϕ_j (x) = x^j; c_j in ℝ; j in [0,N) subset ℤ \
R_i(c_j) & = ∫_𝔻 w_i (x) dot E(x;c_j) d x = 0 | w_i (x) = x^i \
E(x;c_j) & = sum_m [δ_m (x) dot (p(x;c_j) - y_m)] \
R_i(c_j) & = ∫_𝔻 x^i sum_m [δ_m (x) dot (sum_j [c_j x^j] -y_m)] d x = 0 \
& = sum_m [∫_𝔻 x^i δ_m (x) dot sum_j [c_j x^j] d x - ∫_𝔻 x^i δ_m (x) y_m d x] = 0 \
& = sum_m [ sum_j [c_j x_m^(i+j)] - x_m^i y_m] = 0 \
& = sum_j [c_j sum_m x_m^(i+j)] - sum_m [x_m^i y_m] = 0 \
& arrow [sum_m x_m^(i+j)]{c_j} = {sum_m x_m^i y_m}
$
