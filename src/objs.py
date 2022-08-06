from copy import deepcopy
from src import colors, settings

def changes_file(func):
    """Decorator to indicate this function
    alters the user's save file/progress"""
    def inner(*args):
        func(*args)
        settings.UNSAVED_CHANGES = True
    return inner

class Item:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount
    
    def __repr__(self):
        # Represent negative amount as infinity
        amount_repr = self.amount < 0 and colors.PURPLE('Inf') or str(self.amount)
        return f'{colors.by_rarity(self.name.replace("_", " "))} x{amount_repr}'

    def times(self, n):
        """Helper function to print self times a number"""
        tmp = deepcopy(self)
        tmp.amount *= n
        return tmp.__repr__()

class Tool:
    def __init__(self, name, level):
        self.name = name
        self.level = level

    def __repr__(self) -> str:
        return f'{self.name.replace("_", " ")} ({self.level})'
    
    def times(self, n):
        """Helper function to print self times a number"""
        return f'{self.__repr__()} x{n}'

class Inventory:
    def __init__(self):
        self.items    = []
        self.tools    = []
        self.machines = []
        self.checks   = []

    def __repr__(self) -> str:
        return f'Items:\n {self.items}\nTools:\n {self.tools}'

    def clear(self):
        self.items.clear()
        self.tools.clear()
        self.checks.clear()
    
    def find_item(self, item_name):
        for item in self.items:
            if item.name == item_name:
                return item
    def find_tool(self, tool):
        for cur_tool in self.tools:
            if cur_tool.name == tool.name\
            and cur_tool.level == tool.level:
                return tool

    @changes_file
    def add_item(self, item):
        cur_item = self.find_item(item.name)
        if cur_item:
            # Special case for infinity
            if cur_item.amount < 0:
                return True

            cur_item.amount += item.amount
            return True
        else:
            self.items.append(deepcopy(item))
            return True

    @changes_file
    def add_tool(self, tool):
        self.tools.append(deepcopy(tool))
        return True

    @changes_file
    def remove_item(self, item):
        cur_item = self.find_item(item.name)
        if cur_item:
            # Special case for infinity
            if cur_item.amount < 0:
                return True

            if cur_item.amount < item.amount:
                print(colors.YELLOW(
f'Warning: tried to remove {item.amount} of \'{item.name}\', but there was only {cur_item.amount}'
                ))
                return False
            cur_item.amount -= item.amount
            if cur_item.amount == 0:
                self.items.remove(cur_item)
            return True
        else:
            print(colors.YELLOW(
f'Warning: tried to remove {item.amount} of \'{item.name}\', but there weren\'t any'
            ))
            return False
    
    @changes_file
    def remove_tool(self, tool):
        cur_tool = self.find_tool(tool)
        if cur_tool:
            if tool.level == 0:
                print(colors.YELLOW(f'You cannot toss this tool!'))
                return False
            
            self.tools.remove(cur_tool)
            return True
    
    def validate(self, recipe):
        """Returns True if inventory contains all items
        and tools needed to run the given recipe"""
        for r_input in recipe.r_inputs:
            item = self.find_item(r_input.name)
            if item:
                if item.amount >= 0 and item.amount < r_input.amount:
                    # Do not have enough of this item
                    return False
            else:
                # Missing this item
                return False

        if self.find_tool(recipe.tool):
            return True
        
        if recipe.tool.level == 0:
            return True

    def run(self, recipe):
        """This function subtracts all input items
        from the inventory and adds the output
        items. It does NOT validate the recipe first."""
        for input_item in recipe.r_inputs:
            self.remove_item(input_item)
        
        if isinstance(recipe, Recipe):
            for output_item in recipe.r_outputs:
                self.add_item(output_item)
        elif isinstance(recipe, Tool_Recipe):
            self.add_tool(recipe.r_output)

class Recipe:
    def __init__(self, r_outputs, tool, r_inputs):
        self.r_outputs = r_outputs
        self.tool  = tool
        self.r_inputs  = r_inputs

    def __repr__(self):
        s = str(self.r_inputs) + ' -> '
        s += str(self.r_outputs) + '\n    '
        s += str(self.tool) + '\n'
        return s

class Tool_Recipe:
    def __init__(self, r_output, tool, r_inputs):
        self.r_output = r_output
        self.tool  = tool
        self.r_inputs  = r_inputs

    def __repr__(self):
        s = str(self.r_inputs) + ' -> ['
        s += str(self.r_output) + ']\n    '
        s += str(self.tool) + '\n'
        return s
