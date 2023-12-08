"""To test possible implementation of custom commands in the terminal."""
import json

#for example, code in cmd.json should be translated into:
"""
def cmd(x):
    y = x + 321
    return y

"""




def ObtainCommand(filename) -> dict:
    with open(filename) as f:
        return json.load(f)

Command = ObtainCommand("D:\Main\Projects\python\TkIDE\test\cmd.json")
print(Command)
code = f"def {Command['name']}({','.join(Command['request'])}):\n\t"
if Command["process"]["add"] and Command['process']["add"]:
    code += f"{Command['process']['add'][-1]} = {Command['process']['add'][0]} + {Command['process']['add'][1]}\n\t"

code += f"return {','.join(Command['return'])}"
exec(code)

print(cmd(123)) #NOTE ignore error, will work.