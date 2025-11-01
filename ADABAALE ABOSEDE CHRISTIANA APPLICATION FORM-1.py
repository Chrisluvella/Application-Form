import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox, simpledialog, ttk
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import random, os, json



class Person:
    """Base class representing a person."""
    def __init__(self, first_name, last_name, gender, dob, email):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.dob = dob
        self.email = email


class Applicant(Person):
    """Derived class representing a job applicant."""
    def __init__(self, first_name, last_name, gender, dob, email,
                 school_name, education_level, phone, address, skills, experience, picture_path, app_id=None):
        super().__init__(first_name, last_name, gender, dob, email)
        self.school_name = school_name
        self.education_level = education_level
        self.phone = phone
        self.address = address
        self.skills = skills
        self.experience = experience
        self.picture_path = picture_path
        self.app_id = app_id if app_id else f"APP-{random.randint(1000,9999)}"

    def save_to_file(self):
        """Encapsulation: Save applicant data in JSON"""
        os.makedirs("applications", exist_ok=True)
        file_path = f"applications/{self.app_id}.json"
        data = self.__dict__
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
        return file_path

    def generate_pdf(self):
        """Encapsulation: create a PDF summary of applicant details"""
        pdf_file = f"{self.app_id}_{self.last_name}.pdf"
        c = canvas.Canvas(pdf_file, pagesize=letter)
        c.setFont("Helvetica-Bold", 18)
        c.drawString(200, 750, "Applicant Information Summary")

        c.setFont("Helvetica", 12)
        y = 700
        for label, value in [
            ("Application ID", self.app_id),
            ("Name", f"{self.first_name} {self.last_name}"),
            ("Gender", self.gender),
            ("Date of Birth", self.dob),
            ("Email", self.email),
            ("Phone", self.phone),
            ("Address", self.address),
            ("School", self.school_name),
            ("Education Level", self.education_level),
            ("Skills", ', '.join(self.skills)),
            ("Experience", self.experience)
        ]:
            c.drawString(50, y, f"{label}: {value}")
            y -= 20

        if self.picture_path and os.path.exists(self.picture_path):
            c.drawImage(self.picture_path, 420, 580, width=130, height=130)

        c.save()
        return pdf_file

    def simulate_email(self, pdf_file):
        """Abstraction: Simulate sending an email confirmation"""
        with open("email_log.txt", "a") as f:
            f.write(f"\nTo: {self.email}\nSubject: Application Confirmation\n\n")
            f.write(f"Dear {self.first_name},\n\n")
            f.write(f"Thank you for your application to Lagos State University.\n")
            f.write(f"Your Application ID is {self.app_id}.\n")
            f.write(f"A PDF copy of your submission ({pdf_file}) has been generated.\n\n")
            f.write(f"Sent on: {datetime.now()}\n{'-'*60}\n")


