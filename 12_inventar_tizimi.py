#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""12. Inventar Tizimi"""
import sqlite3
class Inventory:
    def __init__(self):
        self.conn = sqlite3.connect("inventory.db")
        self.conn.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT UNIQUE, quantity INTEGER, min_qty INTEGER, price REAL)")
        self.conn.commit()
    def add(self, name, qty, min_qty, price):
        self.conn.execute("INSERT OR REPLACE INTO items VALUES (NULL,?,?,?,?)", (name, qty, min_qty, price))
        self.conn.commit(); print("✅")
    def sell(self, name, qty):
        row = self.conn.execute("SELECT quantity, min_qty FROM items WHERE name=?", (name,)).fetchone()
        if row and row[0] >= qty:
            self.conn.execute("UPDATE items SET quantity=quantity-? WHERE name=?", (qty, name))
            self.conn.commit(); print("✅ Sotildi")
            if row[0]-qty <= row[1]: print("⚠️ Kam qoldi")
        else: print("Yetarli emas")
    def low(self):
        for r in self.conn.execute("SELECT name, quantity, min_qty FROM items WHERE quantity <= min_qty"):
            print(f"⚠️ {r[0]}: {r[1]}")
def main():
    inv = Inventory()
    while True:
        print("\n1.Qoshish 2.Sotish 3.Kam 4.Chiqish")
        c = input("> ")
        if c=="1": inv.add(input("Nomi: "), int(input("Miqdor: ")), int(input("Min: ")), float(input("Narx: ")))
        elif c=="2": inv.sell(input("Nomi: "), int(input("Miqdor: ")))
        elif c=="3": inv.low()
        elif c=="4": break
if __name__ == "__main__": main()
