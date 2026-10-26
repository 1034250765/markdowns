
## 第一个 Go 程序

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
```
运行方式有两种：直接执行（不产生二进制文件）或编译后执行。

```cmd
# 方式一：直接运行（开发调试时常用）
$ go run main.go
Hello, RUNOOB!
欢迎来到 Go 语言的世界

# 方式二：编译为二进制文件后执行（生产部署时常用）
$ go build -o hello main.go
$ ./hello
Hello, RUNOOB!
欢迎来到 Go 语言的世界
```

## Go 语言用途

Go 语言被设计成一门应用于搭载 Web 服务器，存储集群或类似用途的巨型中央服务器的系统编程语言。

对于高性能分布式系统领域而言，Go 语言无疑比大多数其它语言有着更高的开发效率。它提供了海量并行的支持，这对于游戏服务端的开发而言是再好不过了。

### 静态类型与类型推断

Go 是**静态类型**语言，所有变量类型在编译时即确定。但与 C/Java 不同的是，Go 支持类型**推断**——编译器可以自动推导变量类型，开发者无需反复声明类型名。

这种设计在保持类型安全的同时，让代码写起来像动态语言一样简洁。

```go
package main

import "fmt"

func main() {
    // 完整声明：显式指定类型
    var name string = "runoob"

    // 类型推断：编译器自动推导类型
    var version = 1.24      // 推导为 float64
    count := 100            // 短变量声明，推导为 int
    message := "Hello Go"   // 推导为 string

    // 多变量声明
    x, y := 10, 20          // 同时声明多个变量

    fmt.Println(name, version, count, message, x, y)
}
```

### 丰富的标准库

Go 的标准库覆盖了现代开发的大部分需求，无需引入第三方依赖即可完成常见任务。下表列出了最常用的标准库包：

| 包名            | 功能           | 典型用途                       |
| ------------- | ------------ | -------------------------- |
| net/http      | HTTP 客户端与服务端 | 构建 Web 服务、RESTful API      |
| encoding/json | JSON 编解码     | API 数据序列化与反序列化             |
| database/sql  | 数据库访问接口      | 配合驱动操作 MySQL、PostgreSQL 等  |
| os            | 操作系统交互       | 文件读写、环境变量、进程管理             |
| fmt           | 格式化输入输出      | 打印日志、格式化字符串                |
| sync          | 同步原语         | Mutex、WaitGroup、Once 等并发控制 |
| testing       | 测试框架         | 单元测试、基准测试、示例测试             |
| time          | 时间处理         | 计时器、定时器、时间格式化              |
| context       | 上下文传递        | 超时控制、请求取消、值传递              |
| io            | I/O 抽象       | 统一的读写接口                    |
| crypto        | 加密算法         | 哈希、对称/非对称加密、TLS            |
| flag          | 命令行参数解析      | CLI 工具开发                   |

## Go语言结构
Go 语言的基础组成有以下几个部分：

- 包声明
- 引入包
- 函数
- 变量
- 语句 & 表达式
- 注释

package main
_package main_ 定义了包名。你必须在源文件中非注释的第一行指明这个文件属于哪个包，如：package main。package main表示一个可独立执行的程序，每个 Go 应用程序都包含一个名为 main 的包。

_import "fmt"_ 告诉 Go 编译器这个程序需要使用 fmt 包（的函数，或其他元素），fmt 包实现了格式化 IO（输入/输出）的函数。

_func main()_ 是程序开始执行的函数。main 函数是每一个可执行程序所必须包含的，一般来说都是在启动后第一个执行的函数

 /*...*/ 是注释，单行注释是最常见的注释形式，你可以在任何地方使用以 // 开头的单行注释。

_fmt.Println(...)_ 可以将字符串输出到控制台，并在最后自动增加换行字符 \n。  
使用 fmt.Print("hello, world\n") 可以得到相同的结果。

当标识符（包括常量、变量、类型、函数名、结构字段等等）以一个大写字母开头，如：Group1，那么使用这种形式的标识符的对象就可以被外部包的代码所使用（客户端程序需要先导入这个包），这被称为导出（像面向对象语言中的 public）；标识符如果以小写字母开头，则对包外是不可见的。


需要注意的是 { 不能单独放在一行，所以以下代码在运行时会产生错误：

```go
package main

import "fmt"

func main()  
{  // 错误，{ 不能在单独的行上
    fmt.Println("Hello, World!")
}
```


Go 语言中使用 fmt.Sprintf 或 fmt.Printf 格式化字符串并赋值给新串

```go
package main

import (
    "fmt"
)

