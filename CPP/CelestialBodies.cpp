/*******************************************************************************
 * Program Name: CelestialWeights
 * Created Date: 09/04/2013
 * Created By: John Cadigan
 * Purpose: Calculates a person's weight on various celestial bodies in the solar system
 * Acknowledgements: None
 *******************************************************************************/



/*******************************************************************************
 * Function Name: get_float()
 * Parameters: prompt (string)
 * Return Value: a float
 * Purpose: This gets a positive float number from the user with a given prompt; 
 it does not allow negative numbers;
 *******************************************************************************/
#include <iostream>
#include <string>
#include <cstdlib>
using namespace std;
float get_float(string prompt)
{
	float floatnumber = 0;
	while(floatnumber <= 0)//A loop which runs until the user inputs a positive value for their weight;
	{
		cout << prompt;
		cin >> floatnumber;
		if(floatnumber > 0) // A test; if positive, returns the value
		{
			return floatnumber;
		}
		else //A test; if it is 0 or negative, it prints an error message and prompts the user again
		{
			cout << "ERROR! You must enter a positive number. \n"; //An error message
		}
	}
}

/*******************************************************************************
 * Function Name: give_result()
 * Parameters: weightOnplanet(float), planet(string)
 * Return Value: prints things to the screen
 * Purpose: This function prints the results to the screen in a formatted table; 
 *******************************************************************************/
#include <iostream>
#include <iomanip>
using namespace std;
void give_result(float weightOnplanet, string planet)
{
	
	//sets the precision to two decimal places
	std::cout.precision(2);
	
	//prints the table's row
	cout << setw(15) << planet << " = " << setw(10) << std::fixed << weightOnplanet << setw(10) << " pounds."<< endl;
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

	float  weight, sunweight, mercuryweight, venusweight, earthweight, moonweight, marsweight, jupiterweight, saturnweight, uranusweight, neptuneweight, plutoweight;
	
	weight = get_float("What is your weight in pounds?: \n"); // sets weight equal to the user's input
	
	//Calculates weight on the Sun
	sunweight = 27.9 * weight;
	give_result(sunweight, "Sun"); //prints the result
	
	//Calculates weight on Mercury
	mercuryweight = 0.38 * weight;
	give_result(mercuryweight, "Mercury"); //prints the result
	
	//Calculates weight on Venus
	venusweight = 0.91 * weight;
	give_result(venusweight, "Venus"); //prints the result
	
	//Calculates weight on Earth
	earthweight = 1.00 * weight;
	give_result(earthweight, "Earth"); //prints the result
	
	//Calculates weight on the moon
	moonweight = 0.17 * weight;
	give_result(moonweight, "Earth's moon"); //prints the result
	
	//Calculates weight on Mars
	marsweight = 0.38 * weight;
	give_result(marsweight, "Mars"); //prints the result
	
	//Calculates weight on Jupiter
	jupiterweight = 2.54 * weight;
	give_result(jupiterweight, "Jupiter"); //prints the result
	
	//Calculates weight on Saturn
	saturnweight = 1.08 * weight;
	give_result(saturnweight, "Saturn"); //prints the result
	
	//Calculates weight on Uranus
	uranusweight = 0.91 * weight;
	give_result(uranusweight, "Uranus"); //prints the result
	
	//Calculates weight on Neptune
	neptuneweight = 1.19 * weight;
	give_result(neptuneweight, "Neptune"); //prints the result
	
	//Calculates weight on Pluto
	plutoweight = .06 * weight;
	give_result(plutoweight, "Pluto"); //prints the result

	system("pause");
	return 0;
}


