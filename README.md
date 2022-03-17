# Markowitz
Portfolio optimization using pyhton


# How to use it

This basic portfolio optimization uses yfinance to extract the financial data.

Its objective is to return a distribution of new weights for a portfolio of firms in the stock market. It can be used with ETFs but certain bond ETFs have such a little variance (close to the risk free rate as it is the case for SHY ETF) or can be the case that index ETFs are higly correlated and the distribution goes all to a single asset.

Markowitz.py will create a portfolio class, let's create a portfolio with AAPL, MSFT, AMZN, GOOG, NVDA

```python
portfolio = Portfolio()

Enter a ticker or 0 to finish:>? aapl
Enter a ticker or 0 to finish:>? msft
Enter a ticker or 0 to finish:>? amzn
Enter a ticker or 0 to finish:>? goog
Enter a ticker or 0 to finish:>? nvda
Enter a ticker or 0 to finish:>? 0
Is this your portfolio?: AAPL MSFT AMZN GOOG NVDA
Yes:1
No:0>? 1
```

Let's check what happens with the historical information of the last 7 years and create 10000 different portfolio distributions

```python
portfolio.markowitz(years=7, simulations=10000)
AAPL
MSFT
AMZN
GOOG
NVDA
```

After the statistic are done we can analize the best portfolio if the we have a risk free rate (treasuries) in 1%

```python
portfolio.plot_efficient(1)
AAPL: 0.8
MSFT: 78.67
AMZN: 3.25
GOOG: 1.49
NVDA: 15.78
```
![alt text](https://github.com/Surikta/Markowitz/blob/main/Image/Markowitz_1.png)


In this case, MSFT has a high portfolio allocation because it has the low variance and nice return. The model can be restricted to a maximum (and/or minimum) allocation and needs to be modify in the code. No short position or leverage is considered either.

Let´s try with 0% risk free rate:

```python
portfolio.plot_efficient(0)
AAPL: 0.63
MSFT: 75.86
AMZN: 8.76
GOOG: 8.17
NVDA: 6.57
```
![alt text](https://github.com/Surikta/Markowitz/blob/main/Image/Markowitz_0.png)
