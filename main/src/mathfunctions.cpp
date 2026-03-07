#include "mathfunctionslib.h"
#include <cmath>
#include <vector>
#include <deque>
#include <iostream>
using namespace std;


vector<double> log_returnshistorical(const vector<double>& prices) //passing prices by reference
{
    vector<double> returns;
    if(prices.size()<2) 
    return returns;
    
    returns.reserve(prices.size()-1);
    for(size_t i=1;i<prices.size();i++) //start i at 1 because we need to use two prices for the formula
    { 
       if(prices[i-1]>0 && prices[i]>0)
       returns.push_back(log(prices[i]/prices[i-1]));
       else
        returns.push_back(0); //to avoid negative or equal to 0
    }
    return returns;
}   
//this would work for historical returns 

double log_returns(const deque<double>& prices_window) //prices from window passed by reference
{
    if(prices_window.size()<2) //enough prices?
    return 0;

    double prev= prices_window[prices_window.size()-2]; //taking second to last element
    double curr = prices_window.back(); //last element

    if(prev<=0 || curr<=0)
    return 0;
    
    return log(curr/prev);
}

