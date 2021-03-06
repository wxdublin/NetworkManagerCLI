######################################################################
# Makefile to control the confD daemon, the Mininet topology, etc
#
#
# See the README files for more information
######################################################################

usage:
	@echo "See README files for more instructions"
	@echo "make all     Build all example files"
	@echo "make clean   Remove all built and intermediary files"
	@echo "make start   Start CONFD daemon and example agent"
	@echo "make stop    Stop any CONFD daemon and example agent"
	@echo "make netconf-mininet	start mininet"
	@echo "make netconf-fibbing	start netconf fibbing"



######################################################################
# Where is ConfD installed? Make sure CONFD_DIR points it out
# CONFD_DIR = /Thesis/confd
CONFD_DIR = ../../confd
# Include standard ConfD build definitions and rules
include $(CONFD_DIR)/src/confd/build/include.mk

# In case CONFD_DIR is not set (correctly), this rule will trigger
$(CONFD_DIR)/src/confd/build/include.mk:
	@echo 'Where is ConfD installed? Set $$CONFD_DIR to point it out!'
	@echo ''

######################################################################
# Example specific definitions and rules

CONFD_FLAGS = --addloadpath $(CONFD_DIR)/etc/confd
# START_FLAGS=0 for normal condition,
#START_FLAGS=1 for debugging
START_FLAGS = 1
MAXREQ = 1000
MAXREQSIZE = 1014

SRC	= segmentrouting.c
OBJS	= $(SRC:.c=.o)

all:  segmentrouting.fxs segmentrouting.h segmentrouting_conf commands-j.ccl commands-c.ccl \
		$(CDB_DIR) ssh-keydir
	@echo "Build complete"


######################################################################
segmentrouting_conf.o: segmentrouting.h
segmentrouting_conf: $(OBJS)
	$(CC) -o $@ $(OBJS) $(LIBS)



######################################################################
clean:	iclean
	-rm -rf segmentrouting.h segmentrouting_conf fibbing.conf segmentrouting.conf *_ns.py *.pyc 2> /dev/null || true

######################################################################
start:  stop start_confd start_subscriber

start_confd:
	$(CONFD) -c confd.conf $(CONFD_FLAGS)

start_subscriber:
	### * In one terminal window, run: tail -f ./confd.log
	### * In another terminal window, run queries
	###   (try 'make query' for an example)
	### * In this window, the DHCP confd daemon now starts:
	###   (hit Enter to exit)
	./segmentrouting_conf $(MAXREQ) $(MAXREQSIZE) $(START_FLAGS)


######################################################################
stop:
	### Killing any confd daemon or confd agents
	$(CONFD) --stop    || true
	$(KILLALL) segmentrouting_conf || true

######################################################################
cli:
	$(CONFD_DIR)/bin/confd_cli --user=admin --groups=admin \
		--interactive || echo Exit

######################################################################

abilene-topo:
	$(CONFD_DIR)/bin/netconf-console ../netconf/abilene/topo.xml

abilene-requirement:
	$(CONFD_DIR)/bin/netconf-console ../netconf/abilene/requirement.xml
