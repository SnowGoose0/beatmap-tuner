file_name = "test.txt"
file_contents = ""
# Open the file in read mode
with open(file_name, "r") as file:
    # Read the contents of the file into a string
    file_contents = file.read()

print("a\nb\nc\n\n".split('\n')[:-1])