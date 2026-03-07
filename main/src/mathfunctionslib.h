#ifndef MATHFUNCTIONSLIB_H
#define MATHFUNCTIONSLIB_H

#include <vector>
#include <deque>

//historical log returns (uses vector, loops through all prices)
std::vector<double> log_returnshistorical(const std::vector<double>& prices);

//sliding-window log return (uses deque, last two prices only)
double log_returns(const std::deque<double>& prices_window);

//compute volatility/standard deviation
double volatility(const std::deque<double>& returns_window);

//mean return
double mean_return(const std::deque<double>&returns_window);

//sharpe ratio
double sharpe_ratio(const std::deque<double>& returns_window, double risk_free_rate = 0.0);

#endif