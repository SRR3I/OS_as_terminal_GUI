import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox


class CommandPromptGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("OS")

        self.command_prompt = CommandPrompt()

        self.create_widgets()

    def create_widgets(self):
        self.run_button = tk.Button(self, text="Run", command=self.run_command)
        self.run_button.pack()

        self.browse_button = tk.Button(
            self, text="Browse", command=self.browse_directory)
        self.browse_button.pack()

        self.output_text = tk.Text(self, height=20, width=80)
        self.output_text.pack()

        self.command_label = tk.Label(self, text="Enter command:")
        self.command_label.pack()

        self.command_entry = tk.Entry(self)
        self.command_entry.pack(fill=tk.X)
        # Bind the Enter key to run the command
        self.bind("<Return>", lambda event: self.run_command())

    def run_command(self):
        command = self.command_entry.get().strip()
        self.output_text.insert(tk.END, f" {command}\n")
        self.output_text.see(tk.END)
        self.command_entry.delete(0, tk.END)

        if command.upper() == "QUIT":
            self.quit_program()
        elif command.upper() == "CLEAR":
            self.clear_screen()
        else:
            output = self.command_prompt.execute_command(command)
            self.output_text.insert(tk.END, output + "\n\n")
            self.output_text.see(tk.END)

    def quit_program(self):
        self.destroy()

    def clear_screen(self):
        self.output_text.delete('1.0', tk.END)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.command_entry.insert(tk.END, f'NAVIGATE {directory}')


class CommandPrompt:
    def execute_command(self, command):
        command = command.upper()
        try:
            if command == "HELP":
                return self.display_help()
            elif command == "LS":
                return self.display_directory_contents(os.getcwd())
            elif command.startswith("NAVIGATE "):
                directory = command[9:]
                return self.change_directory(directory)
            elif command.startswith("CY "):
                source, destination = command[3:].split()
                return self.copy_files(source, destination)
            elif command.startswith("REMOVE_DIR "):
                directory = command[11:]
                return self.delete_dir(directory)
            elif command.startswith("REMOVE_FILE "):
                file_path = command[12:]
                return self.delete_file(file_path)
            elif command.startswith("CREATE_DIR "):
                directory = command[11:]
                return self.create_directory(directory)
            elif command.startswith("CREATE_FILE "):
                file = command[12:]
                return self.create_file(file)
            elif command.startswith("MOV "):
                source, destination = command[4:].split()
                return self.move_file(source, destination)
            elif command.startswith("RENAME "):
                old_name, new_name = command[6:].split()
                return self.rename_file(old_name, new_name)
            elif command == "CLEAR":
                return self.clear_screen()
            elif command == "QUIT":
                return "Exiting Command Prompt GUI."
            else:
                return "Invalid command. Type 'HELP' for assistance."
        except Exception as e:
            return f"Error: {str(e)}"

    def display_help(self):
        help_text = """
        Available commands:
        LS              Displays a list of files and subdirectories in a directory.
        NAVIGATE        Changes the current directory.
        CY              Copies one or more files to another location.
        REMOVE_DIR      Deletes one or more folders.
        REMOVE_FILE     Deletes one or more files.
        CREATE_DIR      Creates a new directory.
        CREATE_FILE     Creates a new File.
        MOV             Moves one or more files from one directory to another.
        RENAME          Renames a file or directory.
        CLEAR           Clears the screen.
        QUIT            Quits the program.
        HELP            Provides help information for commands.
        """
        return help_text

    def display_directory_contents(self, directory):
        contents = os.listdir(directory)
        return "Directory of " + directory + "\n" + "\n".join(contents)

    def change_directory(self, directory):
        try:
            os.chdir(directory)
            return "Directory changed to " + os.getcwd()
        except FileNotFoundError:
            return "Directory not found."

    def copy_files(self, source, destination):
        try:
            shutil.copy(source, destination)
            return "File copied successfully."
        except FileNotFoundError:
            return "File not found."

    def delete_dir(self, directory):
        try:
            os.rmdir(directory)
            return "Folder deleted successfully."
        except FileNotFoundError:
            return "Folder not found."

    def delete_file(self, file_path):
        try:
            os.remove(file_path)
            return "File deleted successfully."
        except FileNotFoundError:
            return "File not found."

    def create_directory(self, directory):
        try:
            os.mkdir(directory)
            return "Directory created successfully."
        except FileExistsError:
            return "Directory already exists."

    def create_file(self, filename):
        try:
            if os.path.exists(filename):
                return f"The file '{filename}' already exists."
            else:
                with open(filename, 'w') as file:
                    file.write("")
                return f"File '{filename}' created successfully."
        except FileExistsError:
            return "Directory already exists."

    def move_file(self, source, destination):
        try:
            shutil.move(source, destination)
            return "moved successfully."
        except FileNotFoundError:
            return "not found."

    def rename_file(self, old_name, new_name):
        try:
            os.rename(old_name, new_name)
            return "renamed successfully."
        except FileNotFoundError:
            return "not found."

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    app = CommandPromptGUI()
    app.mainloop()
