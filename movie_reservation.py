import tkinter as tk
from tkinter import ttk, messagebox


class App(tk.Tk):
    """Main application controller. Holds shared state and switches frames."""

    def __init__(self):
        super().__init__()
        self.title("Movie Reservation System")
        self.geometry("800x600")

        # Shared state
        self.current_user = None
        self.selected_movie = None
        self.selected_cinema = None
        self.selected_schedule = None
        self.selected_seats = []

        # Container for frames
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Register frames
        self.frames = {}
        for F in (LoginFrame, MoviesFrame, CinemaFrame, ScheduleFrame,
                  SeatsFrame, PaymentFrame, ReceiptFrame):
            frame = F(parent=container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Start at login
        self.show_frame("LoginFrame")

    def show_frame(self, name: str):
        frame = self.frames.get(name)
        if frame is None:
            raise ValueError(f"No frame named {name}")
        frame.tkraise()


class LoginFrame(tk.Frame):
    def __init__(self, parent, controller: App):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Welcome", font=("Arial", 24)).pack(pady=10)

        form = tk.Frame(self)
        form.pack(pady=20)

        tk.Label(form, text="Username:").grid(row=0, column=0, sticky="e")
        self.username_entry = tk.Entry(form)
        self.username_entry.grid(row=0, column=1)

        tk.Label(form, text="Password:").grid(row=1, column=0, sticky="e")
        self.password_entry = tk.Entry(form, show="*")
        self.password_entry.grid(row=1, column=1)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Login", command=self.login).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Register", command=self.register).grid(row=0, column=1, padx=5)

        tk.Button(self, text="Continue as Guest",
                  command=lambda: controller.show_frame("MoviesFrame")).pack(pady=10)

    # Placeholder: don't implement real auth yet
    def login(self):
        username = self.username_entry.get().strip()
        # TODO: wire real authentication
        if username:
            self.controller.current_user = username
            self.controller.show_frame("MoviesFrame")
        else:
            messagebox.showwarning("Login", "Enter a username to continue (placeholder).")

    def register(self):
        # TODO: registration flow (placeholder)
        messagebox.showinfo("Register", "Registration is not implemented yet.")


class MoviesFrame(tk.Frame):
    def __init__(self, parent, controller: App):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Now Showing", font=("Arial", 20)).pack(pady=10)

        self.movies_list = tk.Listbox(self, height=8)
        self.movies_list.pack(padx=20, pady=10, fill="x")

        # Sample movies - in real app this will come from a service
        sample_movies = ["The Great Adventure", "Romance in Paris", "Sci-Fi Saga", "Comedy Night"]
        for m in sample_movies:
            self.movies_list.insert(tk.END, m)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Select Movie", command=self.select_movie).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Logout", command=self.logout).grid(row=0, column=1, padx=5)

    def select_movie(self):
        sel = self.movies_list.curselection()
        if not sel:
            messagebox.showwarning("Select", "Please select a movie (placeholder).")
            return
        self.controller.selected_movie = self.movies_list.get(sel[0])
        self.controller.show_frame("CinemaFrame")

    def logout(self):
        # Clear user and go back to login
        self.controller.current_user = None
        self.controller.show_frame("LoginFrame")


class CinemaFrame(tk.Frame):
    def __init__(self, parent, controller: App):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Choose Cinema", font=("Arial", 20)).pack(pady=10)

        self.cinema_var = tk.StringVar()
        cinemas = ["Cinema 1", "Cinema 2", "Cinema 3"]
        self.cinema_dropdown = ttk.Combobox(self, textvariable=self.cinema_var, values=cinemas, state="readonly")
        self.cinema_dropdown.pack(pady=10)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Next", command=self.next).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Back", command=lambda: controller.show_frame("MoviesFrame")).grid(row=0, column=1, padx=5)

    def next(self):
        cinema = self.cinema_var.get()
        if not cinema:
            messagebox.showwarning("Cinema", "Please choose a cinema (placeholder).")
            return
        self.controller.selected_cinema = cinema
        self.controller.show_frame("ScheduleFrame")


class ScheduleFrame(tk.Frame):
    def __init__(self, parent, controller: App):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Choose Date & Time", font=("Arial", 20)).pack(pady=10)

        self.schedules_list = tk.Listbox(self, height=8)
        self.schedules_list.pack(padx=20, pady=10, fill="x")

        # Sample schedules
        for s in ["2025-12-01 14:00", "2025-12-01 18:00", "2025-12-02 20:00"]:
            self.schedules_list.insert(tk.END, s)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Select", command=self.select).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Back", command=lambda: controller.show_frame("CinemaFrame")).grid(row=0, column=1, padx=5)

    def select(self):
        sel = self.schedules_list.curselection()
        if not sel:
            messagebox.showwarning("Schedule", "Please select a schedule (placeholder).")
            return
        self.controller.selected_schedule = self.schedules_list.get(sel[0])
        self.controller.show_frame("SeatsFrame")


