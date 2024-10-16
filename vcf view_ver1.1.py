import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import json

class VCFViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VCF Contact Viewer")
        self.root.geometry("700x500")

        # Setup GUI elements
        self.setup_widgets()

    def setup_widgets(self):
        # Button to open VCF file
        self.open_button = tk.Button(self.root, text="Open VCF File", command=self.open_vcf_file)
        self.open_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Text widget to display parsed VCF data
        self.text_box = tk.Text(self.root, wrap="word")
        self.text_box.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Save button
        self.save_button = tk.Button(self.root, text="Save As", command=self.save_as_file)
        self.save_button.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        # Configure grid weights for resizing
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=0)

    def open_vcf_file(self):
        # Open file dialog to select VCF file
        file_path = filedialog.askopenfilename(filetypes=[("VCF files", "*.vcf")])
        if not file_path:
            return

        # Read VCF file and parse data
        try:
            with open(file_path, "r") as file:
                vcf_data = file.read()
            self.contacts = self.parse_vcf_data(vcf_data)
            self.display_contacts(self.contacts)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read VCF file: {e}")

    def parse_vcf_data(self, vcf_data):
        contacts = []
        contact = {}

        for line in vcf_data.splitlines():
            line = line.strip()
            if line.startswith("FN:"):
                contact['Name'] = line[3:]  # Extract name after "FN:"
            elif line.startswith("TEL:") or line.startswith("TEL;CELL"):
                contact['Phone'] = line.split(":")[1]  # Extract phone number
            elif line == "END:VCARD":
                # If we reached the end of a vCard, add the contact to the list
                if contact:
                    contacts.append(contact)
                    contact = {}  # Reset for the next contact

        return contacts

    def display_contacts(self, contacts):
        # Clear existing text in the Text widget
        self.text_box.delete(1.0, tk.END)

        # Display parsed contacts
        for contact in contacts:
            name = contact.get('Name', 'Unknown')
            phone = contact.get('Phone', 'N/A')
            self.text_box.insert(tk.END, f"Name: {name}\nPhone: {phone}\n\n")

    def save_as_file(self):
        if not hasattr(self, 'contacts') or not self.contacts:
            messagebox.showwarning("Warning", "No contacts to save")
            return

        # Choose the file format and save location
        file_types = [("Text File", "*.txt"), ("CSV File", "*.csv"), ("JSON File", "*.json")]
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=file_types)

        if not file_path:
            return

        # Save the file based on the selected format
        try:
            if file_path.endswith(".txt"):
                self.save_as_txt(file_path)
            elif file_path.endswith(".csv"):
                self.save_as_csv(file_path)
            elif file_path.endswith(".json"):
                self.save_as_json(file_path)
            messagebox.showinfo("Success", f"Contacts saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")

    def save_as_txt(self, file_path):
        # Save contacts as a text file
        with open(file_path, "w") as file:
            for contact in self.contacts:
                name = contact.get('Name', 'Unknown')
                phone = contact.get('Phone', 'N/A')
                file.write(f"Name: {name}\nPhone: {phone}\n\n")

    def save_as_csv(self, file_path):
        # Save contacts as a CSV file
        with open(file_path, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Name", "Phone"])  # Write the header
            for contact in self.contacts:
                writer.writerow([contact.get('Name', 'Unknown'), contact.get('Phone', 'N/A')])

    def save_as_json(self, file_path):
        # Save contacts as a JSON file
        with open(file_path, "w") as json_file:
            json.dump(self.contacts, json_file, indent=4)

if __name__ == "__main__":
    root = tk.Tk()
    app = VCFViewerApp(root)
    root.mainloop()
