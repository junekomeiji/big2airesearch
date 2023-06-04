import tensorflow as tf
import numpy as np
import random
from deap import base, creator, tools
from pygad.kerasga import model_weights_as_matrix
import big2text
import pickle
import gc
import os

def varAnd(population, toolbox, cxpb, mutpb):
    r"""Part of an evolutionary algorithm applying only the variation part
    (crossover **and** mutation). The modified individuals have their
    fitness invalidated. The individuals are cloned so returned population is
    independent of the input population.

    :param population: A list of individuals to vary.
    :param toolbox: A :class:`~deap.base.Toolbox` that contains the evolution
                    operators.
    :param cxpb: The probability of mating two individuals.
    :param mutpb: The probability of mutating an individual.
    :returns: A list of varied individuals that are independent of their
              parents.

    The variation goes as follow. First, the parental population
    :math:`P_\mathrm{p}` is duplicated using the :meth:`toolbox.clone` method
    and the result is put into the offspring population :math:`P_\mathrm{o}`.  A
    first loop over :math:`P_\mathrm{o}` is executed to mate pairs of
    consecutive individuals. According to the crossover probability *cxpb*, the
    individuals :math:`\mathbf{x}_i` and :math:`\mathbf{x}_{i+1}` are mated
    using the :meth:`toolbox.mate` method. The resulting children
    :math:`\mathbf{y}_i` and :math:`\mathbf{y}_{i+1}` replace their respective
    parents in :math:`P_\mathrm{o}`. A second loop over the resulting
    :math:`P_\mathrm{o}` is executed to mutate every individual with a
    probability *mutpb*. When an individual is mutated it replaces its not
    mutated version in :math:`P_\mathrm{o}`. The resulting :math:`P_\mathrm{o}`
    is returned.

    This variation is named *And* because of its propensity to apply both
    crossover and mutation on the individuals. Note that both operators are
    not applied systematically, the resulting individuals can be generated from
    crossover only, mutation only, crossover and mutation, and reproduction
    according to the given probabilities. Both probabilities should be in
    :math:`[0, 1]`.
    """
    offspring = [toolbox.clone(ind) for ind in population]

    # Apply crossover and mutation on the offspring
    for i in range(1, len(offspring), 2):
        if random.random() < cxpb:
            offspring[i - 1], offspring[i] = toolbox.mate(offspring[i - 1],
                                                          offspring[i])
            del offspring[i - 1].fitness.values, offspring[i].fitness.values

    for i in range(len(offspring)):
        if random.random() < mutpb:
            offspring[i], = toolbox.mutate(offspring[i])
            del offspring[i].fitness.values

    return offspring


