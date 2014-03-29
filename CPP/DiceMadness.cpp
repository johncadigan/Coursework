#include <iostream>
#include <time.h>
#include <string>
#include <cstdlib>
using namespace std;

/*******************************************************************************
* Program Name: Dice Madness
* Created Date: 11/18/2013
* Created By: John Cadigan
* Purpose: Plays the dice game with a number of rerolls for each player and
a limited number of levels
*******************************************************************************/

const int maxlevel = 5;//This stores the maximum level of the game
const string gametitle = "Dice Madness";

/*******************************************************************************
* Class Name: Die()
* Purpose: This class has all the functions necessary to prize boxes
for this game. PrintCard translates the numbers representing the values of the
faces and suits into English. DefeatsCard checks to see if one card defeats another.
SetValue gives cards their values.
*******************************************************************************/
class Die
{
private:
	int ivalue;
public:
	Die();
	~Die() {};
	void Show();
	void SetValue(int intvalue);
	int ReturnValue();
	Die operator + (Die temp);
};

Die::Die()
{

};

Die Die::operator + (Die temp)
{

	int totalivalue;
	Die totalDie;
	totalivalue = ivalue + temp.ivalue;
	totalDie.SetValue(totalivalue);
	return totalDie;
}

void Die::Show(void) {
	switch (ivalue)
	{
	case 1:
		cout << " -----\n"
			 <<	"|     |\n"
			 << "|  O  |\n"
			 <<	"|     |\n"
			 <<	" -----\n"; 
		break;
	case 2:
		cout << " -----\n"
			 <<	"|    O|\n"
			 << "|     |\n"
			 <<	"|O    |\n"
			 <<	" -----\n"; 
		break;
	case 3:
		cout << " -----\n"
			 <<	"|    O|\n"
			 << "|  O  |\n"
			 <<	"|O    |\n"
			 <<	" -----\n";  
		break;
	case 4:
		cout << " -----\n"
			 <<	"|O   O|\n"
			 << "|     |\n"
			 <<	"|O   O|\n"
			 <<	" -----\n";
		break;
	case 5:
		cout << " -----\n"
			 <<	"|O   O|\n"
			 << "|  O  |\n"
			 <<	"|O   O|\n"
			 <<	" -----\n"; 
		break;
	case 6:
		cout << " -----\n"
			 <<	"|O   O|\n"
			 << "|O   O|\n"
			 <<	"|O   O|\n"
			 <<	" -----\n"; 
		break;
	}
	cout << "\n";
}

void Die::SetValue(int intvalue) {
	ivalue = intvalue;
}

int Die::ReturnValue(){
	return ivalue;
}


/*******************************************************************************
* Function Name: rolldie()
* Parameters: 
* Return Value: a random number between one and six
* Purpose: This rolls one die and gives it a random value
*******************************************************************************/
int rolldie(){
	int irandom = 0;
	srand(time(NULL));//seeds the random number generator
	irandom = (rand() % 6) + 1;//Sets the value of the die to a random number in the range between 1 and 6		 
	return irandom;
}

/*******************************************************************************
* Class Name: Game()
* Purpose: This class has all the functions necessary to for running a game. It
runs through the menus until the player wants to quit
*******************************************************************************/
class Game
{
public:
	int ilevel, imaxlevel;
	Game(int, int);
	~Game() {};
	void DisplayMenus(int intmenu);//Displays the game's menus
	void RunGame();//Runs the game continually
	int RunLevel();//Plays one level of the game
	int RollDice();//Rolls dice and returns one die with their total value 
};

Game::Game( int level = 0, int maxlevel = 0)
{
	ilevel = level;//The player's current level
	imaxlevel = maxlevel;//The max level of the game
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
	cout << "*^*^*^*^*^*^*^*^ " << gametitle << " *^*^*^*^*^*^*^*^" << endl;
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
			cout << "Input the number of the level you wish to play which is less than " << maxlevel + 1 << ". \n "; //Prompts user for the level they want to play
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
		if(intselection == 2)//Runs only if the user wants to quit
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
			intwin = RunLevel();//Plays the number game with a given level
			if(intwin == 1)//If the user wins
			{
				ilevel++;//Increases the level by 1
				if(ilevel >= maxlevel)// Ends the program if they beat all of the levels
				{
					system("cls"); //Clears the screen
					cout << "Congratulations! You have wasted too much time playing this game. You must quit!\n";
					system("pause");//Allows the user to see the defeating the game message
					break;
				}
				intmenu = 3;//Display the continue screen if they have not beat the game
			}
			else//If the user loses
			{
				intmenu = 2;//Display the replay screen
			}
		}
	}
	while(ilevel !=0 );//The program will continue displaying menus 
	//until the user quits with a menu returning a ilevel of 0 
	
	system("cls"); //Clears the screen
	cout << "Thank you for playing. \n";//Thanks the user;
	system("pause");//Allows the user to see the thanking message

}

