from src import colors, disk, settings

triggers = {
    'Voda' : 'basics2',
}

def check(name):
    if name in triggers.keys()\
    and triggers[name] not in settings.INV.checks:
        disk.load_all(f'{settings.DATA_DIR}/{triggers[name]}')
        settings.INV.checks.append(triggers[name])
        print(colors.GREEN('Congratulations! New recipes unlocked!'))