import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import csv
import os

class VCFtoCSVConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VCF to CSV Converter")
        self.root.geometry("700x500")

        # Setup GUI elements
        self.setup_widgets()

    def setup_widgets(self):
        # Button to open VCF file
        self.open_button = tk.Button(self.root, text="Open VCF File", command=self.open_vcf_file)
        self.open_button.pack(pady=10)

        # Treeview to display CSV data
        self.tree = ttk.Treeview(self.root, columns=("Name", "Phone", "Email"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Email", text="Email")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Button to save CSV file
        self.save_button = tk.Button(self.root, text="Save as CSV", command=self.save_as_csv)
        self.save_button.pack(pady=10)

        # Data storage
        self.contacts = []

    def open_vcf_file(self):
        # Open file dialog to select VCF file
        file_path = filedialog.askopenfilename(filetypes=[("VCF files", "*.vcf")])
        if not file_path:
            return

        # Read VCF file manually
        try:
            with open(file_path, "r") as file:
                contact = {}
                for line in file:
                    line = line.strip()
                    if line.startswith("FN:"):
                        contact['Name'] = line[3:]
                    elif line.startswith("TEL:"):
                        contact['Phone'] = line[4:]
                    elif line.startswith("EMAIL:"):
                        contact['Email'] = line[6:]
                    elif line == "END:VCARD":
                        # If we reached the end of a vCard, add the contact to the list
                        if contact:
                            self.contacts.append(contact)
                            contact = {}
            
            # Update Treeview with contact data
            self.update_treeview()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read VCF file: {e}")

    def update_treeview(self):
        # Clear existing data
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insert new data
        for contact in self.contacts:
            name = contact.get('Name', 'Unknown')
            phone = contact.get('Phone', '')
            email = contact.get('Email', '')
            self.tree.insert("", tk.END, values=(name, phone, email))

    def save_as_csv(self):
        if not self.contacts:
            messagebox.showwarning("Warning", "No contacts to save")
            return

        # Save file dialog to specify the CSV file
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        # Write to CSV file
        try:
            with open(file_path, "w", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["Name", "Phone", "Email"])
                for contact in self.contacts:
                    writer.writerow([
                        contact.get('Name', 'Unknown'),
                        contact.get('Phone', ''),
                        contact.get('Email', '')
                    ])
            messagebox.showinfo("Success", f"Contacts saved to {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save CSV file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VCFtoCSVConverterApp(root)
    root.mainloop()
