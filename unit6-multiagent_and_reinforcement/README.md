# Core Assessment - Game-Playing Agent

## Introduction

### Project Format

This project will involve developing Python code to develop a search algorithm to competitively play a two-player game. The game description is provided in Unit 3. You will begin with code for the minimax algorithm provided by the authors of our book and code for representing game states discussed during Unit 3. You will work in teams of two or as individuals to develop your solutions. 

### Purpose

One of the two main goals of this project is to provide you with a substantial and meaningful problem for which there is no known perfect solution. AI is seldom employed to solve a problem where a 100% correct solution is expected. More often, AI is applied to problems where perfection is out of reach and the goal is to maximize performance as much as possible. In this project, you will write a program that, with limited computing resources, must play a 2-player game as well as it can, which will necessarily involve reasoning about the complexity of the search process and how to optimize it.

The other main goal is to provide a substantial project for you to apply your AI Python programming skills. You will extend code developed by the book authors and professors at Park University to apply a well-known search algorithm (minimax with alpha-beta pruning) to a specific problem. You will learn to use Python to model a problem in such a way as to be solvable by such an algorithm and also learn to work with others to develop AI code. 

### Relation to CLOs

This project will get you more involved in Python programming and the complexity involved with implementing AI algorithms and will thus focus on CLO’s 1, 4, and 5.

### Specific Tools

A Python 3 IDE (either Thonny or another IDE) and GitHub

## Directions

- In Unit 3 we began discussing the choice of 2-player game for our class and Python code to represent game states in a search space. Make sure you’re familiar with this code and the rules of the game.

- By Unit 5 you should have an idea of who you want to work with on the project. Make sure the instructor is aware of your choice of partner and has approved this choice before beginning your work in Unit 6. If you’re not sure who to partner with but want a partner, contact your instructor.

- Your instructor will provide you with a link to a GitHub template repository with the minimax code from AIPython modified to represent game states for the chosen game for this semester. Create your own private repository based on this template and share access with your partner and your instructor. They should both provide you with their GitHub usernames.

- Develop the isLeaf method (look for the TODO comments). This method should determine if the game state in a node represents the end of a game or not by returning True or False. Once you believe you have correctly implemented this method, commit your code to GitHub and ensure it passes the test cases for this method. Once it passes the test cases, move on to the next step.

- Develop the legalMoves method. This method should determine what moves the current player can make from the current game state. This list of moves will be used to generate the child nodes of this node when the node is expanded in the minimax search. Again, commit the code to the repository and ensure it passes the unit tests for this method before moving on to the next step.

- Develop the evaluate method. This method represents your game-playing heuristic and will be used by your game-playing agent to determine what moves to make. It should return a positive value for beneficial game states and a negative value for detrimental game states (0 for a neutral state). Keep in mind that this method must be efficient to allow you to search at greater depths and thus find better moves against your opponent, but it is completely up to you how you develop this heuristic. You can test your heuristic by playing against your own agent or having your agent play against the random-guessing agent.

- Develop your project report. This report should contain 1-2 paragraphs addressing each of the following:
    - Strategy taken to optimize time/memory complexity of isLeaf and legalMoves methods while maintaining correctness.
    - Justification of choices made for the evaluate method and why you believe they would lead to better results for the chosen game.
    - Strategy taken for testing your software, details of the tests performed, and the results of the tests.
    - Problems encountered while developing any of the three methods and how they were resolved.

- When you are finished, submit a PDF file of your project report and each of the python files used for your project.