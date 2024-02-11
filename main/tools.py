import os

class Tools:
    '''This class is meant to be used for creating useful tools amongst the sim'''
    def get_existing_team(self):
        '''Returns all existing teams in the rosters folder'''
        path = "/Users/drewbrown/Projects/Baseball_Sim/rosters"
        team_list = os.listdir(path)

        team_name_list = [team[:-5] for team in team_list]
        team_name_list.remove('template')

        return team_name_list
