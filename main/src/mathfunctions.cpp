#include "mathfunctionslib.h"
#include <iostream>
#include <cmath>
#include <vector>
using namespace std;


vector<double> log_returns(const vector<double>& prices) //passing prices by reference
{
    vector<double> returns;
    if(prices.size()<2) 
    return returns;
    
    returns.reserve(prices.size()-1);
    for(size_t i=1;i<prices.size();i++) //start i at 1 because we need to use two prices for the formula
    { 
       if(prices[i-1]>0 && prices[i]>0)
       returns.push_back(log(prices[i]/[prices[i-1]));
       else
        returns.push_back(0); //to avoid negative or equal to 0
    }
    return returns;
}