int Game::RollDice(){
	Die Total; //For operator overloading
	Die dice[maxlevel+2];
	int extradice = ilevel; //Adds an extra die per level

	Total.SetValue(0);
	dice[0].SetValue(0);//Creates a null dice
	cout << "Rolling dice...\n";
	for(int i=1; i<maxlevel+2; i++)// Adds enough dice for one extra per level until the max level
	{
		int idie = 0;
		do{
			idie = rolldie();
		}while(idie == dice[i-1].ReturnValue());
		dice[i].SetValue(idie);//Sets the value of the die to a random number in the range between 1 and 6		 
	}
	for(int i=1;i<extradice+2; i++)// Shows the real dice relevant to this round; not the null
	{
			dice[i].Show();
			Total = Total + dice[i];
	}

	cout << "They total " << Total.ReturnValue() << endl;
	return Total.ReturnValue();
}



int Game::RunLevel() //This runs one level of the game. It returns 1 with a win; 0, a loss.
{
	int iwin = 0, rounds = 6; 
	int pscore = 0, cscore = 0;//The total scores
	int extradice = ilevel; //Adds an extra die per level
	//The computer and player each get rerolls to use for the level
	int iprerolls = ilevel*2; 
	int icrerolls = ilevel*2;
	
	//Explains the game
	system("cls");
	cout << "You and the computer will each roll " << 1+extradice << " dice during 6 rounds.\n";
	cout << "You both have " <<iprerolls << " chances to reroll the dice on this level.\n";
	cout << "The player with the biggest total at the end wins.\n";
	system("pause");
	

	while(rounds > 0)
	{
		char chredraw = 'y'; // Stores if the player wants to repick; defaults to y
		int pround = 0, cround = 0;// The scores for this round

		//The scoreboard for the game
		system("cls"); //Clears the screen
		cout << "Level " << ilevel << " | Round "<< 6-rounds + 1 << " of 6" << endl;
		
	
		//**** This is the player's turn////////////////////////////////////////////////
		cout << "Player's total score " << pscore << "| Computer's score   " << cscore << endl;
		cout << "Player's rerolls     " << iprerolls << "| Computer's rerolls " << icrerolls << endl;
		cout << "It's your turn. \n";
		
		//Rolls the dice once at least
		pround = RollDice();
		
		//Prompts the user for rerolls if they are available
		while(iprerolls > 0 && chredraw=='y')
		{		
			cout << "Would you like to reroll? You have " << iprerolls << " remaining for this level.\n y\\n?";
			cin >> chredraw;
			if(chredraw == 'n')
			{
				break; // ends the loop iff they do not want to reroll
			}
			else
			{	
				pround = RollDice();//Stores the new value of the score
				iprerolls--;
			}
		}
		
		//**** This is the computer's turn////////////////////////////////////////////////
		cout << "It's the computer's turn. \n";
		//Rolls the dice at least once for the computer
		cround = RollDice();
		
		//Runs if the computer will fall behind the player based on its current roll
		while(icrerolls > 0 && cscore + cround <= pround + pscore)
		{	
			cout << "The computer chooses to reroll. \n";
			cround = RollDice();
			icrerolls--;
		}

		pscore += pround;// Adds the player's score of the current round to the total
		cscore += cround;// Adds the computers's score of the current round to the total
		rounds--;//Takes away one round
		system("pause");///So the user can see what the computer did
	}

	if(cscore <= pscore)//If the player ties or beats the computer then it wins
	{
		iwin = 1;
	}

	///Final scoreboard
	system("cls");
	cout << "FINAL SCORES \n";
	cout << "Player's total score " << pscore << "| Computer's score " << cscore << endl;
	
	//Decides if the player won (iwin = 1) or lost (iwin = 0)	
	switch(iwin)
	{
	case 0: cout << "You lose! \n"; break;//Displays if the user lost (iwin = 0)
	case 1: cout << "You won! \n"; break;//Displays if the user won (iwin = 1)
	}
	system("pause");
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
	Game CurrentGame(1, maxlevel);//Sets up a game to be run at level 1 with a max set by the constant variable maxlevel
	CurrentGame.RunGame(); //Runs the game
	return 0;
}
