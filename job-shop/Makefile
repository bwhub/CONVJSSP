JOB-SHOP= job-shop-baseline job-shop-naive job-shop-hybrid-baseline-jump-half-naive job-shop-hybrid-baseline-jump-half-exhaustive-search job-shop-hybrid-baseline-jump-std-naive job-shop-hybrid-baseline-jump-std-exhaustive-search

CXXFLAGS= -I/usr/local/include/ -I /usr/include/qt4/ -std=c++11
LDFLAGS= -L /usr/local/lib/ -L /usr/lib/x86_64-linux-gnu/

all: ${JOB-SHOP}

${JOB-SHOP}: %: %.o
	# ${CXX} ${LDFLAGS} $^ -o $@ -lgecodedriver -lgecodegist -lgecodesearch -lgecodeminimodel -lgecodeset -lgecodeint -lgecodekernel -lgecodesupport
	${CXX} ${LDFLAGS} $^ -o $@ -lgecodedriver -lgecodesearch -lgecodeminimodel -lgecodeset -lgecodeint -lgecodekernel -lgecodesupport

%.o: %.cpp
	${CXX} ${CXXFLAGS} -c -o $@ $^

clean:
	${RM} -f  ${JOB-SHOP} *.o