def eaSimple(population, toolbox, cxpb, mutpb, ngen, stats=None,
             halloffame=None, verbose=__debug__):
    """This algorithm reproduce the simplest evolutionary algorithm as
    presented in chapter 7 of [Back2000]_. (Modified from the original DEAP package.)

    :param population: A list of individuals.
    :param toolbox: A :class:`~deap.base.Toolbox` that contains the evolution
                    operators.
    :param cxpb: The probability of mating two individuals.
    :param mutpb: The probability of mutating an individual.
    :param ngen: The number of generation.
    :param stats: A :class:`~deap.tools.Statistics` object that is updated
                  inplace, optional.
    :param halloffame: A :class:`~deap.tools.HallOfFame` object that will
                       contain the best individuals, optional.
    :param verbose: Whether or not to log the statistics.
    :returns: The final population
    :returns: A class:`~deap.tools.Logbook` with the statistics of the
              evolution

    The algorithm takes in a population and evolves it in place using the
    :meth:`varAnd` method. It returns the optimized population and a
    :class:`~deap.tools.Logbook` with the statistics of the evolution. The
    logbook will contain the generation number, the number of evaluations for
    each generation and the statistics if a :class:`~deap.tools.Statistics` is
    given as argument. The *cxpb* and *mutpb* arguments are passed to the
    :func:`varAnd` function. The pseudocode goes as follow ::

        evaluate(population)
        for g in range(ngen):
            population = select(population, len(population))
            offspring = varAnd(population, toolbox, cxpb, mutpb)
            evaluate(offspring)
            population = offspring

    As stated in the pseudocode above, the algorithm goes as follow. First, it
    evaluates the individuals with an invalid fitness. Second, it enters the
    generational loop where the selection procedure is applied to entirely
    replace the parental population. The 1:1 replacement ratio of this
    algorithm **requires** the selection procedure to be stochastic and to
    select multiple times the same individual, for example,
    :func:`~deap.tools.selTournament` and :func:`~deap.tools.selRoulette`.
    Third, it applies the :func:`varAnd` function to produce the next
    generation population. Fourth, it evaluates the new individuals and
    compute the statistics on this population. Finally, when *ngen*
    generations are done, the algorithm returns a tuple with the final
    population and a :class:`~deap.tools.Logbook` of the evolution.

    .. note::

        Using a non-stochastic selection method will result in no selection as
        the operator selects *n* individuals from a pool of *n*.

    This function expects the :meth:`toolbox.mate`, :meth:`toolbox.mutate`,
    :meth:`toolbox.select` and :meth:`toolbox.evaluate` aliases to be
    registered in the toolbox.

    .. [Back2000] Back, Fogel and Michalewicz, "Evolutionary Computation 1 :
       Basic Algorithms and Operators", 2000.
    """
    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])
    print("Generation 0")
    # MODIFICATIONS HERE: Fitness is done in groups of 4 instead of individually.
    # All individuals are re-tested for fitness instead of just new individuals.
    invalid_ind = [ind for ind in population]
    group_length = int(np.floor_divide(len(invalid_ind), 4))
    invalid_indgroups = []
    for i in range(4):
        indgroup = []
        for x in range(group_length):
            indgroup.append(invalid_ind[i * group_length + x])
        invalid_indgroups.append(indgroup)
    
    fitnesses = map(toolbox.evaluate, invalid_indgroups[0], invalid_indgroups[1], invalid_indgroups[2], invalid_indgroups[3])
    for n, fitness in enumerate(fitnesses):
        invalid_ind[n].fitness.values = (fitness[0],)
        invalid_ind[n + group_length].fitness.values = (fitness[1],)
        invalid_ind[n + group_length * 2].fitness.values = (fitness[2],)
        invalid_ind[n + group_length * 3].fitness.values = (fitness[3],)
        

    if halloffame is not None:
        halloffame.update(population)

    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, nevals=len(invalid_ind), **record)
    if verbose:
        print(logbook.stream)

    # Begin the generational process
    for gen in range(1, ngen + 1):
        # Select the next generation individuals
        offspring = toolbox.select(population, len(population))

        # Vary the pool of individuals
        offspring = varAnd(offspring, toolbox, cxpb, mutpb)
        
        print(f"Generation {gen}")
        # MODIFICATIONS HERE: Fitness is done in groups of 4 instead of individually.
        # All individuals are re-tested for fitness instead of just new individuals.
        invalid_ind = [ind for ind in offspring]
        group_length = int(np.floor_divide(len(invalid_ind), 4))
        invalid_indgroups = []
        for i in range(4):
            indgroup = []
            for x in range(group_length):
                indgroup.append(invalid_ind[i * group_length + x])
            invalid_indgroups.append(indgroup)
        
        fitnesses = map(toolbox.evaluate, invalid_indgroups[0], invalid_indgroups[1], invalid_indgroups[2], invalid_indgroups[3])
        for n, fitness in enumerate(fitnesses):
            invalid_ind[n].fitness.values = (fitness[0],)
            invalid_ind[n + group_length].fitness.values = (fitness[1],)
            invalid_ind[n + group_length * 2].fitness.values = (fitness[2],)
            invalid_ind[n + group_length * 3].fitness.values = (fitness[3],)

        # Update the hall of fame with the generated individuals
        if halloffame is not None:
            halloffame.update(offspring)

        # Replace the current population by the offspring
        population[:] = offspring

        # Append the current generation statistics to the logbook
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)
        if verbose:
            print(logbook.stream)
            
        # starts garbage cleaning
        gc.collect()

    return population, logbook

