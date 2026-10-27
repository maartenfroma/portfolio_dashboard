import quantstats as qs

class PortfolioAnalyzerAdvanced:

    @staticmethod
    def generate_html_report(portfolio_returns, benchmark_returns=None, output_file='portfolio_report.html'):
        """
        Generate an HTML report for the portfolio performance.

        :param portfolio_returns: A pandas Series of portfolio returns.
        :param benchmark_returns: A pandas Series of benchmark returns (optional).
        :param output_file: The name of the output HTML file.
        """
        qs.reports.html(portfolio_returns, benchmark=benchmark_returns, output=output_file)


    @staticmethod
    def get_quick_stats(df_timeseries):
        returns = df_timeseries['total_value'].pct_change().dropna()
        return {
            "sharpe": qs.stats.sharpe(returns),
            "sortino": qs.stats.sortino(returns),
            "max_drawdown": qs.stats.max_drawdown(returns),
            "win_rate": qs.stats.win_rate(returns),
        }