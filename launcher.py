import sys
import subprocess

menu = subprocess.Popen(["python", "menu.py"])
orders = subprocess.Popen(["python", "orders.py"])
menu.communicate()
orders.communicate()