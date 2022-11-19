class Ground:
    def __init__(self, length, breadth):
        self.length = length
        self.breadth = breadth

    def give_dimensions(self):
        return self.length, self.breadth

    def assign_squares(self):
        l_mid = self.length // 2
        b_mid = self.breadth // 2
        goal_post_left = [b_mid, 0]
        goal_post_right = [b_mid, self.length-1]
        start_sq = [b_mid, l_mid ]
        return goal_post_left, goal_post_right, start_sq

    def create_initial_matrix(self):
        three_pointer = []
        main_matrix = []
        positions1 = [[3, 5], [2, 4], [4, 4], [1, 3], [5, 3]]
        positions2 = [[3, 7], [2, 8], [4, 8], [1, 9], [5, 9]]
        row = 0
        col = 0

        goal_post_left, goal_post_right, start_sq = self.assign_squares()
        print(goal_post_left, goal_post_right, start_sq)
        while row < self.breadth:
            while col < self.length:
                main_matrix.append([row, col])
                if [row, col] == goal_post_left or [row, col] == goal_post_right:
                    print('  O  ', end='')
                elif [row, col] == start_sq:
                    print('  S  ', end='')
                elif [row, col] in positions1:
                    print(' GS' + str(positions1.index([row, col]) + 1) + ' ', end='')
                elif [row, col] in positions2:
                    print(' BC' + str(positions2.index([row, col]) + 1) + ' ', end='')

                elif ((row == 1 and col <= 3) or (1 <= row <= self.breadth - 2 and col == 3)) or (
                        (row == 1 and col >= self.length - 2) or (
                        1 <= row <= self.breadth - 2 and col == self.length - 2)) or (
                        row == self.breadth - 2 and col <= 3) or (row == self.breadth - 2 and col >= self.length - 2):
                    print('  .  ', end='')
                    three_pointer.append([row, col])
                else:
                    print('  .  ', end='')
                col += 1


            print('\n')

            col = 0
            row += 1

        return main_matrix, three_pointer


class Player:
    def __init__(self, team_name, player_name, position, defence, attack):
        self.team_name = team_name
        self.player_name = player_name
        self.position = position
        self.defence = defence
        self.attack = attack

    # def move_player(self):


    # def circumference(self, l, b):
    #     cur_row = self.position[0]
    #     cur_col = self.position[1]
    #     start = []
    #     end = []
    #     count = 0
    #     while count < 2:
    #         if cur_row - 2 >= 0:
    #             start.append(cur_row - 2)
    #         if cur_row - 2 < 0 and cur_row - 1 >= 0:
    #             start.append(cur_row - 1)
    #         if cur_row - 2 < 0 and cur_row - 1 < 0 and cur_row == 0:
    #             start.append(cur_row)
    #         if cur_col - 2 < 0 and cur_col - 1 < 0 and cur_col == 0:
    #             start.append(cur_col)
    #         if cur_col - 2 < 0 and cur_col - 1 >= 0:
    #             start.append(cur_col - 1)
    #         if cur_col - 2 >= 0:
    #             start.append(cur_col - 2)
    #         if cur_row + 2 < b:
    #             end.append(cur_row + 2)
    #         if cur_row + 2 >= b > cur_row + 1:
    #             end.append(cur_row + 1)
    #         if cur_row + 2 >= b and cur_row + 1 >=b and cur_row == b-1:
    #             end.append(cur_row)
    #         if cur_col + 2 < l:
    #             end.append(cur_col + 2)
    #         if cur_col + 2 >= l > cur_col + 1:
    #             end.append(cur_col + 1)
    #         if cur_col + 2 >= l and cur_col + 1 >= l and cur_col == l-1:
    #             end.append(cur_col)
    #
    #     return start, end

    def passing(self, pass_to):
        # pass_to is a list of 2 positions where first position is where player with ball at present is willing to pass and second is where the opposite player wants to move
        pass


if __name__ == '__main__':
    ground1 = Ground(13, 7)
    GS1 = Player('Golden State Warriors', 'GS1', [3, 5], 80, 95)
    GS2 = Player('Golden State Warriors', 'GS2', [2, 4], 85, 85)
    GS3 = Player('Golden State Warriors', 'GS3', [4, 4], 85, 85)
    GS4 = Player('Golden State Warriors', 'GS4', [1, 3], 90, 80)
    GS5 = Player('Golden State Warriors', 'GS5', [5, 3], 90, 80)
    BC1 = Player('Boston Celtics', 'BC1', [3, 7], 80, 95)
    BC2 = Player('Boston Celtics', 'BC2', [2, 8], 85, 85)
    BC3 = Player('Boston Celtics', 'BC3', [4, 8], 85, 85)
    BC4 = Player('Boston Celtics', 'BC4', [1, 9], 90, 80)
    BC5 = Player('Boston Celtics', 'BC5', [5, 9], 90, 80)
    cells, three_ptr = ground1.create_initial_matrix()
