/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_ccu_goatgate (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  // All output pins must be assigned. If not used, assign to 0.
    assign uo_out[3:0] = dout;
    assign uo_out[7:4] = 0;
    assign uio_out = 0;
    assign uio_oe  = 0;
    
    // I/O definitions
    wire [3:0] din = ui_in[3:0];
    wire [3:0] kin = ui_in[7:4];
    wire [3:0] dout;
    
  // List all unused inputs to prevent warnings
  wire _unused = &{ena, 1'b0};
  ccu ccu_inst (
                          .clk(clk),
                          .reset(rst_n),
                          .data_in(din),
                          .key(kin),
                          .data_out1(dout)
                          
                       );
endmodule
