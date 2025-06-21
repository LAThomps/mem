#!/home/lthomps/lin_lat/bin/python

import subprocess 
import sys 
import psutil

def main():
    # run ps aux and capture output, raise error if on non-POSIX system
    ps_aux = subprocess.run(["ps aux"], shell=True, capture_output=True)
    if ps_aux.returncode != 0:
        raise SystemError(
"Non-POSIX system detected, only run on systems where 'ps aux' is a valid command"
        )
    
    # convert output to str, split by line
    ps_aux_out = ps_aux.stdout.decode("ascii")
    parts = ps_aux_out.split("\n")

    # if more than one command arg, sum process matches
    match_strs = [[val, 0] for val in sys.argv[1:]]

    # keep running total and ram available for final calcs
    total = 0
    total_sys_ram = int(psutil.virtual_memory().total / (1024 ** 2))

    # parse ps aux output
    for part in parts[1:-1]:
        line = part.split()
        line = line[:10] + [" ".join(line[10:])] # left all cols on here for future use
        mem_val = int(line[5]) # mem usage in KB
        if match_strs:
            for i, match in enumerate(match_strs):
                if match[0] in line[-1]: # command col
                    match_strs[i][1] += mem_val
        total += mem_val
    
    # add to final output string if user inputs
    if match_strs:
        match_str_final = "\n".join([
            f"{match}:\t\t{int(val/1024)} MB ({(val/1024)/total_sys_ram:.1%})" 
            for match, val in match_strs
        ]) + "\n"
    
    # print final output
    ram_in_use = int(total/1024)
    print(f"""
RAM In Use:\t{ram_in_use} MB ({ram_in_use/total_sys_ram:.1%})
{match_str_final if match_strs else ''}
RAM Free:\t{total_sys_ram - ram_in_use} MB
Total RAM:\t{total_sys_ram} MB
    """.strip())
    return 

if __name__ == "__main__":
    main()