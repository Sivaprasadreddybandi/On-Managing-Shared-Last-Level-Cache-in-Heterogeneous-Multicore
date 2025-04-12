# Open and read configuration file
with open("config.txt", "r") as config_file:
    config_data = config_file.read().split()

# Open and read instructions file
with open("insts.dat", "r") as instructions_file:
    instructions = instructions_file.readlines()

# Extract configuration settings
adjust_memory_offsets = config_data[3]
rename_fp_registers = config_data[7]
merge_increments = config_data[10]

# Print configuration settings
print("Configuration:")
print("  Adjust memory offsets:", adjust_memory_offsets)
print("  Rename fp registers:", rename_fp_registers)
print("  Merge increments:", merge_increments)
print()

# Print original instructions
print("Original Instructions:")
for instruction in instructions:
    print("  ", instruction.strip())

# Initialize lists for different types of instructions
list1 = []  # Instructions for cycle memory reference
list2 = []  # Instructions for FP operation
list3 = []  # Instructions for integer operation

# Process instructions based on conditions
for i in range(len(instructions) - 1):
    inst_curr = instructions[i].strip()
    inst_next = instructions[i + 1].strip()

    if inst_curr[:4] in ['fadd', 'fsub'] and inst_next[:4] in ['fadd', 'fsub']:
        list2.append(inst_curr)
        list3.append(" ")
        for _ in range(3):
            list2.append(" ")
            list3.append(" ")
    elif inst_curr[:4] in ['fadd', 'fsub'] and (inst_next[:4] in ['addi', 'andi', 'ori', 'xori', 'add', 'sub', 'and', 'xor'] or inst_next[:2] in ['or']):
        list3.append(inst_next)
    elif inst_curr[:3] == 'fld' and inst_next[:4] in ['fadd', 'fsub']:
        list1.append(inst_curr)
        list1.append(" ")
        list2.append(" ")
        list2.append(" ")
        list2.append(inst_next)
        list3.append(" ")
    elif inst_curr[:3] == 'fsd' and inst_next[:4] in ['fadd', 'fsub']:
        list1.append(inst_curr)
        list2.append(inst_next)
    elif inst_curr[:4] in ['fadd', 'fsub'] and inst_next[:3] == 'fld':
        list1.append(" ")
        list2.append(inst_curr)
    elif inst_curr[:4] in ['fadd', 'fsub'] and inst_next[:3] == 'fsd':
        for _ in range(3):
            list1.append(" ")
            list2.append(" ")
            list3.append(" ")
        list3.append(" ")

# Print formatted VLIW Instructions
print("\nVLIW Instructions")
print("{:<19}".format("Cycle memory reference"), "{:<18}".format("FP operation"), " "*6, "{:<20}".format("Integer operation"))
print("-"*5, "-"*19, "-"*18, "-"*20)

for i in range(len(list1)):
    if list2[i] != " " and list1[i] != " " and list3[i] != " ":
        print("{:>3} {:<19} {:<18} {:<20}".format(i+1, list1[i], list2[i], list3[i]))
    elif list1[i] != " " and list2[i] == " ":
        print("{:>3} {:<19} {:<18} {:<20}".format(i+1, list1[i], "", list3[i]))
    elif list2[i] != " " and list1[i] == " ":
        print("{:>3} {:<19} {:<18} {:<20}".format(i+1, "", list2[i], list3[i]))
    elif list1[i] != " " and list2[i] != " " and list3[i] == " ":
        print("{:>3} {:<19} {:<18} {:<20}".format(i+1, list1[i], "", ""))
    else:
        print("{:>3} {:<19} {:<18} {:<20}".format(i+1, "", "", list3[i]))

# Print the last instruction
p = instructions[-1][:4]
q = instructions[-2][:4]
if p in ['fsd', 'fld']:
    print("{:>3} {:<19}".format(len(instructions), instructions[-1]))
elif p in ['fadd', 'fsub'] and q not in ['fsd']:
    print("{:>3} {:<19}".format(len(instructions), " "*19 + instructions[-1]))
elif p in ['addi', 'andi', 'ori', 'xori'] and q not in ['fsd', 'fadd']:
    print("{:>3} {:<19}".format(len(instructions), " "*37 + instructions[-1]))
