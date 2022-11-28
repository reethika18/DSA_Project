import random
import sys
import math
from collections import defaultdict

class Ground:
    cur_ball_pos = [-1,-1]
    main_matrix_dict = {}
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

    def current_ball_position(self, ball_position):
        Ground.cur_ball_pos = ball_position

    def reset_matrix(self, start, after_basket, after_basket_team):
        three_pointer = []
        row = 0
        col = 0
        start_ball_pos = (-1, -1)

        if start:
            temp = [(positions1[0], 'GS1'), (positions2[0], 'BC1')]
            start_ball_pos = random.choice(temp)
            Ground.current_ball_position(self, start_ball_pos[0])


        goal_post_left, goal_post_right, start_sq = self.assign_squares()

        while row < self.breadth:
            while col < self.length:
                if [row, col] == goal_post_left or [row, col] == goal_post_right:
                    Ground.main_matrix_dict[row, col] = 'O'
                elif [row, col] == start_sq:
                    Ground.main_matrix_dict[row, col] = 'S'
                elif [row, col] == start_ball_pos[0]:
                    Ground.main_matrix_dict[row, col] = start_ball_pos[1] + '*'
                elif [row, col] in positions1:
                    Ground.main_matrix_dict[row, col] = 'GS' + str(positions1.index([row, col]) + 1)
                elif [row, col] in positions2:
                    Ground.main_matrix_dict[row, col] = 'BC' + str(positions2.index([row, col]) + 1)
                elif ((row == 1 and col <= 3) or (1 <= row <= self.breadth - 2 and col == 3)) or (
                        (row == 1 and col >= self.length - 2) or (
                        1 <= row <= self.breadth - 2 and col == self.length - 2)) or (
                        row == self.breadth - 2 and col <= 3) or (row == self.breadth - 2 and col >= self.length - 2):
                    Ground.main_matrix_dict[row, col] = '.'
                    three_pointer.append([row, col])
                else:
                    Ground.main_matrix_dict[row, col] = '.'
                col += 1

            col = 0
            row += 1

        self.place_player_on_grid(Ground.main_matrix_dict)
        # return main_matrix_dict, three_pointer
        return three_pointer



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

    def move_player(self, direction):
        temp = Ground.main_matrix_dict[(self.position[0], self.position[1])]
        Ground.main_matrix_dict[(self.position[0], self.position[1])] = '.'

        if direction == 'n':
            row = Ground.cur_ball_pos[0]
            col = Ground.cur_ball_pos[1]
            self.position = [row-1, col]
        elif direction == 's':
            row = Ground.cur_ball_pos[0]
            col = Ground.cur_ball_pos[1]
            self.position = [row+1, col]
        elif direction == 'e':
            row = Ground.cur_ball_pos[0]
            col = Ground.cur_ball_pos[1]
            self.position = [row, col+1]
        elif direction == 'w':
            row = Ground.cur_ball_pos[0]
            col = Ground.cur_ball_pos[1]
            self.position = [row, col-1]
        elif direction == 'ne':
            row = Ground.cur_ball_pos[0]
            col = Ground.cur_ball_pos[1]
            self.position = [row-1, col+1]
        elif direction == 'se':
            row = Ground.cur_ball_pos[0]
            col = Ground.cur_ball_pos[1]
            self.position = [row+1, col+1]
        elif direction == 'nw':
            row = Ground.cur_ball_pos[0]
            col = Ground.cur_ball_pos[1]
            self.position = [row-1, col-1]
        elif direction == 'sw':
            row = Ground.cur_ball_pos[0]
            col = Ground.cur_ball_pos[1]
            self.position = [row+1, col-1]

        Ground.current_ball_position(self, [self.position[0], self.position[1]])
        Ground.main_matrix_dict[(self.position[0], self.position[1])] = temp



    def passing(self, pass_to):
        # pass_to is a list of 2 positions where first position is where player with ball at present is willing to
        # pass and second is where the opposite player wants to move
        pass

    def calculate_opp_dist(self, players, curr_player_pos, opp_player_list):
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
            obj = players[i]
            opp_position = obj.position
            defence = obj.defence
            dist = math.dist(curr_player_pos, opp_position)
            if dist <= 2:
                result_list.append([obj, defence])

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

    def calculate_probability(self, curr_player, three_ptr_region_flag):

        # probability = 0

        if three_ptr_region_flag == False:
            if curr_player.attack > 80:
                probability = 0.5
            else:
                probability = 0.40
        else:
            if curr_player.attack > 80:
                probability = 1
            else:
                probability = 0.75

        return probability

    def update_score(self, probability, scoreboard, key):

        print(key)
        if probability == 0.5:
            shoot_success = random.choices(population=(0, 1), weights=(0.5, 0.5))[0]
            print(shoot_success)
            if shoot_success == 1:
                if key in scoreboard:
                    scoreboard[key] += 3
                    return scoreboard
        elif probability == 0.4:
            shoot_success = random.choices(population=(0, 1), weights=(0.6, 0.4))[0]
            print(shoot_success)
            if shoot_success == 1:
                if key in scoreboard:
                    scoreboard[key] += 3
                    return scoreboard
        elif probability == 1:
            shoot_success = random.choices(population=(0, 1), weights=(0, 1.0))[0]
            print(shoot_success)
            if shoot_success == 1:
                if key in scoreboard:
                    scoreboard[key] += 2
                    return scoreboard
        elif probability == 0.75:
            shoot_success = random.choices(population=(0, 1), weights=(0.25, 0.75))[0]
            print(shoot_success)
            if shoot_success == 1:
                if key in scoreboard:
                    scoreboard[key] += 2
                    return scoreboard


