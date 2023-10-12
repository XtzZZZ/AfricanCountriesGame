countries = ['Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi', 'Cabo Verde', 'Cameroon', 'Central African Republic', 'Chad', 'Comoros', 'Ivory Coast', 'Djibouti', 'Democratic Republic of the Congo', 'Egypt', 'Equatorial Guinea', 'Eritrea', 'Eswatini', 'Ethiopia', 'Gabon', 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Kenya', 'Lesotho', 'Liberia', 'Libya', 'Madagascar', 'Malawi', 'Mali', 'Mauritania', 'Mauritius', 'Morocco', 'Mozambique', 'Namibia', 'Niger', 'Nigeria', 'Republic of the Congo', 'Rwanda', 'Sao Tome & Principe', 'Senegal', 'Seychelles', 'Sierra Leone', 'Somalia', 'South Africa', 'South Sudan', 'Sudan', 'Tanzania', 'Togo', 'Tunisia', 'Uganda', 'Zambia', 'Zimbabwe']
usedCountries = []
def game(timeLimit, livesLeft):
    totalScore, inARow = 0, 0
    while livesLeft > 0 or len(usedCountries) < 54:
        country = str(input('Input a country: '))
        country = country.title()
        if country in countries and not country in usedCountries:
            usedCountries.append(country)
            totalScore += 1
            inARow += 1
            print(f'Well done! Your score is {totalScore} and you got {inARow} in a row right! {livesLeft} lives left.')
        elif country in usedCountries:
            print(f'You already guessed this country, try again')
        else:
            livesLeft -= 1
            if livesLeft == 0:
                print('You are out, noob')
                return
            print(f'Ouch! This country is not in africa. Your score remains {totalScore} and you have {livesLeft} lives left.')
    print('I won')
'''def menu():
    print("Welcome to the GUESS AFRICIAN COUNTRIES!\nThere are 54 countries and you have only 3 lives!\nAre you ready?\n")
    print("There are 3 modes. Input a value from 1 to 3 to choose the mode:\n1 - Easy (No time limit and infinite lives. Perfect for practice!)\n2 - Medium (15 minutes time limit and 5 lives. Too hard for you if you are an american.)\n3 - Hardcore (5 minutes time limit and only 1 life. Ready to test yourself?)")
    print("Input 4 to choose custom mode.\n")
    mode = int(input())
    match mode:
        case 1:
            game(999999, 999999)
        case 2:
            game(99999, 5)
        case 3:
            game(99999, 1)
    if mode == 4:
        timeLimit = int(input('Input the time: '))
        livesLeft = int(input('Input the amount of lives: '))
        game(timeLimit, livesLeft)'''

