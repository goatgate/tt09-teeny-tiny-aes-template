# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, Timer

# Parameters
CLOCK_PERIOD_NS = 40  # Clock period in ns (25 MHz)
RESET_CYCLES = 2
D_W = 4  # Data width (4-bit input data and key)

@cocotb.test()
async def test_tt_um_ccu_goatgate(dut):
    # Initialize clock
    dut._log.info("Starting the clock")
    clock = Clock(dut.clk, CLOCK_PERIOD_NS, units="ns")
    cocotb.start_soon(clock.start())

    # Reset the DUT
    dut._log.info("Applying reset")
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, RESET_CYCLES)
    dut.rst_n.value = 1

    # Initialize inputs
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    # Test Case 1: Encrypt with key = 4'b1011 and data_in = 4'b1101
    dut.ui_in.value = 0b1101 | (0b1011 << D_W)
    dut._log.info("Test Case 1: data_in = 4'b1101, key = 4'b1011")
    await RisingEdge(dut.clk)
    await Timer(40, units="ns")
    assert dut.uo_out.value == 0b0110, f"Test Case 1 failed: Expected 0b0110, got {dut.uo_out.value}"

    # Test Case 2: Encrypt with key = 4'b0110 and data_in = 4'b0011
    dut.ui_in.value = 0b0011 | (0b0110 << D_W)
    dut._log.info("Test Case 2: data_in = 4'b0011, key = 4'b0110")
    await RisingEdge(dut.clk)
    await Timer(40, units="ns")
    assert dut.uo_out.value == 0b0101, f"Test Case 2 failed: Expected 0b0101, got {dut.uo_out.value}"

    # Test Case 3: Encrypt with key = 4'b1111 and data_in = 4'b0001
    dut.ui_in.value = 0b0001 | (0b1111 << D_W)
    dut._log.info("Test Case 3: data_in = 4'b0001, key = 4'b1111")
    await RisingEdge(dut.clk)
    await Timer(40, units="ns")
    assert dut.uo_out.value == 0b1110, f"Test Case 3 failed: Expected 0b1110, got {dut.uo_out.value}"

    # Test Case 4: Encrypt with key = 4'b1000 and data_in = 4'b0110
    dut.ui_in.value = 0b0110 | (0b1000 << D_W)
    dut._log.info("Test Case 4: data_in = 4'b0110, key = 4'b1000")
    await RisingEdge(dut.clk)
    await Timer(40, units="ns")
    assert dut.uo_out.value == 0b1110, f"Test Case 4 failed: Expected 0b1110, got {dut.uo_out.value}"

    dut._log.info("All test cases passed successfully")


    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.
