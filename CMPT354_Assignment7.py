# importing modules
from pickle import TRUE
import pyodbc
from datetime import datetime
import string 
import random

################################## Initital Connection to SQL Server ##################################

conn = pyodbc.connect('driver={SQL Server};' 'server=CYPRESS.csil.sfu.ca;' 'uid=s_apa109;pwd=2yHAmyM2a6LHaLEj;' 'database=apa109354')
print('Connect Successfully Established')

cursor = conn.cursor()

############################################## Functions ##############################################

def login():
    given_user_id = input('Enter user_id: ')
    given_user_id = given_user_id.strip()

    query = 'SELECT * FROM user_yelp WHERE user_id = ?'
    cursor.execute(query, (given_user_id,))

    # if no row in user_yelp exists with given user_id, user_row will be None
    user_row = cursor.fetchone()

    # keep prompting user until they enter a valid user_id
    while(not user_row):
        given_user_id = input('Please enter a valid user_id: ')
        cursor.execute(query, (given_user_id,))
        user_row = cursor.fetchone()

    print('Login successful! Welcome ' + user_row[1] + '.')

    return given_user_id

def search_business():
    print('Search for a business. Enter the following filters...')

    # take user input for min stars
    min_stars = input('Enter minimum number of stars (or - for no filter): ')
    min_stars = min_stars.strip()

    # check to see if user entered a number
    try:
        float(min_stars)
        isdigit = True
    except ValueError:
        isdigit = False 

    # if user did not enter a number, set min stars to 0
    if(not isdigit):
        min_stars = 0
       
    # take user input for max stars
    max_stars = input('Enter maximum number of stars (or - for no filter): ')
    max_stars = max_stars.strip()

    # check to see if user entered a number
    try:
        float(max_stars)
        isdigit = True
    except ValueError:
        isdigit = False 

    # if user did not enter a number, set max stars to 5
    if(not isdigit):
        max_stars = 5
    
    # take user input for city
    city = input('Enter city (or - for no filter): ')
    city = city.strip()
    city = city.lower()

    # if user decided not to filter by city, set city to %, meaning 0 or more chararacters
    if(city == '-'):
        city = '%'

    # take user input for name
    name = input('Enter name, or a part of the name (or - for no filter): ')
    name = name.strip()
    name = name.lower()

    # if user decided not to filter by name, set name to %, meaning 0 or more chararacters
    if(name == '-') :
        name = '%'
    else:
        # allow user to filter by part of name
        name = '%' + name + '%'
   

    query = 'SELECT * FROM business WHERE stars >= ? AND stars <= ? AND lower(city) LIKE ? AND lower(name) LIKE ? ORDER BY name ASC'
    
    cursor.execute(query, (min_stars, max_stars, city, name));

    not_empty = cursor.fetchone()

    # display search results
    if(not_empty):
        print('\nResulting business search:\n')
        print('Business ID, Name, Address, City, Number of Stars')
        for row in cursor:
            stars = float(row[5])
            print(str(row[0]) + ', ' + str(row[1]) + ', ' + str(row[2]) + ', ' + str(row[3]) + ', ' + str(stars))
    else:
        print('No businesses matching inputted criteria.')

def search_users():
    print('Search for a user. Enter the following filters...')

    # take user input for name
    name = input('Enter name, or a part of the name (or - for no filter): ')
    name = name.strip()
    name = name.lower()

    # if user decided not to filter by name, set name to %, meaning 0 or more chararacters
    if(name == '-') :
        name = '%'
    else:
        # allow user to filter by part of name
        name = '%' + name + '%'
    
    # take user input for useful
    min_useful = input('Enter useful - yes/no (or - for no filter): ')
    min_useful = min_useful.strip()
    min_useful = min_useful.lower()
    max_useful = 2147483647 # max int in SQL
    
    if(min_useful == '-'):
        min_useful = 0
    elif(min_useful == 'yes'):
        min_useful = 1
    elif(min_useful == 'no'):
        min_useful = 0 
        max_useful = 0

    # take user input for funny
    min_funny = input('Enter funny - yes/no (or - for no filter): ')
    min_funny = min_funny.strip()
    min_funny = min_funny.lower()
    max_funny = 2147483647 # max int in SQL

    if(min_funny == '-'):
        min_funny = 0
    elif(min_funny == 'yes'):
        min_funny = 1
    elif(min_funny == 'no'):
        min_funny = 0 
        max_funny = 0

    # take user input for cool
    min_cool = input('Enter cool - yes/no (or - for no filter): ')
    min_cool = min_cool.strip()
    min_cool = min_cool.lower()
    max_cool = 2147483647 # max int in SQL

    if(min_cool == '-'):
        min_cool = 0
    elif(min_cool == 'yes'):
        min_cool = 1
    elif(min_cool == 'no'):
        min_cool = 0 
        max_cool = 0


    query = 'SELECT * FROM user_yelp WHERE useful >= ? AND useful <= ? AND funny >= ? AND funny <= ? AND cool >= ? AND cool <= ? AND lower(name) LIKE ? ORDER BY name ASC'
    
    cursor.execute(query, (min_useful, max_useful, min_funny, max_funny, min_cool, max_cool, name,))

    not_empty = cursor.fetchone()

    # display search results
    if(not_empty):
        print('\nResulting user search:\n')
        print('User ID, Name, Useful (yes/no), Funny (yes/no), Cool (yes/no), Date Registered')
        for row in cursor:
            useful = 'no'
            funny = 'no'
            cool = 'no'

            if(row[4] > 0):
                useful = 'yes'
            if(row[5] > 0):
                funny = 'yes'
            if(row[6] > 0):
                cool = 'yes'

            print(str(row[0]) + ', ' + str(row[1]) + ', ' + useful + ', ' + funny + ', ' + cool + ', ' + str(row[3]))
    else:
        print('No user matching inputted criteria.')

