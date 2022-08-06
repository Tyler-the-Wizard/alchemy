from inspect import signature
from src import crafting, colors, disk, objs, settings

# Command functions
def show_help():
    for cmd in cmd_list.keys():
        cmd_name = cmd.rjust(12)
        cmd_name = (cmd in debug_cmds.keys() and colors.PURPLE(cmd_name) or cmd_name)
        print(cmd_name, '-', cmd_list[cmd][0])
    print(f'{"exit".rjust(12)} - exit the program')

def show_items():
    print(settings.INV.items)
def show_tools():
    print(settings.INV.tools)
def show_machines():
    print(settings.INV.machines)

def do_toss():
    print(colors.RED('Function not implemented yet!!'))

def craft_helper(recipe, num_times):
    i = -1
    for i in range(num_times):
        if not crafting.run(recipe):
            i -= 1
            break
    
    if i == -1:
        # Failed to craft anything (this should never happen)
        print(colors.RED('Oh no! Something went wrong'))
    else:
        print(colors.GREEN('Successfully crafted:'))
        if isinstance(recipe, objs.Recipe):
            for item in recipe.r_outputs:
                print(f'  {item.times(i + 1)}')
        elif isinstance(recipe, objs.Tool_Recipe):
            print(f'  {recipe.r_output.times(i + 1)}')

def do_craft(cmd_tool):
    cmd_tool = str.title(cmd_tool)
    level = 0
    for tool in settings.INV.tools:
        if tool.name == cmd_tool:
            level = tool.level
    
    print(f'Crafting with {cmd_tool} ({level}).\n{settings.CRAFT_PROMPT}', end='')
    raw_input = input()
    if len(raw_input) == 0:
        # Use all items in the inventory as inputs.
        raw_input = ' '.join([item.name for item in settings.INV.items])

    valid_recipes, num_times = crafting.search(objs.Tool(cmd_tool, level), raw_input)
    if len(valid_recipes) == 0:
        print(colors.YELLOW(f'Warning: No recipes found for given inputs. Aborting'))
    elif len(valid_recipes) == 1:
        craft_helper(valid_recipes[0], num_times)

    else:
        print('Select product to make:')
        for i, recipe in enumerate(valid_recipes):
            if isinstance(recipe, objs.Recipe):
                print(f'  {i+1} - {recipe.r_outputs}')
            elif isinstance(recipe, objs.Tool_Recipe):
                print(f'  {i+1} - {recipe.r_output}')
        
        print(settings.CRAFT_PROMPT, end='')
        raw_selection = input()
        if raw_selection.isdigit():
            selection = int(raw_selection) - 1
            craft_helper(valid_recipes[selection], num_times)
        else:
            print(colors.YELLOW(f'Warning: Invalid selection. Aborting'))

def do_auto():
    print(colors.RED('Function not implemented yet!!'))

# Debug functions
def spawn_item(name, amount):
    settings.INV.add_item(objs.Item(
        str.title(name),
        int(amount)
    ))

def remove_item(name, amount):
    settings.INV.remove_item(objs.Item(
        str.title(name),
        int(amount)
    ))

def get_tool(name, level):
    settings.INV.add_tool(objs.Tool(
        str.title(name),
        int(level)
    ))

def new_recipe(recipe_type):
    recipe_type = str.title(recipe_type)
    if recipe_type == 'Item':
        outputs = []
        while True:
            print('Output: ', end='')
            output_name = str.title(input())
            if output_name == '':
                break
            print('Amount: ', end='')
            output_amount = int(input())

            outputs.append(objs.Item(output_name, output_amount))
        
        print('Tool: ', end='')
        tool_name = str.title(input())
        print('Level: ', end='')
        tool_level = int(input())

        tool = objs.Tool(tool_name, tool_level)

        inputs = []
        while True:
            print('Input: ', end='')
            input_name = str.title(input())
            if input_name == '':
                break
            print('Amount: ', end='')
            input_amount = int(input())

            inputs.append(objs.Item(input_name, input_amount))

        settings.RECIPES.append(objs.Recipe(
            outputs, tool, inputs
        ))

    elif recipe_type == 'Tool':
        print('Output: ', end='')
        output_name = str.title(input())
        print('Level: ', end='')
        output_level = int(input())

        output = objs.Tool(output_name, output_level)
        
        print('Tool: ', end='')
        tool_name = str.title(input())
        print('Level: ', end='')
        tool_level = int(input())

        tool = objs.Tool(tool_name, tool_level)

        inputs = []
        while True:
            print('Input: ', end='')
            input_name = str.title(input())
            if input_name == '':
                break
            print('Amount: ', end='')
            input_amount = int(input())

            inputs.append(objs.Item(input_name, input_amount))

        settings.RECIPES.append(objs.Tool_Recipe(
            output, tool, inputs
        ))

def show_recipes():
    for recipe in settings.RECIPES:
        print(recipe)        

def run_all():
    for recipe in settings.RECIPES:
        name = ''
        if isinstance(recipe, objs.Recipe):
            name = recipe.r_outputs[0].name
        elif isinstance(recipe, objs.Tool_Recipe):
            name = recipe.r_output.name

        if settings.INV.validate(recipe):
            settings.INV.run(recipe)
            print(f'Ran recipe for {name}')
        else:
            print(f'Failed to run recipe for {name}')

# Syntax of a command:
#   'command_name' : ('command_description', command_func)
cmd_list = {
    'help'         : ('show this list', show_help),
    'save'         : ('save your progress', disk.usr_save),
    'load'         : ('load save data from a file', disk.usr_load),
    'inv'          : ('display your current inventory', show_items),
    'tools'        : ('display your current tools', show_tools),
    'machines'     : ('display your current automatic machines', show_machines),
    'toss'         : ('discard an item, tool, or machine', do_toss),
    'use'          : ('use a tool to craft something', do_craft),
    'auto'         : ('set up and manage automatic machines', do_auto),
}
    
debug_cmds = {
    ### DEBUG COMMANDS ###
    'add'          : ('debug command to add items to your inventory', spawn_item),
    'remove'       : ('debug command to remove items from your inventory', remove_item),
    'add_tool'     : ('debug command to add a tool to your inventory', get_tool),
    'add_recipe'   : ('debug command to create a new recipe', new_recipe),
    'view_recipes' : ('debug command to view all loaded recipes', show_recipes),
    'run_all'      : ('debug command to run all recipes', run_all),
}

if settings.DEBUG_MODE:
    cmd_list = cmd_list | debug_cmds

cmd_aliases = {
    '?' : 'help',
    'i' : 'inv',
    't' : 'tools',
    'm' : 'machines',
    ### DEBUG ALIASES ###
    'get' : 'add_tool',
}

def loop():
    while True:
        print(settings.PROMPT, end='')
        raw_input = input()
        if len(raw_input) == 0:
            continue
        user_input = raw_input.split()

        # Parse input as first word being
        # command, all rest being args
        cmd = user_input[0].lower()
        args = user_input[1:]

        if cmd in ['quit', 'exit', 'q']:
            break

        # Substitute aliases
        if cmd in cmd_aliases.keys():
            cmd = cmd_aliases[cmd]

        # Determine if this command can be parsed
        if cmd in cmd_list.keys():
            cmd_func = cmd_list[cmd][1]
            num_args = len(signature(cmd_func).parameters)

            # Determine if the user supplied
            # the correct number of arguments
            if len(args) != num_args:
                print(colors.RED(f'Error: command \'{cmd}\' expects {num_args} parameters, got {len(args)}'))
            else:
                cmd_func(*args)
        else:
            print(colors.RED(f'Error: unknown command \'{raw_input}\'.'))
