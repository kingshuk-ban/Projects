# Makefile to compile the applications

INCL=-I../datafile -I../common -I../linear_model -I../neural_network
GCC =/usr/bin/g++
CFLAGS =$(INCL) -std=c++11

ODIR=obj
LDIR =../lib

BDIR = ./bin

LIBS=-lm -lstdc++

_DEPS = 
DEPS = $(patsubst %,$(IDIR)/%,$(_DEPS))

_OBJ = test_datafile.o test_boston_lr.o test_pima_indians_diabetes.o test_seeds_dataset.o
OBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))

$(ODIR)/%.o: %.cpp
	$(GCC) -c -o $@ $< $(CFLAGS)

test_datafile: $(ODIR)/test_datafile.o
	$(GCC) -o $@ $< $(CFLAGS) $(LIBS)

test_boston_lr: $(ODIR)/test_boston_lr.o
	$(GCC) -o $@ $< $(CFLAGS) $(LIBS)

test_diabetes_lr: $(ODIR)/test_diabetes_lr.o
	$(GCC) -o $@ $< $(CFLAGS) $(LIBS)

test_seeds_neural_network: $(ODIR)/test_seeds_neural_network.o
	$(GCC) -o $@ $< $(CFLAGS) $(LIBS)

all: test_datafile test_boston_lr test_diabetes_lr test_seeds_neural_network

.PHONY: clean

clean:
	rm -f $(ODIR)/*.o *~ core $(INCDIR)/*~ test_datafile test_boston_lr test_diabetes_lr test_seeds_neural_network

