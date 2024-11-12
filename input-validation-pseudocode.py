validHolidays = ["Christmas", "Anniversary"]
validRelationships = {
    "Partner": ["Wife", "Husband", "Girlfriend", "Boyfriend"],
    "Parent": ["Mom", "Dad"],
    "Sibling": ["Brother", "Sister"],
    "Child": ["Son", "Daughter"],
    "Grandparent": ["Grandson", "Granddaughter"],
    "Friend": [],
    "Other": [], # what to do for this (maybe teacher)
}
validAgeRanges = {
    "Partner": [(18, 30), (31, 45), (46, 60), (60, float('inf'))],
    "Parent": [(31, 45), (46, 60), (60, float('inf'))],
    "Sibling": [(10, 18), (18, 30), (31, 45), (46, 60), (60, float('inf'))],
    "Child": [(0, 10), (10, 18)],
    "Friend": [(10, 18), (18, 30), (31, 45), (46, 60), (60, float('inf'))]
}
validBudgetRanges = {
    "Under $25": (0, 25),
    "$25-$50": (25, 50),
    "$50-$100": (50, 100),
    "Over $100": (100, float('inf'))
}
validHobbies = ["Sports", "Tech", "Books", "Fashion", "Outdoors", "Comedy", "Organization", "Self-care", "Photography"]
"""
def validateHoliday(userInput):
    if userInput in validHolidays:
        return true
    else:
        return false

def validateRelationship(input):
    if input in validRelationships:
        followUpOptions = validRelationships[input]
        if followUpOptions is not empty:
            // Prompt user with follow-up options
            print("Please specify: " + join(followUpOptions, ", "))
            followUpInput = getUserInput() // Get user’s specific choice
            if followUpInput in followUpOptions:
                return followUpInput since it's valid, capture this for further processing
            else:
                print("Invalid choice. Please select from: " + join(followUpOptions, ", "))
                return validateRelationship(input) // Retry
        else:
            return input // No follow-up needed (like for friends), capture for further processing
    else:
        print("Invalid relationship choice. Please choose a valid option.")
        return false // Indicate invalid relationship input

def validateAge(userAgeInput, relationshipType):
    // Convert user input to an integer
    userAge = int(userAgeInput)
    // Get valid ranges for the specific relationship type
    ageRanges = validAgeRanges[relationshipType]
    // Check if user age falls within any valid range
    for range in ageRanges:
        if range[0] <= userAge <= range[1]:
            return true // Valid age input (capture this as the age range)
    return false // Invalid age input, try again

def validateBudget(input):
    // Parse user input as a range, e.g., "50-100" would become [50, 100], result as budgetRange
    if budgetRange == null:
        return false // Invalid format

    // Check if input matches any predefined budget range
    for label, range in validBudgetRanges.items():
        if range[0] <= budgetRange[0] and budgetRange[1] <= range[1]:
            return true // Valid budget input, capture this budget range for further processing
    return false // Invalid budget input, try again.

def validateHobbies(input):
    // Split user input into individual hobbies if entered as a comma-separated string
    selectedHobbies = parseMultiSelectInput(input) // depends on how we gather data
    // Check if each hobby is in list of valid hobbies
    for hobby in selectedHobbies:
        if hobby not in validHobbies:
            print("Invalid hobby detected: " + hobby)
            return false // Invalid input, try again
    return true (capture these hobbies for futher processing)

"""

"""
Get the inputs
holidayInput, relationshipInput, budgetInput, ageInput

Call functions for input validation.
"""