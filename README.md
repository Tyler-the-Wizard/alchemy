# alchemy

A command-line alchemical crafting simulator.

### Command documentation

* `help`, `?`

    Display a list of all commands recognized by the program.

* `save`

    Save your progress to the `saves` directory, prompting you to create a folder there if you don't have one yet.

* `load FOLDER`

    Load progress from a folder in the `saves` directory. You can also supply the name of the folder on the command line.

* `inv`, `i`

    Display all items you own.

* `tools`, `t`

    Display all tools you own.

* `machines`, `m`

    Display all machines you own.

* `toss`

    Not implemented yet!

* `use TOOL`

    Use the given tool to attempt to craft something. At the prompt, type all items you wish to use, followed by a number to specify how many times you want the craft to be executed. Omit the number to execute as many as you can. (Each tool has a limit based on its level.) Enter an empty string to display all valid recipes.

* `auto`

    Not implemented yet!

* `exit`, `quit`, `q`

    Exit the program. This will automatically save your unsaved changes.