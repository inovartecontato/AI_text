import random
longterm_memory = []
longterm_associations = []
longterm_sequences = []
totalcombinations = []
generalizations = []
generalized_memories = []
mcounts = dict()
awareness = []
context = []
idea = []
solutions = []
guess = ""
externalinput = ""
awake = 1
lowestQMamount = 100

def analyze(str): #separate string by patterns and throw it in the awareness list
    global awareness
    global mcounts
    global context
    counts = dict()
    words = str.split()        
    if len(words) <= 1:
        return "?"

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    for word in words:
        if word in mcounts:
            counts[word] = mcounts[word]
            #print(mcounts[word])
        else:
            pass

    try:
        del counts['?']
    except KeyError:
        pass
    
    mostcommon_li = sorted(counts.items(), key=lambda x: x[1], reverse=True)   
    
    #print(mostcommon_li)
    pattern = " " + str + " "
    nopattern = " " + str + " "
    difference = " " + str + " "
    size = int(len(mostcommon_li))
    
    size -= 1
    index = 0
    if size <= 1:
        return "?"
        
    b = mostcommon_li[index]
    d = mostcommon_li[size]
    f = mostcommon_li[size - 1]
    
    create_association(f[0],d[0]) #create associations for the least common words and remember relevant info
    context.append(d[0])
    context.append(f[0])
    remember(d[0])
    remember(f[0])
    
    
    while b[0] == "?":
        index += 1
        if index in range(-len(mostcommon_li), len(mostcommon_li)):            
            b = mostcommon_li[index]
        else:
            return "?"    
    
    while d[0] == "?":
        size -= 1
        if size in range(-len(mostcommon_li), len(mostcommon_li)):
            d = mostcommon_li[size]
        else:
            return "?"
        
    bb = " " + b[0] + " "
    dd = " " + d[0] + " "
    
    remember(d[0]) #look for matches for the least common word in the sentence
    
    pattern = pattern.replace(bb," ? ")
    nopattern = nopattern.replace(dd," ? ")
    difference = difference.replace(bb," ? ")
    difference = difference.replace(dd," ? ")
    pattern = pattern.replace(bb," ? ")    
    nopattern = nopattern.replace(dd," ? ")
    difference = difference.replace(bb," ? ")
    difference = difference.replace(dd," ? ")
    difference = difference.replace(bb," ? ")
    difference = difference.replace(dd," ? ")
    #print("most common     : " + pattern)
    awareness.append(pattern)
    #print("remaining info  : " + difference)
    awareness.append(difference)
    #print("most different  : " + nopattern)
    awareness.append(nopattern)
    awareness.append(generalize_sentence(nopattern))
    return "analysis complete"

def remember(str): #find matches for a string in longterm_memory and returns it to the idea list
    global idea
    global longterm_memory
    for i in longterm_memory:
        if str in i:
            idea.append(i)
            
        if len(idea) <= 20:
            examinefurther = str.split()
            for x in examinefurther:
                if x != "?":
                    if x in i:
                        idea.append(i)
                        
    return "done"
                    
def wakeup(): #reads memory.txt into longterm_memory list
    global longterm_memory
    global longterm_associations
    global longterm_sequences
    try:
        with open('sequences.txt', 'r') as file:
            lines = []
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]
            longterm_sequences = lines
            #print(longterm_memory)
            file.close()
      
            
        with open('memories.txt', 'r') as file:
            lines = []
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]
            longterm_memory = lines
            #print(longterm_memory)
            file.close()
      
            
        with open('associations.txt', 'r') as file:
            lines = []
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]
            longterm_associations = lines
            #print(longterm_memory)
            file.close()
            return "done"
    except:
        return "file not there yet"
                          
def sleep(): #commit everything the bot knows to memory.txt
    global awareness
    global solutions
    global idea
    global longterm_memory
    
    memorize = awareness #+ idea + longterm_memory
    for x in memorize:
        x = cleanlines(x)
        
    memorize = list(dict.fromkeys(memorize))
    with open('memories.txt', 'a+') as file:
        for line in memorize:
            line = cleanlines(line)
            for i in file:
                if i == line:
                    pass
                    
            file.write(line)
            #print("remembered: " + line)
            file.write('\n')
        
        file.close()
        awareness = [] #clean awareness
        solutions = [] #clean solutions
        idea = []
        wakeup()
        return "done"
        
