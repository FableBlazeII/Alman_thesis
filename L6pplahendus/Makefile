MANAGER = MotSum_manager
SUBMIT = MotSum_submit

CFLAGS = -O3

all: $(MANAGER) $(SUBMIT)

$(MANAGER): MotSum_manager.o
	$(CXX) MotSum_manager.o -lsqlite3 -o $(MANAGER)

MotSum_manager.o: MotSum_manager.cpp
	$(CXX) -c MotSum_manager.cpp -o MotSum_manager.o $(CFLAGS)

$(SUBMIT): MotSum_submit.o
	$(CXX) MotSum_submit.o -lsqlite3 -o $(SUBMIT)

MotSum_submit.o: MotSum_submit.cpp
	$(CXX) -c MotSum_submit.cpp -o MotSum_submit.o $(CFLAGS)

clean:
	rm *.o MotSum_submit MotSum_manager