func main() {
   // %d 表示整型数字，%s 表示字符串
    var stockcode=123
    var enddate="2020-12-31"
    var url="Code=%d&endDate=%s"
    var target_url=fmt.Sprintf(url,stockcode,enddate)
    fmt.Println(target_url)
}
//Code=123&endDate=2020-12-31
```

## Go 语言数据类型

| 序号  | 类型和描述                                                                                                                                                                       |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **布尔型**  <br>布尔型的值只可以是常量 true 或者 false。一个简单的例子：var b bool = true。                                                                                                           |
| 2   | **数字类型**  <br>整型 int 和浮点型 float32、float64，Go 语言支持整型和浮点型数字，并且支持复数，其中位的运算采用补码。                                                                                                |
| 3   | **字符串类型:**  <br>字符串就是一串固定长度的字符连接起来的字符序列。Go 的字符串是由单个字节连接起来的。Go 语言的字符串的字节使用 UTF-8 编码标识 Unicode 文本。                                                                            |
| 4   | **派生类型:**  <br>包括：<br><br>- (a) 指针类型（Pointer）<br>- (b) 数组类型<br>- (c) 结构化类型(struct)<br>- (d) Channel 类型<br>- (e) 函数类型<br>- (f) 切片类型<br>- (g) 接口类型（interface）<br>- (h) Map 类型 |

## Go 语言变量

Go 语言变量名由字母、数字、下划线组成，其中首个字符不能为数字。

声明变量的一般形式是使用 var 关键字：

**var identifier type**

可以一次声明多个变量：

**var identifier1, identifier2 type**

// 声明一个变量并初始化  ,**根据值自行判定变量类型。**
    **var a = "RUNOOB"**

intVal := 1 相等于： 只能函数内部使用

```go
var intVal int 
intVal =1 
```

```go

//类型相同多个变量, 非全局变量
var vname1, vname2, vname3 type
vname1, vname2, vname3 = v1, v2, v3

var vname1, vname2, vname3 = v1, v2, v3 // 和 python 很像,不需要显示声明类型，自动推断

vname1, vname2, vname3 := v1, v2, v3 // 出现在 := 左侧的变量不应该是已经被声明过的，否则会导致编译错误

// 这种因式分解关键字的写法一般用于声明全局变量
var (
    vname1 v_type1
    vname2 v_type2
)
```


###  值类型和引用类型

当使用等号 `=` 将一个变量的值赋值给另一个变量时，如：`j = i`，实际上是在内存中将 i 的值进行了拷贝：

![[Pasted image 20261018184259.png]]

你可以通过 &i 来获取变量 i 的内存地址，例如：0xf840000040（每次的地址都可能不一样）。值类型变量通常存储在栈中，尤其是当它们是局部变量时。当值类型变量的值需要在函数作用域之外使用时，Go 会将其分配到堆内存中。

内存地址会根据机器的不同而有所不同，甚至相同的程序在不同的机器上执行后也会有不同的内存地址。因为每台机器可能有不同的存储器布局，并且位置分配也可能不同。

更复杂的数据通常会需要使用多个字，这些数据一般使用引用类型保存。

一个引用类型的变量 r1 存储的是 r1 的值所在的内存地址（数字），或内存地址中第一个字所在的位置。

![[Pasted image 20261018184657.png]]


这个内存地址称之为指针，这个指针实际上也被存在另外的某一个值中。

同一个引用类型的指针指向的多个字可以是在连续的内存地址中（内存布局是连续的），这也是计算效率最高的一种存储形式；也可以将这些字分散存放在内存中，每个字都指示了下一个字所在的内存地址。

## Go 语言常量

常量是一个简单值的标识符，在程序运行时，不会被修改的量。常量中的数据类型只可以是布尔型、数字型（整数型、浮点型和复数）和字符串型。

**单词释义**： `const` 是 `constant`（常量）的缩写，表示程序中不可变的值。

常量的定义格式：

```go
const identifier [type] = value
```


### iota 常量计数器

`iota` 是 Go 语言的特殊常量，也称为常量计数器。它可以在 const 声明块中自动生成递增的序列值。

**重要特性**：

- `iota` 在 `const` 关键字出现时将被重置为 0。
- const 中每新增一行常量声明，iota 自动计数加 1。
- 可以理解为 const 语句块中的行索引（从 0 开始）。
```go

package main

  

import "fmt"

  

// iota 从 0 开始，每行加 1

const (

    a = iota   // 0

    b          // 1（省略值，默认使用上一行的 iota）

    c          // 2

)

  

