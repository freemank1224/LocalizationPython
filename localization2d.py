# The function localize takes the following arguments:
#
# colors:
#        2D list, each entry either 'R' (for red cell) or 'G' (for green cell)
#
# measurements:
#        list of measurements taken by the robot, each entry either 'R' or 'G'
#
# motions:
#        list of actions taken by the robot, each entry of the form [dy,dx],
#        where dx refers to the change in the x-direction (positive meaning
#        movement to the right) and dy refers to the change in the y-direction
#        (positive meaning movement downward)
#        NOTE: the *first* coordinate is change in y; the *second* coordinate is
#              change in x
#
# sensor_right:
#        float between 0 and 1, giving the probability that any given
#        measurement is correct; the probability that the measurement is
#        incorrect is 1-sensor_right
#
# p_move:
#        float between 0 and 1, giving the probability that any given movement
#        command takes place; the probability that the movement command fails
#        (and the robot remains still) is 1-p_move; the robot will NOT overshoot
#        its destination in this exercise
#
# The function should RETURN (not just show or print) a 2D list (of the same
# dimensions as colors) that gives the probabilities that the robot occupies
# each cell in the world.
#
# Compute the probabilities by assuming the robot initially has a uniform
# probability of being in any cell.
#
# Also assume that at each step, the robot:
# 1) first makes a movement,
# 2) then takes a measurement.
#
# Motion:
#  [0,0] - stay
#  [0,1] - right
#  [0,-1] - left
#  [1,0] - down
#  [-1,0] - up

def localize(colors,measurements,motions,sensor_right,p_move):
    # initializes p to a uniform distribution over a grid of the same dimensions as colors
    pinit = 1.0 / float(len(colors)) / float(len(colors[0]))
    p = [[pinit for row in range(len(colors[0]))] for col in range(len(colors))]
    
    # >>> Insert your code here <<<
    for step, motion in enumerate(motions):
        p = move(p, motions[step], p_move)
        p = sense(p, colors, measurements[step], sensor_right)

    
#    p = sense(p, colors, measurements[step], sensor_right)
    return p

def show(p):
    rows = ['[' + ','.join(map(lambda x: '{0:.5f}'.format(x),r)) + ']' for r in p]
    print('[' + ',\n '.join(rows) + ']')
    
# Given initial p matrix, return the sense result for a SINGLE measurement!
def sense(p, colors, measurement, sensor_right):
    q = []
    q_row = []
    sensor_wrong = 1-sensor_right
    sum_row = 0
    sum_total = 0
    for i in range(len(p)):
        for j in range(len(p[i])):
            right = (measurement == colors[i][j])
            q_row.append(p[i][j] * (right*sensor_right + (1-right)*sensor_wrong))
            sum_row = sum_row + q_row[j]
            #print(q_row)
        q.append(q_row)
        sum_total = sum_total + sum_row
        sum_row = 0
        q_row = []
        print(sum_total)
    # Normalization
    for i in range(len(q)):
        for j in range(len(q[0])):
            q[i][j] /= sum_total
    
    return q

# Given initial p matrix, return the move result for a SINGLE step!   
# All the probabilities in p matrix should add to ONE !
def move(p, motion, p_move):
    # Identify the direction: Horizontal
    #q = [[0 for row in range(len(p[0]))] for col in range(len(p))]
    q_move = []
    q_move_back = []
    q_stay = p
    q = p
    p_stay = 1-p_move
    if motion[0] == 0:
        #q_temp = []
        for i in range(len(p)):
            q_move.append(p[i][-motion[1]:] + p[i][:-motion[1]])
        for i in range(len(p)):
            for j in range(len(p[i])):
                q_move[i][j] *= p_move
                q_stay[i][j] *= p_stay
                q[i][j] = q_move[i][j] + q_stay[i][j]
        
            
    else:
        # Transpose the matrix, then do the same operation
        p_trans = [[row[i] for row in p] for i in range(len(p[0]))]
        for i in range(len(p_trans)):
            q_move.append(p_trans[i][-motion[0]:] + p_trans[i][:-motion[0]])
        # When finish moving, transpose back to the original matrix p
        q_move_back = [[row[i] for row in q_move] for i in range(len(q_move[0]))]
        q_move = q_move_back
        
        for i in range(len(p)):
            for j in range(len(p[i])):
                q_move[i][j] *= p_move
                q_stay[i][j] *= p_stay
                q[i][j] = q_move[i][j] + q_stay[i][j]        
        
    return q
    
#############################################################
# For the following test case, your output should be 
# [[0.01105, 0.02464, 0.06799, 0.04472, 0.02465],
#  [0.00715, 0.01017, 0.08696, 0.07988, 0.00935],
#  [0.00739, 0.00894, 0.11272, 0.35350, 0.04065],
#  [0.00910, 0.00715, 0.01434, 0.04313, 0.03642]]
# (within a tolerance of +/- 0.001 for each entry)

colors = [['R','G','G','R','R'],
          ['R','R','G','R','R'],
          ['R','R','G','G','R'],
          ['R','R','R','R','R']]
measurements = ['G','G','G','G','G']
motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]
p = localize(colors,measurements,motions,sensor_right = 0.7, p_move = 0.8)
show(p) # displays your answer


# TEST1
#colors = [['G', 'G', 'G'],
#          ['G', 'R', 'G'],
#          ['G', 'G', 'G']]
#measurements = ['R']
#motions = [[0,0]]
#sensor_right = 1.0
#p_move = 1.0
#
#p = localize(colors,measurements,motions,sensor_right, p_move)
#show(p)

# TEST2
#colors = [['G', 'G', 'G'],
#          ['G', 'R', 'R'],
#          ['G', 'G', 'G']]
#measurements = ['R']
#motions = [[0,0]]
#sensor_right = 1.0
#p_move = 1.0
#p = localize(colors,measurements,motions,sensor_right, p_move)
#show(p)

# TEST3
#colors = [['G', 'G', 'G'],
#          ['G', 'R', 'R'],
#          ['G', 'G', 'G']]
#measurements = ['R']
#motions = [[0,0]]
#sensor_right = 0.8
#p_move = 1.0
#p = localize(colors,measurements,motions,sensor_right, p_move)
#show(p)
    
# TEST4
#colors = [['G', 'G', 'G'],
#          ['G', 'R', 'R'],
#          ['G', 'G', 'G']]
#measurements = ['R', 'R']
#motions = [[0,0], [0,1]]
#sensor_right = 0.8
#p_move = 1.0
#p = localize(colors,measurements,motions,sensor_right, p_move)
#show(p)

# TEST5  move ONE step right [0,1]
#colors = [['G', 'G', 'G'],
#          ['G', 'R', 'R'],
#          ['G', 'G', 'G']]
#measurements = ['R', 'R']
#motions = [[0,0], [0,1]]
#sensor_right = 1.0
#p_move = 1.0
#p = localize(colors,measurements,motions,sensor_right, p_move)
#show(p)

# TEST6 
#colors = [['G', 'G', 'G'],
#          ['G', 'R', 'R'],
#          ['G', 'G', 'G']]
#measurements = ['R', 'R']
#motions = [[0,0], [0,1]]
#sensor_right = 0.8
#p_move = 0.5
#p = localize(colors,measurements,motions,sensor_right, p_move)
#show(p)

# TEST7
#colors = [['G', 'G', 'G'],
#          ['G', 'R', 'R'],
#          ['G', 'G', 'G']]
#measurements = ['R', 'R']
#motions = [[0,0], [0,1]]
#sensor_right = 1.0
#p_move = 0.5
#p = localize(colors,measurements,motions,sensor_right, p_move)
#show(p)
