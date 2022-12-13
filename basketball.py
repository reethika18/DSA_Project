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
            print('  1. 1 Step ')
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