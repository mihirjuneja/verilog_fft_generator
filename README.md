# 512-Point DIF FFT (Radix-2) 

## Objective

Design a 512-point Decimation-In-Frequency (DIF) FFT using the Radix-2 algorithm for a **Speech Processing for Machine Learning** application. All Verilog code is written using synthesizable constructs.

---

## System Design

The **Decimation-In-Frequency (DIF) Fast Fourier Transform (FFT)** with Radix-2 is an efficient algorithm for computing the Discrete Fourier Transform (DFT) of a sequence. It employs a divide-and-conquer approach, recursively breaking down an N-point DFT into smaller DFTs. Radix-2 implies that the FFT processes input sizes where **N is a power of 2**, dividing the input into sub-sequences at each stage.

In an N-point Radix-2 DIF FFT, there are **log₂(N)** stages. The input sequence remains in **normal order**, and butterfly computations are applied at each stage. Each butterfly operates on a pair of inputs and uses **twiddle factors** of the form:


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

Validation was done by comparing Verilog outputs to a Python-based FFT implementation, verified via:

[FFT Calculator (SciStatCalc)](https://scistatcalc.blogspot.com/2013/12/fft-calculator.html)

Example input:  
