from tkinter import *
from tkinter import messagebox, Menu
import requests
import json
import sqlite3

pycrypto=Tk()
pycrypto.title("My Portfolio")
pycrypto.iconbitmap('c.ico')

con=sqlite3.connect('coin2.db')
curr=con.cursor()

curr.execute("CREATE TABLE IF NOT EXISTS coin(Id INTEGER PRIMARY KEY, Coin Name TEXT, Amount INTEGER, Price REAL)")
con.commit()

def reset():
    for cell in pycrypto.winfo_children():
        cell.destroy()
    nav()
    header()
    my_portfolio()

def nav():
    def clear_all():
        curr.execute("DELETE FROM coin")
        con.commit()
        messagebox.showinfo("Notification", "Portfolio Cleared")
        reset()

    def close_app():
        pycrypto.destroy()

    menu=Menu(pycrypto)
    file_item=Menu(menu)
    file_item.add_command(label='Clear',command=clear_all)
    file_item.add_command(label='Close App',command=close_app)

    menu.add_cascade(label="File",menu=file_item)
    pycrypto.config(menu=menu)

def my_portfolio():
    api_request=requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=5&convert=USD&CMC_PRO_API_KEY=12c25fef-dd12-4103-8e87-5d59ef125cdc")
    api= json.loads(api_request.content)

    curr.execute("SELECT * FROM coin")
    coins=curr.fetchall()

    print(coins)

    def font_color(amount):
        if amount >= 0:
            return "green"
        else:
            return "red"

    def insert_coin():
        curr.execute("INSERT INTO coin(coin,price,amount) VALUES(?,?,?)",(name_txt.get(),price_txt.get(),amount_txt.get()))
        con.commit()
        messagebox.showinfo("Notification","Coin added to the portfolio successfully")
        reset()

    def update_coin():
        curr.execute("UPDATE coin SET coin=?, price=?, amount=? WHERE id=?",(name_update.get(),price_update.get(),amount_update.get(),id_update.get()))
        con.commit()
        messagebox.showinfo("Notification", "Coin updated successfully")
        reset()

    def del_coin():
        curr.execute("DELETE FROM coin WHERE id=?",(id_del.get()))
        con.commit()
        messagebox.showinfo("Notification", "Coin deleted from the portfolio")
        reset()

    total_pl=0
    coin_row=1
    total_cv=0
    total_amount=0

    for i in range(0,5):
        for coin in coins:
            if api["data"][i]["name"]==coin[1]:
                total_pay=coin[2]*coin[3]
                current=coin[2]*api["data"][i]["quote"]["USD"]["price"]
                pl=api["data"][i]["quote"]["USD"]["price"]-coin[3]
                total_pl_coin=pl*coin[2]

                total_pl+=total_pl_coin
                total_cv+=current
                total_amount+=total_pay

                id = Label(pycrypto, text=coin[0], bg="#F0ECFF", fg="#0D1036",font="Airel 10",borderwidth=2,relief="groove",padx="2",pady="2")
                id.grid(row=coin_row, column=0, sticky=N + S + E + W)

                name = Label(pycrypto, text=api["data"][i]["name"], bg="#F0ECFF", fg="#0D1036",font="Airel 10",borderwidth=2,relief="groove",padx="2",pady="2")
                name.grid(row=coin_row, column=1, sticky=N + S + E + W)

                price = Label(pycrypto, text="${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]), bg="#F0ECFF", fg="#0D1036",font="Airel 10",borderwidth=2,relief="groove",padx="2",pady="2")
                price.grid(row=coin_row, column=2, sticky=N + S + E + W)

                amount = Label(pycrypto, text=coin[2], bg="#F0ECFF", fg="#0D1036",font="Airel 10",borderwidth=2,relief="groove",padx="2",pady="2")
                amount.grid(row=coin_row, column=3, sticky=N + S + E + W)

                total_pay = Label(pycrypto, text="${0:.2f}".format(total_pay), bg="#F0ECFF", fg="#0D1036",font="Airel 10",borderwidth=2,relief="groove",padx="2",pady="2")
                total_pay.grid(row=coin_row, column=4, sticky=N + S + E + W)

                current= Label(pycrypto, text="${0:.2f}".format(current), bg="#F0ECFF", fg="#0D1036",font="Airel 10",borderwidth=2,relief="groove",padx="2",pady="2")
                current.grid(row=coin_row, column=5, sticky=N + S + E + W)

                pl = Label(pycrypto, text="${0:.2f}".format(pl), bg="#F0ECFF", fg=font_color(float("{0:.2f}".format(pl))),font="Airel 10",borderwidth=2,relief="groove",padx="2",pady="2")
                pl.grid(row=coin_row, column=6, sticky=N + S + E + W)

                total_pl_coin = Label(pycrypto, text="${0:.2f}".format(total_pl_coin), bg="#F0ECFF", fg=font_color(float("{0:.2f}".format(total_pl_coin))),font="Airel 10",borderwidth=2,relief="groove",padx="2",pady="2")
                total_pl_coin.grid(row=coin_row, column=7, sticky=N + S + E + W)

                coin_row+=1

    #INSERT
    name_txt=Entry(pycrypto,borderwidth=2,relief="groove")
    name_txt.grid(row=coin_row+1,column=1)

    price_txt=Entry(pycrypto,borderwidth=2,relief="groove")
    price_txt.grid(row=coin_row+1,column=2)

    amount_txt=Entry(pycrypto,borderwidth=2,relief="groove")
    amount_txt.grid(row=coin_row+1,column=3)

    add_coin = Button(pycrypto, text="Add Coin", bg="#1D2F39", fg="white",command=insert_coin, font="Airel 10", borderwidth=2,relief="groove", padx="2", pady="2")
    add_coin.grid(row=coin_row+1, column=4, sticky=N + S + E + W)

    #UDATE
    id_update=Entry(pycrypto,borderwidth=2,relief="groove")
    id_update.grid(row=coin_row+2,column=0)

    name_update=Entry(pycrypto,borderwidth=2,relief="groove")
    name_update.grid(row=coin_row+2,column=1)

    price_update=Entry(pycrypto,borderwidth=2,relief="groove")
    price_update.grid(row=coin_row+2,column=2)

    amount_update=Entry(pycrypto,borderwidth=2,relief="groove")
    amount_update.grid(row=coin_row+2,column=3)

    coin_update= Button(pycrypto, text="Update Coin", bg="#1D2F39", fg="white",command=update_coin, font="Airel 10", borderwidth=2,relief="groove", padx="2", pady="2")
    coin_update.grid(row=coin_row+2, column=4, sticky=N + S + E + W)

    #DELETE
    id_del=Entry(pycrypto,borderwidth=2,relief="groove")
    id_del.grid(row=coin_row+3,column=0)

    coin_del= Button(pycrypto, text="Delete Coin", bg="#1D2F39", fg="white",command=del_coin, font="Airel 10", borderwidth=2,relief="groove", padx="2", pady="2")
    coin_del.grid(row=coin_row+3, column=4, sticky=N + S + E + W)


    total_amount = Label(pycrypto, text="${0:.2f}".format(total_amount), bg="#F0ECFF", fg="#0D1036", font="Airel 10", borderwidth=2,relief="groove", padx="2", pady="2")
    total_amount.grid(row=coin_row, column=4, sticky=N + S + E + W)

    total_cv = Label(pycrypto, text="${0:.2f}".format(total_cv), bg="#F0ECFF", fg="#0D1036", font="Airel 10", borderwidth=2,relief="groove", padx="2", pady="2")
    total_cv.grid(row=coin_row, column=5, sticky=N + S + E + W)

    total_pl = Label(pycrypto, text="${0:.2f}".format(total_pl) , bg="#F0ECFF", fg=font_color(float("{0:.2f}".format(total_pl))), font="Airel 10", borderwidth=2, relief="groove", padx="2", pady="2")
    total_pl.grid(row=coin_row, column=7, sticky=N + S + E + W)

    api=""

    refresh = Button(pycrypto, text="Refresh", bg="#1D2F39", fg="white",command=reset, font="Airel 10", borderwidth=2,relief="groove", padx="2", pady="2")
    refresh.grid(row=coin_row+1, column=7, sticky=N + S + E + W)

def header():
    id=Label(pycrypto,text="Id",bg="#1D2F39",fg="white",font="Ariel 10 bold",padx="2",pady="2",borderwidth=3,relief="groove")
    id.grid(row=0,column=0,sticky=N+S+E+W)

    name=Label(pycrypto,text="Coin Name",bg="#1D2F39",fg="white",font="Ariel 10 bold",padx="2",pady="2",borderwidth=3,relief="groove")
    name.grid(row=0,column=1,sticky=N+S+E+W)

    price=Label(pycrypto,text="Price",bg="#1D2F39",fg="white",font="Ariel 10 bold",padx="2",pady="2",borderwidth=3,relief="groove")
    price.grid(row=0,column=2,sticky=N+S+E+W)

    no_coins=Label(pycrypto,text="No. of coins",bg="#1D2F39",fg="white",font="Ariel 10 bold",padx="2",pady="2",borderwidth=3,relief="groove")
    no_coins.grid(row=0,column=3,sticky=N+S+E+W)

    amont_pay=Label(pycrypto,text="Total amount",bg="#1D2F39",fg="white",font="Ariel 10 bold",padx="2",pady="2",borderwidth=3,relief="groove")
    amont_pay.grid(row=0,column=4,sticky=N+S+E+W)

    curr_val=Label(pycrypto,text="Current Value",bg="#1D2F39",fg="white",font="Ariel 10 bold",padx="2",pady="2",borderwidth=3,relief="groove")
    curr_val.grid(row=0,column=5,sticky=N+S+E+W)

    pl=Label(pycrypto,text="P/L",bg="#1D2F39",fg="white",font="Ariel 10 bold",padx="2",pady="2",borderwidth=3,relief="groove")
    pl.grid(row=0,column=6,sticky=N+S+E+W)

    total_pl=Label(pycrypto,text="Total P/L",bg="#1D2F39",fg="white",font="Ariel 10 bold",padx="2",pady="2",borderwidth=3,relief="groove")
    total_pl.grid(row=0,column=7,sticky=N+S+E+W)

nav()
header()
my_portfolio()
pycrypto.mainloop()
print("Completed")

curr.close()
con.close()

