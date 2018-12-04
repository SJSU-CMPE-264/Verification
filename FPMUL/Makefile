CWD=$(shell pwd)
COCOTB=/home/vagrant/cocotb

TOPLEVEL_LANG ?=verilog
EXTRA_OPTS = -v
TOPLEVEL=FPMUL
MODULE=FPMUL_TB

.PHONY : group-awesome-sources group-awesome group-one-sources group-one requirements

requirements: 
	pip install -r requirements.txt

#####################
### GROUP AWESOME ###
#####################
GA=../group-awesome
GA_SOURCES = $(GA)/FPMul.v $(GA)/Mul.v $(GA)/Components.v $(GA)/AuxFlagGen.v

group-awesome-sources: 
	$(eval export VERILOG_SOURCES=$(GA_SOURCES))

group-awesome: | requirements clean group-awesome-sources sim


###############
### GROUP 1 ###
###############
GONE=../group-1
GONE_SOURCES = $(GONE)/FPMul.v $(GONE)/Mul.v $(GONE)/Components.v $(GONE)/AuxFlagGen.v

group-one-sources: 
	$(eval export VERILOG_SOURCES=$(GA_SOURCES))

group-one: | requirements clean group-one-sources sim


include $(COCOTB)/makefiles/Makefile.inc
include $(COCOTB)/makefiles/Makefile.sim

# list all required Python files here
sim: FPMUL_TB.py FPMUL_Driver.py FPMUL_Generator.py FPMUL_InputMonitor.py \
FPMUL_OutputMonitor.py FPMUL_Scoreboard.py IEEE754.py