def model_build():
    
    inputs = tf.keras.layers.Input(shape=(141,))
    x = tf.keras.layers.Dense(107, activation='relu')(inputs)
    x = tf.keras.layers.Dense(107, activation='relu')(x)
    predictions = tf.keras.layers.Dense(10, activation='sigmoid')(x)

    model_func = tf.keras.models.Model(inputs=inputs, outputs=predictions)
    
    # these are not used for this model, but are needed for compilation
    model_func.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
    return model_func

def generate_input(my_deck, prev_deck, prev_hand):
    inp_vector = []
    for x in range(13):
        try:
            card = big2text.Card.num_to_vector(my_deck[x])
        except IndexError:
            card = [0, 0]
        inp_vector.extend(card)
    for x in range(52):
        try:
            card = big2text.Card.num_to_vector(prev_deck[x])
        except IndexError:
            card = [0,0]
        inp_vector.extend(card)
    for x in range(5):
        try:
            card = big2text.Card.num_to_vector(prev_hand[x])
        except:
            card = [0,0]
        inp_vector.extend(card)
    return inp_vector

def predictions_to_hand(prediction, my_deck):
    hand = []
    for x, pred in zip(range(13), prediction[0]):
        if pred >= 0.5:
            try:
                hand.append(my_deck[x])
            except IndexError:
                pass
        if len(hand) == 5:
            break
    hand.sort()
    return hand

def evaluate_game(ind1, ind2, ind3, ind4):
    big2text.init()
    
    # Building the players
    models = []
    inds = [ind1, ind2, ind3, ind4]
    
    for ind in inds:
        model = model_build()
        model.set_weights(model_weights_as_matrix(model, ind))
        models.append(model)
    
    fitnesses = [0, 0, 0, 0]
    exit = False
    first_hand = True
    consec_skips = 0
    while(not exit):
        # Reading game state
        file = open("gamestate", "r") 
        save = file.readlines()
        file.close()
        skips = int(save[8].strip(" \n"))
        
        prev_deck = []
        if save[5].strip(" \n") != "-1" and save[5].strip(" \n") != "":
            prev_deck = list(map(int, save[5].strip(" \n").split(',')))
            
        prev_empty = save[6].strip(" \n") == "-1"
        prev_hand = []
        if not prev_empty:
            prev_hand = list(map(int, save[6].strip(" \n").split(',')))
        
        playernum = int(save[7].strip(" \n"))
        if save[playernum] == "":
            winner = playernum
            break
        else:
            my_deck = list(map(int, save[playernum].strip(" \n").split(',')))
        
        # Mapping relevant game variables to input vector
        inp_vector = generate_input(my_deck, prev_deck, prev_hand)
        inp_vector.append(int(save[8].strip(" \n")))
        
        #PREDICTION TIME
        model_input = tf.expand_dims(inp_vector, axis=0)
        prediction = models[playernum - 1].predict(model_input)
        
        # Mapping prediction into readable hand
        hand = predictions_to_hand(prediction, my_deck)
        
        # verification and retry
        fails = 0
        while (fails < 5):
            hand_cards = list(map(big2text.Card, hand))
            my_deck_cards = list(map(big2text.Card, my_deck))
            prev_hand_cards = list(map(big2text.Card, prev_hand))
            if big2text.verify(hand_cards, my_deck_cards, prev_hand_cards, prev_empty, first_hand) != 0:
                # try a different prediction by shuffling cards in hand
                fails += 1
                # random.shuffle(my_deck)
                inp_vector = generate_input(my_deck, prev_deck, prev_hand)
                inp_vector.append(int(save[8].strip(" \n")))
                model_input = tf.expand_dims(inp_vector, axis=0)
                prediction = models[playernum - 1].predict(model_input)
                hand = predictions_to_hand(prediction, my_deck)
            else:
                break
        else:
            # if the model fails to produce a valid hand, force to skip
            # except on first move, where 3 of diamonds is forced to be put down
            if first_hand:
                hand_cards = [big2text.Card(0)]
            else:
                hand_cards = []
        
        # Resets skip count if there's a hand.
        if len(hand_cards) == 0:
            consec_skips += 1
        else:
            consec_skips = 0
            
        # Update the gamestate
        big2text.execute_move(hand_cards, playernum)
        
        # Check for winners
        winner = big2text.are_we_done_yet()
        if winner != 0:
            exit = True
        
        # Check for too many skips
        if consec_skips > 12:
            exit = True
        first_hand = False

    # Once finished, calculate fitness
    # When exited because skips, everyone gets a negative fitness
    file = open("gamestate", "r")
    save = file.readlines()
    file.close()
    
    card_count = [0, 0, 0, 0]
    for x in range(4):
        card_count[x] = len(save[x + 1].split(','))
    
    for x in range(4):
        y = x + 1
        if y == winner:
            for z in range(4):
                if z != x:
                    fitnesses[x] += card_count[z]
        else:
            fitnesses[x] = -card_count[x]
    
    # End of evaluation
    return fitnesses

