#ifndef MATHFUNCTIONSLIB_H
#define MATHFUNCTIONSLIB_H

#include <vector>
#include <deque>

//historical log returns (uses vector, loops through all prices)
std::vector<double> log_returnshistorical(const std::vector<double>& prices);

//sliding-window log return (uses deque, last two prices only)
double log_returns(const std::deque<double>& prices_window);

#endif