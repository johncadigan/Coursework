#include <iostream>
#include <string>
#include <sstream>
#include <cstdlib>
using namespace std;

/*******************************************************************************
* Program Name: NumberPictures
* Created Date: 12/13/2013
* Created By: John Cadigan
* Purpose: Displays pictures based on sequences of numbers
*******************************************************************************/



//You can modify these numbers but don't delete these constants or this starting code will not work
const int YMAX = 20; // Array bound for screen height
const int XMAX = 70; // Array bound for screen length

// DO NOT ALTER OR DELETE THIS CODE (START)!!!!!!!!!!!!!!!!!!!!!!!!!!!
/********************************************************************
 * Class: Draw
 * Purpose: To process a list of numbers to draw a picture on the console.
 ********************************************************************/
class Draw {
	protected:
		char display[XMAX][YMAX]; // 20 by 70 character array to hold the picture
		int input, xpos, ypos;
	public:
		// Constructor to initialize object member data
		Draw() : input(0), xpos(0), ypos(YMAX - 1)
		{	}
		void greeting(); // Greeting screen to let the user know what this program is and to instruct the user on how to use the program
		void setup_screen(); // Setup the array 
		void process_picture(); // Process the user provided string and store into the array
		void display_picture(); // Print the picture onto the screen
};

	void Draw::greeting() {
		cout << "Welcome to the picture string generator!" << endl
			 << "Please enter a string of numbers representing " << endl
             << "a picture that you would like to display." << endl
			 << "Numbers print as the following:" << endl << endl
			 << "8   1   2" << endl
			 << " \\  |  /" << endl
			 << "7 --+-- 3" << endl
			 << " /  |  \\" << endl
			 << "6   5   4" << endl << endl
			 << "Positive numbers will draw an *." << endl
			 << "A negative number will move the cursor but not draw a *." << endl;
	}

	void Draw::setup_screen() {
	}

	void Draw::process_picture() {
	}

	void Draw::display_picture() {
	}
// DO NOT ALTER OR DELETE THIS CODE (END)!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


/********************************************************************
 * Class: CodeDraw
 * Purpose: Has the methods to process and display a picture from numbers
 ********************************************************************/
class CodeDraw: public Draw{
	public:
	//Overloads the methods from Draw
	void setup_screen();  
	void process_picture();  
	void display_picture(); 
};

	void CodeDraw::setup_screen()// Fills the array with empty spaces
{
	
	for(int x = 0; x < XMAX; x ++) //Iterates horizontally
	{
		for(int y = 0; y <YMAX; y ++) //Iterates vertically
		{
			display[x][y] = ' ';// Makes the default display ' ';
		}
	}
	
}
	
	void CodeDraw:: process_picture()
{
	
	string input;
	
	//Clear the buffer
	cin.clear();

	cout << "Please input the number sequence ending with 0 to draw a picture. \n";
	getline(cin, input);// Gets the input
	
	//Sets the position to the bottom left
	xpos = 0;
	ypos = 0;
	
	char character;// the character which will be put into the current position
    int i =0;
    while(input.at(i) != '0')//Keeps going until it is a 0
    {
		character = '*'; //sets character to its default
		char cnumber;
		cnumber = input[i];//The current character from the string
		
		if(cnumber != ' ' && cnumber !='-')// If it is not a symbol or a minus symbol
		{
			//Add move the position in the x and y directions
			if(cnumber == '8' || cnumber =='1' || cnumber =='2'){
			ypos++;//These move y up
			}
			if(cnumber == '6' || cnumber == '5' || cnumber =='4'){
			ypos--;//These move y down
			}
			if(cnumber == '2' || cnumber == '3' || cnumber=='4'){
			xpos++;//These move x up
			}
			if(cnumber == '8' || cnumber == '7' || cnumber == '6'){
			xpos--;//These move x down
			}
			
			if(i >= 1)//Begin checking for previous character when possible
			{ 
				if(input[i-1] == '-')//If a minus sign precedes it, the character put into the display will be a space ' '
				{
				character = ' '; //It an empty space will go into the current position
				}  
			}
			
			//Adds the character if it is within the maximum boundaries
			if(ypos >= 0 && xpos >= 0)
			{	
			display[xpos][ypos] = character;
			}
		}
		i++ ;//Increases i
	}
}

	void CodeDraw::display_picture()
{
	
	cout << "Your picture: \n";
	
		for(int y = YMAX-1; y >= 0; y --) //Starts printing from the top 
	{
		for(int x = 0; x < XMAX; x ++) //Starts print from left to right to retain orientation
		{
			cout << display[x][y]; //prints the character
		}
		cout << endl; //Ends once the horizontal line has beeen printed by reaching its end
	}
};


int main() 
{
	CodeDraw drawer;
	string input;
	int icontinue = 1;
	//The menu
	cout << "*****" << "Pictures Worth 1401 Numbers" << "***** \n";
	drawer.greeting();
	//Gives the options
	do{		
		cout << "Please enter your selection: \n 1. Create a picture. \n 2. Quit \n";
		cin.clear();
		getline(cin, input);
		stringstream StringNumber(input);
		StringNumber >> icontinue;
		//If the user wants to make a picture, icontinue will equal 1.
		if(icontinue==1)
		{
		drawer.setup_screen();//Fills the display with empty spaces
		drawer.process_picture();//Gets input and processes it
		drawer.display_picture();//Shows the display
		}
	}while(icontinue==1);
	
	
    cout << "Thank you for using this program! \n Enter any key to end the program: \n";
	cin.ignore().get(); //This is a pause for Linux
	return 0;
}