def export(pop):
    os.system('cls' if os.name == 'nt' else 'clear')
    inp = input("Export how many? (leave empty for whole population): ").strip()
    if inp == "":
        expn = len(pop)
    else:
        expn = int(inp)
        if expn > len(pop):
            expn = len(pop)
    inp = input("[B]est or [w]orst? ").strip().lower()
    match inp:
        case "b":
            expop = sorted(pop, key=lambda ind: ind.fitness, reverse=True)[:expn]
        case "w":
            expop = sorted(pop, key=lambda ind: ind.fitness, reverse=False)[:expn]
        case other:
            return export(pop)
    with open("big2_exporp.pkl", "wb") as exp_file:
        pickle.dump(expop, exp_file)
    return None
    
def impor():
    if os.getcwd()[-5:] != "_data":
        print("moving to save folder")
        try:
            os.mkdir("saved_data")
        except FileExistsError:
            print("folder already exists.")
        os.chdir("saved_data")
    print("Finding saved population...")
    try:
        file = open("big2_exporp.pkl", "rb")
        pop = pickle.load(file)
        file.close()
        print("File loaded...")
        print(f"Population size: {len(pop)}")
        input("Press enter to import...")
        return pop, len(pop)
    except FileNotFoundError:
        print("Saved file doesn't exist?")
        input("Enter to return...")
    return None, -1
    


def main():    
    model = model_build()
    model.summary()
    ind_size = model.count_params()

    print(gc.isenabled())

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    toolbox = base.Toolbox()
    toolbox.register("weight_bin", random.random) # Generating random weights
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.weight_bin, n=ind_size)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.01)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("evaluate", evaluate_game)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("Mean", np.mean)
    stats.register("Max", np.max)
    stats.register("Min", np.min)

    popn = 100
    hof = tools.HallOfFame(1)
    ngen = 30
    cxpb = 0.5
    mutpb = 0.1
    cgen = 0
    
    while(True):
        while(True):
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Current generation: {cgen}")
            print("Configuration:")
            print(f"[P]opulation size: {popn}")
            print(f"[N]umber of generations: {ngen}")
            print(f"[C]rossover probability: {cxpb}")
            print(f"[M]utation probability: {mutpb}")
            print("")
            print(f"[E]xport population")
            print(f"[I]mport population")
            print(f"E[x]it")
            match input("Press Enter to start, or configure settings. ").strip().lower():
                case "p":
                    try:
                        popn = int(input("New population size: ").strip())
                    except:
                        pass
                case "n":
                    try:
                        ngen = int(input("New generation count: ").strip())
                    except:
                        pass
                case "c":
                    try:
                        cxpb = float(input("New crossover proability: ").strip())
                    except:
                        pass
                case "m":
                    try:
                        mutpb = float(input("New mutation probability: ").strip())
                    except:
                        pass
                case "e":
                    if cgen == 0:
                            pop = toolbox.population(n=popn)
                    export(pop)
                case "i":
                    pup, pupn = impor()
                    if pupn != -1:
                        pop = pup
                        popn = pupn
                case "x":
                    return
                case "":
                    break
                case other:
                    pass
                
        # Runs the GA with the specified values
        if cgen == 0:
            pop = toolbox.population(n=popn)
        pop, log = eaSimple(pop, toolbox, cxpb=cxpb, mutpb=mutpb, ngen=ngen, halloffame=hof, stats=stats, verbose=True)
        cgen += ngen
        with open("logbook.log", "a+") as log_file:
            log_file.write(str(log))

    
if __name__ == "__main__":
    main()