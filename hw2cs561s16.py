#@author: Sagar Bharat Makwana
#Last Updated at 21:12 PST on 03/05/2016

from copy import deepcopy
#-------------------------------------Classes and Function Definitions------------------------------------

#Class representing the knowledge base.
class KNOWLEDGE_BASE:

    #Class variable to keep track of number of rules in the knowledge base.
    ruleCount = 0

    #Constructor
    def __init__(self,listofRules):
        KNOWLEDGE_BASE.ruleCount = len(listofRules)
        self.rules = listofRules[:]

    #This function standardizes all the variable in all the rules beforehand and updates the knowledge base.
    #It has to be called immediately after creating the knowledge base.
    def standardize_knowledge_base(self):

        openIndex = -1
        closeIndex = -1

        ruleCount = 1
        for rule in self.rules:
            remaining = rule[:]
            newRule = ''
            openIndex = remaining.find('(')
            closeIndex = remaining.find(')')

            while (openIndex != -1 and closeIndex != -1):
                variables = remaining[openIndex+1:closeIndex]
                newRule = newRule + remaining[0:openIndex]
                remaining = remaining[closeIndex+1:]

                variables = variables.split(',')

                subsVar = ''
                for l in range (0,len(variables)):
                    variables[l] = variables[l].strip()
                    if ord(str(variables[l][0])) >= 97:
                        subsVar = subsVar + variables[l]+''+str(ruleCount)+', '
                    else:
                        subsVar = subsVar + variables[l] + ', '


                subsVar = '(' + subsVar[0:len(subsVar)-2] + ')'
                newRule = newRule + subsVar

                openIndex = remaining.find('(')
                closeIndex = remaining.find(')')

            self.rules[ruleCount-1] = newRule
            ruleCount = ruleCount + 1

    #It returns all the rules in the knowledge base that match the given goal
    def fetch_rules_for_goal(self,goal):
        goalName = goal[0:goal.index('(')]

        #List of rules that match with goal
        fetched_rules = []

        for rule in self.rules:
            implicationSplit = rule.split(' => ')

            name = ''
            if len(implicationSplit) == 2:
                consequent = implicationSplit[1].strip()
                name = consequent[0:consequent.index('(')]
            else:
                name = rule[0:rule.index('(')]

            if name == goalName:
                fetched_rules.append(rule)

        return fetched_rules

    #It returns all the rules in the knowledge base
    def fetch_all_rules(self):
        return self.rules

#---Unification Function Definitions---

#Implementation of UNIFY in psuedo code
#This function unifies the given x and y and returns a substitution dictionary if there exists a valid substitution
# or else return failure
def unify(x,y,theta):

    theta = deepcopy(theta)

    if theta == 'failure':
        return 'failure'
    elif x==y:
        return theta
    elif isVariable(x):
        return unifyVariables(x,y,theta)
    elif isVariable(y):
        return unifyVariables(y,x,theta)
    elif isCompound(x) and isCompound(y):
        return unify(getArguments(x),getArguments(y),unify(getOperator(x),getOperator(y),theta))
    elif isList(x) and isList(y):
        return unify(getRest(x),getRest(y),unify(getFirst(x),getFirst(y),theta))
    else:
        return 'failure'

#This function returns a boolean saying whether the input var is indeed a variable or not.
def isVariable(var):
    #Check if it is compound statement or list
    if var.find('(') != -1 or var.find(',') != -1:
        return False
    elif ord(str(var[0])) >= 97:
        return True
    else:
        return False

#This function returns a boolean saying whether the input var is indeed a compound statement or not.
def isCompound(var):

    if isVariable(var) == False and var.find('(') != -1:
        return True
    else:
        return False

#This function returns a boolean saying whether the input var is indeed a compound statement or not.
def isList(var):

    if isVariable(var) == False and isCompound(var) == False and var.find(',') != -1:
        return True
    else:
        return False

#It returns the arguments of the given compound statement
def getArguments(var):
    return str(var[var.find('(')+1:len(var)-1]).strip()

#It returns the operator of the given compound statement
def getOperator(var):
    return str(var[:var.find('(')]).strip()

