CWD=$(shell pwd)
COCOTB=/home/vagrant/cocotb

TOPLEVEL_LANG ?=verilog

# VERILOG_SOURCES = $(wildcard $(WPWD)/../../Design/FPMUL/FPMUL.v)
# VERILOG_SOURCES = /home/vagrant/code/Design/FPMUL/FPMUL.v
VERILOG_SOURCES = /home/vagrant/Verification/FPMUL/FPMUL_dummy.v

TOPLEVEL=FPMUL
MODULE=FPMUL_TB

include $(COCOTB)/makefiles/Makefile.inc
include $(COCOTB)/makefiles/Makefile.sim

# list all required Python files here
sim: FPMUL_TB.py FPMUL_Driver.py FPMUL_Generator.py FPMUL_InputMonitor.py \
FPMUL_OutputMonitor.py FPMUL_Scoreboard.py IEEE754.py
