from pycoingecko import CoinGeckoAPI
from Tonviewer import Wallet , Coin

cg = CoinGeckoAPI()

price_data = cg.get_price(ids='toncoin', vs_currencies='usd')

print(price_data)

## Prints TON and USDT balance of wallet
wallet = Wallet("")    #wallet_address_here
wallet.balance()

# Prints live price
coin = Coin("toncoin")   #ex: "toncoin" , "bitcoin" , ...
coin.price()    # Prints live price
coin.about()    # Prints description of the coin

print(coin)

COURSE = coin