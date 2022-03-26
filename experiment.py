import numpy as np
from botbowl.core import Action, Agent, ActionType
import botbowl
from copy import deepcopy
import random


class Node():
    
    def __init__(self, state, parent=None, parent_action=None):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        return


    def untried_actions(self):
        self._untried_actions = self.state.get_available_actions()
        return self._untried_actions


    def newChild(self):

        print("\nExpand called")
        print("Available Actions:", self.state.get_available_actions())

        #The pop() returns an ActionChoice() object
        recievedAction = self._untried_actions.pop()
        
        #Get a random position and a random player for the given Action Choice's action type
        try:
            position = random.choice(recievedAction.positions)
        except:
            position = None

        try:
            player = random.choice(recievedAction.players)
        except:
            player = None

        #Create the action object with the given action type and the obtained position and player
        action = botbowl.core.Action(recievedAction.action_type, position=position, player=player)

        #Check if action is allowed
        print("Action allowed:",self.state._is_action_allowed(action))
        print("Is hard-coded TAILS allowed?:", self.state._is_action_allowed(Action(ActionType.TAILS)))

        #Perform the action
        next_state = self.state.step(action)
        # next_state = self.state.step(Action(ActionType.TAILS)) #This fails too

        #Get child node of that action and append to list of children of current node
        child_node = Node(
            next_state, parent=self, parent_action=action)
        self.children.append(child_node)

        return child_node 


class bot(botbowl.Agent):

    def __init__(self, name, seed=None):
        super().__init__(name)
        self.my_team = None
        self.rnd = np.random.RandomState(seed)

    def new_game(self, game, team):
        self.my_team = team

    def act(self, game):
        game_copy = deepcopy(game)
        game_copy.enable_forward_model()
        game_copy.home_agent.human = True
        game_copy.away_agent.human = True
        print("\nact method called")
        print("Game Copy Available actions:", game_copy.get_available_actions())
        print("Is hard-coded TAILS allowed?:", game_copy._is_action_allowed(Action(ActionType.TAILS)))

        root_node = Node(state=game_copy)
        selectedChild = root_node.newChild()

        print("\nSelected Action:",selectedChild.action.action_type)

        return selectedChild.action


# Register the bot to the framework
botbowl.register_bot('experiment-bot', bot)

import botbowl.web.server as server

server.start_server(debug=True, use_reloader=False, port=1234)

# Load configurations, rules, arena and teams
config = botbowl.load_config("bot-bowl")
ruleset = botbowl.load_rule_set(config.ruleset)
arena = botbowl.load_arena(config.arena)
home = botbowl.load_team_by_filename("human", ruleset)
away = botbowl.load_team_by_filename("human", ruleset)
config.competition_mode = False
config.debug_mode = False
config.fast_mode = True
config.pathfinding_enabled = False

# Play a game
bot_a = botbowl.make_bot("experiment-bot")
bot_b = botbowl.make_bot("experiment-bot")
game = botbowl.Game(1, home, away, bot_a, bot_b, config, arena=arena, ruleset=ruleset)
print("Starting game")
game.init()
print("Game is over")





 



