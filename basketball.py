import random
import sys
import math
import tcod


class Ground:
    cur_ball_pos = [-1, -1]
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

    def reset_matrix(self, start, next_chance_after_shoot):
        three_pointer = []
        row = 0
        col = 0
        start_ball_pos = (-1, -1)

        if start:
            temp = [(positions1[0], 'GS1'), (positions2[0], 'BC1')]
            start_ball_pos = random.choice(temp)
            Ground.current_ball_position(self, start_ball_pos[0])

        if next_chance_after_shoot == 'GS':
            start_ball_pos = (positions1[0], 'GS1')
            Ground.current_ball_position(self, start_ball_pos[0])
        if next_chance_after_shoot == 'BC':
            start_ball_pos = (positions2[0], 'BC1')
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

        self.display_ground(Ground.main_matrix_dict)
        # return main_matrix_dict, three_pointer
        return three_pointer

    def handing_ball_to_player(self, player_name_obj, player_name):
        pos = player_name_obj.position
        Ground.main_matrix_dict[pos[0], pos[1]] = str(player_name) + '*'

    def display_ground(self, matrix):
        # matrix, three = Ground.create_initial_matrix(self)
        for i in range(self.breadth):
            print('\n')
            for j in range(self.length):
                if matrix[i, j] == '.' or matrix[i, j] == 'O' or matrix[i, j] == 'S':
                    print('   ' + matrix[i, j] + '   ', end='')
                else:
                    print('  ' + matrix[i, j] + '  ', end='')

        print('\n')

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

    def navigator(self, direction, length, breadth):
        row1 = self.position[0]
        col1 = self.position[1]

        if direction == 'n':
            row = self.position[0]
            col = self.position[1]
            if row < 0 or row > breadth or col < 0 or col > length:
                pass
            else:
                row1, col1 = row - 1, col
        elif direction == 's':
            row = self.position[0]
            col = self.position[1]
            if row < 0 or row > breadth or col < 0 or col > length:
                pass
            else:
                row1, col1 = row + 1, col
        elif direction == 'e':
            row = self.position[0]
            col = self.position[1]
            if row < 0 or row > breadth or col < 0 or col > length:
                pass
            else:
                row1, col1 = row, col + 1
        elif direction == 'w':
            row = self.position[0]
            col = self.position[1]
            if row < 0 or row > breadth or col < 0 or col > length:
                pass
            else:
                row1, col1 = row, col - 1
        elif direction == 'ne':
            row = self.position[0]
            col = self.position[1]
            if row < 0 or row > breadth or col < 0 or col > length:
                pass
            else:
                row1, col1 = row - 1, col + 1
        elif direction == 'se':
            row = self.position[0]
            col = self.position[1]
            if row < 0 or row > breadth or col < 0 or col > length:
                pass
            else:
                row1, col1 = row + 1, col + 1
        elif direction == 'nw':
            row = self.position[0]
            col = self.position[1]
            if row < 0 or row > breadth or col < 0 or col > length:
                pass
            else:
                row1, col1 = row - 1, col - 1
        elif direction == 'sw':
            row = self.position[0]
            col = self.position[1]
            if row < 0 or row > breadth or col < 0 or col > length:
                pass
            else:
                row1, col1 = row + 1, col - 1

        # self.position = row1, col1
        return row1, col1

    def place_player_on_ground(self, row_to, col_to):
        temp = Ground.main_matrix_dict[(self.position[0], self.position[1])]
        Ground.main_matrix_dict[(self.position[0], self.position[1])] = '.'
        new_row, new_col = row_to, col_to
        Ground.main_matrix_dict[(new_row, new_col)] = temp

    def move_player_on_ground_with_ball(self, team):
        if team == 'BC':
            direction = random.choices(['n', 's', 'e', 'w', 'ne', 'nw', 'se', 'sw'], weights=(5, 5, 5, 25, 5, 25, 5, 25), k=1)[0]
            print(direction)
            moves = random.choice(['1', '2'])
        else:
            print('In which direction do you want to move?')
            print('Example: N, S, NE, SW')
            direction = input('Enter your choice: ').lower().strip()
            print('\n')
            print('How many steps do you want to take in that direction?')
            print('  1. 1 Step')
            print('  2. 2 Steps')
            moves = input('Enter your choice: ').lower().strip()

        row_no_attack, col_no_attack = self.navigator(direction, ground1.length, ground1.breadth)

        self.position[0] = row_no_attack
        self.position[1] = col_no_attack

        if moves == '2':
            row_no_attack, col_no_attack = self.navigator(direction, ground1.length, ground1.breadth)
        to_move = [row_no_attack, col_no_attack]
        return to_move

    def pass_ball_to_teammate(self):
        GS_team = ['GS1', 'GS2', 'GS3', 'GS4', 'GS5']
        BC_team = ['BC1', 'BC2', 'BC3', 'BC4', 'BC5']
        team_name = self.player_name[:2]
        if team_name == 'GS':
            GS_team.remove(self.player_name)
            print('Choose which teammate you want to pass:')
            for i in GS_team:
                print('  ' + i)
            new_player = input('Enter your choice: ').upper().strip()
        else:
            BC_team.remove(player_with_ball.player_name)
            new_player = random.choice(BC_team)

        return new_player

    def move_defense_to_itercept(self, team):
        if team == 'BC':
            defense_direction = random.choices(['n', 's', 'e', 'w', 'ne', 'nw', 'se', 'sw'])
            steps = random.choice(['1', '2'])
        else:
            defense_direction = input(
                'Enter your direction choice where you want to move the defender. Example: N, S, NE, SW: \n').lower().strip()
            print('\n')
            print('How many steps do you want to take in that direction?')
            print('  1. 1 Step')
            print('  2. 2 Steps')
            steps = input('Enter your choice: ').lower().strip()
            print('\n')
        to_go = defender.navigator(defense_direction, ground1.length, ground1.breadth)
        if steps == '2':
            to_go = defender.navigator(defense_direction, ground1.length, ground1.breadth)

        return to_go

    def calculate_opp_dist(self, curr_player_pos, opp_player_list):
        """
        Identifies all opponent players and their corresponding distances from the current player.
        If the distance is not more than 2 cells, then the opponent is said to be in close range.
        :param curr_player_pos: index of the current player possessing the ball
        :param opp_player_list: list of all opponents
        """

        result_list = []
        for i in opp_player_list:
            opp_position = i.position
            dist = math.dist(curr_player_pos, opp_position)
            if dist <= 2:
                result_list.append(i)

        return result_list

    def extract_three_ptr(self, three_ptr, length):
        """
        Extracts and splits indices of three-pointer regions on both sides of the court into two lists
        :param three_ptr: list containing index values of both three pointer regions
        :param length: length of the court
        """
        three_pointer_GS = []
        three_pointer_BC = []

        for i in three_ptr:
            if i[1] > length / 2:
                three_pointer_BC.append(i)
            else:
                three_pointer_GS.append(i)

        return three_pointer_GS, three_pointer_BC

    def three_ptr_region_valid(self, curr_player_pos, three_ptr):
        """
        Checks whether current player is inside or outside the three-pointer region and returns boolean value.
        :param curr_player_pos: index of the current player possessing the ball
        :param three_ptr: three-pointer region index values of the opponent's side of the court
        """

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

    def calculate_probability(self, curr_player, three_ptr_region_flag, close_player_list):
        """
        Calculates the probability of scoring a basket based on attacker's position, attack strength and presence of close standing opponents
        :param curr_player_pos: index of the current player possessing the ball
        :param three_ptr_region_flag: boolean value stating whether attacker is inside or outside three-pointer region
        :param close_player_list: list containing opponents close to the attacker
        """

        if three_ptr_region_flag == False:
            if len(close_player_list) > 0:
                if curr_player.attack > 80:
                    probability = 0.75 * 0.5
                else:
                    probability = 0.40 * 0.5
            else:
                if curr_player.attack > 80:
                    probability = 0.75
                else:
                    probability = 0.40
        else:
            if curr_player.attack > 80:
                probability = 1
            else:
                probability = 0.75

        return probability

    def update_score(self, probability, scoreboard, key, three_ptr_region_flag):
        """
        Updates and tracks the total score of both teams after every basket
        :param probability: probability of scoring a basket by current attacker
        :param scoreboard: dictionary maintaining current score of both teams
        :param key: key value of scoreboard dictionary
        :param three_ptr_region_flag: boolean value stating whether attacker is inside or outside three-pointer region
        """
        print(f"Shooting Team: {key}")
        p = probability
        not_p = 1 - p
        shoot_success = random.choices(population=(0, 1), weights=(not_p, p))[0]
        if three_ptr_region_flag == False:
            print(f"Shoot Success: {shoot_success}")
            if shoot_success == 1:
                if key in scoreboard:
                    scoreboard[key] += 3
                    return scoreboard
        else:
            print(f"Shoot Success: {shoot_success}")
            if shoot_success == 1:
                if key in scoreboard:
                    scoreboard[key] += 2
                    return scoreboard

    def line_of_sight(self, player1, player2, outsider):
        line = tcod.los.bresenham(player1.position, player2.position).tolist()
        # print(f"line of sighttt: {line}")
        # print(f"outsider position: {outsider.position}")
        if outsider.position in line:
            return True
        else:
            return False

    def move_remaining_players(self, remaining_player_dict, ball_pos):
        new_positions = {}
        for key, value in remaining_player_dict.items():
            row1, col1 = 0, 0
            if ball_pos[1] == value[1] and ball_pos[0] < value[0]:
                row1, col1 = value[0] - 1, value[1]
            if ball_pos[1] == value[1] and ball_pos[0] > value[0]:
                row1, col1 = value[0] + 1, value[1]
            if ball_pos[1] > value[1] and ball_pos[0] == value[0]:
                row1, col1 = value[0], value[1] + 1
            if ball_pos[1] < value[1] and ball_pos[0] == value[0]:
                row1, col1 = value[0], value[1] - 1
            if ball_pos[1] > value[1] and ball_pos[0] < value[0]:
                row1, col1 = value[0] - 1, value[1] + 1
            if ball_pos[1] < value[1] and ball_pos[0] < value[0]:
                row1, col1 = value[0] - 1, value[1] - 1
            if ball_pos[1] > value[1] and ball_pos[0] > value[0]:
                row1, col1 = value[0] + 1, value[1] + 1
            if ball_pos[1] < value[1] and ball_pos[0] > value[0]:
                row1, col1 = value[0] + 1, value[1] - 1
            new_positions[key] = [row1, col1]

        return new_positions

    def move_other_players(self, position_dict):
        for key, value in position_dict.items():
            prev_position = key.position
            if Ground.main_matrix_dict[value[0], value[1]] == '.':
                Ground.main_matrix_dict[prev_position[0], prev_position[1]] = '.'
                Ground.main_matrix_dict[value[0], value[1]] = key.player_name
                key.position = [value[0], value[1]]
        return

