module ccu(
    input wire [3:0] data_in,   // 4-bit input data (plaintext)
    input wire [3:0] key,       // 4-bit key for encryption
    input wire clk,             // Clock signal
    input wire reset,           // Reset signal
    output wire [3:0] data_out1 // 4-bit output data (ciphertext with key1)
    
);

    reg [3:0] key1, key2, key3;
    reg [3:0] ciphered_data;

    // Function to derive keys from the original key using simple XOR and rotations
    // Key derivation example: Rotate key and XOR with constants
    always @(*) begin
        key1 = key;                // First key is the original key
        key2 = {key[2:0], key[3]}; // Rotate left by 1 bit
        key3 = key ^ 4'b1010;      // XOR with a constant value (for example, 1010)
    end

    // Process the input data on the rising edge of the clock
    always @(posedge clk or posedge reset) begin
        if (reset) begin
            ciphered_data <= 4'b0000;  // Reset to 0 when reset signal is high
            
        end else begin
            // Encrypt the data using the derived keys
          	ciphered_data <= ((data_in ^ key1)^ key2)^ key3;  // XOR with key1
            
        end
    end

    // Output the ciphered data
    assign data_out1 = ciphered_data;

endmodule

