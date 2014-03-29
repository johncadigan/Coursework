#include <iostream>
#include <time.h>
#include <string>
#include <cstdlib>
using namespace std;

/*******************************************************************************
* Program Name: BoxGame
* Created Date: 10/2/2013
* Created By: John Cadigan
* Purpose: Plays the box picking game
*******************************************************************************/

/*******************************************************************************
* Class Name: Box()
* Purpose: This class has all the functions necessary to prize boxes
for this game. PrintCard translates the numbers representing the values of the
faces and suits into English. DefeatsCard checks to see if one card defeats another.
SetValue gives cards their values.
*******************************************************************************/
class Box
{

public:
	int irevealed, iposition, iwinner;
	string sprize;
	Box();
	~Box() {};
	void Reveal();
	void SetValue(string prize, int position, int winner=0);
};

Box::Box()
{

};

void Box::SetValue(string prize, int position, int winner)
{
	irevealed = 0;// 0 means it has not been revealed; 1 means it has.
	iwinner = winner;// 0 means it is not the winning prize; 0 means it is.
	iposition = position; //The card's box number
	sprize = prize; // The box's prize
}

void Box::Reveal(void) {
	irevealed = 1;
	cout << "Box #" << iposition << " had " << sprize << " in it!\n";
}



/*******************************************************************************
* Function Name: get_number_in_range()
* Parameters: lower_bound (int) , upper_bound (int), intguessed (int)
* Return Value: an integer
* Purpose: This gets an integer between the bounds from the user;
it does not allow a number out of the range
*******************************************************************************/
#include <iostream>
using namespace std;
void get_number_in_range(int lower_bound, int upper_bound, int &intguessed)
{
	while(intguessed < lower_bound || intguessed > upper_bound)//A loop which runs until the user inputs a value in the range;
	{
		cout << "Enter a number between " << lower_bound << " and " << upper_bound << endl;
		cin >> intguessed;
		if(intguessed >= lower_bound && intguessed <= upper_bound) // A test; if in range, returns the value
		{
			break;// Ends the while loop with the passed-by-value number in the range
		}
		else //A test; if it is out of range, it prints an error message and prompts the user again
		{
			cout << "ERROR! You must enter a number in the range. \n"; //An error message
		}
	}
}

/*******************************************************************************
* Class Name: Game()
* Purpose: This class has all the functions necessary to for running a game. It
runs through the menus until the player wants to quit
*******************************************************************************/
class Game
{
public:
	int ilevel;
	Game(int);
	~Game() {};
	void DisplayMenus(int intmenu);//Displays the game's menus
	void RunGame();//Runs the game continually
	int OneRound();//Plays one round of the game
};

Game::Game( int level = 0)
{
	ilevel = level;//The player's current level
}

/*******************************************************************************
* Function Name: main_game_menus()
* Parameters: intmenu chooses the menu to display
ilevel is the player's current level which is part of the class
* Return Value: Makes the current level 0 if the user wants to quit, a positive number for the level they will play.
* Purpose: This runs the menus for the start of the game and when finishes a level. It sets the
level to the one the user will play
*******************************************************************************/
void Game::DisplayMenus(int intmenu)
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
			ilevel = 1; //Sets the level to one
		}
		else if(intselection == 2) //Start playing at a level specified by the user
		{
			cout << "Input the number of the level you wish to play. \n "; //Prompts user for the level they want to play
			cin >> ilevel; //Sets the level to the user's input
		}
		if(intselection == 3)//Quits the program
		{
			ilevel = 0; //Sets the level to 0 which will end the program
		}
	}
	else if(intmenu == 2)// The menu displayed if the user loses
	{
		//The prompt asking if they want to replay the level they lost 
		cout << "Do you want to try level "<< ilevel << " again? \n" 
			<< "1. Yes. \n" 
			<< "2. Quit. \n";
		//Stores the menu selection
		cin >> intselection;

		// We only need to know if the user wants to quit; otherwise, the level returned will be the same as when it came in;
		if(intselection == 2)
		{
			ilevel = 0; //Sets the level to 0 which will end the program
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
			ilevel++;//Increases the level by 1
		}
		else if(intselection == 2)//The user wants to quit
		{
			ilevel = 0; //Sets the level to 0 which will end the program
		}
	}	
}

void Game::RunGame()
{
	int intmenu = 1;//Display the first menu by default
	int intwin = 0;//Assume that the user lost

	do//Ensures that the loop runs at least once despite the value of ilevel
	{
		DisplayMenus(intmenu);//Gets the level to be played; 0 means quit
		if(ilevel !=0)//If the user does not want to quit
		{	
			intwin = OneRound();//Plays the number game with a given level
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
	while(ilevel !=0);//The program will continue displaying menus 
	//until the user quits with a menu returning a ilevel of 0 

	system("cls"); //Clears the screen
	cout << "Thank you for playing. \n";//Thanks the user;
	system("pause");//Allows the user to see the thanking message

}

int Game::OneRound()
{
	int iwin = 0;
	int iplayerbox = -1;
	int iotherbox = -1;
	int irandom = 0;
	string slevel = to_string(ilevel);//Converts the level to a string to concatenate it into one of the prizes
	char chredraw; // Stores if the player wants to repick
	Box boxes[3];

	system("cls"); //Clears the screen
	cout << "Level " << ilevel << endl;

	cout << "Putting prizes in the boxes.... \n" ;

	srand(time(0));//seeds the random number generator
	irandom = (rand() % 2) + 1;//Creates a random number in the range between 0 and 3 for the array of the boxes

	//Puts prizes in the three boxes
	int boxposition = 1; //The current position as one of 3 boxes (#1,#2,#3)
	for(int i=0; i < 3; i++)
	{
		if(i == irandom)
		{
			boxes[i].SetValue(slevel+" million dollars", boxposition, 1);
		}
		else
		{
			boxes[i].SetValue("a herring", boxposition, 0);
		}
		boxposition++;	
	}

	cout << "There are 3 boxes. One of them has "<< slevel << " million dollars in it. \n Please input the number of the box you desire. \n";
	get_number_in_range(1,3,iplayerbox);

	iplayerbox -=1;//Subtracts one to set it equal to one of the boxes in the array

	for (int i=0; i < 3; i++)//This for loop picks a box to be revealed
	{
		if(boxes[i].iwinner == 0 && iplayerbox != i)
		{
			boxes[i].Reveal();
			break;
		}
	}

	for (int i=0; i < 3; i++)//This for loop figures out the other box that can be chosen.
	{
		if(iplayerbox != i && boxes[i].irevealed == 0)
			{
				iotherbox = i;//This is the number of box the player can choose when they get a chance to repick.
			}
	}



		cout << endl << "Would you like to switch to box #" << iotherbox+1 << "? y\\n \n";//Prompts the user to pick the other box. Adding one translates from array position to one of three boxes.
		cin >> chredraw;//Stores input

		if(chredraw == 'y')
		{
			iplayerbox = iotherbox;
		}

		boxes[iplayerbox].Reveal();

		if(boxes[iplayerbox].iwinner)//If they picked the winning box, iwin records that they won.
		{
			iwin = 1;
		}

		//Decides if the player won (iwin = 1) or lost (iwin = 0)	
		switch(iwin)
		{
		case 0: cout << "You lose! \n"; break;//Displays if the user lost (iwin = 0)
		case 1: cout << "You won! \n"; break;//Displays if the user won (iwin = 1)
		}

		return iwin;//Tells main whether the player won or lost
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
		Game CurrentGame(1);//Sets up a game to be run at level 1
		CurrentGame.RunGame(); //Runs the game
		return 0;
	}