def make_friend(user_id):
    # get the id of the user they want to friend
    friend_id = input("Please enter the user ID of the user you would like to be a friend of: ")
    friend_id = friend_id.strip()
    
    # check if that user exists in the database
    search_query = 'SELECT * FROM user_yelp WHERE user_id = ?'
    cursor.execute(search_query, (friend_id,))
    not_empty = cursor.fetchone()
    
    if(not_empty):
        # check if friendship already exists with entered user
        search_friendship = 'SELECT * FROM friendship WHERE (user_id = ? AND friend = ?) OR (user_id = ? AND friend = ?)'
        cursor.execute(search_friendship, (user_id, friend_id, friend_id, user_id,))
        friendship_exists = cursor.fetchone()

        if(not friendship_exists):
            # insert into friendship table
            insert_query = f'INSERT INTO friendship VALUES (\'{user_id}\', \'{friend_id}\')'
            cursor.execute(insert_query)

            # commit changes to database
            conn.commit() 

            print('Friend Added!')
        else:
            print('You are already friends with inputted user.')
    else:
        print('There is no user with inputted ID.')

# helper function to determine if a rating is valid
def is_valid_rating(num_stars):
    # check to see if user entered a number 
    try:
        float(num_stars)
        isValid = True
        num_stars = float(num_stars)
    except ValueError:
        isValid = False
    
    # check to see if user entered an integer between 1 and 5
    if(num_stars != 1 and num_stars != 2 and num_stars != 3 and num_stars != 4 and num_stars != 5):
        isValid = False

    return isValid

# helper function to generate a random review ID 
def generate_random_review_id():
    review_id = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(22))

    # check if such an ID already exists
    search_query = 'SELECT * FROM review WHERE review_id = ?'
    cursor.execute(search_query, (review_id,))
    not_empty = cursor.fetchone()

    # regenerate until a unique review ID is created
    while(not_empty):
        review_id = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(22))

        cursor.execute(search_query, (review_id,))
        not_empty = cursor.fetchone()

    return review_id

def write_review(user_id):
    # get the businessID of the business they want to write a review for
    business_id = input('Please enter the business ID of the business you would like to write a review for: ')
    business_id = business_id.strip()

    # check if that business exists in the database
    search_query = 'SELECT * FROM business WHERE business_id = ?'
    cursor.execute(search_query, (business_id,))
    not_empty = cursor.fetchone()

    if(not_empty):
        # get number of stars for review
        num_stars = input('Please enter the rating (integer from 1 to 5) for your review: ')
        num_stars = num_stars.strip()

        # prompt user until they enter a valid rating
        while(not is_valid_rating(num_stars)):
            num_stars = input('That rating is invalid. Please try again: ')
            num_stars = num_stars.strip()

        review_id = generate_random_review_id() # random review ID
        now = datetime.now() # current date and time
        now = now.strftime("%Y-%m-%dT%H:%M:%S")

        # insert into review table
        insert_query = f'INSERT INTO review VALUES (\'{review_id}\', \'{user_id}\', \'{business_id}\', {int(float(num_stars))}, DEFAULT, DEFAULT, DEFAULT, \'{now}\')'
        cursor.execute(insert_query)

        # commit changes to database
        conn.commit() 

        print('Review Created! ID = ' + review_id)
    else:
        print('There is no business with inputted ID.')


################################################# Menu #################################################

user_id = None

while True:
    print()
    print("(1) Login")
    print("(2) Search Business")
    print("(3) Search Users")
    print("(4) Make Friend")
    print("(5) Write Review")
    print("(6) Quit")

    option = input("Select An Option: ")
    option = option.strip()

    if(option == "1"):
        user_id = login();
    elif(option == "2"):
        search_business()
    elif(option == "3"):
        search_users()
    elif(option == "4"):
        if(user_id == None):
            print("Must be logged in to make a friend!")
        else:
            make_friend(user_id)
    elif(option == "5"):
        if(user_id == None):
            print("Must be logged in to write a review!")
        else:
            write_review(user_id)
    elif(option == "6"):
        print("Goodbye!")
        break
    else:
        print("Invalid Option. Please Try Again.")

    print()


print()
print("Closing Connection")
conn.close()