func main() {

    fmt.Printf("a=%d, b=%d, c=%d\n", a, b, c)

    fmt.Printf("iota = %d", iota)

}
```



- 当常量值省略时，默认使用上一行的 iota 值。
- 因此 b=1, c=2。


下表列出了Go语言的其他运算符。

|运算符|描述|实例|
|---|---|---|
|&|返回变量存储地址|&a; 将给出变量的实际地址。|
|*|指针变量。|*a; 是一个指针变量|

## Go 语言函数


Go 语言函数定义格式如下：

```go
func function_name( [parameter list] ) [return_types] {
   函数体
}
```

函数定义解析：

- func：函数由 func 开始声明
- function_name：函数名称，参数列表和返回值类型构成了函数签名。
- parameter list：参数列表，参数就像一个占位符，当函数被调用时，你可以将值传递给参数，这个值被称为实际参数。参数列表指定的是参数类型、顺序、及参数个数。参数是可选的，也就是说函数也可以不包含参数。
- return_types：返回类型，函数返回一列值。return_types 是该列值的数据类型。有些功能不需要返回值，这种情况下 return_types 不是必须的。
- 函数体：函数定义的代码集合。

以下实例为 max() 函数的代码，该函数传入两个整型参数 num1 和 num2，并返回这两个参数的最大值：

```go

/* 函数返回两个数的最大值 */
func max(num1, num2 int) int {
   /* 声明局部变量 */
   var result int

   if (num1 > num2) {
      result = num1
   } else {
      result = num2
   }
   return result 
}
```

Go 函数可以返回多个值，例如：

```go
package main

import "fmt"

func swap(x, y string) (string, string) {
   return y, x
}

func main() {
   a, b := swap("Google", "Runoob")
   fmt.Println(a, b)
}
```

### Go 语言函数引用传递值

引用传递是指在调用函数时将实际参数的地址传递到函数中，那么在函数中对参数所进行的修改，将影响到实际参数。

引用传递指针参数传递到函数内，以下是交换函数 swap() 使用了引用传递：

```go
/* 定义交换值函数*/
func swap(x *int, y *int) {
   var temp int
   temp = *x    /* 保持 x 地址上的值 */
   *x = *y      /* 将 y 值赋给 x */
   *y = temp    /* 将 temp 值赋给 y */
}
```

### Go 语言函数作为实参

Go 语言中，函数是一等公民（First-class citizen），可以像普通变量一样被赋值、传递和使用。将函数作为实参传递给另一个函数，是 Go 中常见的编程模式，常用于回调、策略模式等场景。

函数可以赋值给一个变量，通过该变量来调用函数：

```go
package main

import (
    "fmt"
    "math"
)

func main() {
    /* 将匿名函数赋值给变量 getSquareRoot */
    getSquareRoot := func(x float64) float64 {
        return math.Sqrt(x)
    }

    /* 通过变量调用函数 */
    fmt.Println(getSquareRoot(9))   // 输出：3
    fmt.Println(getSquareRoot(16))  // 输出：4
}
```

将函数作为实参传递给另一个函数时，接收方需要声明对应的函数类型参数。以下示例定义了一个 `apply` 函数，接收一个操作函数和两个操作数，对两个数执行任意指定的操作：

```go
package main

import (
    "fmt"
    "math"
)

/* 定义一个函数，接收一个函数类型的参数 op */
/* op 的类型为 func(float64, float64) float64，表示接受两个 float64 参数、返回 float64 的函数 */
func apply(op func(float64, float64) float64, a, b float64) float64 {
    return op(a, b)
}

func main() {
    /* 定义加法函数 */
    add := func(a, b float64) float64 {
        return a + b
    }

    /* 定义乘法函数 */
    multiply := func(a, b float64) float64 {
        return a * b
    }

    /* 将 add 函数作为实参传入 apply */
    fmt.Println(apply(add, 3, 4))       // 输出：7

    /* 将 multiply 函数作为实参传入 apply */
    fmt.Println(apply(multiply, 3, 4))  // 输出：12

    /* 也可以直接传入匿名函数 */
    fmt.Println(apply(func(a, b float64) float64 {
        return math.Pow(a, b) // a 的 b 次方
    }, 2, 10))                          // 输出：1024
}
```
### Go 语言函数闭包（匿名函数）
Go 语言支持匿名函数，可作为闭包。匿名函数是一个"内联"语句或表达式。匿名函数的优越性在于可以直接使用函数内的变量，不必申明。匿名函数是一种没有函数名的函数，通常用于在函数内部定义函数，或者作为函数参数进行传递。

```go
package main

import "fmt"

func getSequence() func() int {
   i:=0
   return func() int {
      i+=1
     return i  
   }
}

func main(){
   /* nextNumber 为一个函数，函数 i 为 0 */
   nextNumber := getSequence()  

   /* 调用 nextNumber 函数，i 变量自增 1 并返回 */
   fmt.Println(nextNumber())
   fmt.Println(nextNumber())
   fmt.Println(nextNumber())
   
   /* 创建新的函数 nextNumber1，并查看结果 */
   nextNumber1 := getSequence()  
   fmt.Println(nextNumber1())
   fmt.Println(nextNumber1())
}
```

## Go 语言变量作用域

在函数体内声明的变量称之为局部变量，它们的作用域只在函数体内，参数和返回值变量也是局部变量。

以下实例中 main() 函数使用了局部变量 a, b, c：

```go
package main

