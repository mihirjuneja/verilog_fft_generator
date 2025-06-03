# 512-Point DIF FFT (Radix-2) 

## Objective

Design a 512-point Decimation-In-Frequency (DIF) FFT using the Radix-2 algorithm for a **Speech Processing for Machine Learning** application. All Verilog code is written using synthesizable constructs.

---

## System Design

The **Decimation-In-Frequency (DIF) Fast Fourier Transform (FFT)** with Radix-2 is an efficient algorithm for computing the Discrete Fourier Transform (DFT) of a sequence. It employs a divide-and-conquer approach, recursively breaking down an N-point DFT into smaller DFTs. Radix-2 implies that the FFT processes input sizes where **N is a power of 2**, dividing the input into sub-sequences at each stage.

In an N-point Radix-2 DIF FFT, there are **log₂(N)** stages. The input sequence remains in **normal order**, and butterfly computations are applied at each stage. Each butterfly operates on a pair of inputs and uses **twiddle factors** of the form:

