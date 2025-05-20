
import json
import os
import time
import sys

records = []

def loading_animation():
    animation = "|/-\\"
    print("Loading", end="")
    for i in range(15):
        sys.stdout.write("\rLoading " + animation[i % len(animation)])
        sys.stdout.flush()
        time.sleep(0.1)
    print("\rLoading complete!     ")


def recursive_count(lst):
    if not lst:
        return 0
    return 1 + recursive_count(lst[1:])

def welcome_screen():
    
    print("Welcome to the Hospital Patient Record System")
    loading_animation()

def input_nonempty(prompt):
    while True:
        val = input(prompt).strip()
        if val == '':
            print("Input cannot be empty. Please try again.")
        else:
            return val

def input_int(prompt, min_val=None, max_val=None):
    while True:
        val = input(prompt).strip()
        try:
            iv = int(val)
            if (min_val is not None and iv < min_val) or (max_val is not None and iv > max_val):
                print(f"Input must be between {min_val} and {max_val}.")
                continue
            return iv
        except ValueError:
            print("Invalid integer. Please try again.")

def add_record():
    print("\nAdd New Patient Record")
    pid = input_nonempty("Enter Patient ID: ")
    for rec in records:
        if rec['id'] == pid:
            print("ID already exists. Please use a unique ID.")
            return
    name = input_nonempty("Enter Patient Name: ")
    age = input_int("Enter Patient Age: ", 0, 120)
    diagnosis = input_nonempty("Enter Diagnosis: ")
    records.append({'id': pid, 'name': name, 'age': age, 'diagnosis': diagnosis})
    print("Patient record added successfully.")

def view_records():
    if not records:
        print("\nNo patient records available.")
        return
    print("\nAll Patient Records:")
    print(f"{'ID':<10} {'Name':<20} {'Age':<5} {'Diagnosis':<30}")
    print("-"*65)
    for r in records:
        print(f"{r['id']:<10} {r['name']:<20} {r['age']:<5} {r['diagnosis']:<30}")

def search_record():
    pid = input_nonempty("Enter Patient ID to search: ")
    found = [r for r in records if r['id'] == pid]
    if found:
        print("\nSearch Result:")
        print(f"{'ID':<10} {'Name':<20} {'Age':<5} {'Diagnosis':<30}")
        print("-"*65)
        for r in found:
            print(f"{r['id']:<10} {r['name']:<20} {r['age']:<5} {r['diagnosis']:<30}")
    else:
        print(f"No record found with ID {pid}.")

def update_record():
    pid = input_nonempty("Enter Patient ID to update: ")
    for r in records:
        if r['id'] == pid:
            print(f"Current Name: {r['name']}, Age: {r['age']}, Diagnosis: {r['diagnosis']}")
            new_name = input("Enter new name (press enter to keep current): ").strip()
            if new_name:
                r['name'] = new_name
            new_age = input("Enter new age (press enter to keep current): ").strip()
            if new_age:
                try:
                    r['age'] = int(new_age)
                except ValueError:
                    print("Invalid age. Keeping current.")
            new_diagnosis = input("Enter new diagnosis (press enter to keep current): ").strip()
            if new_diagnosis:
                r['diagnosis'] = new_diagnosis
            print("Patient record updated successfully.")
            return
    print("Patient not found.")

def delete_record():
    pid = input_nonempty("Enter Patient ID to delete: ")
    global records
    for r in records:
        if r['id'] == pid:
            confirm = input(f"Are you sure you want to delete patient {pid}? (y/n): ").strip().lower()
            if confirm == 'y':
                records = [rec for rec in records if rec['id'] != pid]
                print("Patient record deleted.")
            else:
                print("Delete operation canceled.")
            return
    print("Patient not found.")

def calculate_stats():
    if not records:
        print("No records to calculate stats.")
        return
    total_age = sum(r['age'] for r in records)
    avg_age = total_age / len(records)
    print(f"\nSummary Statistics:")
    print(f"Total Patients: {len(records)}")
    print(f"Average Age: {avg_age:.2f}")

def save_records():
    try:
        with open("patients.json", "w") as f:
            json.dump(records, f)
        print("Records saved to patients.json.")
    except Exception as e:
        print(f"Error saving records: {e}")

def load_records():
    global records
    try:
        if os.path.exists("patients.json"):
            with open("patients.json", "r") as f:
                records = json.load(f)
            print("Records loaded from patients.json.")
        else:
            print("No saved patient records found.")
    except Exception as e:
        print(f"Error loading records: {e}")

def clear_data():
    confirm = input("Are you sure you want to clear ALL patient data? (yes/no): ").strip().lower()
    if confirm == "yes":
        global records
        records = []
        print("All patient data cleared.")
    else:
        print("Clear operation cancelled.")

def display_help():
    print("""
Help / Instructions:
1. Add New Patient Record - Add a new patient with ID, name, age, and diagnosis.
2. View All Records - Display all patient records.
3. Search for a Patient - Search by patient ID.
4. Update a Patient Record - Update name, age, and/or diagnosis.
5. Delete a Patient Record - Delete by ID.
6. Calculate Summary Stats - Total patients and average age.
7. Save to File - Save all records to patients.json.
8. Load from File - Load saved records.
9. Clear All Data - Delete all records.
10. Help - Show this help menu.
0. Exit - Exit the system.
""")

def sort_records():
    if not records:
        print("No records to sort.")
        return
    print("Sort by field:")
    print("1. ID")
    print("2. Name")
    print("3. Age")
    choice = input("Choose field to sort by (1-3): ").strip()
    if choice == '1':
        records.sort(key=lambda r: r['id'])
        print("Records sorted by ID.")
    elif choice == '2':
        records.sort(key=lambda r: r['name'].lower())
        print("Records sorted by Name.")
    elif choice == '3':
        records.sort(key=lambda r: r['age'])
        print("Records sorted by Age.")
    else:
        print("Invalid choice.")

def main():
    try:
        welcome_screen()
        load_records()
        while True:
            print("""
Main Menu:
1. Add New Patient Record
2. View All Records
3. Search for a Patient
4. Update a Patient Record
5. Delete a Patient Record
6. Calculate Summary Stats
7. Save to File
8. Load from File
9. Clear All Data
10. Help
11. Sort Records
0. Exit
""")
            choice = input("Select an option: ").strip()
            if choice == '1':
                add_record()
            elif choice == '2':
                view_records()
            elif choice == '3':
                search_record()
            elif choice == '4':
                update_record()
            elif choice == '5':
                delete_record()
            elif choice == '6':
                calculate_stats()
            elif choice == '7':
                save_records()
            elif choice == '8':
                load_records()
            elif choice == '9':
                clear_data()
            elif choice == '10':
                display_help()
            elif choice == '11':
                sort_records()
            elif choice == '0':
                print("Exiting Hospital Record System. Goodbye!")
                break
            else:
                print("Invalid option. Please select a valid menu number.")
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
