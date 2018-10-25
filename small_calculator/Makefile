TOPLEVEL_LANG ?= verilog

PWD=$(shell pwd)
#COCOTB=~/cocotb

WPWD=$(shell pwd)
PYTHONPATH := $(WPWD)/../model:$(PYTHONPATH)

VERILOG_SOURCES = $(WPWD)/../../Design/small_calculator/alu.v
VERILOG_SOURCES += $(WPWD)/../../Design/small_calculator/mux2.v
VERILOG_SOURCES += $(WPWD)/../../Design/small_calculator/mux4.v
VERILOG_SOURCES += $(WPWD)/../../Design/small_calculator/register_file.v
VERILOG_SOURCES += $(WPWD)/../../Design/small_calculator/small_calculator_cu.v
VERILOG_SOURCES += $(WPWD)/../../Design/small_calculator/small_calculator_dp.v
VERILOG_SOURCES += $(WPWD)/../../Design/small_calculator/small_calculator.v

TOPLEVEL := small_calculator
MODULE   := test_small_calculator

include $(COCOTB)/makefiles/Makefile.inc
include $(COCOTB)/makefiles/Makefile.sim
