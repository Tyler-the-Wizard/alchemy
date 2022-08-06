import os, json
from src import colors, objs, settings

# Loading
def load_json(filename):
    file = open(filename)
    json_str = file.read()
    file.close()

    return json.loads(json_str)

def load_recipes(filename):
    recipes = load_json(filename)
    for recipe in recipes:

        outputs = recipe['outputs']
        r_outputs = []
        for output in outputs:
            r_outputs.append(objs.Item(
                output['name'],
                output['amount']
            ))

        tool = objs.Tool(
            recipe['tool']['name'],
            recipe['tool']['level']
        )

        inputs = recipe['inputs']
        r_inputs = []
        for input in inputs:
            r_inputs.append(objs.Item(
                input['name'],
                input['amount']
            ))

        settings.RECIPES.append(objs.Recipe(
            r_outputs, tool, r_inputs
        ))

def load_tool_recipes(filename):
    recipes = load_json(filename)
    for recipe in recipes:

        r_output = objs.Tool(
            recipe['output']['name'],
            recipe['output']['level']
        )

        tool = objs.Tool(
            recipe['tool']['name'],
            recipe['tool']['level']
        )

        inputs = recipe['inputs']
        r_inputs = []
        for input in inputs:
            r_inputs.append(objs.Item(
                input['name'],
                input['amount']
            ))

        settings.RECIPES.append(objs.Tool_Recipe(
            r_output, tool, r_inputs
        ))

def load_inv(filename):
    inv_dat = load_json(filename)

    for item in inv_dat['items']:
        settings.INV.items.append(objs.Item(
            item['name'],
            item['amount']
        ))
    
    for tool in inv_dat['tools']:
        settings.INV.tools.append(objs.Tool(
            tool['name'],
            tool['level']
        ))

    for check in inv_dat['checks']:
        settings.INV.checks.append(check)

def load_all(dirname):
    if os.path.isdir(dirname):
        recipe_path = dirname + '/recipes.json'
        tool_recipe_path = dirname + '/tool_recipes.json'
        inv_path = dirname + '/inv.json'

        if os.path.isfile(recipe_path):
            load_recipes(recipe_path)
        if os.path.isfile(tool_recipe_path):
            load_tool_recipes(tool_recipe_path)
        if os.path.isfile(inv_path):
            load_inv(inv_path)
        
        return True
    else:
        print(colors.RED(f'Failed to load \'{dirname}\''))

def usr_load(save_name):
    settings.RECIPES.clear()
    settings.INV.clear()

    res = load_all(f'{settings.SAVE_DIR}/{save_name}')
    if res:
        settings.CURRENT_SAVE = save_name
    return res

# Saving
def save_json(json_obj, filename):
    json_str = json.dumps(json_obj, indent=4)

    file = open(filename, 'w')
    file.write(json_str)
    file.close()

def save_recipes(filename):
    json_recipes = []
    for recipe in [obj for obj in settings.RECIPES if isinstance(obj, objs.Recipe)]:
        json_recipe = {}

        json_recipe['outputs'] = []
        for r_output in recipe.r_outputs:
            json_recipe['outputs'].append({
                'name' : r_output.name,
                'amount' : r_output.amount
            })
        
        json_recipe['tool'] = {
            'name' : recipe.tool.name,
            'level' : recipe.tool.level
        }

        json_recipe['inputs'] = []
        for r_input in recipe.r_inputs:
            json_recipe['inputs'].append({
                'name' : r_input.name,
                'amount' : r_input.amount
            })
        
        json_recipes.append(json_recipe)
    save_json(json_recipes, filename)

def save_tool_recipes(filename):
    json_recipes = []
    for recipe in [obj for obj in settings.RECIPES if isinstance(obj, objs.Tool_Recipe)]:
        json_recipe = {}

        json_recipe['output'] = {
            'name' : recipe.r_output.name,
            'level' : recipe.r_output.level
        }
        
        json_recipe['tool'] = {
            'name' : recipe.tool.name,
            'level' : recipe.tool.level
        }

        json_recipe['inputs'] = []
        for r_input in recipe.r_inputs:
            json_recipe['inputs'].append({
                'name' : r_input.name,
                'amount' : r_input.amount
            })
        
        json_recipes.append(json_recipe)
    save_json(json_recipes, filename)

def save_inv(filename):
    json_inv = {
        'items'  : [],
        'tools'  : [],
        'checks' : []
    }

    for item in settings.INV.items:
        json_inv['items'].append({
            'name' : item.name,
            'amount' : item.amount
        })

    for tool in settings.INV.tools:
        json_inv['tools'].append({
            'name' : tool.name,
            'level' : tool.level
        })
    
    for check in settings.INV.checks:
        json_inv['checks'].append(check)
    
    save_json(json_inv, filename)

def save_all(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    
    recipe_path = dirname + '/recipes.json'
    tool_recipe_path = dirname + '/tool_recipes.json'
    inv_path = dirname + '/inv.json'

    save_recipes(recipe_path)
    save_tool_recipes(tool_recipe_path)
    save_inv(inv_path)
    
    settings.UNSAVED_CHANGES = False
    print(colors.GREEN('Progress saved.'))

def usr_save():
    if settings.CURRENT_SAVE:
        save_all(f'{settings.SAVE_DIR}/{settings.CURRENT_SAVE}')
    else:
        while True:
            print('Enter a name for your save progress: ', end='')
            raw_input = input()
            usr_input = str.title(raw_input)

            if os.path.exists(f'{settings.SAVE_DIR}/{usr_input}'):
                print(colors.YELLOW(f'Warning: \'{raw_input}\' exists. Choose another location to save.'))
            else:
                settings.CURRENT_SAVE = usr_input
                save_all(f'{settings.SAVE_DIR}/{settings.CURRENT_SAVE}')
                break
