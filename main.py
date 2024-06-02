import csv
from tkinter import Tk, Label, Button, Canvas, PhotoImage, Entry, END
from tkinter import messagebox
import pandas
import random


def generate_password():
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()[]{}"
    random_password = "".join(random.choice(letters) for _ in range(12))
    password_input.delete(0, END)
    password_input.insert(0, random_password)


def save():
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        is_ok = messagebox.askokcancel(title=website,
                                       message=f"These are the details entered: \nEmail: {email}\nPassword: {password}\nIs it ok to save?")
        if is_ok:
            new_data = {
                "Website": [website],
                "Email": [email],
                "Password": [password]
            }

            try:
                data = pandas.read_csv("data.csv")
            except FileNotFoundError:
                data_for_make_new_file = {
                    "Website": [website],
                    "Email": [email],
                    "Password": [password]
                }
                df = pandas.DataFrame(data_for_make_new_file)
                df.to_csv("data.csv", index=False)
                data = pandas.read_csv("data.csv")
                
            new_data = pandas.DataFrame(new_data)
            data = pandas.concat([data, new_data], ignore_index=True)

            data.to_csv("data.csv", index=False)

            website_input.delete(0, END)
            password_input.delete(0, END)

def search():
    website = website_input.get()
    data = pandas.read_csv("data.csv")
    data_dict = {row["Website"]: [row["Email"], row["Password"]] for (index, row) in data.iterrows()}
    try:
        messagebox.showinfo(title="Search result", message=f"Name {website}\nEmail {data_dict[website][0]}\nPassword {data_dict[website][1]}")
    except KeyError:
        messagebox.showinfo(title="Oops", message="This is not have")
    website_input.delete(0, END)
    password_input.delete(0, END)

# Screen
window = Tk()
window.title("Password Generator")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=image)
canvas.grid(row=0, column=1)

website_text = Label(text="Website")
website_text.grid(row=1, column=0)

website_input = Entry(width=35)
website_input.grid(row=1, column=1)
website_input.focus()

email_text = Label(text="Email")
email_text.grid(row=2, column=0)

email_input = Entry(width=35)
email_input.grid(row=2, column=1)
email_input.insert(0, "example.com")

password_text = Label(text="Password")
password_text.grid(row=3, column=0)

password_input = Entry(width=21)
password_input.grid(row=3, column=1)

# Buttons
generate_password_btn = Button(text="Generate Password", command=generate_password)
generate_password_btn.grid(row=3, column=2)

add_btn = Button(text="Add", width=15, command=save)
add_btn.grid(row=4, column=1)

search_button = Button(text="Search", command=search, width=15)
search_button.grid(row=1, column=2)

window.mainloop()
