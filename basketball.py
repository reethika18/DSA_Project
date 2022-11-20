import math
import random


class Ground:
    def __init__(self, length, breadth):
        self.length = length
        self.breadth = breadth

    def assign_squares(self):
        l_mid = self.length // 2
        b_mid = self.breadth // 2
        goal_post_left = [b_mid, 1]
        goal_post_right = [b_mid, self.length]
        start_sq = [b_mid, l_mid + 1]
        return goal_post_left, goal_post_right, start_sq

    def create_initial_matrix(self):
        three_pointer = []
        main_matrix = []
        row = 0
        col = 0

        goal_post_left, goal_post_right, start_sq = self.assign_squares()
        print(goal_post_left, goal_post_right, start_sq)
        while row < self.breadth:
            while col < self.length:
                main_matrix.append([row, col])
                col += 1
                if [row, col] == goal_post_left or [row, col] == goal_post_right:
                    print('  O  ', end='')
                elif [row, col] == start_sq:
                    print('  S  ', end='')
                elif ((row == 1 and col <= 3) or (1 <= row <= self.breadth - 2 and col == 3)) or (
                        (row == 1 and col >= self.length - 2) or (
                        1 <= row <= self.breadth - 2 and col == self.length - 2)) or (
                        row == self.breadth - 2 and col <= 3) or (row == self.breadth - 2 and col >= self.length - 2):
                    print('  .  ', end='')
                    three_pointer.append([row, col])
                else:
                    print('  .  ', end='')

            print('\n')

            col = 0
            row += 1

        return main_matrix, three_pointer


class Player:
    def __init__(self, team, position, defence, attack):
        self.team = team
        self.position = position
        self.defence = defence
        self.attack = attack

class Basket:
    """
    when a player shoots a basket.
    """
    def __init__(self, basket_type, score, shoot_probability, opponent_dist, player_action):
        self.basket_type = basket_type
        self.score = score
        self.shoot_probability = shoot_probability
        self.opponent_dist = opponent_dist
        self.player_action = player_action

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
        max_col =  max(col_list)
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
                probability = 0.75
        else:
            probability = 1

        return probability

    def update_score(self, curr_player, probability, score_board):
        if probability == 0.5:
            basket = random.choices(population=(0,1), weights= (0.5,0.5))
        elif probability == 0.75







if __name__ == '__main__':
    scoreboard = {'GSW': 0, 'BC': 0 }
    ground1 = Ground(19, 7)
    cells, three_ptr = ground1.create_initial_matrix()
    GS1 = Player('Golden State Warriors', (3, 4), 80, 95)
    GS2 = Player('Golden State Warriors', (3, 4), 80, 85)
    GS3 = Player('Golden State Warriors', (3, 4), 85, 85)
    GS4 = Player('Golden State Warriors', (3, 4), 85, 80)
    GS5 = Player('Golden State Warriors', (3, 4), 95, 80)
    BC1 = Player('Boston Celtics', (3, 4), 80, 95)
    BC2 = Player('Boston Celtics', (3, 4), 80, 85)
    BC3 = Player('Boston Celtics', (3, 4), 85, 85)
    BC4 = Player('Boston Celtics', (3, 4), 85, 80)
    BC5 = Player('Boston Celtics', (3, 4), 95, 80)