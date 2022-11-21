import random
import math

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
    def calculate_opp_dist(self, curr_player_pos, opp_player_list):
        """
        Identifies all opponent players and their corresponding distances from the current player.
        If the distance is not more than 2 cells, then the opponent is said to be in close range.
        :param curr_player_pos: index of the current player possessing the ball
        :param opp_player_list: list of all opponents
        """
        # curr_player_row = curr_player_pos[0]
        # curr_player_col = curr_player_pos[1]
        result_list = []
        for i in opp_player_list:
            opp_position = i.position
            defence = i.defence
            dist = math.dist(curr_player_pos, opp_position)
            if dist <= 2:
                result_list.append([i, defence])

        return result_list

    def extract_three_ptr(self, three_ptr, length):
        three_pointer_GS = []
        three_pointer_BC = []

        for i in three_ptr:
            if i[1] > length / 2:
                three_pointer_BC.append(i)
            else:
                three_pointer_GS.append(i)

        return three_pointer_GS, three_pointer_BC

    def three_ptr_region_valid(self, curr_player_pos, three_ptr):

        curr_player_row = curr_player_pos[0]
        curr_player_col = curr_player_pos[1]
        row_list = []
        col_list = []
        for i in three_ptr:
            row_list.append(i[0])
            col_list.append(i[1])
        min_row = min(row_list)
        max_row = max(row_list)
        min_col = min(col_list)
        max_col = max(col_list)
        if curr_player_row >= min_row and curr_player_row <= max_row and curr_player_col >= min_col and curr_player_col <= max_col:
            return True
        else:
            return False

    def calculate_probability(self, curr_player_pos, opp_player_list, three_ptr, curr_player):
        probability = 0
        close_players = self.calculate_opp_dist(curr_player_pos, opp_player_list)
        three_ptr_region_flag = self.three_ptr_region_valid(self, curr_player_pos, three_ptr)
        if three_ptr_region_flag == True:
            if len(close_players) > 0:
                if curr_player.attack > 80:
                    for i in close_players:
                        if i[1] > 80:
                            probability = 0.5
                        else:
                            probability = 0.60
            else:
                if curr_player.attack > 80:
                    probability = 0.75
                else:
                    probability = 0.65
        else:
            probability = 1

        return probability

    # def update_score(self, curr_player, probability, score_board):
    #     if probability == 0.5:
    #         basket = random.choices(population=(0, 1), weights=(0.5, 0.5))
    #     elif probability == 0.75

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

    gs_player_list = [GS1, GS2, GS3, GS4, GS5]
    bc_player_list = [BC1, BC2, BC3, BC4, BC5]
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