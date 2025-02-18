class AccessControl:
    def __init__(self):
        # User details with roles, clearance, and device access
        self.users = {
            "deng": {"role": "doctor", "clearance": "top-secret", "device": "company-laptop"},
            "red": {"role": "admin", "clearance": "confidential", "device": "personal-laptop"},
            "keng": {"role": "nurse", "clearance": "secret", "device": "company-desktop"},
            "luna": {"role": "assistant", "clearance": "confidential", "device": "company-laptop"}
        }
        # File permissions for each user
        self.file_permissions = {
            "deng": ["file1", "file2"],
            "red": ["file3"],
            "keng": ["file1"],
            "luna": ["file2", "file3"]
        }
        self.work_hours = (9, 17)  # Access allowed only between 9 AM and 5 PM
        self.access_log = []  # Stores access attempts

    def log_access(self, user, model, result):
        """Logs access attempts for tracking."""
        self.access_log.append(f"{user} tried {model} access: {result}")

    def mac_access(self, user, required_clearance):
        """Mandatory Access Control: Checks clearance level."""
        if user in self.users and self.users[user]["clearance"] == required_clearance:
            self.log_access(user, "MAC", "Access Granted")
            return True
        self.log_access(user, "MAC", "Access Denied")
        return False
    
    def dac_access(self, user, file):
        """Discretionary Access Control: Checks if user has file access."""
        if user in self.users and file in self.file_permissions.get(user, []):
            self.log_access(user, "DAC", "Access Granted")
            return True
        self.log_access(user, "DAC", "Access Denied")
        return False
    
    def rbac_access(self, user, required_role):
        """Role-Based Access Control: Checks user role."""
        if user in self.users and self.users[user]["role"] == required_role:
            self.log_access(user, "RBAC", "Access Granted")
            return True
        self.log_access(user, "RBAC", "Access Denied")
        return False
    
    def abac_access(self, user, current_hour, device):
        """Attribute-Based Access Control: Checks work hours and device type."""
        if user in self.users:
            within_hours = self.work_hours[0] <= current_hour < self.work_hours[1]
            correct_device = self.users[user]["device"] == device
            if within_hours and correct_device:
                self.log_access(user, "ABAC", "Access Granted")
                return True
        self.log_access(user, "ABAC", "Access Denied")
        return False

    def display_access_log(self):
        """Prints the access attempt log."""
        print("\nAccess Log:")
        for log in self.access_log:
            print(log)


# Main program loop
ac = AccessControl()
user = input("Enter your username: ").strip().lower()

if user not in ac.users:
    print("Invalid username. Access Denied.")
else:
    print("\nChoose an access control model:")
    print("1. MAC (Mandatory Access Control)")
    print("2. DAC (Discretionary Access Control)")
    print("3. RBAC (Role-Based Access Control)")
    print("4. ABAC (Attribute-Based Access Control)")
    
    choice = input("Enter your choice (1-4): ").strip()

    if choice == "1":
        required_clearance = input("Enter required clearance (top-secret, confidential, secret): ").strip().lower()
        print("Access Granted" if ac.mac_access(user, required_clearance) else "Access Denied")
    
    elif choice == "2":
        file = input("Enter file name (file1, file2, file3): ").strip()
        print("Access Granted" if ac.dac_access(user, file) else "Access Denied")
    
    elif choice == "3":
        required_role = input("Enter required role (doctor, admin, nurse, assistant): ").strip().lower()
        print("Access Granted" if ac.rbac_access(user, required_role) else "Access Denied")
    
    elif choice == "4":
        try:
            current_hour = int(input("Enter current hour (0-23): ").strip())
            device = input("Enter your device (company-laptop, personal-laptop, company-desktop): ").strip().lower()
            print("Access Granted" if ac.abac_access(user, current_hour, device) else "Access Denied")
        except ValueError:
            print("Invalid input for hour. Please enter a number between 0-23.")
    
    else:
        print("Invalid choice.")

    ac.display_access_log()  # Show access logs at the end
