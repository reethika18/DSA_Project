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
    def __init__(self, team, position, defence, attack, passing):
        self.team = team
        self.position = position
        self.defence = defence
        self.attack = attack
        self.passing = passing




if __name__ == '__main__':
    ground1 = Ground(19, 7)
    cells, three_ptr = ground1.create_initial_matrix()
