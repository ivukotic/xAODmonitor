RC     := root-config
ifeq ($(shell which $(RC) 2>&1 | sed -ne "s@.*/$(RC)@$(RC)@p"),$(RC))
MKARCH := $(wildcard $(shell $(RC) --etcdir)/Makefile.arch)
endif
ifneq ($(MKARCH),)
include $(MKARCH)
else
#include $(ROOTSYS)/test/Makefile.arch
endif

ALIBS = $(LIBS) -lTreePlayer

#------------------------------------------------------------------------------
INSPO       = TFileAccessTracer.o
INSPS       = TFileAccessTracer.cxx
INSP        = TFileAccessTracer

OBJS          = $(INSPO)
PROGRAMS      = $(INSP)

#------------------------------------------------------------------------------

all:            $(PROGRAMS)

$(INSP):      $(INSPO)
		$(LD) $(LDFLAGS) $^ $(ALIBS) $(OutPutOpt)$@
		$(MT_EXE)
		@echo "$@ done"
