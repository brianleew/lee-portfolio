# create a function called nickels_and_pennies to return the number of nickels and pennies
# needed to make a given number of cents
# the function should have three parameters: nickels, pennies, and cents
# the function should return a list with the number of nickels and number of pennies used
# the function should return [-1, -1] if there is no solution
def nickels_and_pennies(nickels, pennies, cents):
    # return the result in a list called coins
    coins = [-1, -1]
    # determine the number of nickels and pennies needed to make cents
    # maximize the number of nickels needed and minimize the number of pennies
    # compute the number of nickels by taking the minimum of nickels and cents // 5
    # compute the number of pennies needed by subtracting the number of nickels * 5 from cents
    # satisfy the constraint that coins[0]*5 + coins[1] == cents
    # satisfy the constraint that coins[0] <= nickels and coins[1] <= pennies else coins = [-1,-1]
    if (nickels * 5 + pennies) >= cents:
        coins[0] = min(nickels, cents // 5)
        coins[1] = cents - coins[0] * 5
        if (coins[0] > nickels) or (coins[1] > pennies):
            coins = [-1, -1]
    # return coins

    return coins