import "fmt"

func main() {
   /* 声明局部变量 */
   var a, b, c int 

   /* 初始化参数 */
   a = 10
   b = 20
   c = a + b

   fmt.Printf ("结果： a = %d, b = %d and c = %d\n", a, b, c)
}
```

在函数体外声明的变量称之为全局变量，全局变量可以在整个包甚至外部包（被导出后）使用。

全局变量可以在任何函数中使用，以下实例演示了如何使用全局变量：

```go
package main

import "fmt"

/* 声明全局变量 */
var g int

func main() {

   /* 声明局部变量 */
   var a, b int

   /* 初始化参数 */
   a = 10
   b = 20
   g = a + b

   fmt.Printf("结果： a = %d, b = %d and g = %d\n", a, b, g)
}
```

形式参数会作为函数的局部变量来使用。实例如下：

```go

package main

import "fmt"

/* 声明全局变量 */
var a int = 20;

func main() {
   /* main 函数中声明局部变量 */
   var a int = 10
   var b int = 20
   var c int = 0

   fmt.Printf("main()函数中 a = %d\n",  a);
   c = sum( a, b);
   fmt.Printf("main()函数中 c = %d\n",  c);
}

/* 函数定义-两数相加 */
func sum(a, b int) int {
   fmt.Printf("sum() 函数中 a = %d\n",  a);
   fmt.Printf("sum() 函数中 b = %d\n",  b);

   return a + b;
}
```

不同类型的局部和全局变量默认值为：

| 数据类型    | 初始化默认值 |
| ------- | ------ |
| int     | 0      |
| float32 | 0      |
| pointer | nil    |

## Go 语言数组

Go 语言提供了数组类型的数据结构。

数组是具有相同唯一类型的一组已编号且长度固定的数据项序列，这种类型可以是任意的原始类型例如整型、字符串或者自定义类型。

相对于去声明 **number0, number1, ..., number99** 的变量，使用数组形式 **numbers[0], numbers[1] ..., numbers[99]** 更加方便且易于扩展。

数组元素可以通过索引（位置）来读取（或者修改），索引从 0 开始，第一个元素索引为 0，第二个索引为 1，以此类推。

![[Pasted image 20261021132557.png]]

Go 语言数组声明需要指定元素类型及元素个数，语法格式如下：

```go
var arrayName [size]dataType
```
以下演示了数组初始化：

以下实例声明一个名为 numbers 的整数数组，其大小为 5，在声明时，数组中的每个元素都会根据其数据类型进行默认初始化，对于整数类型，初始值为 0。

```go
var numbers = [5]int{1, 2, 3, 4, 5}
```

在 Go 语言中，数组的大小是类型的一部分，因此不同大小的数组是不兼容的，也就是说 [5]int 和 [10]int 是不同的类型。

如果数组长度不确定，可以使用 ... 代替数组的长度，编译器会根据元素个数自行推断数组的长度：

```go
var balance = [...]float32{1000.0, 2.0, 3.4, 7.0, 50.0}
或
balance := [...]float32{1000.0, 2.0, 3.4, 7.0, 50.0}
```

如果设置了数组的长度，我们还可以通过指定下标来初始化元素：

```go
//  将索引为 1 和 3 的元素初始化
balance := [5]float32{1:2.0,3:7.0}
```

数组元素可以通过索引（位置）来读取。格式为数组名后加中括号，中括号中为索引的值。

## Go 语言指针

Go 语言中指针是很容易学习的，Go 语言中使用指针可以更简单的执行一些任务。

接下来让我们来一步步学习 Go 语言指针。

我们都知道，变量是一种使用方便的占位符，用于引用计算机内存地址。

Go 语言的取地址符是 &，放到一个变量前使用就会返回相应变量的内存地址。

以下实例演示了变量在内存中地址：

```go
package main

import "fmt"

func main() {
   var a int = 10   

   fmt.Printf("变量的地址: %x\n", &a  )
}
```

一个指针变量指向了一个值的内存地址。

类似于变量和常量，在使用指针前你需要声明指针。指针声明格式如下：

```go
var var_name *var-type
```

在指针类型前面加上 * 号（前缀）来获取指针所指向的内容。

```go
package main

import "fmt"

