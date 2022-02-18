This version for the N-Queen Code included Island Migration Implementation of Genetic Algorithm\

There are few improvements made to the Genetic Algorithm Code, firstly, there are six islands which will at every fix iteration migrate to the other islands such that the population will be refreshed. The choose for migrating population is selected randomly and during each migration, 2 randomly chosen population will migrate to the other island, which means that a total of 10 new population will be introduced to each island at each migration. Therefore, to ensure survival of natively population, a minimum population of at least 12 is asserted in the code. However, in practice, 30 population is used for each island.\

Furthermore, to add on towards last assignment’s improvement of refreshing the population, at a pre-defined iteration called *refresh rate*, a new population will be generated for a single island. For example, if the*refresh rate* is set to be 500 iteration, island 1’s population will be regenerated at 500 iterations, island 2’s population will be regenerated at 1,000 iterations and island 3’s population will be regenerated at 1,500 iterations, so on and so forth.\

To run the python file, you would need *scipy* library which can be install using pip install\

-pip install scipy-\

When you launch the script, you will be prompted to define the following\

Number of Queen: Which sets the number of Queen in the chess board, this value needs to be bigger or equals to 1.

Population Size:  Which sets the population size for each island, this value needs to be bigger than 12

Mutation Rate: Which sets the probability of mutation, this value needs to be between 0 to 1

Run Limit (α): Which sets the upper limit for the script, if no answer is found after α iterations, the algorithm will stop.

Migration Rate (β): Which sets the rate of migration. Island migration will occur every β iterations.

Refresh Rate (γ): Which sets the refresh rate. After γ iteration, the population in the first island will get regenerated, while at iteration nγ,n island’s population will get regenerated. This is added to getting the model out of the local minimum.
