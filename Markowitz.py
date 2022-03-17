import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import yfinance as yf


class Portfolio:
    # Sets the tickers
    def __init__(self):

        self.covariance = pd.DataFrame()
        self.time_series = pd.DataFrame()
        self.r = []
        self.v = []
        self.simulations = 0
        self.port = np.array([0.0])
        self.efficient = np.array([0.0])

        self.tickers = []
        self.trigger = 1
        while self.trigger:
            tk = input('Enter a ticker or 0 to finish:')
            if tk != '0':
                # Can be written in lowercase
                self.tickers.append(tk.upper())
            else:
                # Shows the portfolio in case of an error
                self.trigger = not(int(input('Is this your portfolio?: ' +
                                             ' '.join(self.tickers) +
                                             '\nYes:1\nNo:0')))
                # If there was an error, the portfolio resets
                if self.trigger:
                    print('Starting from the beginning')
                    self.tickers = []

        self.exp_ret = []
        self.variance = []
        self.payoff = list()
        self.allocation = np.repeat(1/len(self.tickers), len(self.tickers))

    # Sets the initial state
    def new_port(self):
        self.__init__()

    # Calculates the Markowitz efficient frontier.
    # Requires the last n-years of data to calculate the variance (risk) and expected return.
    # simulations variable is the number of different portfolio distributions to do the math.
    def markowitz(self, years, simulations):

        self.simulations = simulations
        self.r = []
        self.v = []
        self.port = np.array(np.repeat(0.0, simulations*len(self.tickers)))
        self.port = self.port.reshape([simulations, len(self.tickers)])

        for i in self.tickers:
            # Get the data
            print(i)
            data = yf.Ticker(i).history(period='max')

            today = datetime.datetime.now()
            if (today - data.index[0]).days >= years*365:
                data = data[data.index >= today-datetime.timedelta(years*365)]
                data = data.dropna()
            else:
                print(f'Contains a period less than {years} years')

            # Get the monthly price + any dividend payment (payoff)
            payoff = np.array(np.log(data['Close'][0]))
            dividend = 0
            start = data.index[0]
            for j in range(len(data)):
                dividend = dividend + data['Dividends'][j]
                if data.index[j].month != start.month:
                    # Dividends must be treated as capital gains.
                    payoff = np.append(payoff, np.log(dividend + data['Close'][j]))
                    start = data.index[j]

            payoff = np.append(payoff, np.log(dividend + data['Close'][len(data)-1]))

            self.payoff.append((np.diff(payoff)*100))

        # Time series as a pandas Data Frame
        self.time_series = pd.DataFrame(self.payoff)
        self.time_series = self.time_series.transpose()
        self.time_series.columns = self.tickers

        # Var-Cov matrix and mean return statistics
        self.covariance = self.time_series.cov()
        self.exp_ret = self.time_series.mean()

        # High number of simulations will make the process slow
        # I recommend less than 50000 simulations
        for i in range(simulations):

            # First needs to be equal-weight portfolio
            # The allocation does NOT consider a short position or leverage in any asset.
            if i == 0:
                distrib = np.repeat(1/len(self.tickers), len(self.tickers))
            else:
                distrib = np.random.dirichlet(np.repeat(1, len(self.tickers)))

            self.port[i, :] = distrib
            distrib = pd.DataFrame(distrib).transpose()
            distrib.columns = self.tickers

            # Calculation of expected return and expected variance
            port_ret = 0
            port_var = 0
            for j1 in self.tickers:
                port_ret = port_ret + distrib[j1]*self.exp_ret[j1]
                for j2 in self.tickers:
                    port_var = port_var + distrib[j1]*self.covariance[j1][j2]*distrib[j2]

            self.r.append(port_ret)
            self.v.append(port_var)

    # The visualization and analysis requires a new variable: the interest rate
    # Interest rate as a %
    def plot_efficient(self, interest_rate):

        # Calculates the best portfolio distribution
        maximum = 0
        index = 0
        for i in range(self.simulations):
            m = float((self.r[i] - interest_rate)/self.v[i])
            if m > maximum:
                maximum = m
                index = i
                self.efficient = self.port[i, :]

        # Plot of the simulations
        fig, ax = plt.subplots()
        ax.scatter(self.v, self.r, s=10, alpha=0.5, color='cyan')
        ax.scatter(self.v[index], self.r[index], s=10,
                   alpha=1, color='green', label='Efficient Portfolio')
        ax.scatter(self.v[0], self.r[0], s=10,
                   alpha=1, color='black', label='Equal Weight')
        ax.legend()
        ax.set_xlabel("Variance %")
        ax.set_ylabel("Return %")

        # Prints your new portfolio
        for i in range(len(self.tickers)):
            print(self.tickers[i] + ': ' + str(np.round(self.efficient[i]*100, 2)))


portfolio = Portfolio()
