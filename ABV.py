# Math121, Fall 2017, Miniproject 2


# ---------------------------------------------------------------------------#
# You will need to implement and use the following functions.
# ---------------------------------------------------------------------------#

# shooters.txt
# Takes a string-type filename, which is the name of the file where the
# recipees for shooters are stored.
# returns a dictionary where each key is a string-type name of a shooter, and
# the value is a list of strings each storing a line of recipee
# for the shooter.
# Example of an item:
#   'Red Hot' : ['1 oz.   peppermint schnapps', 'Note: drops of Tabasco']
def getShooterRecipe(filename) :
    fhandle = open(filename)
    RecipeDic = dict()
    Drinknumber = 0
    for line in fhandle:
        newline = line.strip() # get rid of all spaces
        if not 'oz.' in newline and not 'Note:' in newline and not newline == '':
            Drink = newline
            Drinknumber += 1
            RecipeList = [] # create a new RecipeList (list of values) for each drink (key)
        else:
            if 'oz' in newline or 'Note:' in newline:
                RecipeList.append(newline)
            elif newline == '':
                RecipeDic[Drink] = RecipeList
    return RecipeDic

# ingredientsABV.txt
# Takes a string-type filename, which is the name of the file where the
# percent of alcohol by volume (%ABV) of all the ingredients are stored.
# Returns a dictionary where each key is a string-type name of the ingredient,
# and the value is the float-type number of %ABV.
# Example of an item:
#   'Cafe Royale' : 8.5
def getIngredientsABV(filename) :
    fhandle = open(filename)
    ABVdic = dict()
    for line in fhandle:
        Drink = line.split(':')[0].strip() # ex) Advocaat
        percentABV = line.split(':')[1].strip() # includes the unit - ex) 17%ABV
        ABV = percentABV.replace("%ABV", "") # only the number - ex) 17
        floatABV = float(ABV) # converts string to float type
        ABVdic[Drink] = floatABV
    return ABVdic

# Takes a string-type line of recipee.
# Returns True if the line contains an ingredient
# (when the line contains 'oz.''))
# Else returns False
def hasIngredient(line) :
    if 'oz.' in line:
        return True
    else:
        return False

# Takes a string-type line of recipee that contains an ingredient.
# Returns a string-type ingredient name.
# Example:
#     string = '1 oz.   peppermint schnapps'
#     returns 'peppermint schnapps'
def extractIngredient(line) :
    Ingredient = line.split('oz.')[1].strip() #take the right part of 'oz.' and remove black spaces
    return Ingredient

# Takes a string-type line of recipee that contains an ingredient.
# Returns float-type amount of oz. specified for that ingredient.
# Example:
#     string = '3/4 oz. creme de banana' '1 oz.   Sambuca'
#     returns 0.75
def extractIngredientAmount(line) :
    IngAmount = line.split('oz.')[0].strip() #take the left part of 'oz.' and remove black spaces
    if len(IngAmount) == 3: # '3/4' has a length of 3
        numerator = int(IngAmount[0]) # '3' of '3/4', 0th index, as integer
        denominator = int(IngAmount[2]) # '4' of '3/4', 2nd index, as integer
        FloatIngAmount = numerator/denominator # converts fraction to float
    else: # when the length of Amount is not 3 EX) '1 oz.'
        FloatIngAmount = float(IngAmount)
    return FloatIngAmount

# Takes string-type line of recipe that contains an ingredient
# and the Amount of Ingredient in the recipe
# returns the amount of alochol from that specific ingredient,
# rounded to two decimal points
# Ex) 2/5 oz. Kahlua --> 0.4 * 27% (ABV) --> 0.11 oz. of alcohol
def AlcoholAmount(line, IngAmount):
    IngredientName = extractIngredient(line)
    PercentABV = ABVdic[IngredientName] # percent of ABV for the ingredient (recipeline)
    DecimalABV = PercentABV / 100 # converts percent (27%) to decimal (0.27)
    AlcoholAmount = IngAmount * DecimalABV # float type
    return AlcoholAmount

# Takes:
#   recipe : a list of strings that describe the recipe for a shooter
#   ingredientDict : dictionary of ingredients and their ABV
# Returns: the percent of alcohol by volume of the drink, as a float-type,
#   rounded to 1 decimal digit.
# Example:
#   recipe = ['2/5 oz. Kahlua', '2/5 oz. Anisette', '1/5 oz. cream', 'Note: Drop cream into liqueurs.']
#   returns 23.0
def getTotalABV(recipe, ingredientDict) :
    TotalAlcohol = 0 # Total amount of alcohol in oz.
    TotalABV = 0 # ABV in percent
    for recipeline in recipe:
        if hasIngredient(recipeline) == True:
            IngAmount = extractIngredientAmount(recipeline)
            AmountofAlcohol = AlcoholAmount(recipeline, IngAmount) # amount of alocohol for each ingredient
            TotalAlcohol = TotalAlcohol + AmountofAlcohol
    TotalABV = TotalAlcohol * 100 # Ex) 0.228 oz. --> 22.8 ABV
    RoundedTotalABV = round(TotalABV, 1) # round to 1 decimal point
    return RoundedTotalABV

