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
    

def formatText(s , type):
    if(type == 'red'):
        return ("\033[91m " + s + " \033[00m")
    if(type == 'green'):
        return ("\033[92m" + s + "\033[00m")
    if(type == 'bold'):
        return ('\033[1m' + s + '\033[0m')
    return  s 

def getInput(sentence , start_time , mode):

    print("\r                           ",end="")
    click.echo("\rGo... : ", nl = False)
    finished = False
    mistakes = 0
    corrects = 0
    # String initiation for storing characters in after typing of each character (st)
    result = ""
    st = ""
    # Word count showing current iteration of word
    word = 0
    
    # While loop for as long as length of user typed string is less the string to be typed ( Replace is used for removing red colours from string)
    while len(sentence) > (len(st.replace("\033[91m","").replace("\033[00m" , ""))):
        if finished:  break
        if(mode == "1" and time.time() - start_time >= 60): break
        # Get char gets a character as input
        c = click.getchar(echo=False)
        # "\x08" is the code for backspace key
        if(c == "\x08"):
            # Dont include the last character
            lastCharacters = st[-5:]
            lengthOfStr = len(st.replace("\033[91m","").replace("\033[00m" , "")) 
            if(lastCharacters == "\033[00m"):
                charsToExculde = 5 + 5 + 1
                st = st[:(len(st) - charsToExculde)]
                mistakes = mistakes - 1
            else:
                st = st[:len(st) - 1]
                corrects = corrects - 1
            word = word - 1

            # click.echo(("\r"+"        " + ( " " * lengthOfStr) ), nl=False)
            click.clear()
            
            print( f" \n Type the sentence given in BOLD writing below: \n\n" + (5 * " ") +"\"" + formatText(sentence , 'bold'))
            print()
            click.echo("\r"+"Go... : " + st , nl=False)

            # Enter key produced "\r" code
        elif(c == "\r"):
            finished = True

# repr() changes a character to raw form like for (a) it will be ('a') and for any special keys it will be a code with len > 3
#  hence only alphabets will pass
        elif(len(repr(c)) == 3):
            # c = c[-1]
            withoutFormattingS = st.replace("\033[91m","").replace("\033[00m" , "")
            withoutFormattingS = withoutFormattingS + c
            if(withoutFormattingS[word] != sentence[word]):
                winsound.Beep(2000,30)
                st = st + ("\033[91m" + c + "\033[00m")
                mistakes += 1
            else: 
                st = st + c
                corrects = corrects + 1
            click.clear()
            print( f" \n Type the sentence given in BOLD writing below: \n\n" + (5 * " ") +"\"" + formatText(sentence , 'bold'))
            print()
            click.echo("\r"+"Go... : " +st , nl=False)
            word = word + 1
            
            # print(st , end="")
        
    withoutFormattingS = st.replace("\033[91m","").replace("\033[00m" , "")

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
    if minScore >= userScore :
        return "",changedUserId
    
    name = input("Enter your username  (Max 16 characters): ")
    while len(name) > 16: name = input("Enter your username  (Max 16 characters): ")

    if name == "" : name = "guest"

    for i in range(len(lines.split("\n"))):
        j = lines.split("\n")[i]
        current_i_score = int(j.split(",")[-1])

        if(userScore > current_i_score ):
            if(changedUserId == 99): changedUserId = i + 1
            lines = lines.replace(j,f"{name},{round(w_p_min)},{round(userScore)}")

            name = j.split(",")[0]
            w_p_min = int(j.split(",")[1])

            userScore = current_i_score
            continue
    text_file.close()
    text_file = open("leaderboard.txt", "w")
    text_file.write(lines)
    text_file.close()
    return lines , changedUserId

# Function to calculate typing speed in WPM
def calculate_wpm(time_taken, sentence):
    print(sentence , "Sentenced to Death!")
    sentence_length = len(sentence)
    # WPM in case of time less than 1 min
    # in that case time in second will be checked what multiple of a minute it is 
    # then the sentence length will be multiplied by the same multiple to calculate in 1 complete min
    time_in_mins = time_taken / 60
    words = sentence_length / 5
    print(words, time_taken ,time_in_mins , words/time_in_mins)

    return words / time_in_mins


# Function to print leaderboard in a tabular form
def print_leaderboard(leaderboard,userI):
    lines = leaderboard.split("\n")
    print(f"{"Position": <10}|    {"Name": <20}    |    {"Words Per Minute": <20}    |    {"Accuracy": <20}")
    print(f"--------------------------------------------------------------------------------------------")

    for i in range(len(lines)):
        if(userI == i + 1):
            s = f"    {i + 1: 4d}  |    {lines[i].split(",")[0]: <20}    |     {lines[i].split(",")[1]: <20}    |     {(int(lines[i].split(",")[2])-int(lines[i].split(",")[1])): <20} "
            print(formatText(s , 'green'))
            print("-" * ( len(s) -10))
            continue
        s = f"    {i + 1: 4d}  |    {lines[i].split(",")[0]: <20}    |     {(lines[i].split(",")[1]): <20}    |     {(int(lines[i].split(",")[2])-int(lines[i].split(",")[1])): <20} "
        print(s)
        print("-" * ( len(s) - 10))

# Main Function Of The Program
def start_typing_test():
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
    print( f" \n Type the sentence given in BOLD writing below: \n\n" + (5 * " ") +"\"" + formatText(sentence , 'bold'))
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
    print(f"Your accuracy is {accuracy: .2f}")
    print("\n")
    lb = ""
    if(accuracy > 60): 
        while(lb != "1" and lb != "2"): lb = input("Showoff your skill in the leaderboard? \n (1 for Yes) \n (2 for No) \n Choice: ")

    if(lb  != "2"):        
        updated , userI = update_leaderboard(wpm , round(accuracy))
        if( userI == 99 ): print(formatText("Alas...! You did not make it to the leaderboard this time.!!" , 'red')) 
        else:
            print_leaderboard(updated , userI )

    print("Sayonara!")

start_typing_test()

# text.txt file contains random sentences of which 1 is picked at random
# leaderboard contains usernames with wpm and (wpm + accuracy) in the form (user,wpm,score) repectively

