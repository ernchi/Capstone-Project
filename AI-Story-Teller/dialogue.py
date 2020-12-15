import re
with open('shakespeare.txt', 'r') as file:
    data = file.read().replace('\n', '')

    delimiters = ". ", ".\n"
    segments =re.split(r'[.?!]\s*', data)
    dialogue = ""
    for x in range(0, len(segments)):
        if segments[x].isupper():
            dialogue += segments[x + 1]
            if segments[x+2].isupper() is False:
                dialogue += segments[x + 2]
                break
            else:
                break


    if dialogue == "":
        print("no dialogie found")
    
    print (dialogue)