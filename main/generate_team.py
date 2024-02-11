import random
import json
import os
from faker import Faker
import configuration as c

class GenerateTeam:
    '''
    This class is for generating a team from scratch
    '''
    def __init__(self):
        with open('/Users/drewbrown/Projects/Baseball_Sim/rosters/template.json', 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        self.team = json_data
              
    def generate_names(self, team):
        '''generate_names takes in a team and creates random names for all players'''
        for pitcher in team['players']["pitchers"]:
            team['players']["pitchers"][pitcher]['name'] = Faker().first_name_male() + " " + Faker().last_name_male()
        for hitter in team['players']["hitters"]:
            team['players']["hitters"][hitter]['name'] = Faker().first_name_male() + " " + Faker().last_name_male()
        return team
    
    def generate_pitching_stats(self, team):
        '''
        generate_pitching_stats loops through all pitchers and creates random stats
        Starters get higher stamina and stamina weighs more in the overall calculation
        Relievers and Closers, the stamina is not as heavy along with being capped at 40
        '''
        starter = team['players']['pitchers']['starter']
        reliever = team['players']['pitchers']['reliever']
        closer = team['players']['pitchers']['closer']

        # Starter
        starter['stamina'] = random.randint(c.DEFAULT_STARTER_STAMINA_MIN, c.DEFAULT_STARTER_STAMINA_MAX)
        starter['control'] = random.randint(c.DEFAULT_STARTER_CONTROL_MIN,c.DEFAULT_STARTER_CONTROL_MAX)
        starter['velocity'] = random.randint(c.DEFAULT_STARTER_VELO_MIN,c.DEFAULT_STARTER_VELO_MAX)
        starter['movement'] = random.randint(c.DEFAULT_STARTER_MOVEMENT_MIN,c.DEFAULT_STARTER_MOVEMENT_MAX)
        # Overall evenly calculated between all 4 stats
        starter['overall'] = int((starter['stamina'] + starter['control'] + starter['velocity'] + starter['movement'])/4)

        # Reliever and closer
        reliever['stamina'] = random.randint(c.DEFAULT_RELIEVER_STAMINA_MIN,c.DEFAULT_RELIEVER_STAMINA_MAX)
        reliever['control'] = random.randint(c.DEFAULT_RELIEVER_CONTROL_MIN,c.DEFAULT_RELIEVER_CONTROL_MAX)
        reliever['velocity'] = random.randint(c.DEFAULT_RELIEVER_VELO_MIN,c.DEFAULT_RELIEVER_VELO_MAX)
        reliever['movement'] = random.randint(c.DEFAULT_RELIEVER_MOVEMENT_MIN,c.DEFAULT_RELIEVER_MOVEMENT_MAX)
        closer['stamina'] = random.randint(c.DEFAULT_CLOSER_STAMINA_MIN,c.DEFAULT_CLOSER_STAMINA_MAX)
        closer['control'] = random.randint(c.DEFAULT_CLOSER_CONTROL_MIN,c.DEFAULT_CLOSER_CONTROL_MAX)
        closer['velocity'] = random.randint(c.DEFAULT_CLOSER_VELO_MIN,c.DEFAULT_CLOSER_VELO_MAX)
        closer['movement'] = random.randint(c.DEFAULT_CLOSER_MOVEMENT_MIN,c.DEFAULT_CLOSER_MOVEMENT_MAX)

        # Reliever and closer overall weighs stamina less
        reliever['overall'] = int(reliever['stamina'] * 0.2) + int((reliever['control'] 
                                                                + reliever['velocity'] 
                                                                + reliever['movement'])
                                                                /3)
        closer['overall'] = int(closer['stamina'] * 0.2) + int((closer['control'] 
                                                                + closer['velocity'] 
                                                                + closer['movement'])
                                                                /3)

        return team
    
    def generate_hitting_stats(self, team):
        '''
        generate_hitting_stats loops through all hitters, creating random stats
        All stats are weighed equally in the overall calculation
        '''
        for hitter in team['players']['hitters']:
            team['players']["hitters"][hitter]['contact'] = random.randint(20,80)
            team['players']["hitters"][hitter]['power'] = random.randint(20,80)
            team['players']["hitters"][hitter]['speed'] = random.randint(20,80)
            team['players']["hitters"][hitter]['eye'] = random.randint(20,80)
            team['players']["hitters"][hitter]['defense'] = random.randint(20,80)
            team['players']["hitters"][hitter]['overall'] = int((team['players']["hitters"][hitter]['contact']
                                        + team['players']["hitters"][hitter]['power']
                                        + team['players']["hitters"][hitter]['speed']
                                        + team['players']["hitters"][hitter]['eye']
                                        + team['players']["hitters"][hitter]['defense'])
                                        /5)
        return self.team
    
    def save_team(self, team):
        '''
        save_team checks if a team exists with the same name and if not, 
        saves a new team to the rosters folder
        '''
        team_name = team['team_name']
        team_path = f'/Users/drewbrown/Projects/python_projects/baseball_sim/rosters/{team_name}.json'
        if not os.path.exists(team_path):
            with open(team_path, 'w', encoding='utf-8') as f:
                json.dump(team, f, ensure_ascii=False, indent=4)
        else:
            print(f'{team_name} already exists!')
    
    def generate_team(self, team_name):
        '''
        generate_team compiles all the different data to create a team
        The overall for the team is calculated, all players weigh equally into this calculation
        '''
        GenerateTeam().generate_names(self.team)
        GenerateTeam().generate_pitching_stats(self.team)
        GenerateTeam().generate_hitting_stats(self.team)

        # Calculate the team overall
        hitters_overall = sum(player_dict['overall'] for player_dict in self.team['players']['hitters'].values())   
        pitchers_overall = sum(player_dict['overall'] for player_dict in self.team['players']['pitchers'].values())
        team_overall = (hitters_overall + pitchers_overall)/(len(self.team['players']['pitchers']) + len(self.team['players']['hitters']))
        self.team['team_overall'] = int(team_overall)

        # Set Team Name
        self.team["team_name"] = team_name
        
        GenerateTeam().save_team(self.team)

        return self.team