class OOPApplication(tk.Tk):
    """Main Application integrating all OOP principles."""
    def __init__(self):
        super().__init__()
        self.title("OOP Application Project - Lagos State University")
        self.geometry("950x700")
        self.configure(bg="#E3F2FD")
        self.create_intro_page()

    def create_intro_page(self):
        """Page 1 - Introduction"""
        for widget in self.winfo_children():
            widget.destroy()

        Label(self, text="PROGRAMMING LANGUAGES (CSC 825)", bg="#0D47A1", fg="white",
              font=("Helvetica", 20, "bold"), pady=15).pack(fill="x")

        Label(self, text="A Project Demonstrating the Integration of the Four OOP Features",
              bg="#E3F2FD", fg="#0D47A1", font=("Arial", 16, "bold")).pack(pady=15)

        info_frame = Frame(self, bg="#BBDEFB", padx=30, pady=20)
        info_frame.pack(pady=20, fill="x", padx=50)

        Label(info_frame, text="Name: Adabaale Abosede Christiana", font=("Arial", 14, "bold"), bg="#BBDEFB", fg="#0D47A1").pack(anchor="w")
        Label(info_frame, text="Matric No: 243105911317", font=("Arial", 14, "bold"), bg="#BBDEFB", fg="#0D47A1").pack(anchor="w")
        Label(info_frame, text="School: Lagos State University, Ojo", font=("Arial", 14, "bold"), bg="#BBDEFB", fg="#0D47A1").pack(anchor="w")
        Label(info_frame, text="Course Title: Programming Languages", font=("Arial", 14, "bold"), bg="#BBDEFB", fg="#0D47A1").pack(anchor="w")
        Label(info_frame, text="Course Code: CSC 825", font=("Arial", 14, "bold"), bg="#BBDEFB", fg="#0D47A1").pack(anchor="w")
        Label(info_frame, text="Topic: Using any programming language, write a program that shows the integration of the four features of OOP, tailored to solve a problem.",
              font=("Arial", 13), bg="#BBDEFB", fg="#1A237E", wraplength=800, justify="left").pack(anchor="w", pady=10)

        Label(self, text="Problem Solved:", bg="#E3F2FD", fg="#0D47A1", font=("Arial", 14, "bold")).pack(pady=(20, 0))
        Label(self, text="This application provides a digital form for applicants to apply for university-related opportunities. "
                         "It demonstrates encapsulation, abstraction, inheritance, and polymorphism in OOP.",
              bg="#E3F2FD", fg="#1A237E", font=("Arial", 13), wraplength=850, justify="left").pack(padx=20)

        Button(self, text="Continue to Application Form", bg="#1565C0", fg="white",
               font=("Arial", 14, "bold"), width=35, pady=10, command=self.create_form_page).pack(pady=15)
        Button(self, text="Admin Login", bg="#1B5E20", fg="white",
               font=("Arial", 14, "bold"), width=20, pady=10, command=self.admin_login).pack(pady=10)

    def create_form_page(self, loaded_data=None):
        """Page 2 - Application Form"""
        for widget in self.winfo_children():
            widget.destroy()

        Label(self, text="APPLICANT INFORMATION FORM", bg="#0D47A1", fg="white",
              font=("Helvetica", 18, "bold"), pady=15).pack(fill="x")

        form = Frame(self, bg="#E3F2FD")
        form.pack(pady=10)

        labels = ["First Name", "Last Name", "Gender", "Date of Birth", "Email", "Phone", "Address",
                  "School Name", "Education Level", "Work Experience", "Skills", "Profile Picture"]
        self.entries = {}
        row = 0

        for lbl in labels:
            Label(form, text=f"{lbl}:", bg="#E3F2FD", fg="#0D47A1", font=("Arial", 12, "bold")).grid(row=row, column=0, sticky=W, pady=5)
            if lbl == "Gender":
                self.gender = StringVar(value=loaded_data["gender"] if loaded_data else "")
                Radiobutton(form, text="Male", variable=self.gender, value="Male", bg="#E3F2FD").grid(row=row, column=1, sticky=W)
                Radiobutton(form, text="Female", variable=self.gender, value="Female", bg="#E3F2FD").grid(row=row, column=2, sticky=W)
            elif lbl == "Skills":
                self.skills = Listbox(form, selectmode=MULTIPLE, height=4, width=25)
                for skill in ["Python", "Web Design", "Data Analysis", "Machine Learning", "AI", "Graphic Design"]:
                    self.skills.insert(END, skill)
                if loaded_data:
                    for i, skill in enumerate(["Python", "Web Design", "Data Analysis", "Machine Learning", "AI", "Graphic Design"]):
                        if skill in loaded_data["skills"]:
                            self.skills.selection_set(i)
                self.skills.grid(row=row, column=1, columnspan=2, sticky=W)
            elif lbl == "Profile Picture":
                self.pic_entry = Entry(form, width=30)
                self.pic_entry.grid(row=row, column=1, sticky=W)
                Button(form, text="Upload", command=self.upload_pic, bg="#1565C0", fg="white").grid(row=row, column=2, sticky=W)
                if loaded_data:
                    self.pic_entry.insert(0, loaded_data["picture_path"])
            else:
                entry = Entry(form, width=30)
                entry.grid(row=row, column=1, columnspan=2, sticky=W)
                if loaded_data and lbl.replace(" ", "_").lower() in loaded_data:
                    entry.insert(0, loaded_data[lbl.replace(" ", "_").lower()])
                self.entries[lbl] = entry
            row += 1

        Button(form, text="Submit Application", bg="#1B5E20", fg="white", font=("Arial", 12, "bold"),
               command=self.submit_application).grid(row=row, column=1, pady=20)
        Button(form, text="Continue Application", bg="#1565C0", fg="white", font=("Arial", 12, "bold"),
               command=self.load_previous_application).grid(row=row, column=2, pady=20)

    def upload_pic(self):
        file_path = filedialog.askopenfilename(title="Select Profile Picture",
                                               filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if file_path:
            self.pic_entry.delete(0, END)
            self.pic_entry.insert(0, file_path)

    def submit_application(self):
        data = {k: v.get() for k, v in self.entries.items()}
        gender = self.gender.get()
        selected_skills = [self.skills.get(i) for i in self.skills.curselection()]
        pic = self.pic_entry.get()

        applicant = Applicant(data["First Name"], data["Last Name"], gender, data["Date of Birth"], data["Email"],
                              data["School Name"], data["Education Level"], data["Phone"], data["Address"],
                              selected_skills, data["Work Experience"], pic)

        applicant.save_to_file()
        pdf = applicant.generate_pdf()
        applicant.simulate_email(pdf)

        messagebox.showinfo("Success", f"Application Submitted Successfully!\nYour Application ID: {applicant.app_id}")
        self.create_intro_page()

    def load_previous_application(self):
        app_id = simpledialog.askstring("Continue Application", "Enter your Application ID (e.g. APP-1234):")
        if not app_id:
            return

        file_path = f"applications/{app_id}.json"
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "Application ID not found.")
            return

        with open(file_path, "r") as f:
            data = json.load(f)
        self.create_form_page(loaded_data=data)

    def admin_login(self):
        """Simple password-protected admin access"""
        password = simpledialog.askstring("Admin Login", "Enter Admin Password:", show='*')
        if password == "admin123":
            self.admin_dashboard()
        else:
            messagebox.showerror("Access Denied", "Incorrect password.")

    def admin_dashboard(self):
        """Admin page showing all applicants"""
        for widget in self.winfo_children():
            widget.destroy()

        Label(self, text="ADMIN DASHBOARD", bg="#1B5E20", fg="white",
              font=("Helvetica", 18, "bold"), pady=15).pack(fill="x")

        search_frame = Frame(self, bg="#E8F5E9")
        search_frame.pack(fill="x", pady=10)

        Label(search_frame, text="Search Applicant:", bg="#E8F5E9", fg="#1B5E20", font=("Arial", 12, "bold")).pack(side=LEFT, padx=10)
        search_entry = Entry(search_frame, width=30)
        search_entry.pack(side=LEFT, padx=10)
        Button(search_frame, text="Search", bg="#1B5E20", fg="white", command=lambda: self.load_admin_data(search_entry.get())).pack(side=LEFT)

        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Email", "Phone"), show="headings", height=15)
        for col in ("ID", "Name", "Email", "Phone"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)
        self.tree.pack(fill=BOTH, expand=True, pady=10)

        Button(self, text="Back to Home", bg="#1565C0", fg="white", command=self.create_intro_page).pack(pady=10)

        self.load_admin_data()

    def load_admin_data(self, query=""):
        """Load applicant data in grid"""
        for row in self.tree.get_children():
            self.tree.delete(row)

        if not os.path.exists("applications"):
            return

        for file in os.listdir("applications"):
            if file.endswith(".json"):
                with open(os.path.join("applications", file), "r") as f:
                    data = json.load(f)
                    name = f"{data['first_name']} {data['last_name']}"
                    if query.lower() in name.lower() or query.lower() in data['email'].lower() or query.lower() in data['app_id'].lower():
                        self.tree.insert("", END, values=(data["app_id"], name, data["email"], data["phone"]))


if __name__ == "__main__":
    OOPApplication().mainloop()