def cleanlines(s): #removes blank spaces on the front of the lines
    if (s[0] == " "):
        return s[1:]
    else: 
        return(s)

def combine(one, two): #combines two strings filling in the "?" when possible and return the results to solutions list
    firstphrase = one.split()
    #print(firstphrase)    
    global lowestQMamount
    secondphrase = two.split()
    #print(secondphrase)                         
    #print(firstphrase)
    resulting_list = []
    if len(firstphrase) <= len(secondphrase):
        for i in range(len(firstphrase)):
            resulting_list.append(firstphrase[i] if firstphrase[i] != "?" else secondphrase[i])
        
    if len(firstphrase) > len(secondphrase):
        for i in range(len(secondphrase)):
            resulting_list.append(secondphrase[i] if secondphrase[i] != "?" else firstphrase[i])
        
    solution = str(' '.join(resulting_list))    
    
    currentQMamount = solution.count('?')
    
    if currentQMamount > lowestQMamount:
        solutions.append(solution)        
    
    if currentQMamount <= lowestQMamount:
        if solution == externalinput and len(solution) >= 1:
            solutions.insert(1, solution)
        else:
            solutions.insert(0, solution)
        
        lowestQMamount = currentQMamount
       
    return "done"
        
def test(): #debugging tool
    print("awareness: ", awareness)
    print("solutions: ", solutions)
    print("ideas: ", idea)
    #print("longterm memory: ", longterm_memory)
  
def removedoublememories():
    try:
        lines = open('associations.txt', 'r').readlines()
        lines_set = set(lines)
        out  = open('associations.txt', 'w')
        for line in lines_set:
            out.write(line)
        
        lines = open('sequences.txt', 'r').readlines()
        lines_set = set(lines)
        out  = open('sequences.txt', 'w')
        for line in lines_set:
            out.write(line)
        
        lines = open('memories.txt', 'r').readlines()
        lines_set = set(lines)
        out  = open('memories.txt', 'w')
        for line in lines_set:
            out.write(line)
    except:
        return "file not there yet"

def memorymap():
    global mcounts
    for x in longterm_memory:        
        words = x.split()        
        if len(words) <= 1:
            return "?"

        for word in words:
            if word == "?":
                break
                
            if word in mcounts:
                mcounts[word] += 1
            else:
                mcounts[word] = 1

def create_association(one,two):
    memorize = one + " " + two
    #print(memorize)
    #print("association between :" + memorize + "found")
    
    with open('associations.txt', 'a+') as file:
            memorize = cleanlines(memorize)
            for line in file:
                if line == memorize:
                    file.close()
                    return "association already known"
                    
            file.write(memorize)
            file.write('\n')        
            file.close()

def unscramble_list_sequentially(list): #check the combination of each two against sequencer words and then spit ou a list
    resulting_sentence_li = []
    backup = list
    for index, elem in enumerate(list):
        if (index+1 < len(list)):
            for indx, elem2 in enumerate(list):
                if index == indx:
                    pass
                    
                testphrase = elem + " " + elem2
                for index_2, i in enumerate(longterm_sequences):
                    if i == testphrase:
                        #print("verificando: " + testphrase + i)
                        resulting_sentence_li.append(testphrase)
                    else:
                        if index_2 >= len(longterm_sequences):
                            resulting_sentence_li.append(elem)
                        else:
                            pass
                        
    #print("testing -----")
    #print(resulting_sentence_li)
    temporary_sentence = " ".join(resulting_sentence_li)
    temporary_li = temporary_sentence.split()
    for index_li, elem in enumerate(temporary_li):
        if index_li+1 < len(temporary_li):
            if elem == temporary_li[index_li + 1]:
                del temporary_li[index_li +1]
        
        
    #list = resulting_sentence_li
    for i in backup:
        if i not in temporary_li:
            temporary_li.insert(0,i)
    list = temporary_li
    #print(resulting_sentence_li)
    #print(" ".join(list))
    return(list)
            
