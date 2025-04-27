import sys

class MNT_Tuple:
    def __init__(self, name, index):
        self.Name = name
        self.Index = index

    def __str__(self):
        return f"[{self.Name}, {self.Index}]"

class MacroProcessor:
    MNT = []
    MDT = []
    MNT_Counter = 0
    MDT_Counter = 0
    MDT_P = 0
    ALA = []
    ALA_MacroBinding = {}

    @staticmethod
    def initializeTables():
        MacroProcessor.MNT = []
        MacroProcessor.MDT = []
        MacroProcessor.MNT_Counter = 0
        MacroProcessor.MDT_Counter = 0
        MacroProcessor.ALA = []
        MacroProcessor.ALA_MacroBinding = {}

    @staticmethod
    def main():
        MacroProcessor.initializeTables()
        print("===== PASS 1 =====\n")
        MacroProcessor.Pass1()
        print("\n===== PASS 2 =====\n")
        MacroProcessor.Pass2()

    @staticmethod
    def Pass1():
        with open('Input.txt', 'r') as Input, open('OutputPass1.txt', 'w') as output:
            for s in Input:
                s = s.strip()
                if s.upper() == "MACRO":
                    MacroProcessor.processMacroDefinition()
                else:
                    output.write(s + '\n')

        print("ALA:")
        MacroProcessor.ShowALA(1)
        print("\nMNT:")
        MacroProcessor.ShowMNT()
        print("\nMDT:")
        MacroProcessor.ShowMDT()

    @staticmethod
    def processMacroDefinition():
        with open('Input.txt', 'r') as inp:
            lines = inp.readlines()

        current_line_idx = 0
        for idx, line in enumerate(lines):
            if line.strip().upper() == "MACRO":
                current_line_idx = idx + 1
                break

        s = lines[current_line_idx].strip()
        macro_name = s.split()[0]
        MacroProcessor.MNT.append(MNT_Tuple(macro_name, MacroProcessor.MDT_Counter))
        MacroProcessor.MNT_Counter += 1
        MacroProcessor.Pass1ALA(s)
        tokens = s.replace(',', ' ').split()
        x = tokens[0].ljust(12)
        for token in tokens[1:]:
            x += token if ',' in token else ',' + token
        MacroProcessor.MDT.append(x)
        MacroProcessor.MDT_Counter += 1
        MacroProcessor.AddIntoMDT(len(MacroProcessor.ALA) - 1, lines[current_line_idx+1:])

    @staticmethod
    def Pass1ALA(s):
        tokens = s.replace(',', ' ').split()
        MacroName = tokens[0]
        l = []
        for x in tokens[1:]:
            if '=' in x:
                x = x[:x.index('=')]
            l.append(x)
        MacroProcessor.ALA.append(l)
        MacroProcessor.ALA_MacroBinding[MacroName] = len(MacroProcessor.ALA_MacroBinding)

    @staticmethod
    def AddIntoMDT(ALA_Number, remaining_lines):
        l = MacroProcessor.ALA[ALA_Number]
        for s in remaining_lines:
            s = s.strip()
            if s.upper() == "MEND":
                MacroProcessor.MDT.append("MEND")
                MacroProcessor.MDT_Counter += 1
                break
            tokens = s.replace(',', ' ').split()
            Line = tokens[0].ljust(12)
            for token in tokens[1:]:
                if token.startswith("&"):
                    idx = l.index(token)
                    token = ",#" + str(idx)
                else:
                    token = "," + token
                Line += token
            MacroProcessor.MDT.append(Line)
            MacroProcessor.MDT_Counter += 1

    @staticmethod
    def ShowALA(Pass):
        with open(f'OutputALA_Pass{Pass}.txt', 'w') as out:
            for l in MacroProcessor.ALA:
                print(l)
                out.write(str(l) + '\n')

    @staticmethod
    def ShowMNT():
        with open('OutputMNT.txt', 'w') as out:
            for l in MacroProcessor.MNT:
                print(l)
                out.write(str(l) + '\n')

    @staticmethod
    def ShowMDT():
        with open('OutputMDT.txt', 'w') as out:
            for l in MacroProcessor.MDT:
                print(l)
                out.write(l + '\n')

    @staticmethod
    def Pass2():
        with open('OutputPass1.txt', 'r') as Input, open('OutputPass2.txt', 'w') as output:
            for s in Input:
                s = s.strip()
                tokens = s.split()
                i = 0
                while i < len(tokens):
                    Token = tokens[i]
                    if len(tokens) > 2:
                        i += 1
                        Token = tokens[i]
                    x = None
                    for m in MacroProcessor.MNT:
                        if m.Name.lower() == Token.lower():
                            x = m
                            break
                    if x:
                        MacroProcessor.MDT_P = x.Index
                        l = MacroProcessor.Pass2ALA(s)
                        MacroProcessor.MDT_P += 1
                        temp = ""
                        while MacroProcessor.MDT_P < len(MacroProcessor.MDT) and (temp := MacroProcessor.MDT[MacroProcessor.MDT_P].strip()) != "MEND":
                            tokens2 = temp.replace(',', ' ').split()
                            Line = " " * 12
                            opcode = tokens2[0]
                            Line += opcode
                            Line += " " * (24 - len(Line))
                            operand = tokens2[1]
                            if "#" in operand:
                                idx = int(operand.replace("#", ""))
                                Line += l[idx]
                            else:
                                Line += operand
                            for operand in tokens2[2:]:
                                if "#" in operand:
                                    idx = int(operand.replace("#", ""))
                                    Line += "," + l[idx]
                                else:
                                    Line += "," + operand
                            MacroProcessor.MDT_P += 1
                            output.write(Line + '\n')
                            print(Line)
                        break
                    else:
                        output.write(s + '\n')
                        print(s)
                        break
                    i += 1
        print("\nALA:")
        MacroProcessor.ShowALA(2)

    @staticmethod
    def Pass2ALA(s):
        tokens = s.split()
        MacroName = tokens[0]
        ALA_No = MacroProcessor.ALA_MacroBinding.get(MacroName, 0)
        l = MacroProcessor.ALA[ALA_No][:]
        try:
            actual_params = tokens[1].split(',')
            for idx, val in enumerate(actual_params):
                l[idx] = val
        except Exception:
            pass

        return l

if __name__ == "__main__":
    MacroProcessor.main()
