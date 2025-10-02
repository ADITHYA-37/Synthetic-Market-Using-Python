#!/usr/bin/env python3
import random
from typing import List, Dict

class Order:
    def __init__(self, price: float, size: float, side: str):
        self.price = price
        self.size = size
        self.side = side  # "buy" or "sell"

class OrderBook:
    def __init__(self):
        self.buys: List[Order] = []
        self.sells: List[Order] = []
        self.mid_price = 100.0

    def place_order(self, order: Order):
        if order.side == "buy":
            self.buys.append(order)
            self.buys.sort(key=lambda o: -o.price)
        else:
            self.sells.append(order)
            self.sells.sort(key=lambda o: o.price)

    def match_orders(self):
        trades = []
        while self.buys and self.sells and self.buys[0].price >= self.sells[0].price:
            trade_price = (self.buys[0].price + self.sells[0].price)/2
            trade_size = min(self.buys[0].size, self.sells[0].size)
            trades.append({"price": trade_price, "size": trade_size})
            self.buys[0].size -= trade_size
            self.sells[0].size -= trade_size
            if self.buys[0].size == 0:
                self.buys.pop(0)
            if self.sells[0].size == 0:
                self.sells.pop(0)
        if trades:
            self.mid_price = sum(t["price"] for t in trades)/len(trades)
        return trades

class MarketMaker:
    def __init__(self, order_book: OrderBook, spread: float = 1.0, size: float = 10.0):
        self.order_book = order_book
        self.spread = spread
        self.size = size

    def provide_liquidity(self):
        mid = self.order_book.mid_price
        self.order_book.place_order(Order(mid - self.spread/2, self.size, "buy"))
        self.order_book.place_order(Order(mid + self.spread/2, self.size, "sell"))

def simulate_market(days: int = 10):
    ob = OrderBook()
    mm = MarketMaker(ob)
    price_history = []

    for day in range(days):
        # Market maker places liquidity
        mm.provide_liquidity()
        # Random external orders
        for _ in range(random.randint(1,5)):
            side = random.choice(["buy","sell"])
            price = ob.mid_price * (1 + random.uniform(-0.02,0.02))
            size = random.uniform(5,20)
            ob.place_order(Order(price, size, side))
        trades = ob.match_orders()
        price_history.append(ob.mid_price)
        print(f"Day {day+1} | Mid Price: {round(ob.mid_price,2)} | Trades: {len(trades)}")
    return price_history

def demo():
    history = simulate_market(days=20)
    print("Final mid-price history:", [round(p,2) for p in history])

if __name__ == "__main__":
    demo()
