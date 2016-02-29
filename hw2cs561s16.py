#@author Sagar Makwana

#---------------------------------------Function Definitions------------------------------------------------

def convertRuleToDict(rule):
    #The dictionary that is to be returned after converting the rule into dictionary.
    ruleDict = ''

    implicationSplit = rule.split(' => ')

    #If it is a complex sentence
    if len(implicationSplit) == 2:
        #Premise Section
        conjunctionSplit = implicationSplit[0].split(" && ")
        ruleDict = {'premiseCount':len(conjunctionSplit)}

        for i in range(0,len(conjunctionSplit)):
            premise = conjunctionSplit[i].strip()

            if premise[0] == '~':
                ruleDict['premise'+str(i+1)] = {'not': True}
                premise = premise[1:]
            else:
                ruleDict['premise'+str(i+1)] = {'not': False}

            name = premise[0:premise.index('(')]
            variables = premise[premise.index('(')+1:premise.index(')')]
            variables = variables.split(',')
            varCount = len(variables)

            ruleDict['premise'+str(i+1)]['varCount'] = varCount
            ruleDict['premise'+str(i+1)]['variables'] = variables
            ruleDict['premise'+str(i+1)]['name'] = name

        #Conclusion Section
        conclusion = implicationSplit[1].strip()

        if conclusion[0] == '~':
            ruleDict['conclusion'] = {'not': True}
            conclusion = conclusion[1:]
        else:
            ruleDict['conclusion'] = {'not': False}

        name = conclusion[0:conclusion.index('(')]
        variables = conclusion[conclusion.index('(')+1:conclusion.index(')')]
        variables = variables.split(',')
        varCount = len(variables)

        ruleDict['conclusion']['varCount'] = varCount
        ruleDict['conclusion']['variables'] = variables
        ruleDict['conclusion']['name'] = name


    #If it is an atomic sentence
    elif len(implicationSplit) == 1:

        ruleDict = {'premiseCount': 0}

        conclusion = implicationSplit[0].strip()

        if conclusion[0] == '~':
            ruleDict['conclusion'] = {'not': True}
            conclusion = conclusion[1:]
        else:
            ruleDict['conclusion'] = {'not': False}

        name = conclusion[0:conclusion.index('(')]
        variables = conclusion[conclusion.index('(')+1:conclusion.index(')')]
        variables = variables.split(',')
        varCount = len(variables)

        ruleDict['conclusion']['varCount'] = varCount
        ruleDict['conclusion']['variables'] = variables
        ruleDict['conclusion']['name'] = name

    return ruleDict







#----------------------------------------Input and Control--------------------------------------------------

#filename = sys.argv[-1]
filename = 'input.txt'

#Reading the input file
inputFile = open(filename)

#Reading the goal Inference
goalInference = inputFile.readline().strip()

#Reading the Knowledge Base
kbCount = int(inputFile.readline().strip())
KNOWLEDGE_BASE = []

for i in range(0,kbCount):
    rule = inputFile.readline().strip()
    KNOWLEDGE_BASE.append(convertRuleToDict(rule))
    print KNOWLEDGE_BASE[i]


