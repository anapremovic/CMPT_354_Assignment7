Course: CMPT 354 D100 
Name: Ana Premovic 
Student Number: 301452722 
  
To use my application, open the .py file in your favourite IDE, build it, and run it.
  
At the start of the program, a connection to the SQL Server database is established.
  
The program will then prompt you to enter a number from 1 to 6 to use the various functionalities, where:
  
1 - Login
2 - Search Business
3 - Search Users
4 - Make Friend
5 - Write Review
6 - Quit the program
  
Here is a tutorial for each functionality:
  
Login:
- The program will prompt you to enter a User ID.
- If you enter a valid user_id from the Yelp database, and you will be logged in.
- Otherwise, the program will prompt you until you enter a valid user_id.
  
Search Business:
- The program will prompt you to enter some filters. Each filter will be on a separate line.
- If for a specific filter, you do not want to filter by that value, enter '-'.
- The program will display all the businesses matching the inputted filters. The format is (business_id, name, address, city, rating).
- If you enter '-' for all filters, the program will output the entire Business table.
  
Search Users
- Works the same way as Search Business.
- The output format is (user_id, name, useful, funny, cool, yelping_since).

Make Friend
- Must be logged in to use this functionality.
- The program will prompt you to enter a user_id of a user in the user_yelp table.
- If you enter a valid user_id, a friendship will be created in the friendship table with you as the user_id and the friend you entered as the friend.
  
Write Review
- Must be logged in to use this functionality.
- The program will prompt you to enter a business_id of a business in the business table.
- If you enter a valid business_id, the program will prompt you to enter a rating.
- If you enter an invalid rating, the program will keep prompting you to enter a valid rating (an integer from 1 to 5) until you do so.
- Once you enter a valid rating, a review will be created for you in the review table with a randomly generated user_id, the business_id you entered, the given rating, the current time, and default values for the useful, funny, and cool attributes.
  
Quit
- The connection is closed, and the program terminates.