# parameter : RecipeDic
# Creates a dictionary with shooter name as keys and its total ABV as values
def ShooterABVdic(RecipeDic):
    ShooterIndex = 0
    ShooterABVdic = {} # new dic that sorts shooter as key and TotalABV as value
    while ShooterIndex < len(ShooterList):
        Shooter = ShooterList[ShooterIndex]
        ARecipe = RecipeDic[Shooter] # list of all recipe lines for specific shooter at ShooterIndex
        ARecipeIng = [] # List of recipe lines that have ingredients in it
        for line in ARecipe:
            if hasIngredient(line) == True:
                ARecipeIng.append(line)
        TotalABV = getTotalABV(ARecipeIng, ABVdic) # Total ABV for specific shooter at each index
        ShooterABVdic[Shooter] = TotalABV # adds a new element in the dictionary (Shooter: TotalABV)
        ShooterIndex += 1
    return ShooterABVdic

# Creates a dictionary in which sorts ShooterABVdic by value (from lowest total ABV to highest ABV)
def ShooterDicByABV():
    ShooterABV = ShooterABVdic(RecipeDic)
    ShooterDicByABV = {} # sorted By ABV
    ABVvals = list(ShooterABV.values()) # a list of total ABV values of all shooters in alphabetical order
    ABVvals_sorted = [] # a list of total ABV values in order (lowest to highest)
    index = 0
    while len(ABVvals_sorted) != len(ShooterABV):
        minval = min(ABVvals)
        ABVvals_sorted.append(minval)
        ABVvals.remove(minval)
        index += 1
    n = 0 # index to go through ShooterABVdic
    k = 0 # index to go through ABVvals_sorted
    while k < len(ABVvals_sorted):
        for shooter in ShooterList:
            if ABVvals_sorted[k] == ShooterABV[shooter]: # if the kth value of ABVvals_sorted matches a shooter's ABV
                ShooterDicByABV[shooter] = ABVvals_sorted[k] # add new element to the new dictionary (ShooterDicByABV)
            n += 1
        k += 1
    return ShooterDicByABV

# --- main code --- #

RecipeDic = getShooterRecipe('shooters.txt')
# 'Red Hot' : ['1 oz.   peppermint schnapps', 'Note: drops of Tabasco']
ABVdic = getIngredientsABV('ingredientsABV.txt')
# 'Cafe Royale' : 8.5
ShooterList = list(RecipeDic.keys()) # list of keys (name of shooters) -- Global Variable
ShooterList.sort() # list of shooters sorted in alphabetical order

fwrite = open('NewShooters.txt', 'w')
ShooterDicByABV = ShooterDicByABV() # dictionary of Shooter names from highest total ABV amount to lowest
for shooter in ShooterDicByABV: # go through each key sorted in the order of Total ABV amount
    ARecipe = RecipeDic[shooter] # list of recipe lines for specific shooter at index
    TotalABV = getTotalABV(ARecipe, ABVdic)
    fwrite.write(str(shooter) + " (" + str(TotalABV)  + " ABV)" + "\n") # prints the title of recipe (shooter name) and total ABV
    for recipeline in ARecipe: # each recipe line in the list
        if hasIngredient(recipeline) == True:
            IngredientName = extractIngredient(recipeline)
            IngAmount = extractIngredientAmount(recipeline) # Amount of each ingredient in oz.
            RoundedIngAmount = round(IngAmount,2) # round up float number to 2 decimal points for printing purposes
            PercentABV = ABVdic[IngredientName] #ABV % of each ingredient
            AmountofAlcohol = AlcoholAmount(recipeline, IngAmount) # The amount of alcohol coming from each ingredient
            RoundedAmofAlc = round(AmountofAlcohol, 2)
            if PercentABV == 0.00:
                fwrite.write(recipeline + '\n')
            else:
                fwrite.write(recipeline + ' (' + str(PercentABV) + ' ABV' + ', ' + str(RoundedAmofAlc) + ' oz. of alcohol)' + '\n')
                # ex) 2/5 oz. Kahlua (27.0 ABV, 0.11 oz. of alcohol)
        else:
            fwrite.write(recipeline + '\n')
    fwrite.write('\n') # just to add a space between each recipe