if __name__ == '__main__':
    print('\n')
    print('  -------------------Welcome to NBA FINALS 2022!!-------------------')
    print('\n')
    print('You are team Golden State Warriors and you will compete against Boston Celtics (AI)')
    positions1 = [[3, 5], [2, 4], [4, 4], [1, 3], [5, 3]]
    positions2 = [[3, 7], [2, 8], [4, 8], [1, 9], [5, 9]]
    ground1 = Ground(13, 7, positions1, positions2)
    three_ptr = ground1.reset_matrix(True, '')
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

    players = {'GS1': GS1, 'GS2': GS2, 'GS3': GS3, 'GS4': GS4, 'GS5': GS5, 'BC1': BC1, 'BC2': BC2, 'BC3': BC3,
               'BC4': BC4, 'BC5': BC5}
    print('\n\n')


    attack = ''
    defense = ''

    scoreboard = {'GS': 0, 'BC': 0}
    gs_player_list = [players['GS1'], players['GS2'], players['GS3'], players['GS4'], players['GS5']]
    bc_player_list = [players['BC1'], players['BC2'], players['BC3'], players['BC4'], players['BC5']]

    while True:
        golden_state = [GS1, GS2, GS3, GS4, GS5]
        boston_celtics = [BC1, BC2, BC3, BC4, BC5]
        teams_list = ['GS', 'BC']
        ball_with_which_team = ground1.main_matrix_dict[(ground1.cur_ball_pos[0], ground1.cur_ball_pos[1])]
        team_with_ball = ball_with_which_team[:2]
        player_with_ball = ball_with_which_team[:3]
        attack = team_with_ball
        teams_list.remove(attack)
        defense = teams_list[0]
        attacker = players[player_with_ball]
        attack_initial_pos = [attacker.position[0], attacker.position[1]]
        player_with_ball = attacker
        attack_flag1 = True
        defense_flag1 = True
        attacker_next_pos = attacker.position
        flag = 0
        chose_to_pass = False

        if attack == 'BC':
            print("AI's turn")
            i = random.choices(['1', '2', '3'], weights=(60, 20, 20), k=1)[0]
            if i == '1':
                print('The AI has decided to move with the ball. Defend it!')
            elif i == '2':
                print('The AI has decided to pass the ball. Intercept it!')
            else:
                print('The AI has decided to shoot the ball!')
        else:
            print('This move is for the ' + attack + ' team. Choose one of the following:\n')
            print('  1. Move player with the ball in any direction')
            print('  2. Pass the ball to your teammate')
            print('  3. Shoot towards the basket')
            print('  Q. Quit game')
            i = input('Enter your choice: ').lower().strip()
        print('\n')
        if i == '1':
            flag = 1
            while attack_flag1:
                attacker_next_pos = attacker.move_player_on_ground_with_ball(attack)
                if attacker_next_pos[0] < 0 or attacker_next_pos[0] > ground1.breadth or attacker_next_pos[1] < 0 or \
                        attacker_next_pos[1] > ground1.length:
                    continue
                else:
                    if ground1.main_matrix_dict[attacker_next_pos[0], attacker_next_pos[1]] and \
                            ground1.main_matrix_dict[attacker_next_pos[0], attacker_next_pos[1]] != '.':
                        if attack == 'GS':
                            print("That place is already occupied. Choose another place to move your player")
                            print('\n')
                        continue
                    else:
                        attack_flag1 = False

        if i == '2':
            chose_to_pass = True
            initial_attacker = attacker
            teammate = attacker.pass_ball_to_teammate()
            teammate_obj = players[teammate]
            ground1.main_matrix_dict[attack_initial_pos[0], attack_initial_pos[1]] = attacker.player_name
            attacker = teammate_obj
            attacker_next_pos = attacker.position
            # initial_attack_pos = attacker.position

        if i == '3':
            length1 = int(ground1.length)
            three_pointer_GS, three_pointer_BC = attacker.extract_three_ptr(three_ptr, length1)
            if team_with_ball == 'GS':
                bc_close_players = attacker.calculate_opp_dist(attack_initial_pos, bc_player_list)
                is_player_in_three_ptr = attacker.three_ptr_region_valid(attack_initial_pos, three_pointer_BC)
                probability = attacker.calculate_probability(attacker, is_player_in_three_ptr, bc_close_players)
                attacker.update_score(probability, scoreboard, team_with_ball, is_player_in_three_ptr)
                print("*************************** SCOREBOARD ***************************")
                print('                 ', 'Golden State Warriors: ', scoreboard['GS'], '    ')
                print('                        ', 'Boston Celtics: ', scoreboard['BC'], '    ')

                ground1 = Ground(13, 7, positions1, positions2)
                threes = ground1.reset_matrix(True, 'BC')
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
                continue

            elif team_with_ball == 'BC':
                gs_close_players = attacker.calculate_opp_dist(attack_initial_pos, gs_player_list)
                is_player_in_three_ptr = attacker.three_ptr_region_valid(attack_initial_pos, three_pointer_GS)
                probability = attacker.calculate_probability(attacker, is_player_in_three_ptr, gs_close_players)
                attacker.update_score(probability, scoreboard, team_with_ball, is_player_in_three_ptr)
                print("*************************** SCOREBOARD ***************************")
                print('                 ', 'Golden State Warriors: ', scoreboard['GS'], '    ')
                print('                        ', 'Boston Celtics: ', scoreboard['BC'], '    ')
                ground1 = Ground(13, 7, positions1, positions2)
                threes = ground1.reset_matrix(True, 'GC')
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
                continue
        print('\n\n')

        if defense == 'BC':
            print("AI's turn")
            j = random.choice(['1'])
        else:
            print('This move is for the ' + defense + ' team. Choose one of the following defensive move:\n')
            print('  1. Choose your player to move and intercept')
            print('  Q. Quit game')
            j = input('Enter your choice: ').lower().strip()

        print('\n')
        if j == '1':
            if defense == 'BC':
                defense_player = random.choice(['BC1', 'BC2', 'BC3', 'BC4', 'BC5'])
            else:
                GS_team = ['GS1', 'GS2', 'GS3', 'GS4', 'GS5']
                for i in GS_team:
                    print('  ' + i)
                defense_player = input('Enter the player who you want to move: ').upper().strip()

            defender = players[defense_player]
            defense_initial_position = defender.position
            defender_next_pos = defender.position
            while defense_flag1:
                defender_next_pos = defender.move_defense_to_itercept(defense)
                if defender_next_pos[0] < 0 or defender_next_pos[0] > ground1.breadth or defender_next_pos[1] < 0 or \
                        defender_next_pos[1] > ground1.length:
                    continue
                else:
                    if ground1.main_matrix_dict[attacker_next_pos[0], attacker_next_pos[1]] and \
                            ground1.main_matrix_dict[defender_next_pos[0], defender_next_pos[1]] != '.':
                        if defense == 'GS':
                            print("That place is already occupied. Choose another place to move your player")
                            print('\n')
                        continue
                    else:
                        defense_flag1 = False

            if attacker_next_pos == defender_next_pos:
                player_with_ball = defender
                ground1.cur_ball_pos = defender.position
                # -------- need to add cases when the position goes out of bound of the ground---------
                ground1.main_matrix_dict[defense_initial_position[0], defense_initial_position[1]] = '.'
                attacker_player_name = attacker.player_name
                ground1.main_matrix_dict[attack_initial_pos[0], attack_initial_pos[1]] = attacker.player_name
                defender.position = defender_next_pos
                attacker.position = attack_initial_pos
                # -------------------------------------------------------------------------------------
            if chose_to_pass:
                is_defender_in_middle = attacker.line_of_sight(initial_attacker, teammate_obj, defender)
                if is_defender_in_middle:
                    player_with_ball = defender
                    ground1.cur_ball_pos = defender.position
                    # -------- need to add cases when the position goes out of bound of the ground---------
                    ground1.main_matrix_dict[defense_initial_position[0], defense_initial_position[1]] = '.'
                    attacker_player_name = attacker.player_name
                    ground1.main_matrix_dict[attack_initial_pos[0], attack_initial_pos[1]] = attacker.player_name
                    defender.position = defender_next_pos
                    attacker.position = attack_initial_pos
                else:
                    player_with_ball = attacker
                    ground1.main_matrix_dict[defense_initial_position[0], defense_initial_position[1]] = '.'
                    ground1.main_matrix_dict[defender_next_pos[0], defender_next_pos[1]] = defender.player_name
                    if flag == 1:
                        # print(f"{attack_initial_pos[0], attack_initial_pos[1]}")
                        ground1.main_matrix_dict[attack_initial_pos[0], attack_initial_pos[1]] = '.'

                    # print(f"attack initial position: {attack_initial_pos}")
                    # print(f"value: {ground1.main_matrix_dict[attack_initial_pos[0], attack_initial_pos[1]]}")
                    attacker.position = attacker_next_pos
                    defender.position = defender_next_pos

            if attacker_next_pos != defender_next_pos and not chose_to_pass:
                player_with_ball = attacker
                ground1.main_matrix_dict[defense_initial_position[0], defense_initial_position[1]] = '.'
                ground1.main_matrix_dict[defender_next_pos[0], defender_next_pos[1]] = defender.player_name
                if flag == 1:
                    # print(f"{attack_initial_pos[0], attack_initial_pos[1]}")
                    ground1.main_matrix_dict[attack_initial_pos[0], attack_initial_pos[1]] = '.'

                # print(f"attack initial position: {attack_initial_pos}")
                # print(f"value: {ground1.main_matrix_dict[attack_initial_pos[0], attack_initial_pos[1]]}")
                attacker.position = attacker_next_pos
                defender.position = defender_next_pos



        ground1.cur_ball_pos = player_with_ball.position
        ground1.handing_ball_to_player(player_with_ball, player_with_ball.player_name)

        #moving the other 8 players on the field
        if attacker in golden_state:
            golden_state.remove(attacker)
        if attacker in boston_celtics:
            boston_celtics.remove(attacker)
        if defender in golden_state:
            golden_state.remove(defender)
        if defender in boston_celtics:
            boston_celtics.remove(defender)

        list_of_remaining = golden_state + boston_celtics
        remaining_player_positions = {}
        #getting all of their positions
        # print("Getting players positions")
        for rem_player in list_of_remaining:
            remaining_player_positions[rem_player] = rem_player.position

        new_positions = attacker.move_remaining_players(remaining_player_positions, ground1.cur_ball_pos)
        # print(f"These are the new positions: {new_positions}")

        attacker.move_other_players(new_positions)
        ground1.display_ground(ground1.main_matrix_dict)



        print('\n\n')