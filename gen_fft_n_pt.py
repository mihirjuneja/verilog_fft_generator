import math as math

import numpy as np

###################################################################
#
# Function: prnt_module_header()
# Arguments: N (fft needed for N points)
# Description:
# Prints module header - module name and ports with appropriate sizes based on N
# Ports are flattened into an array of size 16*N, 16 bits being the size of each value
# Flattening is required since 1-D arrays only are synthesizable
#
###################################################################
def prnt_module_header(N):
    stage = 1
    t_str = '\nmodule auto_' + str(int(N)) + '_fft(input [0:' + str(N * 16 - 1) + '] inp_r,'
    t_str += 'input [0:' + str(N * 16 - 1) + '] inp_i,'
    t_str += 'output [0:' + str(N * 16 - 1) + '] out_r,'
    t_str += 'output [0:' + str(N * 16 - 1) + '] out_i);\n'
    print(t_str)


###################################################################
#
# Function: prnt_wires()
# Arguments: N (fft needed for N points)
# Description:
# Prints local wires with appropriate sizes based on N
# Wires are flattened into an array of size 16*N, 16 bits being the size of each value
#
###################################################################
def prnt_wires(N):
    t_str = '\twire [0:' + str(N * 16 - 1) + '] s0_out_r;\n'
    t_str += '\twire [0:' + str(N * 16 - 1) + '] s0_out_i;\n'


    stages = int(math.log2(N))  # Calculate the number of stages for N-point DIF FFT


    for stage in range(1, stages + 1):
        t_str += f'\twire [0:{N * 16 - 1}] s{stage}_out_r;\n'
        t_str += f'\twire [0:{N * 16 - 1}] s{stage}_out_i;\n'

    print(t_str)
    print('\n\tassign s0_out_r = inp_r;')
    print('\tassign s0_out_i = inp_i;\n')


###################################################################
#
# Function: generate_twiddle_wires()
# Arguments: N (fft needed for N points)
# Description:
# Prints wires which will hold values of twiddle factors with appropriate sizes based on N
# These wires are of size 16 bits, signed.
#
###################################################################

def generate_twiddle_wires(N):
    num_twiddles = N // 2  # Number of twiddles is N/2 for N-point FFT

    real_wires = ', '.join([f"w{i}_r" for i in range(num_twiddles)])
    imag_wires = ', '.join([f"w{i}_i" for i in range(num_twiddles)])

    print(f"\twire [15:0] {real_wires};")
    print(f"\twire [15:0] {imag_wires};")
    print("")  # Adds a blank line for better readability

###################################################################
#
# Function: generate_twiddle_factors()
# Arguments: N (fft needed for N points)
# Description:
# Generates Twiddle factors (TFs) based on the formula. Number of TFs is k, obtained by floor division of N by 2
# Formula gives integer values which are converted into hex, in the 8.8 format
#
###################################################################

def generate_twiddle_factors(N):
    twiddle_factors = []

    for k in range(N // 2):
        # Calculate the real and imaginary parts of the twiddle factor W_N^k
        real = np.cos(2 * np.pi * k / N)
        imag = -np.sin(2 * np.pi * k / N)

        # Convert to 8.8 fixed-point format
        real_fixed = int(np.round(real * 256))
        imag_fixed = int(np.round(imag * 256))

        # Convert to signed 16-bit hexadecimal format
        real_hex = format(real_fixed & 0xFFFF, '04X')
        imag_hex = format(imag_fixed & 0xFFFF, '04X')

        twiddle_factors.append((f"16'h{real_hex}", f"16'h{imag_hex}"))

    return twiddle_factors

###################################################################
#
# Function: print_twiddle_factors()
# Arguments: Array of reaal, imaginary pairs for all the needed TFs
# Description:
# Prints assign statements to assign TFs to the right variable names
#
###################################################################
def print_twiddle_factors(twiddle_factors):

    print('\t// Twiddle factors for all stages')

    for idx, (real, imag) in enumerate(twiddle_factors):
        print(f"\tassign w{idx}_r = {real};")
        print(f"\tassign w{idx}_i = {imag};")
        print("")  # Adds a blank line for better readability

###################################################################
#
# Function: print_bf()
# Arguments: stage - which of the log2 N stage is being printed
#            i1 & i2 - starting and ending indices of the ports for the stage for the BF
#            w_str - Name of the twiddle factor for the particular BF
# Description:
# Prints ONE instance of a butterfly module (BF).
# These instances are in groups.
#   First group has 1 set of N/2 BFs
#   Second group has 2 sets of N/4 BFs each
#   Third group has 4 sets of N/8 BFs each and so on
#
###################################################################

def prnt_bf(stage, i1, i2, w_str):
    s1 = str(i1 * 16) + ':' + str((i1 + 1) * 16 - 1)
    s2 = str(i2 * 16) + ':' + str((i2 + 1) * 16 - 1)
    ss = str(stage)
    prev = str(stage - 1)

    s = '\tbf s' + ss + '_' + str(i1)
    s += ' (.a(s' + prev + '_out_r[' + s1 + ']), .b(s' + prev + '_out_i[' + s1 + ']), '
    s += '.c(s' + prev + '_out_r[' + s2 + ']), .d(s' + prev + '_out_i[' + s2 + ']), '
    s += '.w_r(' + w_str + '_r), .w_i(' + w_str + '_i), '
    s += '.out1_r(s' + ss + '_out_r[' + s1 + ']), '
    s += '.out1_i(s' + ss + '_out_i[' + s1 + ']), '
    s += '.out2_r(s' + ss + '_out_r[' + s2 + ']), '
    s += '.out2_i(s' + ss + '_out_i[' + s2 + ']));'

    print(s)

###################################################################
#
# Function: print_all_stages()
# Arguments: N (fft needed for N points)
# Description:
# Prints instances of butterfly modules (BFs).
# These instances are in stages.
#   First stage has 1 set of N/2 BFs
#   Second stage has 2 sets of N/4 BFs each
#   Third stage has 4 sets of N/8 BFs each and so on
#
###################################################################

def prnt_all_stages(N):
    delta = int(N)

    sn = int(math.log2(N))

    for s in range(1,sn+1):
        print('\n\t//   Stage = ' + str(s))
        delta = int(delta/2)
        loops = int(2**(s-1))
        #print('stage = ' + str(s) + ' has ' + str(loops))
        j = 0

        for l in range(1,loops+1):
            #print('loop number = ' + str(l))
            for i in range(0,delta):
                #print('bf ' + str(i + j) + ' ' + str(i + j + delta) + ' twiddle = ' + str((i)*2**(s-1)))
                prnt_bf(s, i+j, i+j+delta, 'w' + str((i)*2**(s-1)))
            j = j + 2*delta

def prnt_out_assign(N):
    print('\n\tassign out_r = s' + str(int(math.log2(N))) + '_out_r;')
    print('\tassign out_i = s' + str(int(math.log2(N))) + '_out_i;')

def prnt_end():
    print('\nendmodule')

####################################################################
#######             MAIN
####################################################################
#if __name__ == "__main__":
N = 8
prnt_module_header(N)
prnt_wires(N)
generate_twiddle_wires(N)
twiddle_factors = generate_twiddle_factors(N)
print_twiddle_factors(twiddle_factors)
prnt_all_stages(N)
prnt_out_assign(N)
prnt_end()