func main() {
   var a int= 20   /* 声明实际变量 */
   var ip *int        /* 声明指针变量 */

   ip = &a  /* 指针变量的存储地址 */

   fmt.Printf("a 变量的地址是: %x\n", &a  )

   /* 指针变量的存储地址 */
   fmt.Printf("ip 变量储存的指针地址: %x\n", ip )

   /* 使用指针访问值 */
   fmt.Printf("*ip 变量的值: %d\n", *ip )
}
```

当一个指针被定义后没有分配到任何变量时，它的值为 nil。

nil 指针也称为空指针。

nil在概念上和其它语言的null、None、nil、NULL一样，都指代零值或空值。

一个指针变量通常缩写为 ptr。

## Go 语言结构体
Go 语言中数组可以存储同一类型的数据，但在结构体中我们可以为不同项定义不同的数据类型。

结构体是由一系列具有相同类型或不同类型的数据构成的数据集合。

结构体表示一项记录，比如保存图书馆的书籍记录，每本书有以下属性：

- Title ：标题
- Author ： 作者
- Subject：学科
- ID：书籍ID
结构体定义需要使用 type 和 struct 语句。struct 语句定义一个新的数据类型，结构体中有一个或多个成员。type 语句设定了结构体的名称。结构体的格式如下：

```go
type struct_variable_type struct {
   member definition
   member definition
   ...
   member definition
}
```

一旦定义了结构体类型，它就能用于变量的声明，语法格式如下：

```go
package main

import "fmt"

type Books struct {
   title string
   author string
   subject string
   book_id int
}


func main() {

    // 创建一个新的结构体
    fmt.Println(Books{"Go 语言", "www.runoob.com", "Go 语言教程", 6495407})

    // 也可以使用 key => value 格式
    fmt.Println(Books{title: "Go 语言", author: "www.runoob.com", subject: "Go 语言教程", book_id: 6495407})

    // 忽略的字段为 0 或 空
   fmt.Println(Books{title: "Go 语言", author: "www.runoob.com"})
}
```

如果要访问结构体成员，需要使用点号 . 操作符，格式为：
结构体.成员名

Go 通过**接收者（receiver）**把方法绑定到结构体类型上。接收者写在 `func` 和方法名之间：

```go

type Person struct {
    Name string
}

// 值接收者
func (p Person) SayHello() {
    fmt.Println("你好，我是", p.Name)
}

// 指针接收者：可以修改原结构体
func (p *Person) Rename(name string) {
    p.Name = name
}

func main() {
    p := Person{Name: "小明"}
    p.SayHello()
    p.Rename("小红")
}
```

##  Go 语言切片(Slice)

Go 语言切片是对数组的抽象。

Go 数组的长度不可改变，在特定场景中这样的集合就不太适用，Go 中提供了一种灵活，功能强悍的内置类型切片("动态数组")，与数组相比切片的长度是不固定的，可以追加元素，在追加时可能使切片的容量增大。

你可以声明一个未指定大小的数组来定义切片：

```go
var identifier []type
```

切片不需要说明长度。

或使用 **make()** 函数来创建切片:

### 切片初始化

s :=[] int {1,2,3 } 

make([]T, length, capacity)

初始化切片 **s**，是数组 arr 的引用。

s := arr[startIndex:endIndex]

将 arr 中从下标 startIndex 到 endIndex-1 下的元素创建为一个新的切片。

s := arr[startIndex:] 

### len() 和 cap() 函数

切片是可索引的，并且可以由 len() 方法获取长度。

切片提供了计算容量的方法 cap() 可以测量切片最长可以达到多少。

以下为具体实例：

```go
package main

import "fmt"

func main() {
   var numbers = make([]int,3,5)

   printSlice(numbers)
}

func printSlice(x []int){
   fmt.Printf("len=%d cap=%d slice=%v\n",len(x),cap(x),x)
}
```

### 可以通过设置下限及上限来设置截取切片

```go
package main

import "fmt"

func main() {
   /* 创建切片 */
   numbers := []int{0,1,2,3,4,5,6,7,8}   
   printSlice(numbers)

   /* 打印原始切片 */
   fmt.Println("numbers ==", numbers)

   /* 打印子切片从索引1(包含) 到索引4(不包含)*/
   fmt.Println("numbers[1:4] ==", numbers[1:4])

   /* 默认下限为 0*/
   fmt.Println("numbers[:3] ==", numbers[:3])

   /* 默认上限为 len(s)*/
   fmt.Println("numbers[4:] ==", numbers[4:])

   numbers1 := make([]int,0,5)
   printSlice(numbers1)

   /* 打印子切片从索引  0(包含) 到索引 2(不包含) */
   number2 := numbers[:2]
   printSlice(number2)

   /* 打印子切片从索引 2(包含) 到索引 5(不包含) */
   number3 := numbers[2:5]
   printSlice(number3)

}

func printSlice(x []int){
   fmt.Printf("len=%d cap=%d slice=%v\n",len(x),cap(x),x)
}
```

###  append() 和 copy() 函数

如果想增加切片的容量，我们必须创建一个新的更大的切片并把原分片的内容都拷贝过来。

```go
package main

import "fmt"

