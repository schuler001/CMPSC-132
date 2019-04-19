#HW 5
#Due Date: 04/16/2019, 11:59PM
########################################
#
# Name: Hunter Schuler
# Collaboration Statement: Neither sought nor gave assistance
#
########################################


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __str__(self):
        return "Node({})".format(self.value)

    __repr__ = __str__


class Stack:
    def __init__(self):
        self.top = None

    def __str__(self):
        temp = self.top
        out = []
        while temp:
            out.append(str(temp.value))
            temp = temp.next
        out = '\n'.join(out)
        return ('Top:{}\nStack:\n{}'.format(self.top, out))

    __repr__ = __str__

    def isEmpty(self):
        # Check if there is a top value to determine if the stack has any items
        if self.top == None:
            return True
        return False

    def __len__(self):
        # If the stack is empty, there are no items
        # Otherwise loop to find the end of the stack
        if self.isEmpty():
            return 0
        else:
            count = 1
            temp = self.top
            while temp:
                if temp.next == None:
                    return count
                else:
                    temp = temp.next
                    count += 1

    def peek(self):
        # Simply return the top of the stack unless empty
        if self.isEmpty():
                return None
        return self.top.value

    def push(self, value):
        # Just add to the top of the stack
        node = Node(value)
        node.next = self.top
        self.top = node

    def pop(self):
        # If there are values in the stack, remove the top item
        if not self.isEmpty():
            value = self.top.value
            self.top = self.top.next
            return value
        return 'Stack is empty'


def findNextOpr(txt):
    if not isinstance(txt, str) or len(txt) <= 0:
        return "error: findNextOpr"
    # Checks for the position of the first operator in a text and returns the position value
    for i in range(len(txt)):
        if txt[i] == '*' or txt[i] == '+' or txt[i] == '-' or txt[i] == '/' or txt[i] == '^' or txt[i] == '(' or txt[i] == ')':
            return i
    return -1


def isNumber(txt):
    if not isinstance(txt, str) or len(txt) == 0:
        return "error: isNumber"
    # Test to see if it can be converted to a number
    try:
        if float(txt):
            return True
    except ValueError:
        return False


def getNextNumber(expr, pos):
    if not isinstance(expr, str) or not isinstance(pos, int) or len(expr) == 0 or pos < 0 or pos >= len(expr):
        return None, None, "error: getNextNumber"
    expr = expr[pos:]
    # Check to see if the string is simply a number with no operators
    if isNumber(expr):
        return (float(expr), None, None)
    # Find the operator and if there is none, set both operator and position to None
    opPos = findNextOpr(expr)
    if opPos < 0:
        op = None
        opPos = None
    else:
        # Define the operator if it exists
        op = expr[opPos]
        # Check if there is a number before the -
        # If there isn't then the first number is a negative
        if op == '-' and getNextNumber(expr, opPos+1)[1] != '(' and (opPos == 0 or not isNumber(expr[:opPos])):
            secondOp = findNextOpr(expr[opPos+1:]) + opPos + 1
            num = float("".join(expr[opPos:secondOp].split()))
            op = expr[secondOp]
            opPos = pos + secondOp
            return (num, op, opPos)
        expr = expr[:opPos]
        opPos += pos
    # If there is no number after the operator, just return the operator and its position
    if len(expr) == 0:
        return(None, op, opPos)
    # Otherwise just push the number with the operators
    if isNumber(expr):
        num = float(expr)
    else:
        num = None
    return (num, op, opPos)


