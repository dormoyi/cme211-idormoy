CXX := g++ -O3 -std=c++11
CXXFLAGS := -Wall -Wconversion -Wextra -Wpedantic

main: main.cpp COO2CSR.cpp CGSolver.cpp
	$(CXX) $(CXXFLAGS) -o main main.cpp heat.cpp sparse.cpp CGSolver.cpp matvecops.cpp COO2CSR.cpp

.PHONY: clean
clean:
	$(RM) main
 