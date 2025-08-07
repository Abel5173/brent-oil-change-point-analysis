import pandas as pd
import numpy as np
import pymc3 as pm
import matplotlib.pyplot as plt
import os

# Load price data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRICES_PATH = os.path.join(BASE_DIR, 'data', 'brent_oil_prices.csv')
EVENTS_PATH = os.path.join(BASE_DIR, 'data', 'events.csv')
OUTPUT_PATH = os.path.join(BASE_DIR, 'data', 'change_points.csv')

def load_data():
    prices = pd.read_csv(PRICES_PATH)
    prices['Date'] = pd.to_datetime(prices['Date'], format='%d-%b-%y')
    prices = prices.sort_values('Date')
    prices['Log_Returns'] = np.log(prices['Price']).diff().dropna()
    return prices

def bayesian_change_point_model(data):
    log_returns = data['Log_Returns'].dropna().values
    n = len(log_returns)
    idx = np.arange(n)

    with pm.Model() as model:
        # Prior for change point (uniform over data indices)
        tau = pm.DiscreteUniform("tau", lower=0, upper=n-1)

        # Priors for mean log returns before and after change point
        mu_1 = pm.Normal("mu_1", mu=0, sd=0.1)
        mu_2 = pm.Normal("mu_2", mu=0, sd=0.1)

        # Prior for shared standard deviation
        sigma = pm.HalfNormal("sigma", sd=0.1)

        # Switchpoint logic
        mu = pm.math.switch(tau > idx, mu_1, mu_2)

        # Likelihood
        observation = pm.Normal("obs", mu=mu, sd=sigma, observed=log_returns)

        # Sampling
        trace = pm.sample(2000, tune=1000, return_inferencedata=False)

    return trace, data.index[1:]  # Skip first index due to diff()

def analyze_change_points(trace, dates, events):
    # Extract posterior mean of tau
    tau_mean = int(np.mean(trace['tau']))
    change_date = dates[tau_mean]

    # Extract mean log returns before/after
    mu_1_mean = np.mean(trace['mu_1'])
    mu_2_mean = np.mean(trace['mu_2'])

    # Convert log returns to approximate price change percentage
    price_change = (np.exp(mu_2_mean) - np.exp(mu_1_mean)) * 100

    # Find closest event
    events['Date'] = pd.to_datetime(events['Date'])
    closest_event = events.iloc[(events['Date'] - change_date).abs().argsort()[:1]]
    event_date = closest_event['Date'].iloc[0]
    event_desc = closest_event['Event'].iloc[0]

    # Create change point data
    change_points = [{
        'Date': change_date.strftime('%Y-%m-%d'),
        'Mean_Before': mu_1_mean,
        'Mean_After': mu_2_mean,
        'Price_Change_Percent': price_change,
        'Description': f"Change point near {event_desc} ({event_date.strftime('%Y-%m-%d')})"
    }]

    return pd.DataFrame(change_points)

def main():
    # Load data
    prices = load_data()
    events = pd.read_csv(EVENTS_PATH)

    # Run model
    trace, dates = bayesian_change_point_model(prices)

    # Analyze results
    change_points = analyze_change_points(trace, dates, events)

    # Save change points
    change_points.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved change points to {OUTPUT_PATH}")

    # Plot posterior distribution of tau
    plt.figure(figsize=(10, 6))
    plt.hist(trace['tau'], bins=50, density=True)
    plt.title('Posterior Distribution of Change Point (tau)')
    plt.xlabel('Index')
    plt.ylabel('Density')
    plt.savefig(os.path.join(BASE_DIR, 'notebooks', 'tau_posterior.png'))
    plt.close()

    # Print insights
    print("\nInsights:")
    for _, cp in change_points.iterrows():
        print(f"Change point detected on {cp['Date']}:")
        print(f"Mean log return before: {cp['Mean_Before']:.4f}")
        print(f"Mean log return after: {cp['Mean_After']:.4f}")
        print(f"Approximate price change: {cp['Price_Change_Percent']:.2f}%")
        print(f"Associated event: {cp['Description']}")

if __name__ == '__main__':
    main()