def postfix(expr):
    # Check parentheses
    openCount = 0
    closeCount = 0
    for i in expr:
        if i == '(':
            openCount += 1
        if i == ')':
            closeCount += 1
    if openCount != closeCount:
        return 'Error, invalid expression'
    # Initialize variable
    postStack = Stack()
    postExpr = []
    # Create the next number tuple and check if there is a operator with no operand or just a number
    nextNum = getNextNumber(expr, 0)
    if nextNum[0] == None and (nextNum[1] != None and nextNum[1] != '('):
        return 'Error, invalid expression'
    if nextNum[1] == None:
        if isNumber(expr):
            postExpr.append(getNextNumber(expr, 0)[0])
            postStr = ' '.join(map(str, postExpr))
            return postStr
        return 'Error, invalid expression'
    # Store the operator and add the operand to the expression
    postStack.push(nextNum[1])
    if nextNum[0] != None:
        postExpr.append(nextNum[0])
    pos = nextNum[2] + 1
    # Check to make sure the operator isn't the last value in the expression
    if pos > len(expr)-1:
        return 'Error, invalid expression'
    # While the position in the expression exists loop
    try:
        while pos < len(expr):
            # Get the next number
            nextNum = getNextNumber(expr, pos)
            if nextNum == 'Error, invalid expression':
                return nextNum
            if nextNum == (None, None, None) and not (expr[pos:]).isspace():
                return 'Error, invalid expression'
            # Add the number to the expression and check the operator
            if nextNum[0] != None:
                postExpr.append(nextNum[0])
            # If a open parenthesis is found, just add it to the stack
            if nextNum[1] == '(':
                postStack.push(nextNum[1])
                pos = nextNum[2] + 1
            # If an close parenthesis is added, pop until an open parenthesis is found
            elif nextNum[1] == ')':
                # Pop until the open parenthesis
                while postStack.peek() != '(':
                    postExpr.append(postStack.pop())
                # Pop the open parenthesis
                postStack.pop()
                pos = nextNum[2] + 1
            # If the operator is lowest priority, pop the whole stack
            elif nextNum[1] == '+' or nextNum[1] == '-':
                while postStack.peek() != None and postStack.peek() != '(':
                    postExpr.append(postStack.pop())
                postStack.push(nextNum[1])
                pos = nextNum[2] + 1
            # If the operator is multiply or divide, pop the stack if the operator on top is an exponentiation
            # Otherwise add the operator
            elif nextNum[1] == '*' or nextNum[1] == '/':
                if postStack.peek() != '+' and postStack.peek() != '-':
                    while postStack.peek() != None and postStack.peek() != '(':
                        postExpr.append(postStack.pop())
                    postStack.push(nextNum[1])
                else:
                    postStack.push(nextNum[1])
                pos = nextNum[2] + 1
            # If the operator is an exponentiation, add it to the stack
            elif nextNum[1] == '^':
                postStack.push(nextNum[1])
                pos = nextNum[2] + 1
            # If there is no operator, it is assumed that it is the end of the function
            # and it breaks
            else:
                while postStack.peek() != None:
                    postExpr.append(postStack.pop())
                break
        while postStack.peek() != None:
            postExpr.append(postStack.pop())
        postStr = ' '.join(map(str, postExpr))
        return postStr
    except:
        return "Error, invalid expression"


def calculator(expr):
    # Convert the postfix expr into a list of item
    expr = postfix(expr)
    if expr == 'Error, invalid expression':
        return expr
    expr = expr.split(" ")
    calculateStack = Stack()
    i = 0
    # Loop through the length of the list
    while i < len(expr):
        # If the item is an operator, calculate the value and push back into the stack
        if expr[i] == '*' or expr[i] == '+' or expr[i] == '-' or expr[i] == '/' or expr[i] == '^':
            op = expr[i]
            try:
                op2 = float(calculateStack.pop())
                op1 = float(calculateStack.pop())
            except ValueError:
                return 'Error, invalid expression'
            if op == '*':
                value = op1 * op2
            elif op == '/':
                if op2 == 0:
                    return 'Error, zero division'
                value = op1 / op2
            elif op == '+':
                value = op1 + op2
            elif op == '-':
                value = op1 - op2
            elif op == '^':
                value = op1 ** op2
            calculateStack.push(value)
        else:
            # Push all values into the stack
            value = expr[i]
            calculateStack.push(value)
        i += 1
    return calculateStack.pop()