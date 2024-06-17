import subprocess
import os


def run_main():
    # Define the path to the main.py file
    main_file_path = os.path.join("src", "main.py")

    # Check if the file exists
    if not os.path.isfile(main_file_path):
        print(f"Error: {main_file_path} does not exist.")
        return

    # Execute the main.py file
    result = subprocess.run(["python3", main_file_path], capture_output=True, text=True)

    # Print the output and errors (if any)
    print(result.stdout)
    if result.stderr:
        print(f"Error: {result.stderr}")


if __name__ == "__main__":
    run_main()