if __name__ == '__main__':
    positions1 = [[3, 5], [2, 4], [4, 4], [1, 3], [5, 3]]
    positions2 = [[3, 7], [2, 8], [4, 8], [1, 9], [5, 9]]
    ground1 = Ground(13, 7, positions1, positions2)
    three_ptr = ground1.reset_matrix(True, False, '')

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

    players = {'GS1': GS1, 'GS2': GS2, 'GS3': GS3, 'GS4': GS4, 'GS5': GS5, 'BC1': BC1, 'BC2': BC2, 'BC3': BC3, 'BC4':BC4, 'BC5': BC5}
    print('\n\n')

    attack = ''
    defense = ''
    teams_list = ['GS', 'BC']

    scoreboard = {'GS': 0, 'BC': 0}
    gs_player_list = [players['GS1'], players['GS2'], players['GS3'], players['GS4'], players['GS5']]
    bc_player_list = [players['BC1'], players['BC2'], players['BC3'], players['BC4'], players['BC5']]

    while True:
        teams_list = ['GS', 'BC']
        ball_with_which_team = Ground.main_matrix_dict[(Ground.cur_ball_pos[0], Ground.cur_ball_pos[1])]
        team_with_ball = ball_with_which_team[:2]
        attack = team_with_ball
        teams_list.remove(attack)
        defense = teams_list[0]

        print('This move is for the '+attack+' team. Choose one of the following:\n')
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
            temp_player = Ground.main_matrix_dict[(Ground.cur_ball_pos[0], Ground.cur_ball_pos[1])]
            temp_player_name = temp_player[:3]
            obj = players[temp_player_name]
            obj.move_player(direction)

            print('\n')
            print('How many steps do you want to take in that direction?')
            print('  1. 1 Step')
            print('  2. 2 Steps')
            steps = input('Enter your choice: ').lower().strip()
            if steps == '2':
                obj.move_player(direction)

            ground1.place_player_on_grid(Ground.main_matrix_dict)

        elif i == '2':
            GS_team = ['GS1', 'GS2', 'GS3', 'GS4', 'GS5']
            BC_team = ['BC1', 'BC2', 'BC3', 'BC4', 'BC5']
            temp_player = Ground.main_matrix_dict[(Ground.cur_ball_pos[0], Ground.cur_ball_pos[1])]
            temp_player_team = temp_player[:2]
            temp_player_name = temp_player[:3]
            if temp_player_team == 'GS':
                GS_team.remove(temp_player_name)
                print('Choose which teammate you want to pass:')
                for i in GS_team:
                    print(i)
                teammate = input('Enter your choice: ').upper().strip()
                Ground.main_matrix_dict[(Ground.cur_ball_pos[0], Ground.cur_ball_pos[1])] = temp_player_name
                for k, v in Ground.main_matrix_dict.items():
                    if v == teammate:
                        new = v+'*'
                        Ground.main_matrix_dict[k] = new
                        Ground.cur_ball_pos = k
                ground1.place_player_on_grid(Ground.main_matrix_dict)
            else:
                BC_team.remove(temp_player_name)
                print('Choose which teammate you want to pass:')
                for i in BC_team:
                    print('  '+i)
                teammate = input('Enter your choice: ').upper().strip()
                Ground.main_matrix_dict[(Ground.cur_ball_pos[0], Ground.cur_ball_pos[1])] = temp_player_name
                for k, v in Ground.main_matrix_dict.items():
                    if v == teammate:
                        new = v + '*'
                        Ground.main_matrix_dict[k] = new
                        Ground.cur_ball_pos = k
                ground1.place_player_on_grid(Ground.main_matrix_dict)

        elif i == '3':
            temp_player = Ground.main_matrix_dict[(Ground.cur_ball_pos[0], Ground.cur_ball_pos[1])]
            temp_player_team = temp_player[:2]
            temp_player_name = temp_player[:3]
            obj = players[temp_player_name]
            curr_player_pos = obj.position
            length1 = int(ground1.length)
            three_pointer_GS, three_pointer_BC = obj.extract_three_ptr(three_ptr, length1)
            print(type(temp_player_team))
            if temp_player_team == 'GS':
                # bc_close_players = obj.calculate_opp_dist(players, curr_player_pos, bc_player_list)
                is_player_in_three_ptr = obj.three_ptr_region_valid(curr_player_pos, three_pointer_BC)
                probability = obj.calculate_probability(obj , is_player_in_three_ptr)
                obj.update_score(probability, scoreboard, temp_player_team)
                print(temp_player_team, curr_player_pos, is_player_in_three_ptr, probability, scoreboard)

            elif temp_player_team == 'BC':
                # gs_close_players = obj.calculate_opp_dist(players, curr_player_pos, gs_player_list)
                is_player_in_three_ptr = obj.three_ptr_region_valid(curr_player_pos, three_pointer_GS)
                probability = obj.calculate_probability(obj, is_player_in_three_ptr)
                obj.update_score(probability, scoreboard, temp_player_team)
                print(temp_player_team, curr_player_pos, is_player_in_three_ptr, probability, scoreboard)


        elif i == 'q':
            break
        print('\n\n')

        print('This move is for the '+defense+' team. Choose one of the following defensive move:\n')
        print('  1. Choose your player to move and intercept')
        print('  Q. Quit game')
        i = input('Enter your choice: ').lower().strip()
        print('\n')
        if i == '1':
            print('Which player do you want to choose?')
        elif i == 'q':
            break
        print('\n\n')