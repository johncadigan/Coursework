/*******************************************************************************
 * Program Name: NumberGuessingGame 
 * Created Date: 09/16/2013
 * Created By: John Cadigan
 * Purpose: Plays the number guessing game which tells the user if they guessed too high or too low.
 * Acknowledgements: None
 *******************************************************************************/

/*******************************************************************************
 * Function Name: game_menus()
 * Parameters: intmenu (int) 0 means false and (int) 1 means true, intlevel is the level the player's current level
 * Return Value: Returns 0 if the user wants to quit, a positive number for the level they will play.
 * Purpose: This runs the menus for the start of the game and when finishes a level. It returns
 the level at which the user will play
  *******************************************************************************/
#include <iostream>
#include <cstdlib>

using namespace std;
int game_menus( int intmenu, int intlevel)
{
	// The menu selection
	int intselection = 0;

	
    if(intmenu==1)//Displays the first menu of the program
	{
		//The prompt for the first menu
		cout << "Do you want to play? \n" 
			 << "1. Play starting at level 1. \n" 
			 << "2. Input a level at which you want to start playing. \n"
			 << "3. Quit. \n";
		
		cin >> intselection; //Stores the menu selection

		if(intselection == 1) //Start playing at level one
		{
			intlevel = 1; //Sets the level to one
		}
		else if(intselection == 2) //Start playing at a level specified by the user
		{
			cout << "Input the number of the level you wish to play. \n "; //Prompts user for the level they want to play
		    cin >> intlevel; //Sets the level to the user's input
		}
		if(intselection == 3)//Quits the program
		{
			intlevel = 0; //Sets the level to 0 which will end the program
		}
	}
	else if(intmenu == 2)// The menu displayed if the user loses
	{
		//The prompt asking if they want to replay the level they lost 
		cout << "Do you want to try level "<< intlevel << " again? \n" 
		<< "1. Yes. \n" 
		<< "2. Quit. \n";
		//Stores the menu selection
		cin >> intselection;
		
		// We only need to know if the user wants to quit; otherwise, the level returned will be the same as when it came in;
		if(intselection == 2)
		{
			intlevel = 0; //Sets the level to 0 which will end the program
		}
	}
	else if(intmenu == 3) // The menu displayed if the user won
	{
		//The prompt asking if they want to advance to the next level
		cout << "Do you want to continue playing at the next level? \n" 
		<< "1. Yes. \n" 
		<< "2. Quit. \n";

		cin >> intselection;// Stores the input
		if(intselection == 1)//The user wants to advance
		{
			intlevel++;//Increases the level by 1
		}
		else if(intselection == 2)//The user wants to quit
		{
			intlevel = 0; //Sets the level to 0 which will end the program
		}
	}
	
	return intlevel;//Returns the level to be played; 0 means the user wants to quit.
}


/*******************************************************************************
 * Function Name: get_number_in_range()
 * Parameters: lower_bound (int) , upper_bound (int)
 * Return Value: an integer
 * Purpose: This gets an integer between the bounds from the user;
 it does not allow a number out of the range
 *******************************************************************************/
#include <iostream>
using namespace std;
int get_number_in_range(int lower_bound, int upper_bound)
{
	int intguessed = 0; //Stores the user's guess
	while(intguessed < lower_bound || intguessed > upper_bound)//A loop which runs until the user inputs a value in the range;
	{
		cout << "Enter a number between " << lower_bound << " and " << upper_bound << endl;
		cin >> intguessed;
		if(intguessed >= lower_bound && intguessed <= upper_bound) // A test; if in range, returns the value
		{
			return intguessed; //Returns the guess in the appropriate range
			break;// Ends the while loop
		}
		else //A test; if it is out of range, it prints an error message and prompts the user again
		{
			cout << "ERROR! You must enter a number in the range. \n"; //An error message
		}
	}
}

/*******************************************************************************
 * Function Name: play_number_game()
 * Parameters: intlevel (int)
 * Return Value: 1 meaning they won, 0 meaning they lost
 * Purpose: This function plays the number guessing game given a level;
 the user always has 5 guesses, the lower bound of the range is always 1 and 
 the upper bound is level * 32 which makes the final guess range equal to the level
 if the user guesses with the optimal strategy of divide and conquer;
 *******************************************************************************/
