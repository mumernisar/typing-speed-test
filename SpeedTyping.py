import random
import time
# click is an external library used for getting a single character input at a time
import click
import winsound
# Function to generate a random sentence from a file (text.txt)

def generate_random_sentence(mode):
    text_file = open("text.txt", "r")
    lines = text_file.readlines()
    if mode == '1':
        return random.choice(lines).replace("\n" , "") + random.choice(lines)
    return random.choice(lines)

# Function for printing the current string each time a character is entered
# checks if there were any errors made with if "^^red^^"...then for each(while loop) red found it get the index of middle character
# and add it to the redIndexes list which is then later used by for loop to print accodingly
def printStr_Helper(st):
    temp = st
    redIndexes = []
    if "^^red^^" in st:
        start = 0
        while "^^red^^" in temp:
            i = temp.find("^^red^^")
            redIndexes.append(i + 7 + ( start * 14))
            temp = temp.replace("^^red^^" ,"", 2)
            start +=1
        click.echo("\rGo... : " , nl = False)
        start = 0
        for i in redIndexes:
            click.echo(st[start:i-7], nl=False)
            click.echo(click.style(st[i:i+1] , bg='red'), nl=False)
            start = i+1+7
            
    else:
            click.echo("\rGo... : " + st , nl = False)

def getInput(sentence , start_time , mode):
    print("\r                           ",end="")
    click.echo("\rGo... : ", nl = False)
    finished = False
    mistakes = 0
    corrects = 0
    # String initiation for storing characters in after typing of each character (st)
    st = ""
    # Word count showing current iteration of word
    word = 0
    # While loop for as long as length of user typed string is less the string to be typed ( Replace is used for removing red colours from string)
    while len(sentence) > (len(st)):
        if finished:  break
        if(mode == "1" and time.time() - start_time >= 60): break
        # Get char gets a character as input
        c = click.getchar()
        # "\x08" is the code for backspace key
        if(c == "\x08" and word != 0):
            # Dont include the last character
            # rep = repr(st)[:-1]
            lastCharacters = st[-7:]
            # Check if the last characters in the st are from backspace code "^^red^^"
            if(lastCharacters == "^^red^^"):
                charsToExculde = 7 + 7 + 1
                st = st[:(len(st) - charsToExculde)]
                mistakes = mistakes - 1
            else:
                st = st[:len(st) - 1]
                corrects = corrects - 1
            word = word - 1
            click.clear()
            click.echo(f" \n Type the sentence given in BOLD writing below: \n\n" + (5 * " ") , nl=False )
            click.echo(click.style(sentence , bold= True))
            print()
            printStr_Helper(st)

        # Enter key produced "\r" code
        elif(c == "\r" and corrects > 60):
            finished = True
# repr() changes a character to raw form like for (a) it will be ('a') and for any special keys it will be a code with len > 3
#  hence only alphabets will pass
        if(len(repr(c)) == 3):
            withoutFormattingS = st.replace("^^red^^","")
            withoutFormattingS = withoutFormattingS + c
            print()
            print(withoutFormattingS , "without formating s")
            if(withoutFormattingS[word] != sentence[word]):
                winsound.Beep(2000,30)
                st = st + ("^^red^^" + c + "^^red^^")
                mistakes += 1
            else:
                st = st + c
                corrects = corrects + 1
            click.clear()
            click.echo(f" \n Type the sentence given in BOLD writing below: \n\n" + (5 * " ") , nl=False )
            click.echo(click.style(sentence , bold= True))
            print()
            printStr_Helper(st)
            word = word + 1

    withoutFormattingS = st.replace("^^red^^","")
    return withoutFormattingS , corrects

# Function to update leader if user choses to
def update_leaderboard(w_p_min , accuracy):
    # Function will check if the current variable score is higher score than current iteration score  if so ...,
    # it will replace them with variable score and put the iteration score in variable for the next cycle

