from src import game_logic, objs, settings

def run(recipe):
    name = ''
    if isinstance(recipe, objs.Recipe):
        name = recipe.r_outputs[0].name
    elif isinstance(recipe, objs.Tool_Recipe):
        name = recipe.r_output.name

    if settings.INV.validate(recipe):
        settings.INV.run(recipe)
        game_logic.check(name)
        return True

def parse_inputs(raw_input):
    inputs = str.title(raw_input).split()
    num_times = None
    if inputs[-1].isdigit():
        num_times = int(inputs[-1])
        inputs = inputs[:-1]
    
    return inputs, num_times

def max_from_level(level):
    return (level + 1) * 8

def search(tool, raw_input):
    """Returns a list of all recipes
    that can be ran at this time"""
    input_names, num_times = parse_inputs(raw_input)

    max_times = max_from_level(tool.level)
    if num_times:
        num_times = min(num_times, max_times)
    else:
        num_times = max_times

    found = []
    for recipe in settings.RECIPES:
        if recipe.tool.name == tool.name\
        and recipe.tool.level <= tool.level:
            recipe_is_valid = True
            for r_input in recipe.r_inputs:
                for input_name in input_names:
                    if r_input.name == input_name:
                        break
                else:
                    # This recipe ingredient was not found in the user input
                    recipe_is_valid = False

            if not recipe_is_valid:
                continue
            
            if settings.INV.validate(recipe):
                found.append(recipe)

    return found, num_times