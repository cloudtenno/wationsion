# This script is modified from https://github.com/chengxi600/RLStuff/blob/master/Genetic%20Algorithms/8Queens_GA.ipynb
# Modification made in initialization population generation and mutation to avoid duplicating queens
# Improvement made in user interface where user can set the number of queen, population size, mutation rate and maximum epoch
# Error Control also implemented
# Result will be log in text file named Final_Result.txt and should be found under the same directory
# Also added feature to refresh the population to prevent GA getting stuck at local point
# If stuck at local point, try increasing the population size or increasing the mutation rate
# Change the refresh_rate if the program refresh the population too fast

import random
from scipy import special as sc
import itertools

log = open('N_Queen_Output.txt','w')

print('\nProgram Written by Lu Xinpei')
print('\nProgram Started, to stop press Ctrl+C\n')

reset_seq = 0

generation = 1

MIXING_NUMBER = 2

result = []

def get_number_queen():
    try:
        NUM_QUEENS = int(input('Enter Number of Queens: '))
        assert NUM_QUEENS > 0, 'Population size must be greater than 0'
        return int(NUM_QUEENS)
    except KeyboardInterrupt:
        print('\nProgram Stopped')
        exit()
    except:
        print('Please Enter integral above 0')
        retry_queen = get_number_queen()
        return retry_queen

def get_population_size():
    try:
        POPULATION_SIZE = int(input('Enter Population Size: '))
        assert POPULATION_SIZE > 12, 'Population size must be greater than 12'
        return int(POPULATION_SIZE)
    except KeyboardInterrupt:
        print('\nProgram Stopped')
        exit()
    except:
        print('Please Enter integral above 12')
        retry_pop_size = get_population_size()
        return retry_pop_size

def get_mutation_rate():
    try:
        MUTATION_RATE = float(input('Enter Mutation Rate: '))
        assert MUTATION_RATE > 0 and MUTATION_RATE < 1, 'Mutation Rate must be between 0 and 1'
        return float(MUTATION_RATE)
    except KeyboardInterrupt:
        print('\nProgram Stopped')
        exit()
    except:
        print('Please Enter decimal between 0 and 1')
        retry_mut_rate = get_mutation_rate()
        return retry_mut_rate

def get_run_limit():
    try:
        run_limits = int(input('Enter Maximum Epoch: '))
        assert run_limits > 10000, 'Must have more than 10,000 Epoch'
        return int(run_limits)
    except KeyboardInterrupt:
        print('\nProgram Stopped')
        exit()
    except:
        print('Please Enter integral above 10,000')
        retry_run_limits = get_run_limit()
        return retry_run_limits

def get_migration_rate():
    try:
        migration_rate = int(input('Enter Migration Rate: '))
        assert migration_rate > 25 and migration_rate < 250, 'Must have more than 10,000 Epoch'
        return int(migration_rate)
    except KeyboardInterrupt:
        print('\nProgram Stopped')
        exit()
    except:
        print('Please Enter integral between 25 to 250')
        retry_migration_rate = get_migration_rate()
        return retry_migration_rate

def get_refresh_rate():
    try:
        refresh_rate = int(input('Define the number of epoch before population refreshes: '))
        assert refresh_rate >= 500, 'refresh rate must be greater than 500'
        return int(refresh_rate)
    except KeyboardInterrupt:
        print('\nProgram Stopped')
        exit()
    except:
        print('Refresh rate must be greater than 500')
        retry_refresh_rate = get_refresh_rate()
        return retry_refresh_rate

def fitness_score(seq):
    score = 0
    for row in range(NUM_QUEENS):
        col = seq[row]
        for other_row in range(NUM_QUEENS):
            #queens cannot pair with itself
            if other_row == row:
                continue
            if seq[other_row] == col:
                continue
            if other_row + seq[other_row] == row + col:
                continue
            if other_row - seq[other_row] == row - col:
                continue
            score += 1
    #divide by 2 as pairs of queens are commutative
    return score/2


