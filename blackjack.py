import tkinter as tk

from App import App
from Dealer import Dealer
from Player import Player
from Deck import Deck
from Table import Table

def main():
  root = tk.Tk()
  app = App(root)
  app.pack()
  app.mainloop()

if __name__ == "__main__":
   main()