#include <iostream>
#include <time.h>
int play_number_game(int intlevel)
{
	int intrandom = 0;
	int intguesses = 4 + intlevel;

	//Calculates the upper bound based on the level; if the user follows the optimal strategy they
	//will end up guessing in a range equal to the current level; they should always win level 1;
	//they should come within +/- 1 on level 2, +/- 2 on level 3, etc...
	int upper_bound = intlevel * 32;
	
	
	int lower_bound = 1;
	int intguessed = 0;
	int intwin = 0;// Sets the default to mean that the user lost
	
	srand(time(0));//seeds the random number generator
	intrandom = (rand() % upper_bound) + 1;//Creates a random number in the range between 1 and the upper bound

	system("cls"); //Clears the screen
	cout << "Level " << intlevel << "\n \n"; //Displays the current level

	cout << "Your mission is to select a number between " << lower_bound << " and " << upper_bound << ". You have "<< intguesses <<  " guesses to get it correct. \n \n";
	
	while(intguesses > 0)//A loop which runs until the user has no more guesses
	{
		intguessed = get_number_in_range(lower_bound, upper_bound); //gets a number in the appropriate range
		
		intguesses--;// Takes away one guess

		if(intguessed > intrandom)//If they are too high
		{
		cout << "Your guess was too high! \n";
		}
		else if(intguessed < intrandom)//If they are too low
		{
		cout << "Your guess was too low! \n";
		}
		else if(intguessed == intrandom)//If they are correct
		{
		intwin = 1;//Stores that the user won
		break;// Ends the loop
		}

		if(intguesses > 1)// If more than one guess is left
		{
		cout << "You have " << intguesses << " guesses left! \n"; //Tells them how many guesses are left
		}
		else if(intguesses == 1) // if only one guess is left
		{
		cout << "You have 1 guess left! \n"; //Tells them one guess remains
		}
	}

	if(intwin == 1)//Runs if the user won
	{
		switch(intguesses)//The cases are equal to the number of guesses the user has left
		{
		case 4: cout << "Wow! You got that in 1 guess. Did you cheat? \n"; break;// Message displayed if they guessed on the first try
		case 3: cout << "Fantastic! You got that in 2 guesses. \n"; break;// Message displayed if they guessed on the second try
		case 2: cout << "Pretty Good! You got that in 3 guesses. \n"; break;// Message displayed if they guessed on the third try
		case 1: cout << "Good! You got that in 4 guesses. \n"; break;// Message displayed if they guessed on the fourth try
		case 0: cout << "Barely! You got that in 5 guesses. \n"; break;// Message displayed if they guessed on the fifth try
		}
	}
	else if(intwin == 0)//Runs if the user lost
	{
		cout << "You lose! \n" 
			<< "The correct number was " << intrandom << endl; //Tells them the correct number
	}
	
	return intwin;//Tells main whether the student won or lost
}


/*******************************************************************************
 * Function Name: main()
 * Parameters: None
 * Return Value: None
 * Purpose: Runs the program
 *******************************************************************************/
#include <iostream>
using namespace std;
int main()
{
	int intlevel = 0;//0 will close the program if unchanged
	int intmenu = 1;//Display the first menu by default
	int intwin = 0;//Assume that the user lost

	do//Assures that the loop runs at least once despite the value of intlevel
	{
		intlevel = game_menus(intmenu, intlevel);//Gets the level to be played; 0 means quit
		if(intlevel !=0)//If the user does not want to quit
		{	
			intwin = play_number_game(intlevel);//Plays the number game with a given level
			if(intwin == 1)//If the user wins
			{
				intmenu = 3;//Display the continue screen
			}
			else//If the user loses
			{
				intmenu = 2;//Display the replay screen
			}
		}
	}
	while(intlevel !=0);//The program will continue displaying menus 
	//until the user quits with a menu returning a intlevel of 0 

	system("cls"); //Clears the screen
	cout << "Thank you for playing. \n";//Thanks the user;
	system("pause");//Allows the user to see the thanking message

	return 0;
}






