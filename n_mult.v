module n_mult(
    input signed [15:0] A,
    input signed [15:0] B,
    output reg signed [31:0] product
);
    reg signed [31:0] multiplicand;
    reg signed [31:0] multiplier;
    reg [4:0] count;  // Update the count width to handle up to 16 bits
    reg sign_A, sign_B;

    always @(*) begin
        product = 0;

        // Prepare the multiplicand and multiplier
        multiplicand = A; // The value to be multiplied
        multiplier = B;   // The value to multiply by

        // Extract sign bits
        sign_A = A[15]; // Sign bit of A
        sign_B = B[15]; // Sign bit of B

        // If the multiplier is negative, take its two's complement
        if (sign_B) begin
            multiplier = ~multiplier + 1; // Negate multiplier
        end

        // If the multiplicand is negative, take its two's complement
        if (sign_A) begin
            multiplicand = ~multiplicand + 1; // Negate multiplicand
        end

        // Perform shift-and-add multiplication
        for (count = 0; count < 16; count = count + 1) begin
            if (multiplier[count]) begin
                product = product + (multiplicand << count);
            end
        end

        // If the original signs of A and B are different, negate the product
        if (sign_A ^ sign_B) begin
            product = ~product + 1; // Two's complement to negate
        end
    end
endmodule
