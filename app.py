"""
Offline dino game:
You start at the beginning of 'levelX' string, dino move forward automatically
He will face obstacles on the way to the finish line, and needs to avoid them
2 possible actions:
- crouch
- jump
2 types of obstacles:
- ground obstacles: Dino needs to JUMP to avoid them
- sky obstacles: Dino needs to CROUCH to avoid them
For the first deadline we will only deal with ground obstacles (level1 string)
"""

# Level configuration
level1 = """_____#_____#_______#__#_______#____*"""
level2 = """__#______^___^___#__^__#_____#___#_*"""

# Level components
GROUND = '_'
GROUND_OBSTACLE = '#'
SKY_OBSTACLE = '^'
GOAL = '*'

# Actions
CROUCH = 'C'
JUMP = 'J'
ACTIONS = [CROUCH, JUMP]

# Rewards
REWARD_CROUCH = 10
REWARD_JUMP = 10
REWARD_GOAL = 100
REWARD_OBSTACLE = -1000


class Environment:
    def __init__(self):
        pass


class Dino:
    def __init__(self):
        pass
