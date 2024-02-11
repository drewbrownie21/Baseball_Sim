import json

class Roster:
    '''Roster is for setting lineups'''
    def __init__(self, team_name):
        file_path = f'/Users/drewbrown/Projects/Baseball_Sim/rosters/{team_name}.json'
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        self.team = json_data

    def set_spot_in_lineup(self, lineup:list, arg_one:str, arg_two:str, arg_three:str=None):
        '''
        set_spot_in_lineup is for being able to set a spot in the lineup based off of certain overalls
        '''
        new_total = 0
        for hitter in lineup:
            total = lineup[hitter][arg_one] + lineup[hitter][arg_two] + lineup[hitter].get(arg_three,0)
            if total > new_total:
                player = hitter
                new_total = total
        return player

    def lineup(self):
        '''
        lineup is for setting the lineup based off stats
        1 - highest contact + speed
        2 - best contact + eye
        3 - best contact + power + eye
        4 - best power
        5 - 2nd best power + contact + eye
        6-8 - third-fifth best power + contact + eye
        9 - Second fastest speed left after 1-4
        '''
        lineup_temp = self.team['players']['hitters']
        lineup = [''] * 9
        default_lineup_contruction = {
            0 : ['contact', 'speed', None],
            1 : ['contact', 'eye', None],
            2 : ['contact', 'power', 'eye'],
            3 : ['contact', 'power', None],
            8 : ['contact', 'speed', None],
            4 : ['contact', 'power', 'eye'],
            5: ['contact', 'power', 'eye'],
            6 : ['contact', 'power', 'eye'],
            7 : ['contact', 'power', 'eye'],
        }

        for spot in default_lineup_contruction.items():
            hitter = Roster('Giants').set_spot_in_lineup(lineup_temp,
                                                         spot[1][0],
                                                         spot[1][1],
                                                         spot[1][2])
            lineup[spot[0]] = hitter
            lineup_temp.pop(hitter) 

        return lineup

    def display_lineup(self, lineup):
        '''Display the lineup as Batting Spot - Player Name - Player Position'''
        display_lineup_list = [f"{self.team['players']['hitters'][player]['name']} - {player}" for player in lineup]

        for index, player in enumerate(display_lineup_list, start=1):
            print(f'{index}) {player}')
            
