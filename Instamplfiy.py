import tkinter as tk
from tkinter import *
from InstagramAccount import *


class Instamplify:
    """
    Instagram Bot user interface that allows for easy access to typical daily user needs
    """
    def __init__(self):
        self.master = tk.Tk()
        self.username = tk.Label(self.master, text="Username", bg='white', fg='black')
        self.username.grid(row=0, padx=10, pady=10)
        self.password = tk.Label(self.master, text="Password", bg='white', fg='black')
        self.password.grid(row=1, padx=10, pady=10)
        self.hashtag_follow_label = tk.Label(self.master, text="", bg='white', fg='black')
        
        self.master.iconbitmap(r'instagram_ico.ico')
        self.master.title("InstagramBot")
        self.master.configure(bg='white')

        # Ensuring window appears in middle of OS screen
        screen_width = self.master.winfo_screenwidth() + 100
        screen_height = self.master.winfo_screenheight()
        x_coordinate = (screen_width / 2) - (420 / 2)
        y_coordinate = (screen_height / 2) - (200 / 2)
        self.master.geometry("%dx%d+%d+%d" % (420, 200, x_coordinate, y_coordinate))

        options = [
            "Get Daily Homepage Feed",
            "Like Photo With Hashtag",
            "Follow Certain Person"
        ]
        variable = StringVar(self.master)
        variable.set(options[0])

        self.option_menu = OptionMenu(self.master, variable, *options, command=lambda _: self.update_option())
        self.option_menu.grid(row=0, column=3)

        self.username_input = tk.Entry(self.master)
        self.password_input = tk.Entry(self.master, show="*", width=20)
        self.hashtag_follow_user_input = tk.Entry(self.master)

        self.username_input.grid(row=0, column=1)
        self.password_input.grid(row=1, column=1)

        self.go_button = tk.Button(self.master, text='Go', command=self.do_desired_operation)
        self.go_button.grid(row=4, column=1)

        self.master.mainloop()

    def update_option(self):
        
        option = self.option_menu.cget("text")
        print(option)
        if option == "Like Photo With Hashtag":
            self.hashtag_follow_label['text'] = 'Hashtag'
            self.hashtag_follow_label.grid(row=2)
            self.hashtag_follow_user_input.grid(row=2, column=1)
        elif option == "Follow Certain Person:":
            self.hashtag_follow_label['text'] = 'Follow Certain Person:'
            self.hashtag_follow_label.grid(row=2)
            self.hashtag_follow_user_input.grid(row=2, column=1)
        else:
            self.hashtag_follow_label.grid_forget()
            self.hashtag_follow_user_input.grid_forget()

    def do_desired_operation(self):
        """
        Adjusts labels and input boxes based on option selected
        """
        username = self.username_input.get()
        password = self.password_input.get()
        user_account = InstagramAccount(username, password)
        user_account.login();
        if self.option_menu.cget("text") == "Get Daily Homepage Feed":
            user_account.get_daily_homepage_feed(True)
        elif self.option_menu.cget("text") == "Like Photo With Hashtag":
            hashtag = self.hashtag_follow_user_input.get()
            user_account.like_photo_with_hashtag(hashtag)
        else:
            account_name = self.hashtag_follow_user_input.get()
            user_account.follow(account_name)

    def exit_app(self):
        self.master.quit()
        sys.exit()


if __name__ == '__main__':
    ui = Instamplify()





