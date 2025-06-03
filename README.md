# 512-Point DIF FFT (Radix-2) 

## Objective

Design a 512-point Decimation-In-Frequency (DIF) FFT using the Radix-2 algorithm for a **Speech Processing for Machine Learning** application. All Verilog code is written using synthesizable constructs.

---

## System Design

The **Decimation-In-Frequency (DIF) Fast Fourier Transform (FFT)** with Radix-2 is an efficient algorithm for computing the Discrete Fourier Transform (DFT) of a sequence. It employs a divide-and-conquer approach, recursively breaking down an N-point DFT into smaller DFTs. Radix-2 implies that the FFT processes input sizes where **N is a power of 2**, dividing the input into sub-sequences at each stage.

In an N-point Radix-2 DIF FFT, there are **log₂(N)** stages. The input sequence remains in **normal order**, and butterfly computations are applied at each stage. Each butterfly operates on a pair of inputs and uses **twiddle factors**.


These are complex roots of unity used to perform the frequency-domain transformation.

At every stage, data is split into smaller blocks, and each pair of values is processed using a butterfly unit with the relevant twiddle factor. The problem size reduces by half at each stage until the transformation is complete.

The **butterfly module** takes six inputs: the real and imaginary parts of the input pair, and the real and imaginary parts of the stage-specific twiddle factor. The outputs are the combined frequency-domain values.

---

## FFT Module

- Multiplication within the butterfly is handled by a separate `n_mult` module using a shift-and-add method.
- The FFT is constructed by chaining multiple butterfly stages, with **N/2 butterflies per stage** across **log₂(N)** stages.
- **Twiddle factors** are declared as wires and reused within their corresponding stage.
- For example, a **16-point FFT** requires 4 stages with 8 butterflies per stage and 8 twiddle factors.

Temporary wires are created to store the outputs of each stage. These are then connected to the inputs of the next stage. The final stage's output is assigned to the FFT module’s output ports.

---

## Simulation and Testing

The design was tested for **4-, 8-, and 16-point** Radix-2 DIF FFTs.


All values were represented in **signed 8.8 fixed-point notation**.

---

## Discussion

### Design Challenges  
A key challenge was **managing the stage-wise data flow**, i.e., storing intermediate results correctly and passing them to the next stage. This concept is well illustrated in this video:  
DSP#47 Problem on 8-point DFT using DIF FFT — *EC Academy* (YouTube)

### Improvements  
- Twiddle factors ideally don’t require 8 integer bits, since their range is [-1, 1]. Using more fractional bits (e.g., 0.15 format) could save area and improve accuracy.

---

## Conclusion

A Python script was developed to generate synthesizable Verilog code for an **N-point DIF FFT using Radix-2**. It automatically generates all necessary stages and butterfly instances given a value of N.

Two foundational modules were written before the FFT:
1. **Multiplier module** (`n_mult`) using shift-and-add in signed 8.8 fixed-point format.
2. **Butterfly module**, which uses the multiplier to compute frequency-domain outputs.

---

## Future Work

- Explore **recursive or hierarchical FFT design**: build larger FFTs using smaller FFT cores (e.g., using two 8-point FFTs to construct a 16-point FFT).
- Investigate **resource sharing**, pipelining, or memory-optimized approaches for hardware implementation of 512-point FFTs.

Validation was done by comparing Verilog outputs to a Python-based FFT implementation, verified via:

[FFT Calculator (SciStatCalc)](https://scistatcalc.blogspot.com/2013/12/fft-calculator.html)
