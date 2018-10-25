CWD=$(shell pwd)
# COCOTB=$(CWD)/../../..

TOPLEVEL_LANG ?=verilog

VERILOG_SOURCES = $(wildcard $(WPWD)/../../Design/small_calculator/*.v)

# TOPLEVEL=dff
MODULE=$(TOPLEVEL)_cocotb

# CUSTOM_SIM_DEPS=$(CWD)/Makefile

# VSIM_ARGS=-t 1ps

include $(COCOTB)/makefiles/Makefile.inc
include $(COCOTB)/makefiles/Makefile.sim

# list all required Python files here
sim: $(MODULE).py
