class CommandDescriptor:
    """
    Tokenized wrapper of a parsed command.
    Every command must consist of the command itself and an unlimited number of arguments, separated by spaces.
    """
    def __init__(self, raw_input: str):

        command_tokens = str(raw_input).split(" ")
        self.command = str(command_tokens[0]).lower()

        if len(command_tokens) > 1:
            self.arguments = command_tokens[1:len(command_tokens)]
        else:
            self.arguments = []

    def __repr__(self):
        return "cmd={0};args={1}".format(self.command, self.arguments)