def selection(population):
    parents = []
    for ind in population:
        #select parents with probability proportional to their fitness score
        if random.randrange(sc.comb(NUM_QUEENS, 2)*2) < fitness_score(ind):
            parents.append(ind)
    return parents

def island(island_A,island_B, island_C, island_D, island_E, island_F):
    random_sample = random.sample(range(POPULATION_SIZE), 2)
    migration_a = [island_A[random_sample[0]], island_A[random_sample[1]]]
    random_sample = random.sample(range(POPULATION_SIZE), 2)
    migration_b = [island_B[random_sample[0]], island_B[random_sample[1]]]
    random_sample = random.sample(range(POPULATION_SIZE), 2)
    migration_c = [island_C[random_sample[0]], island_C[random_sample[1]]]
    random_sample = random.sample(range(POPULATION_SIZE), 2)
    migration_d = [island_D[random_sample[0]], island_D[random_sample[1]]]
    random_sample = random.sample(range(POPULATION_SIZE), 2)
    migration_e = [island_E[random_sample[0]], island_E[random_sample[1]]]
    random_sample = random.sample(range(POPULATION_SIZE), 2)
    migration_f = [island_F[random_sample[0]], island_F[random_sample[1]]]

    island_A[0:2] = migration_b
    island_A[2:4] = migration_c
    island_A[4:6] = migration_d
    island_A[6:8] = migration_e
    island_A[8:10] = migration_f

    island_B[0:2] = migration_a
    island_B[2:4] = migration_c
    island_B[4:6] = migration_d
    island_B[6:8] = migration_e
    island_B[8:10] = migration_f

    island_C[0:2] = migration_a
    island_C[2:4] = migration_b
    island_C[4:6] = migration_d
    island_C[6:8] = migration_e
    island_C[8:10] = migration_f

    island_D[0:2] = migration_a
    island_D[2:4] = migration_b
    island_D[4:6] = migration_c
    island_D[6:8] = migration_e
    island_D[8:10] = migration_f

    island_E[0:2] = migration_a
    island_E[2:4] = migration_b
    island_E[4:6] = migration_c
    island_E[6:8] = migration_d
    island_E[8:10] = migration_f

    island_F[0:2] = migration_a
    island_F[2:4] = migration_b
    island_F[4:6] = migration_c
    island_F[6:8] = migration_d
    island_F[8:10] = migration_e

    return island_A,island_B,island_C,island_D,island_E,island_F

def crossover(parents):
    #random indexes to to cross states with
    cross_points = random.sample(range(NUM_QUEENS), MIXING_NUMBER - 1)
    offsprings = []
    #all permutations of parents
    permutations = list(itertools.permutations(parents, MIXING_NUMBER))
    for perm in permutations:
        offspring = []
        #track starting index of sublist
        start_pt = 0
        for parent_idx, cross_point in enumerate(cross_points): #doesn't account for last parent
            #sublist of parent to be crossed
            parent_part = perm[parent_idx][start_pt:cross_point]
            offspring.append(parent_part)
            #update index pointer
            start_pt = cross_point
        #last parent
        last_parent = perm[-1]
        parent_part = last_parent[cross_point:]
        offspring.append(parent_part)
        #flatten the list since append works kinda differently
        offsprings.append(list(itertools.chain(*offspring)))

    return offsprings

def mutate(seq):
    for row in range(len(seq)):
        if random.random() < MUTATION_RATE:
            swap_seq = random.sample(range(NUM_QUEENS), 2)
            place_holder = seq[swap_seq[1]]
            seq[swap_seq[1]] = seq[swap_seq[0]]
            seq[swap_seq[0]] = place_holder
    return seq

