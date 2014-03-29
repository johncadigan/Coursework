#include <iostream>
#include <sstream>
#include <string>
#include <cstdlib>
using namespace std;

/*******************************************************************************
* Program Name: CaesarCipher
* Created Date: 12/2/2013
* Created By: John Cadigan
* Purpose: Encrypts and decrypts messages with a given cypher using Caesar Encoding
*******************************************************************************/

int INT_MAX = 20;

/*******************************************************************************
 * Function Name: get_number_in_range()
 * Parameters: lower_bound (int) , upper_bound (int)
 * Return Value: an integer
 * Purpose: This gets an integer between the bounds from the user;
 it does not allow a number out of the range
 *******************************************************************************/
int get_number_in_range(int lower_bound, int upper_bound)
{
	string input;
	int validint = 0; //Stores the user's  number
	while(validint < lower_bound || validint > upper_bound)//A loop which runs until the user inputs a value in the range;
	{
		cin.clear(); 
		cin.ignore(INT_MAX,'\n'); 
		cout << "Enter a number between " << lower_bound << " and " << upper_bound << endl;
		getline(cin, input);
		stringstream StringNumber(input);
		if(StringNumber >> validint)
		{
			if(validint >= lower_bound && validint <= upper_bound) // A test; if in range, returns the value
			{
				return validint; //Returns the guess in the appropriate range
				break;// Ends the while loop
			}
			else //A test; if it is out of range, it prints an error message and prompts the user again
			{
			cout << "ERROR! You must enter a number in the range. \n"; //An error message
			}
		}
		else
		{
			cout << "ERROR! Invalid value for a number. \n";
		}
		
	}
}

class Message
{
private:
		string smessage;
		int icipher;
public:
	Message();
	~Message() {};
	void print_encoded();
	void print_decoded();
	void get_message();
	char shift_alpha_char(char alphachar, int ishiftvalue);
};

Message::Message()
{

}

void Message::print_encoded()
{
	int shiftvalue = 0 + icipher; //We add the value of the cipher to encode a message
	for(int i=0; i < smessage.length(); i ++)
	{
	cout << shift_alpha_char(smessage.at(i), shiftvalue);//Iterates through the message's characters w/ the shiftvalue
	}
}
void Message::print_decoded()
{
	int shiftvalue = 0 - icipher;//The encoded message had the cipher added to it; we add the negative value of the cipher to reverse this
	for(int i=0; i < smessage.length(); i ++)
	{
		cout << shift_alpha_char(smessage.at(i), shiftvalue);//Iterates through the message's characters w/ the shiftvalue
	}
}		
char Message::shift_alpha_char(char alphachar, int ishiftvalue)
{
	int alphaint = int(alphachar);
	int intvalue = alphaint; //Stores the integer value of the character
	
	if (65 <= alphaint && alphaint <= 90)//Runs for capital letters
	{
		intvalue = alphachar + ishiftvalue; //Sets intvalue to the sum
		if(intvalue > 90)// If the sum exceeds the capital letter range;
		{
			intvalue = 64 + (intvalue) % 90; // it wraps around to equal the remainder
		}
		else if(intvalue < 65)// If the sum goes under the capital letter range
		{
			intvalue = 91 + (intvalue-65); // it adds the wrap around in the opposite direction
		}
	}

	if (97 <= alphaint && alphaint <= 122)//Runs for lowercase letters
	{
		intvalue = alphachar + ishiftvalue; //Sets intvalue to the sum
		if(intvalue > 122)// If the sum exceeds the capital letter range;
		{
			intvalue = 96 + (intvalue) % 122; // it wraps around to equal the remainder
		}
		else if(intvalue < 97)// If the sum goes under the capital letter range
		{
			intvalue = 123 + (intvalue-97); // it adds the wrap around in the opposite direction
		}
	}


	return char(intvalue);
}
	
void Message::get_message()
{
	string operation;
	cout << "Please input \"encode\" or \"decode\" to begin.\n";
	getline(cin, operation);//Stores the value of the input in operation
	cout << "Please input your message and end it with a ~: \n";
	getline(cin, smessage, '~');//Stores the encrypted or decrypted string
	cout << "Please input the cipher shift. \n";
	icipher = get_number_in_range(1,20);
	cout << "Your result is: \n";
	if (operation == "encode")
	{	
		print_encoded();//Returns the message in its encoded form
	}
	else
	{
		print_decoded();//Returns the message in its decoded form
	}
	cout << "\n\n";
	system("pause");//Allows the user to see the returned value

}



int main()
{
	Message message;
	int icontinue;
	string input;
	
	//Runs the main menu of the program
	do{
	system("cls");
	cout << "*****" << "Secure Message Service" << "***** \n";
	cout << "Please enter your selection: \n 1. Process a message. \n 2. Quit \n";
	getline(cin, input);
	stringstream StringNumber(input);
	StringNumber >> icontinue;
    //If the user wants to operate on a message, icontinue will equal 1.
	if(icontinue==1)
	{
		message.get_message();
	}
	}while(icontinue==1);
	cout << "Thank you for using this service. \n";
	system("pause");

	return 0;
}