func main() {
   var numbers []int
   printSlice(numbers)

   /* 允许追加空切片 */
   numbers = append(numbers, 0)
   printSlice(numbers)

   /* 向切片添加一个元素 */
   numbers = append(numbers, 1)
   printSlice(numbers)

   /* 同时添加多个元素 */
   numbers = append(numbers, 2,3,4)
   printSlice(numbers)

   /* 创建切片 numbers1 是之前切片的两倍容量*/
   numbers1 := make([]int, len(numbers), (cap(numbers))*2)

   /* 拷贝 numbers 的内容到 numbers1 */
   copy(numbers1,numbers)
   printSlice(numbers1)   
}

func printSlice(x []int){
   fmt.Printf("len=%d cap=%d slice=%v\n",len(x),cap(x),x)
}


```

## Go 语言范围(Range)

Go 语言中 range 关键字用于 for 循环中迭代数组(array)、切片(slice)、通道(channel)或集合(map)的元素。在数组和切片中它返回元素的索引和索引对应的值，在集合中返回 key-value 对。

for 循环的 range 格式可以对 slice、map、数组、字符串等进行迭代循环。格式如下：

```go
for key, value := range oldMap {
    newMap[key] = value
}

```

## Go 语言Map(集合)

可以使用内建函数 make 或使用 map 关键字来定义 Map:

```go
/* 使用 make 函数 */
map_variable := make(map[KeyType]ValueType, initialCapacity)
```

delete() 函数用于删除集合的元素, 参数为 map 和其对应的 key。

## Go 语言类型转换

类型转换用于将一种数据类型的变量转换为另外一种类型的变量。

Go 语言类型转换基本格式如下：

```go
type_name(expression)

var a int = 10  
var b float64 = float64(a)
```

## Go 语言接口

### 接口的特点

**隐式实现**：

- Go 中没有关键字显式声明某个类型实现了某个接口。
- 只要一个类型实现了接口要求的所有方法，该类型就自动被认为实现了该接口。

**接口类型变量**：

- 接口变量可以存储实现该接口的任意值。
- 接口变量实际上包含了两个部分：
    - **动态类型**：存储实际的值类型。
    - **动态值**：存储具体的值。

**零值接口**：

- 接口的零值是 `nil`。
- 一个未初始化的接口变量其值为 `nil`，且不包含任何动态类型或值。

**空接口**：

- 定义为 `interface{}`，可以表示任何类型。Go 1.18 起也可以写成 `any`。
### 接口的常见用法

1. **多态**：不同类型实现同一接口，实现多态行为。
2. **解耦**：通过接口定义依赖关系，降低模块之间的耦合。
3. **泛化**：使用空接口 `interface{}` 表示任意类型。

接口定义使用关键字 interface，其中包含方法声明。

```go
/* 定义接口 */
type interface_name interface {
   method_name1 [return_type]
   method_name2 [return_type]
   method_name3 [return_type]
   ...
   method_namen [return_type]
}

/* 定义结构体 */
type struct_name struct {
   /* variables */
}

/* 实现接口方法 */
func (struct_name_variable struct_name) method_name1() [return_type] {
   /* 方法实现 */
}
...
func (struct_name_variable struct_name) method_namen() [return_type] {
   /* 方法实现*/
}
```

 类型通过实现接口要求的所有方法来实现接口。
```go
package main

import (
        "fmt"
        "math"
)

// 定义接口
type Shape interface {
        Area() float64
        Perimeter() float64
}

// 定义一个结构体
type Circle struct {
        Radius float64
}

// Circle 实现 Shape 接口
func (c Circle) Area() float64 {
        return math.Pi * c.Radius * c.Radius
}

func (c Circle) Perimeter() float64 {
        return 2 * math.Pi * c.Radius
}

func main() {
        c := Circle{Radius: 5}
        var s Shape = c // 接口变量可以存储实现了接口的类型
        fmt.Println("Area:", s.Area())
        fmt.Println("Perimeter:", s.Perimeter())
}
```

空接口 `interface{}` 是 Go 的特殊接口，表示所有类型的超集。

- 任意类型都实现了空接口。
- 常用于需要存储任意类型数据的场景，如泛型容器、通用参数等。

## 类型断言

类型断言用于从接口类型中提取其底层值。

基本语法:
```go
    s, ok := i.(string)  
    if ok {  
        fmt.Println("断言成功:", s)  
    } else {  
        fmt.Println("断言失败")  
    }
```





## Go 继承


在面向对象编程（OOP）中，继承是一种机制，允许一个类（子类）从另一个类（父类）继承属性和方法。通过继承，子类可以复用父类的代码，并且可以在不修改父类的情况下扩展或修改其行为。

Go 语言并不是一种传统的面向对象编程语言，它没有类和继承的概念。

Go 使用结构体（struct）和接口（interface）来实现类似的功能。

Go 语言没有传统面向对象语言中的类(class)和继承(inheritance)概念，而是通过组合(composition)和接口(interface)来实现类似的功能。

### 1. 组合（Composition）

组合是 Go 中实现代码复用的主要方式。通过将一个结构体嵌入到另一个结构体中，子结构体可以"继承"父结构体的字段和方法。

```go
package main

