/*******************************************************************************
 * Program Name: CardGame 
 * Created Date: 10/2/2013
 * Created By: John Cadigan
 * Purpose: Plays the card drawing game with a number of redraws for each player
 *******************************************************************************/
#include <iostream>
#include <time.h>
#include <string>
#include <cstdlib>
using namespace std;


/*******************************************************************************
 * Class Name: Card()
 * Purpose: This Class has all the functions necessary to replicate cards
 for this game. PrintCard translates the numbers representing the values of the
 faces and suits into English. DefeatsCard checks to see if one card defeats another.
 SetValue gives cards their values.
  *******************************************************************************/
  
   class Card
 {
	
	public:
	int icardnumber, icardsuit;
	Card();
	~Card() {};
	void PrintCard();
	void SetValue(int inumber, int isuit);
	int DefeatsCard(Card othercard);

 };


 Card::Card()
{
		
};

 void Card::SetValue(int inumber, int isuit)
{
	icardnumber = inumber;// Card number; Jack = 11, Queen = 12, King = 13, Ace = 14
	icardsuit = isuit; // Card's suit; //clubs = 1, diamonds = 2, hearts = 3, and spades = 4;
}


void Card::PrintCard(void) {
  switch(icardnumber)//Prints the face of the card from a value
  {
  case 11: cout << "Jack "; break;
  case 12: cout << "Queen "; break;
  case 13: cout << "King "; break;
  case 14: cout << "Ace "; break;
  default: cout << icardnumber << ' '; break;
  }
  switch(icardsuit)// Prints the suit of the card from a value
  {
  case 1: cout << "of Clubs \n"; break;
  case 2: cout << "of Diamonds \n"; break;
  case 3: cout << "of Hearts \n"; break;
  case 4: cout << "of Spades \n" ; break;
  }

}

int Card::DefeatsCard(Card othercard)
{
	int idefeats = 0; //By default it returns a loss
	if(othercard.icardnumber < icardnumber)//If the card's face value beats the other's
	{
		idefeats = 1;
	}
	else if(othercard.icardnumber == icardnumber && othercard.icardsuit < icardsuit)// If there is a tie in face values and the card's suit defeats the other's...
	{
		idefeats = 1;
	}
	return idefeats;
}





/*******************************************************************************
 * Function Name: main_game_menus()
 * Parameters: intmenu chooses the menu to display, intlevel is the level the player's current level
 * Return Value: Returns 0 if the user wants to quit, a positive number for the level they will play.
 * Purpose: This runs the menus for the start of the game and when finishes a level. It returns
 the level at which the user will play
  *******************************************************************************/

int main_game_menus( int intmenu, int intlevel)
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
 * Function Name: draw_card()
 * Parameters: iothercard (int) , player (string)
 * Return Value: an integer
 * Purpose: This gets a card position different from the other players and prints
 out that they drew a card.
 *******************************************************************************/
#include <iostream>
using namespace std;
int draw_card(int iothercard, string player)
{
	
	int irandom = -1; //Sets the card positions to a nonsensical value
	do
	{
		srand(time(0));//seeds the random number generator
		irandom = (rand() % 51) + 1;//Creates a random number in the range between 0 and 51 for the array of the deck

	}while(irandom==iothercard); // A test; if it is the same it keeps going
	
	cout << player << " draws a card.... \n"; //Let's the user know that the player or computer drew a card
	return irandom;//Returns a different card position than the other player 

}

/*******************************************************************************
 * Function Name: play_card_game()
 * Parameters: ilevel (int)
 * Return Value: 1 meaning they won, 0 meaning they lost
 * Purpose: This function plays the number card game given a level;
 the user and computer both have a number of redraws equal to
 the level.
 *******************************************************************************/
#include <iostream>
int play_card_game(int ilevel)
{
	int iwin = 0;
	int iplayerredraws = ilevel;
	int icomputerredraws = ilevel;
	int iplayercard = -1;
	int icomputercard = -1;
	Card deck[52];
	
	system("cls"); //Clears the screen
	cout << "Level " << ilevel << endl;
	
	
	
	cout << "Shuffling the deck.... \n" ;
	
	//Creates deck of cards
	int cardposition = 0; //The current position in the array
	for( int isuit =1; isuit < 5; isuit++)//clubs = 1, diamonds = 2, hearts = 3, and spades = 4
	{
		for(int inumber =2; inumber < 15; inumber++)// Jack = 11, Queen = 12, King = 13, Ace = 14
		{
			deck[cardposition].SetValue(inumber,isuit);
			cardposition++;
		}
	}
	
		
	
	
	char chredraw; // Stores if the player wants to redraw

	while(iplayerredraws > 0)//A loop which runs until the user has no more redraws
	{
		iplayerredraws--;//decrements the redraws
		iplayercard = draw_card(icomputercard, "Player");//draws a card
		
		//Lets the user know what card they have
		cout << "Your card is the ";
		deck[iplayercard].PrintCard(); 
		
		if(iplayerredraws > 0)//Displays option to redraw if the user can
		{
		cout << endl << "Would you like to redraw your card? y\\n \n";//Prompts the user to redraw
		cin >> chredraw;//Stores input
		if(chredraw == 'n'){break;};//If the user does not want to redraw, it will break the loop
		}
		
	}

	while(icomputerredraws > 0)//A loop which runs until the computer has no more redraws
	{
		icomputercard = draw_card(iplayercard, "Computer"); //Draws a card for the computer
		icomputerredraws--;//takes away one redraw

		// With one redraw, it try to stick with 7 or better; 2 redraws, 10ish;
		// It will adjust when the redraws goes down
		int expected_average_card = 0;
		expected_average_card = 14 - (14 /(icomputerredraws+1));
		
		//Ends the computers redraws if it runs out of them or draws a card which is good for the
		//number of redraws that remain
		if(icomputerredraws == 0 || deck[icomputercard].icardnumber > expected_average_card)
		{
		break;
		}

		
	}


	//Lets the user know what the computer drew
	cout << "The computer drew a ";
	deck[icomputercard].PrintCard();
	cout << endl;

	//Decides if the player won (iwin = 1) or lost (iwin = 0)
	iwin = deck[iplayercard].DefeatsCard(deck[icomputercard]);
	
	switch(iwin)
	{
	case 0: cout << "You lose! \n"; break;//Displays if the user lost (iwin = 0)
	case 1: cout << "You won! \n"; break;//Displays if the user won (iwin = 1)
	}

	return iwin;//Tells main whether the student won or lost
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

	do//Ensures that the loop runs at least once despite the value of intlevel
	{
		intlevel = main_game_menus(intmenu, intlevel);//Gets the level to be played; 0 means quit
		if(intlevel !=0)//If the user does not want to quit
		{	
			intwin = play_card_game(intlevel);//Plays the number game with a given level
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






