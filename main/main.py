import json 
import os
from roster import Roster
from generate_team import GenerateTeam
from tools import Tools

class GamePlay:
    '''
    This is going to start as the gameplay class
    '''
    def __init__(self, team_name):
        self.team_name = team_name
        self.team_path = f'/Users/drewbrown/Projects/Baseball_Sim/rosters/{self.team_name}.json'
        with open(self.team_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        self.team = json_data

    # def pitcher(self): 
    #     '''pitcher gets the pitchers stats for the team'''
    #     a = self.team['players']['pitchers']['starter']
    #     b = Roster('Giants').lineup()

    def main_menu(self):
        user_input = input('[1] Start a scrimmage \n')
        if user_input == '1':
            print('Starting scrimmage...')
            print(f'The lineup for {self.team_name} is: ')
            Roster(self.team_name).display_lineup(Roster(self.team_name).lineup())
          
        
if __name__ == "__main__":
    print("Welcome to baseball sim 2024, select an option below.")
    user_input = input('[0] Generate a team.\n[1]Select Current Team! \n ')
    if user_input == '0':
            create_team_name = input("What is the name of the team you want to create? ")
            GenerateTeam().generate_team(create_team_name)
    elif user_input == '1':
        existing_teams = Tools().get_existing_team()
        for index, team in enumerate(existing_teams, start=1):
             print(f'[{index}] {team}')
        select_team_index = int(input()) - 1
        select_team = existing_teams[select_team_index]

    GamePlay(team_name=select_team).main_menu()