def print_found_goal(population, generation, to_print=True):
    for ind in population:
        score = fitness_score(ind)
        if to_print:
            print(f'Current Generation: {generation}, Fitness Score: {score}/{sc.comb(NUM_QUEENS, 2)}', end='\r')
        if score == sc.comb(NUM_QUEENS, 2):
            print('\n\n\n')
            print(ind)
            print('\n\n')
            human_output =  [x+1 for x in ind] #Since Python counts from 0, This line of code add 1 to make it easier for human to understand
            to_output_file = f'The Final solution is {human_output}'
            print('\n')
            print(to_output_file)
            print('\n')

            board = [] #Building Visualize Board

            for x in range(NUM_QUEENS):
                board.append(["X"] * NUM_QUEENS)

            for i in range(NUM_QUEENS):
                for j in range(NUM_QUEENS):
                    if ind[i] == j:
                        board[i][j] = "Q"
            
            log.writelines(str(to_output_file))
            log.writelines('\n\nBoard Configuration is Visualized Below \n')
            print_board(board)
            print('\n')
            log.close()
            return True
    return False

def evolution(population):
    #select individuals to become parents
    parents = selection(population)
    #recombination. Create new offsprings
    offsprings = crossover(parents)
    #mutation
    offsprings = list(map(mutate, offsprings))
    #introduce top-scoring individuals from previous generation and keep top fitness individuals
    new_gen = offsprings
    for ind in population:
        new_gen.append(ind)
    new_gen = sorted(new_gen, key=lambda ind: fitness_score(ind), reverse=True)[:POPULATION_SIZE]
    return new_gen

def generate_population():
    population = []

    for individual in range(POPULATION_SIZE):
        new = [random.sample(range(NUM_QUEENS), NUM_QUEENS) for idx in range(NUM_QUEENS)] #Generate Non Duplicate Sequence
        population.append(new[0])
    
    return population

def print_board(board):
    for row in board:
        print (' '.join(row))
        log.writelines('\n')
        log.writelines(str(row))

def get_population():
    island_1 = generate_population()
    island_2 = generate_population()
    island_3 = generate_population()
    island_4 = generate_population()
    island_5 = generate_population()
    island_6 = generate_population()
    population = island_1 + island_2 + island_3 + island_4 + island_5 + island_6

    return island_1, island_2, island_3, island_4, island_5, island_6, population

if __name__ == "__main__":
    NUM_QUEENS = get_number_queen()
    POPULATION_SIZE = get_population_size()
    MUTATION_RATE = get_mutation_rate()
    run_limits = get_run_limit()
    refresh_rate = get_refresh_rate()
    migration_rate = get_migration_rate()

    print(f'\nNumber of Queens: {NUM_QUEENS}, Population Size: {POPULATION_SIZE}, Mutation Rate: {MUTATION_RATE}')
    print('\n')

    island_1, island_2, island_3, island_4, island_5, island_6, population = get_population()
        
    while not print_found_goal(population, generation):
        island_1 = evolution(island_1)
        island_2 = evolution(island_2)
        island_3 = evolution(island_3)
        island_4 = evolution(island_4)
        island_5 = evolution(island_5)
        island_6 = evolution(island_6)
        population = island_1 + island_2 + island_3 + island_4 + island_5 + island_6
        generation += 1

        if generation % migration_rate == 0:
            island_1, island_2, island_3, island_4, island_5, island_6 = island(island_1, island_2, island_3, island_4, island_5, island_6)
            print('\nMigrating...')

        if int(generation % refresh_rate)==1:
            reset_seq += 1
            print('\n')
            if reset_seq == 1:
                island_1 = generate_population()
                print('Resetting Island 1 Population...')
            if reset_seq == 2:
                island_2 = generate_population()
                print('Resetting Island 2 Population...')
            if reset_seq == 3:
                island_3 = generate_population()
                print('Resetting Island 3 Population...')
            if reset_seq == 4:
                island_4 = generate_population()
                print('Resetting Island 4 Population...')
            if reset_seq == 5:
                island_5 = generate_population()
                print('Resetting Island 5 Population...')
            if reset_seq == 6:
                island_6 = generate_population()
                print('Resetting Island 6 Population...')
                reset_seq = 0
            population = island_1 + island_2 + island_3 + island_4 + island_5 + island_6

        if generation > run_limits:
            print('\n')
            print('Thought Unlikely, but it seems that the GA is stuck at some local point. Please try restart the program or change the run limits')
            break

input('Press Enter to Exit')