def elaborarte(str,int):
    number_of_words = int
    initial_input = str
    initial_input_li = initial_input.split()
    size = len(initial_input_li)
    last_word = initial_input_li[size - 1]
    print(last_word, end=" ")
    for i in range(0,number_of_words):
        looping_index = len(longterm_sequences)
        for x in range(0,looping_index):
            sequence_spl = longterm_sequences[x].split()
            if last_word == sequence_spl[0]:
                print(sequence_spl[1], end=" ")
                newsplit = last_word.split()
                sizze = len(newsplit)
                sizze -=1
                last_word = sequence_spl[1]
                i += 1
                x = looping_index
            else:
                pass
                
    print("-- ")
                
    
def organize_sentence(str,int):
    words = str.split()
    global totalcombinations
    newcombination = []
    newsentence = ""
    matcheshighscore = 0
    matchesscore = 0
    for i in range(0,int): 
        random.shuffle(words)        
        newsentence = ' '.join(words) 
        #print(newsentence)
        for x in longterm_associations:
            if x in newsentence:
                matchesscore += 1
                if matchesscore > matcheshighscore:
                    totalcombinations.insert(0, newsentence)
                    matcheshighscore = matchesscore
                    matchesscore = 0
                else:
                    totalcombinations.append(newsentence)
                    matchesscore = 0
                    
def sort_by_occurrence(str):
    new_di = dict()
    new_li = str.split()
    second_li = []
    for x in new_li:
        if x in new_di:
            new_di[x] += 1
        else:
            new_di[x] = 1
    
    new_li_sorted = sorted(new_di.items(), key=lambda x: x[1], reverse=True)   
    #return
    for y in new_li_sorted:
        second_li.append(y[0])
        #print(y[0])
        
    xx = ' '.join(second_li) 
    str = xx
    #print(str)
    return xx

def generalize_sentence(str):
    #return "error"
    sentence = str.split()
    #print(sentence)
    replacement = []
    original_sentence = str.split()
    resulting_sentence = sentence
    index = 0
    for i in sentence:
        word = original_sentence[original_sentence.index(i)]        
        newword = ""
        for x in generalizations:
            if word in x:
                replacement = x.split() 
                #print(resulting_sentence)
                #print("original sentence:")
                #print(original_sentence)
                original_sentence = str.split()
                index = original_sentence.index(word)
                resulting_sentence[index] = replacement[0]
                pass
                #print("with : " + i)
  
               
        #index +=1    
        #replacement.append(newword)
        
    newsentence = ' '.join(replacement) 
    #print(replacement)
    resulting_answer = ' '.join(resulting_sentence)
    #print("generalized answer :")
    #print(resulting_answer)
    replacement = []
    newsentence = ""
    return resulting_answer
            
def dothething(inlist):
    if len(inlist) == 0:
        return "?"
        
    inlist.sort()
    output = inlist[0]
    outlist = []
    for i in range(1, len(inlist)):
        el = inlist[i].split(" ")
        if el[0] in output or el[1] in output:
            output += " " + inlist[i]
        else:
            outlist.append(output)
            output = inlist[i]
    outlist.append(output)
    #print(outlist)
    return outlist

def merge(s1, s2):
    i = 0
    while not s2.startswith(s1[i:]):
        i += 1
    return s1[:i] + s2

def remember_sequence(sentence):
    sequence_li = sentence.split()
    global longterm_sequences
    #if (len(sequence_li) % 2) != 0:
    #    del sequence_li[len(sequence_li)]
        
    for index, elem in enumerate(sequence_li):
        if (index+1 < len(sequence_li)):
            #prev_el = str(sequence_li[index-1])
            curr_el = str(elem)
            next_el = str(sequence_li[index+1])
            
            longterm_sequences.append(curr_el +" "+ next_el)
            
    
    for t in longterm_sequences:
        if t.count(" ") >= 2:
            print(t)
            del longterm_sequences[t]
        
    longterm_sequences = list(dict.fromkeys(longterm_sequences))
    memorize = longterm_sequences
    with open('sequences.txt', 'a+') as file:
        for line in memorize:
            line = cleanlines(line)
            file.write(line)
            file.write('\n')
        file.close()
    #print(longterm_sequences)
    return "done"

removedoublememories()
wakeup()
memorymap()
longterm_associations = list(dict.fromkeys(longterm_associations)) #remove duplicate associations

