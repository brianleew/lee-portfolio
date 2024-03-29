#include <iostream>
#include <string>

using namespace std;

class WordGuess {
private:
	string solution;
	string puzzle;
	string guessedLetters;
	int misses;
	int maxMisses;
	bool gameOver;
public:
	WordGuess(string s) {
		this->solution = s;
		puzzle = "";
		guessedLetters = "";
		misses = 0;
		gameOver = false;
		maxMisses = 3;
	}

	void guessLetter(char match)
	{
		bool gameOver = false;
		for (int i = 0; i < guessedLetters.length(); i++)
		{
			if (match == guessedLetters[i])
			{
				return;
			}
		}
			for (int i = 0; i <= solution.length(); i++)
			{
				if (match == solution[i])
				{
					gameOver = true;
				}
			}
			if (gameOver == false)
			{
				misses++;
			}

			guessedLetters += match;
		}

		string getGuessedLetters()
		{
			return guessedLetters;
		}

		string getPuzzle()
		{
			return puzzle;
		}

		int getMisses()
		{
			return misses;
		}

		void calculatePuzzle()
		{
			bool gameOver = false;

			puzzle = "";
            
			for (int i = 0; i < solution.length(); i++) // solution array size is always 4, containing kissa 5 letters
			{
				puzzle += "-";
				gameOver = false;
			    
			   	for (int i = 0; i < guessedLetters.length(); i++) // varies dependingg on commenting out i and k which is 4 
				{
					if (solution[i] == guessedLetters[i])
					{
						
						puzzle[i] = solution[i];
					    gameOver = true;
					}
					if (solution[i] != guessedLetters[i])
					{
				        //puzzle += "-";
				        
				        
				        //solution[i] = guessedLetters[i];
				        //solution[i] = puzzle[i];
				        //guessedLetters[i] = solution[i];
				        //guessedLetters[i] = puzzle[i];
				        //puzzle[i] = guessedLetters[i];
				        //puzzle[i] = solution[i];
				        
				        gameOver = false;
					}
					
	            }
	           
			}
			
		}


		bool isGameOver()
		{
			if (puzzle == solution)
			{
				gameOver = true;
			}
			else
			{
				gameOver = false;
			}
			return gameOver;
		}
	};

	int main()
	{
		WordGuess wordGuess("kissa"); // Instantiate the class.
		wordGuess.calculatePuzzle(); // Assemble current puzzle.
		cout << "Puzzle: " << wordGuess.getPuzzle() << endl; // Display puzzle to the user.
		cout << "Guessing: a, d, s, f, d" << endl; // This is what user is guessing

		// Inputting what the user guessed
		wordGuess.guessLetter('a'); // correct but commented out initially
		wordGuess.guessLetter('d'); // wrong
		wordGuess.guessLetter('s'); // correct
		wordGuess.guessLetter('f'); // wrong
		wordGuess.guessLetter('d'); // No effect on the number of misses since d was already guessed
		//wordGuess.guessLetter('k'); // correct but commented out initially
		//wordGuess.guessLetter('i'); // correct but commented out initially

		wordGuess.calculatePuzzle(); // Assemble/refresh current puzzle.

		// Print the result of the guesses...
		cout << "Guessed letters: " << wordGuess.getGuessedLetters() << endl;
		cout << "Number of misses: " << wordGuess.getMisses() << endl;
		cout << "Puzzle: " << wordGuess.getPuzzle() << endl; // Display puzzle to the user.
		cout << "Game over? " << wordGuess.isGameOver() << endl; // 0 for no, 1 for yes.

		// Print the result of the guesses...
		cout << "Guessed letters: " << wordGuess.getGuessedLetters() << endl;
		cout << "Number of misses: " << wordGuess.getMisses() << endl;
		cout << "Puzzle: " << wordGuess.getPuzzle() << endl; // Display puzzle to the user.
		cout << "Game over? " << wordGuess.isGameOver() << endl; // 0 for no, 1 for yes.
	}





