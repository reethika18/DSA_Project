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

        print(main_matrix)

        return main_matrix, three_pointer

# def output(matrix):
#     for i in matrix:
#         print(i)
#     print("\n")
#
# def initialise_basketball_court(court):
#     row = col = 0
#     rows = 7
#     cols = 13
#     for i in range(rows):
#         court.append([])
#         for j in range(cols):
#             court[i]. append('  ')
#     output(court)
    # while row < rows:
    #     while col < cols:
    #
    #
    #         col += 1
    #     row += 1
    #     col = 0

class Player(Ground):
    def __init__(self, team_name, player_name, position, defence, attack):
        self.team_name = team_name
        self.player_name = player_name
        self.position = position
        self.defence = defence
        self.attack = attack




if __name__ == '__main__':
    basketball_court = []
    # initial_basketball_court = initialise_basketball_court(basketball_court)
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
    ground1 = Ground(13, 7)
    cells, three_ptr = ground1.create_initial_matrix()

    while True:
        # two cases - attack and defense...depends who the ball is the with
        print('This move is for the Golden State Warriors team. Choose one of the following:\n')
        print('  1. Move player with the ball in any direction')
        print('  2. Pass the ball to your teammate')
        print('  3. Shoot towards the basket')
        print('  Q. Quit game')
        i = input('Enter your choice: ').lower().strip()
        if i == '1':
            pass
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