#mostcommon_general = sorted(mcounts.items(), key=lambda x: x[1], reverse=True)  
#print(mostcommon_general)
runs = 0

while awake == 1:
    #print(longterm_associations)
    externalinput = input("Q :")
    elaborarte(externalinput,20)
    remember_sequence(externalinput)
    longterm_sequences = list(dict.fromkeys(longterm_sequences)) #remove duplicate sequences
    
    #sort_by_occurrence(externalinput)
    #externalinput = " " + externalinput
    analyze(externalinput)
    awareness = list(dict.fromkeys(awareness))#remove duplicates from awareness
    
    #create_generalizations(longterm_associations)
    #generalize()
    new_generalizations = dothething(longterm_associations)
    for i in new_generalizations:
        generalizations.append(sort_by_occurrence(i))
    
    #print(generalizations)
    #generalizations = list(dict.fromkeys(generalizations)) #remove duplicate generalizations
        

    #print(generalizations)
    generalized_memories = []
    generalized_input = generalize_sentence(externalinput)
    best_general_answer_score = 0
    general_answer_score = 0
    for memory in longterm_memory:
        i = generalize_sentence(memory)
        i_li = i.split()
        for xy in i_li:
            if xy in generalized_input:
                general_answer_score +=1
                if general_answer_score > best_general_answer_score:
                    generalized_memories.insert(0,i)
                    best_general_answer_score = general_answer_score
    
    if len(generalized_memories) > 0:
        testing = generalized_memories[0]
        other_li = unscramble_list_sequentially(testing.split())
        testing = " ".join(other_li)
        string1 = testing
        words = string1.split()
        print("-------------------thought------------------------")
        print ("G :"+" ".join(sorted(set(words), key=words.index)))
        print("--------------------------------------------------")
        generalized_memories = []
    
    awareness.append(externalinput)    
    
    for i in awareness:
        remember(i)        
    
    idea = list(dict.fromkeys(idea))
    #awareness = awareness + idea
    
    for y in awareness:
        for n in idea:
            combine(y,n)

            #mix the two strings then find the result that has the least ?? signs
    #test()
    solutions = list(dict.fromkeys(solutions)) #remove duplicate solutions
    
    contextual_sol = []
    clues_highscore = 0
    clue_amount = 0
    
    for x in contextual_sol:
        x = cleanlines(x)
    
    #for x in contextual_sol:
    #    x = cleanlines(x)
    
    if len(solutions) > 0: # find the most useful solution from the list
        for solution in solutions: 
            clue_amount = 0
            for clue in context:                
                if clue in solution:
                    clue_amount += 1 #make this number bigger to result in more contextually relevant answers, smaller makes it more value precedent more
                    for precedent in longterm_associations: #if clue is in longtem associations add it more weight to it
                        if clue in precedent:
                            clue_amount += 1
                            
                    if clue_amount > clues_highscore and solution != externalinput:
                        contextual_sol.insert(0,solution)
                        clues_highscore = clue_amount
                    else:
                        contextual_sol.append(solution)
                    
       # print(contextual_sol)
        if len(contextual_sol) > 0:
            selected_solution = contextual_sol[0]
            organize_sentence(selected_solution,1000)
            if len(totalcombinations) > 0:
                selected_solution = totalcombinations[0]
                other_li = unscramble_list_sequentially(selected_solution.split())
                testing = " ".join(other_li)
                string1 = testing
                words = string1.split()
                print ("AI:"+" ".join(sorted(set(words), key=words.index)))
                #print("Ai :" + testing)
                totalcombinations = []
            else:
                other_li = unscramble_list_sequentially(selected_solution.split())
                testing = " ".join(other_li) 
                string1 = testing
                words = string1.split()
                print ("AI:"+" ".join(sorted(set(words), key=words.index)))
                totalcombinations = []
        else:
            selected_solution = solutions[0]
            organize_sentence(selected_solution,1000)
            other_li = unscramble_list_sequentially(selected_solution.split())
            testing = " ".join(other_li) 
            string1 = testing
            words = string1.split()
            print ("AI:"+" ".join(sorted(set(words), key=words.index)))
        
    sleep()
    removedoublememories()
    