# 99 is taken as an impossible number if this number is returned from function as is..! function will deduce the user did not make
# to leaderboard
    changedUserId = 99
    text_file = open("leaderboard.txt", "r")
    lines = text_file.read()
    userScore = (w_p_min + accuracy)
    minScore = int(lines.split("\n")[-1].split(",")[-1])

    # If last person has better score then dont execute loop
    name = input("Enter your username  (Max 16 characters): ")
    while len(name) > 16: name = input("Enter your username  (Max 16 characters): ")

    if(lines == ""):
        lines = f"\n{name},{round(w_p_min)},{round(userScore)}"
        text_file.close()
        text_file = open("leaderboard.txt", "w")
        text_file.write(lines)
        text_file.close()
        return lines,len(lines.split("\n")[-1])

    if minScore >= userScore :
        lines = lines + f"\n{name},{round(w_p_min)},{round(userScore)}"
        text_file.close()
        text_file = open("leaderboard.txt", "w")
        text_file.write(lines)
        text_file.close()
        return lines,len(lines.split("\n")[-1])


    for i in range(len(lines.split("\n"))):
        j = lines.split("\n")[i]
        current_i_score = int(j.split(",")[-1])
        if(userScore > current_i_score ):
            if(changedUserId == 99): changedUserId = i + 1
            lines = lines.replace(j,f"j\n{name},{round(w_p_min)},{round(userScore)}")
            # lines = lines.split("\n")[:-1]
            break
    text_file.close()
    text_file = open("leaderboard.txt", "w")
    text_file.write(lines)
    text_file.close()
    return lines , changedUserId

# Function to calculate typing speed in WPM
def calculate_wpm(time_taken, sentence):
    sentence_length = len(sentence)
    time_in_mins = time_taken / 60
    words = sentence_length / 5
    return words / time_in_mins

# Function to print leaderboard in a tabular form
def print_leaderboard(leaderboard,userI):
    lines = leaderboard.split("\n")
    print(f"{"Position": <10}|    {"Name": <20}    |    {"Words Per Minute": <20}    |    {"Accuracy": <20}")
    print(f"--------------------------------------------------------------------------------------------")
    for i in range(len(lines)):
        if(userI == i + 1):
            s = f"    {i + 1: 4d}  |    {lines[i].split(",")[0]: <20}    |     {lines[i].split(",")[1]: <20}    |     {(int(lines[i].split(",")[2])-int(lines[i].split(",")[1])): <20} "
            click.secho(s, color='green')
            print("-" * ( len(s) -10))
            continue
        s = f"    {i + 1: 4d}  |    {lines[i].split(",")[0]: <20}    |     {(lines[i].split(",")[1]): <20}    |     {(int(lines[i].split(",")[2])-int(lines[i].split(",")[1])): <20} "
        print(s)
        print("-" * ( len(s) - 10))

# Main Function Of The Program
def begin():
    print(" " * 10 , "________                 _________   ________           _____ ")
    print(" " * 10 , "__  ___/_______________________  /   ___  __/_____________  /_")
    print(" " * 10 , "_____ \\___  __ \\  _ \\  _ \\  __  /    __  /  _  _ \\_  ___/  __/")
    print(" " * 10 , "____/ /__  /_/ /  __/  __/ /_/ /     _  /   /  __/(__  )/ /_  ")
    print(" " * 10 , "/____/ _  .___/\\___/\\___/\\__,_/      /_/    \\___//____/ \\__/  ")
    print(" " * 10 , "        /_/                                                   ")
    mode = input("Select mode: \n 1. One minute Rush \n 2. Speed Test \n Choice: ")
    while mode != "1" and mode != "2": mode = input("Select mode: \n 1. One minute Rush \n 2. Speed Test \n Choice: ")
    click.clear()
    sentence = generate_random_sentence(mode)
    click.echo(f" \n Type the sentence given in BOLD writing below: \n\n" + (5 * " ") , nl=False )
    click.echo(click.style(click.style(sentence , bold= True)))
    print()
    # While loop to give the user time (n seconds) to get ready for the test
    remainingTime = 3
    while remainingTime > 0:
        print(f" \rBegin in {remainingTime} seconds ⏰" , end="" )
        time.sleep(1)
        remainingTime = remainingTime - 1
        print(f" \rBegin in {remainingTime} seconds ⏰" , end="" )
    start_time = time.time()
    input_text , correctCount = getInput(sentence , start_time , mode)
    end_time = time.time()
    time_taken = end_time - start_time
    wpm = calculate_wpm(time_taken, input_text)
    print(f"\nYou took {round(time_taken)} seconds to type the sentence, achieving a speed of \033[92m {round(wpm)} \033[00m WPM.")
    accuracy = ((correctCount)/len(input_text)) * 100
    print(f"Your accuracy is {accuracy: .2f} \n")
    lb = ""
    if(accuracy > 60):
        while(lb != "1" and lb != "2"): lb = input("Showoff your skill in the leaderboard? \n (1 for Yes) \n (2 for No) \n Choice: ")
    if(lb  == "1"):
        updated , userI = update_leaderboard(wpm , round(accuracy))

        if( userI == 99 ): click.secho("Alas...! You did not make it to the leaderboard this time.!!" , 'red')
        else: print_leaderboard(updated , userI )

    take_again = input("Try again ?? : [y/n]")
    if(take_again == "y" ): begin()
    else:
        print("Sayonara!")
begin()
