import random

class Ground:
    def __init__(self, length, breadth, positions1, positions2):
        self.length = length
        self.breadth = breadth
        self.positions1 = positions1
        self.positions2 = positions2

    def give_dimensions(self):
        return self.length, self.breadth

    def assign_squares(self):
        l_mid = self.length // 2
        b_mid = self.breadth // 2
        goal_post_left = [b_mid, 0]
        goal_post_right = [b_mid, self.length - 1]
        start_sq = [b_mid, l_mid]
        return goal_post_left, goal_post_right, start_sq

    def reset_matrix(self, start, after_basket, after_basket_team):
        three_pointer = []
        main_matrix = {}
        row = 0
        col = 0
        start_ball_pos = (-1,-1)

        if start:
            temp = [(positions1[0], 'GS1'), (positions2[0], 'BC1')]
            start_ball_pos = random.choice(temp)

        goal_post_left, goal_post_right, start_sq = self.assign_squares()

        while row < self.breadth:
            while col < self.length:
                if [row, col] == goal_post_left or [row, col] == goal_post_right:
                    main_matrix[row, col] = 'O'
                elif [row, col] == start_sq:
                    main_matrix[row, col] = 'S'
                elif [row,col] == start_ball_pos[0]:
                    main_matrix[row, col] = start_ball_pos[1] + '*'
                elif [row, col] in positions1:
                    main_matrix[row, col] = 'GS' + str(positions1.index([row, col]) + 1)
                elif [row, col] in positions2:
                    main_matrix[row, col] = 'BC' + str(positions2.index([row, col]) + 1)
                elif ((row == 1 and col <= 3) or (1 <= row <= self.breadth - 2 and col == 3)) or (
                        (row == 1 and col >= self.length - 2) or (
                        1 <= row <= self.breadth - 2 and col == self.length - 2)) or (
                        row == self.breadth - 2 and col <= 3) or (row == self.breadth - 2 and col >= self.length - 2):
                    main_matrix[row, col] = '.'
                    three_pointer.append([row, col])
                else:
                    main_matrix[row, col] = '.'
                col += 1

            col = 0
            row += 1

        self.place_player_on_grid(main_matrix)
        # return main_matrix, three_pointer
        return

    def place_player_on_grid(self, matrix):
        # matrix, three = Ground.create_initial_matrix(self)

        for i in range(self.breadth):
            print('\n')
            for j in range(self.length):
                if matrix[i, j] == '.' or matrix[i, j] == 'O' or matrix[i, j] == 'S':
                    print('   ' + matrix[i, j] + '   ', end='')
                else:
                    print('  ' + matrix[i, j] + '  ', end='')

        return



# Player is a child of ground
class Player(Ground):
    def __init__(self, length, breadth, positions1, positions2, team_name, player_name, position, defence, attack):
        # attributed of parent class
        Ground.__init__(self, length, breadth, positions1, positions2)
        Ground.length = length
        Ground.breadth = breadth
        Ground.positions1 = positions1
        Ground.positions2 = positions2

        # attributes of child class
        self.team_name = team_name
        self.player_name = player_name
        self.position = position
        self.defence = defence
        self.attack = attack

    def passing(self, pass_to):
        # pass_to is a list of 2 positions where first position is where player with ball at present is willing to
        # pass and second is where the opposite player wants to move
        pass


if __name__ == '__main__':
    positions1 = [[3, 5], [2, 4], [4, 4], [1, 3], [5, 3]]
    positions2 = [[3, 7], [2, 8], [4, 8], [1, 9], [5, 9]]
    ground1 = Ground(13, 7, positions1, positions2)
    ground1.reset_matrix(True, False, '')

    GS1 = Player(13, 7, positions1, positions2, 'Golden State Warriors', 'GS1', [3, 5], 80, 95)
    GS2 = Player(13, 7, positions1, positions2, 'Golden State Warriors', 'GS2', [2, 4], 85, 85)
    GS3 = Player(13, 7, positions1, positions2, 'Golden State Warriors', 'GS3', [4, 4], 85, 85)
    GS4 = Player(13, 7, positions1, positions2, 'Golden State Warriors', 'GS4', [1, 3], 90, 80)
    GS5 = Player(13, 7, positions1, positions2, 'Golden State Warriors', 'GS5', [5, 3], 90, 80)
    BC1 = Player(13, 7, positions1, positions2, 'Boston Celtics', 'BC1', [3, 7], 80, 95)
    BC2 = Player(13, 7, positions1, positions2, 'Boston Celtics', 'BC2', [2, 8], 85, 85)
    BC3 = Player(13, 7, positions1, positions2, 'Boston Celtics', 'BC3', [4, 8], 85, 85)
    BC4 = Player(13, 7, positions1, positions2, 'Boston Celtics', 'BC4', [1, 9], 90, 80)
    BC5 = Player(13, 7, positions1, positions2, 'Boston Celtics', 'BC5', [5, 9], 90, 80)
    # cells, three_ptr = ground1.create_initial_matrix()

    print('\n\n')

    while True:
        # two cases - attack and defense...depends who the ball is the with
        print('This move is for the Golden State Warriors team. Choose one of the following:\n')
        print('  1. Move player with the ball in any direction')
        print('  2. Pass the ball to your teammate')
        print('  3. Shoot towards the basket')
        print('  Q. Quit game')
        i = input('Enter your choice: ').lower().strip()
        print('\n')
        if i == '1':
            print('In which direction do you want to move?')
            print('Example: N, S, NE, SW')
            direction = input('Enter your choice: ').lower().strip()
            print('\n')
            print('How many steps do you want to take in that direction?')
            print('  1. 1 Step')
            print('  2. 2 Steps')
            steps = input('Enter your choice: ').lower().strip()
            # print_final_boards('grandmasters-standard-2018-2022.pgn')
        elif i == '2':
            # frequency_of_first_moves('grandmasters-standard-2018-2022.pgn')
            pass
        elif i == '3':
            # with open('grandmasters-standard-2018-2022.pgn') as pgn:
            # g = chess.pgn.read_game(pgn)  # get first game in file
            # print_game_details(g)
            pass
        elif i == 'q':
            break
        print('\n\n')
