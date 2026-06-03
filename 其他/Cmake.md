1. CMake概述
CMake 是一个项目构建工具，并且是跨平台的。关于项目构建我们所熟知的还有Makefile（通过 make 命令进行项目的构建），大多是IDE软件都集成了make，比如：VS 的 nmake、linux 下的 GNU make、Qt 的 qmake等，如果自己动手写 makefile，会发现，makefile 通常依赖于当前的编译平台，而且编写 makefile 的工作量比较大，解决依赖关系时也容易出错。

而 CMake 恰好能解决上述问题， 其允许开发者指定整个工程的编译流程，在根据编译平台，自动生成本地化的Makefile和工程文件，最后用户只需make编译即可，所以可以把CMake看成一款自动生成 Makefile的工具，其编译流程如下图：



预处理器 - 把头文件展开，注释，宏

编译器 进行编译 GCC G++ 得到汇编文件

通过汇编器 得到二进制文件 .obj / .o

通过链接 得到一个二进制文件 可执行文件 .exe



* Cmake不依赖平台 

![image-20251224205912482](C:\Users\LYX10\AppData\Roaming\Typora\typora-user-images\image-20251224205912482.png)