import "fmt"

// 父结构体
type Animal struct {
    Name string
}

// 父结构体的方法
func (a *Animal) Speak() {
    fmt.Println(a.Name, "says hello!")
}

// 子结构体
type Dog struct {
    Animal // 嵌入 Animal 结构体
    Breed  string
}

func main() {
    dog := Dog{
        Animal: Animal{Name: "Buddy"},
        Breed:  "Golden Retriever",
    }

    dog.Speak() // 调用父结构体的方法
    fmt.Println("Breed:", dog.Breed)
}
```

接口是 Go 中实现多态的主要方式。通过定义接口，不同的结构体可以实现相同的方法，从而实现类似继承的多态行为。

```go
package main

import "fmt"

// 定义接口
type Speaker interface {
    Speak()
}

// 父结构体
type Animal struct {
    Name string
}

// 实现接口方法
func (a *Animal) Speak() {
    fmt.Println(a.Name, "says hello!")
}

// 子结构体
type Dog struct {
    Animal
    Breed string
}

func main() {
    var speaker Speaker

    dog := Dog{
        Animal: Animal{Name: "Buddy"},
        Breed:  "Golden Retriever",
    }

    speaker = &dog
    speaker.Speak() // 通过接口调用方法
}

```

## go语言泛型

泛型主要通过以下两个核心概念来实现：

- **类型参数（Type Parameters）：**允许你在函数或类型定义中使用一个或多个类型作为参数。
- **类型约束（Type Constraints）：**指定类型参数必须满足的条件，确保在函数内部可以安全地操作这些类型。

| 概念               | 作用                         | 示例                                               |
| ---------------- | -------------------------- | ------------------------------------------------ |
| **类型参数**         | 在函数或类型名后声明，表示待定的类型。        | `[T any]`                                        |
| **类型约束**         | 定义类型参数必须满足的条件（如支持的操作符或方法）。 | `int，float64，comparable，constraints.Ordered，any` |
| **`any`**        | 约束类型参数为**任何**类型。           | `[T any]`                                        |
| **`comparable`** | 约束类型参数为**可比较**的类型。         | `[K comparable]`                                 |

在引入泛型之前，如果我们想要处理不同类型的数据，通常需要为每种类型编写重复的函数。

```go
// 处理 int 类型的函数
func MaxInt(a, b int) int {
    if a > b {
        return a
    }
    return b
}

// 处理 float64 类型的函数
func MaxFloat(a, b float64) float64 {
    if a > b {
        return a
    }
    return b
}
```


**使用泛型的解决方案：**

```go
// 一个函数处理多种类型
func Max[T comparable](a, b T) T {
    if a > b {
        return a
    }
    return b
}
```

泛型函数和类型通过类型参数列表来声明，语法为 `[类型参数 约束]`。

```go
// 基本语法结构
func 函数名[T 约束](参数 T) 返回值类型 {
    // 函数体
}

type 类型名[T 约束] struct {
    // 结构体字段
}
```

- 通常使用大写字母：`T`、`K`、`V`、`E` 等
- `T`：表示 Type（类型）
- `K`：表示 Key（键）
- `V`：表示 Value（值）
- `E`：表示 Element（元素）

约束定义了类型参数必须满足的条件，是泛型的核心概念。

`any` 是空接口 `interface{}` 的别名，表示任何类型都可以。

`comparable` 表示类型支持 `==` 和 `!=` 操作符。

使用 `|` 运算符组合多个类型。

### 自定义约束

```go

// 定义 Stringer 约束
type Stringer interface {
    String() string
}

func PrintString[T Stringer](value T) {
    fmt.Println(value.String())
}

// 实现自定义类型
type Person struct {
    Name string
    Age  int
}

func (p Person) String() string {
    return fmt.Sprintf("%s (%d years old)", p.Name, p.Age)
}

// 使用示例
person := Person{Name: "Alice", Age: 25}
PrintString(person)  // 输出: Alice (25 years old)
```


## Go 错误处理

Go 语言通过内置的错误接口提供了非常简单的错误处理机制。

Go 语言的错误处理采用显式返回错误的方式，而非传统的异常处理机制。这种设计使代码逻辑更清晰，便于开发者在编译时或运行时明确处理错误。

**Go 的错误处理主要围绕以下机制展开：**

1. **`error` 接口**：标准的错误表示。
2. **显式返回值**：通过函数的返回值返回错误。
3. **自定义错误**：可以通过标准库或自定义的方式创建错误。
4. **`panic` 和 `recover`**：处理不可恢复的严重错误。

## error 接口

Go 标准库定义了一个 error 接口，表示一个错误的抽象。

error 类型是一个接口类型，这是它的定义：
```go

