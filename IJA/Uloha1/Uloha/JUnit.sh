
# Ukazka prekladu a spusteni

PWD=`pwd`
SRC="src"
LIB="lib"

JUNIT="junit-platform-console-standalone-1.6.0.jar"

rm -rf build
mkdir build

#javac -classpath ${SRC}:${LIB}/junit.jar:ija2020-ukol1.jar -d build ${SRC}/ija/ija2020/homework1/Homework1Test.java
javac -classpath ${SRC}:${LIB}/${JUNIT} -d build ${SRC}/ija/homework1/IJAHomework1Test.java

#java -cp build:${LIB}/junit.jar:ija2020-ukol1.jar org.junit.runner.JUnitCore ija.ija2020.homework1.Homework1Test
java -cp build:${LIB}/${JUNIT} org.junit.runner.JUnitCore ija.homework1.IJAHomework1Test

