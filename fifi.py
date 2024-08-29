import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Liste des tickers du NASDAQ 100 (exemple avec quelques tickers)
nasdaq_100_tickers = [
    'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'FB', 'TSLA', 'NVDA', 'GOOG', 'PYPL', 'CMCSA',
    # Ajoutez ici les autres tickers du NASDAQ 100
]

# Paramètres de la simulation de Monte Carlo
num_simulations = 1000  # Nombre de simulations
num_days = 252  # Nombre de jours de négociation dans un an
T = num_days  # Période T sur laquelle on souhaite calculer le prix final

# Liste pour stocker les résultats
L = []

# Télécharger les données historiques et effectuer la simulation pour chaque ticker
for ticker in nasdaq_100_tickers:
    try:
        # Télécharger les données
        stock_data = yf.download(ticker, start="2023-01-01", end="2023-12-31", progress=False)
        
        # Calculer les rendements journaliers
        returns = stock_data['Adj Close'].pct_change().dropna()
        
        # Calculer la moyenne et la volatilité des rendements journaliers
        mean_return = returns.mean()
        volatility = returns.std()
        
        # Simulation de Monte Carlo
        simulations = np.zeros((num_simulations, num_days))
        for i in range(num_simulations):
            price_series = [stock_data['Adj Close'].iloc[-1]]
            for j in range(1, num_days):
                price = price_series[-1] * np.exp((mean_return - 0.5 * volatility ** 2) + volatility * np.random.normal())
                price_series.append(price)
            simulations[i, :] = price_series
            
        # Tracer les résultats pour ce ticker (facultatif)
        plt.figure(figsize=(10, 6))
        plt.plot(simulations.T, lw=1)
        plt.title(f'Simulation de Monte Carlo pour {ticker}')
        plt.xlabel('Jour de négociation')
        plt.ylabel('Prix simulé')
        plt.show()
        
        # Calculer le prix final après la période T pour chaque simulation
        final_prices = simulations[:, -1]  # Le prix final après T jours
        initial_price = stock_data['Adj Close'].iloc[-1]  # Prix initial au début de la simulation
        
        # Calculer le rapport demandé pour chaque simulation et le stocker dans L
        percentage_changes = ((final_prices - initial_price) * 100) / initial_price
        L.append({
            'ticker': ticker,
            'average_percentage_change': np.mean(percentage_changes),
            'stddev_percentage_change': np.std(percentage_changes)
        })
        
    except Exception as e:
        print(f"Erreur lors du traitement pour {ticker}: {e}")

# Identifier l'action la plus rentable
most_profitable_stock = max(L, key=lambda x: x['average_percentage_change'])

# Afficher le résultat
print(f"L'action la plus rentable est {most_profitable_stock['ticker']} avec un pourcentage moyen de variation de {most_profitable_stock['average_percentage_change']:.2f}%.")

# Afficher tous les résultats de la liste L (facultatif)
for result in L:
    print(result)
    
 