class SeatsFrame(tk.Frame):
    def __init__(self, parent, controller: App):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Select Seats", font=("Arial", 20)).pack(pady=10)

        self.seats_frame = tk.Frame(self)
        self.seats_frame.pack(pady=10)

        # Create a simple seat grid (5 rows x 8 cols)
        self.seat_buttons = {}
        for r in range(5):
            for c in range(8):
                seat_id = f"R{r+1}C{c+1}"
                btn = tk.Button(self.seats_frame, text=seat_id, width=6,
                                command=lambda s=seat_id: self.toggle_seat(s))
                btn.grid(row=r, column=c, padx=2, pady=2)
                self.seat_buttons[seat_id] = btn

        control_frame = tk.Frame(self)
        control_frame.pack(pady=10)
        tk.Button(control_frame, text="Check Availability", command=self.check_availability).grid(row=0, column=0, padx=5)
        tk.Button(control_frame, text="Confirm Seats", command=self.confirm_seats).grid(row=0, column=1, padx=5)
        tk.Button(control_frame, text="Back", command=lambda: controller.show_frame("ScheduleFrame")).grid(row=0, column=2, padx=5)

    def toggle_seat(self, seat_id: str):
        if seat_id in self.controller.selected_seats:
            self.controller.selected_seats.remove(seat_id)
            self.seat_buttons[seat_id].config(relief=tk.RAISED, bg="SystemButtonFace")
        else:
            self.controller.selected_seats.append(seat_id)
            self.seat_buttons[seat_id].config(relief=tk.SUNKEN, bg="lightgreen")

    def check_availability(self):
        # TODO: call actual availability service. Placeholder shows a message.
        messagebox.showinfo("Availability", "Seat availability checked (placeholder).")

    def confirm_seats(self):
        if not self.controller.selected_seats:
            messagebox.showwarning("Seats", "No seats selected.")
            return
        # In real app: hold seats briefly and then move to confirmation/payment
        self.controller.show_frame("PaymentFrame")


class PaymentFrame(tk.Frame):
    def __init__(self, parent, controller: App):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Payment", font=("Arial", 20)).pack(pady=10)

        self.pay_method = tk.StringVar(value="Cashless")
        methods_frame = tk.Frame(self)
        methods_frame.pack(pady=10)
        tk.Radiobutton(methods_frame, text="Cash", variable=self.pay_method, value="Cash").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(methods_frame, text="Cashless", variable=self.pay_method, value="Cashless").pack(side=tk.LEFT, padx=5)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Pay", command=self.pay).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Back", command=lambda: controller.show_frame("SeatsFrame")).grid(row=0, column=1, padx=5)

    def pay(self):
        # TODO: process payment. Here we simulate success.
        success = True  # placeholder
        if success:
            self.controller.show_frame("ReceiptFrame")
        else:
            retry = messagebox.askretrycancel("Payment Failed", "Payment failed. Retry?")
            if not retry:
                # Release seats placeholder
                self.controller.selected_seats = []
                self.controller.show_frame("MoviesFrame")


class ReceiptFrame(tk.Frame):
    def __init__(self, parent, controller: App):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Receipt", font=("Arial", 20)).pack(pady=10)

        self.summary = tk.Text(self, height=15, width=70, state=tk.DISABLED)
        self.summary.pack(padx=10, pady=10)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Finish", command=self.finish).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Start Over", command=self.start_over).grid(row=0, column=1, padx=5)

    def tkraise(self, *args, **kwargs):
        # Populate the receipt before showing
        self.render_summary()
        super().tkraise(*args, **kwargs)

    def render_summary(self):
        self.summary.config(state=tk.NORMAL)
        self.summary.delete("1.0", tk.END)
        lines = [f"User: {self.controller.current_user}",
                 f"Movie: {self.controller.selected_movie}",
                 f"Cinema: {self.controller.selected_cinema}",
                 f"Schedule: {self.controller.selected_schedule}",
                 f"Seats: {', '.join(self.controller.selected_seats) if self.controller.selected_seats else 'None'}",
                 "Payment: (placeholder)"]
        self.summary.insert(tk.END, "\n".join(lines))
        self.summary.config(state=tk.DISABLED)

    def finish(self):
        messagebox.showinfo("Done", "Reservation completed (placeholder).")
        self.controller.show_frame("MoviesFrame")

    def start_over(self):
        # Reset selections but keep user logged in
        self.controller.selected_movie = None
        self.controller.selected_cinema = None
        self.controller.selected_schedule = None
        self.controller.selected_seats = []
        self.controller.show_frame("MoviesFrame")


if __name__ == "__main__":
    app = App()
    app.mainloop()