type error interface {
    Error() string
}
```


panic 用于处理不可恢复的错误，recover 用于从 panic 中恢复。

panic:

- 导致程序崩溃并输出堆栈信息。
- 常用于程序无法继续运行的情况。

recover:

- 捕获 `panic`，避免程序崩溃。
##  Go 并发
并发是指程序同时执行多个任务的能力。

Go 语言支持并发，通过 goroutines 和 channels 提供了一种简洁且高效的方式来实现并发。

**Goroutines：**

- Go 中的并发执行单位，类似于轻量级的线程。
- Goroutine 的调度由 Go 运行时管理，用户无需手动分配线程。
- 使用 `go` 关键字启动 Goroutine。
- Goroutine 是非阻塞的，可以高效地运行成千上万个 Goroutine。

**Channel：**

- Go 中用于在 Goroutine 之间通信的机制。
- 支持同步和数据共享，避免了显式的锁机制。
- 使用 `chan` 关键字创建，通过 `<-` 操作符发送和接收数据。
**Scheduler（调度器）：**

Go 的调度器基于 GMP 模型，调度器会将 Goroutine 分配到系统线程中执行，并通过 M 和 P 的配合高效管理并发。

- **G**：Goroutine。
- **M**：系统线程（Machine）。
- **P**：逻辑处理器（Processor）。

goroutine 是轻量级线程，goroutine 的调度是由 Golang 运行时进行管理的。

goroutine 语法格式：

```go
go 函数名( 参数列表 )
go f(x, y, z)
```

Go 允许使用 go 语句开启一个新的运行期线程， 即 goroutine，以一个不同的、新创建的 goroutine 来执行一个函数。 同一个程序中的所有 goroutine 共享同一个地址空间。

通道（Channel）是用于 Goroutine 之间的数据传递。

通道可用于两个 goroutine 之间通过传递一个指定类型的值来同步运行和通讯。

使用 `make` 函数创建一个 channel，使用 `<-` 操作符发送和接收数据。如果未指定方向，则为双向通道。

声明一个通道很简单，我们使用chan关键字即可，通道在使用前必须先创建：
```go
ch := make(chan int)

ch <- v    // 把 v 发送到通道 ch
v := <-ch  // 从 ch 接收数据
           // 并把值赋给 v
```

默认情况下，通道是不带缓冲区的。发送端发送数据，同时必须有接收端相应的接收数据。

通道可以设置缓冲区，通过 make 的第二个参数指定缓冲区大小：

```go
ch := make(chan int, 100)
```


## Go Modules

Go Modules 是 Go 语言的官方依赖管理工具，自 Go 1.11 版本开始引入，在 Go 1.16 版本成为默认的依赖管理模式。

Go Modules 解决了 Go 语言长期以来在依赖管理方面的痛点，为开发者提供了版本控制、依赖隔离和可重复构建等核心功能。

**模块（Module）**：包含 `go.mod` 文件的目录树，该文件定义了模块的路径、Go 版本要求和依赖关系。

**版本（Version）**：遵循语义化版本控制（Semantic Versioning）的标识符，格式为 `vMAJOR.MINOR.PATCH`。

**依赖图（Dependency Graph）**：模块及其所有传递依赖的层次结构，Go 工具会自动解析和维护。

### go.mod 文件

`go.mod` 是模块的定义文件，包含以下主要部分：

```go

module example.com/mymodule  // 模块路径

go 1.21                     // Go 版本要求

require (
    github.com/gin-gonic/gin v1.9.1
    golang.org/x/text v0.12.0
)

replace golang.org/x/text => ../local/text  // 本地替换

exclude github.com/old/module v1.0.0        // 排除特定版本
```

### 模块初始化

```go
# 创建新模块
go mod init example.com/myproject

# 在现有项目中初始化
cd /path/to/project
go mod init
```

### 依赖管理

```go
# 添加依赖（自动选择最新版本）
go get github.com/gin-gonic/gin

# 添加特定版本
go get github.com/gin-gonic/gin@v1.9.1

# 更新到最新版本
go get -u github.com/gin-gonic/gin

# 更新所有依赖
go get -u all

# 下载依赖到本地缓存
go mod download

# 整理 go.mod 文件
go mod tidy
```

### 依赖查询

```go
# 查看所有依赖
go list -m all

# 查看特定依赖的可用版本
go list -m -versions github.com/gin-gonic/gin

# 查看为什么需要某个依赖
go mod why github.com/gin-gonic/gin
```

### 私有仓库支持

```go
# 配置私有仓库认证
git config --global url."https://user:token@github.com".insteadOf "https://github.com"

# 或使用环境变量
export GOPRIVATE=github.com/mycompany/*
```


