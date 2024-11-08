# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer

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

    # Assuming data_x and data_y are provided (you need to initialize them)
    data_x = 0xFFFFFFFF  # Example data, replace with actual values
    data_y = 0xAAAAAAAA  # Example data, replace with actual values

    # Iterate over input bits in steps of 4
    for i in range(0, 32, 4):
        # Load 4 bits of data_x and data_y
        dut.ui_in[0].value = (data_x >> i) & 1
        dut.ui_in[1].value = (data_x >> (i + 1)) & 1
        dut.ui_in[2].value = (data_x >> (i + 2)) & 1
        dut.ui_in[3].value = (data_x >> (i + 3)) & 1

        dut.ui_in[4].value = (data_y >> i) & 1
        dut.ui_in[5].value = (data_y >> (i + 1)) & 1
        dut.ui_in[6].value = (data_y >> (i + 2)) & 1
        dut.ui_in[7].value = (data_y >> (i + 3)) & 1

        # Wait for the values to be processed
        await Timer(40, units="ns")

        # Deassert the load signal
        dut.ui_in[2].value = 0
        await Timer(40, units="ns")

        # Assert and deassert init signal
        dut.ui_in[3].value = 1
        await Timer(40, units="ns")
        dut.ui_in[3].value = 0
        await Timer(140, units="ns")

    dut._log.info("Test completed successfully")

    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.