#It returns the first argument in the given list
def getFirst(var):
    return var.partition(', ')[0]

#It returns the arguments excluding the first argument in the given list
def getRest(var):
    return var.partition(', ')[2]

#Implementation of UNIFY-VAR in psuedo code
def unifyVariables(var,x,theta):

    theta = deepcopy(theta)

    if theta.has_key(var):
        return unify(theta[var],x,theta)
    elif theta.has_key(x):
        return unify(var,theta[x],theta)
    else:
        theta[var]=x
        return theta

#---XXUnification Function DefinitionsXX----


#----AND/OR Function Definitions------------

#Implementation of FOL-BC-AK in psuedo code
def FOL_BC_ASK(KB,query):
    return FOL_BC_OR(KB,query,{})

#Implementation of FOL-BC-OR in psuedo code
def FOL_BC_OR(KB,goal,theta):
    for rule in KB.fetch_rules_for_goal(goal):
        lhs,rhs = splitRule(rule)
        for theta1 in FOL_BC_AND(KB,lhs,unify(rhs,goal,theta)):
            yield theta1

#Implementation of FOL-BC-AND in psuedo code
def FOL_BC_AND(KB,goals,theta):
    if theta == 'failure':
        return
    elif len(goals) == 0:
        yield theta
    else:
        first,rest = splitConjunctions(goals)
        for theta1 in FOL_BC_OR(KB,substitution(theta,first),theta):
            for theta2 in FOL_BC_AND(KB,rest,theta1):
                yield theta2

#It returns the LHS and the RHS of the given rule
def splitRule(rule):
    implicationSplit = rule.split(' => ')

    if len(implicationSplit) == 2:
        return implicationSplit[0].strip(),implicationSplit[1].strip()
    else:
        return '',rule.strip()

#It returns the first and the rest of the given conjunctions.
def splitConjunctions(goals):
    conjunctionSplit = goals.split(' && ')

    if len(conjunctionSplit) == 1:
        return goals,''
    else:
        conjunctionPartition = goals.partition(' && ')
        return conjunctionPartition[0].strip(),conjunctionPartition[2].strip()

#It returns a new rule after substituting it with values in theta
def substitution(theta,first):
    openIndex = first.find('(')
    closeIndex = first.find(')')

    variables = first[openIndex+1:closeIndex]
    variables = variables.split(',')
    newRule =first[0:openIndex]

    subsVar = ''
    for l in range (0,len(variables)):
        variables[l] = variables[l].strip()
        if ord(str(variables[l][0])) >= 97 and theta.has_key(variables[l]):
            subsVar = subsVar + theta[variables[l]]+', '
        else:
            subsVar = subsVar + variables[l] + ', '

    subsVar = '(' + subsVar[0:len(subsVar)-2] + ')'
    newRule = newRule + subsVar

    return newRule

#---XXAND/OR Function DefinitionsXX---------

#----------------------------------------Input and Control-----------------------------------------------

#filename = sys.argv[-1]
filename = 'input.txt'

#Reading the input file
inputFile = open(filename)

#Reading the goal Input and generating list of goals,i.e, goals
goalInput = inputFile.readline().strip()
goals = goalInput.split(" && ")
for i in range(0,len(goals)):
    goals[i] = goals[i].strip()

#Reading the knowledge base and generating an object of knowledge base,i.e, KB
kbCount = int(inputFile.readline().strip())
kb = []
for i in range(0,kbCount):
    rule = inputFile.readline().strip()
    kb.append(rule)
KB = KNOWLEDGE_BASE(kb)
KB.standardize_knowledge_base()

finalResult = True
for goal in goals:
    subsGenerator = FOL_BC_ASK(KB,goal)
    try:
        firstGeneration = next(subsGenerator)
        finalResult = finalResult and True
        print firstGeneration

    except StopIteration:
        finalResult = finalResult and False
        print False
        break

if finalResult:
    print True
#a= next(subsGenerator)
#subsList = list(subsGenerator)

#print a
#print subsList
'''if len(subsList) > 0:
    print 'True'
else:
    print 'False'
'''

