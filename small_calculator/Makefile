TOPLEVEL_LANG ?= verilog

PWD=$(shell pwd)
#COCOTB=~/cocotb

WPWD=$(shell pwd)
PYTHONPATH := $(WPWD)/../model:$(PYTHONPATH)

VERILOG_SOURCES = $(wildcard $(WPWD)/../../Design/small_calculator/*.v)

TOPLEVEL := small_calculator
MODULE   := test_small_calculator

include $(COCOTB)/makefiles/Makefile.inc
include $(COCOTB)/makefiles/Makefile.sim
