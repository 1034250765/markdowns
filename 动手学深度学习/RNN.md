## Pytorch中RNN Layer的使用

**2.1 RNN模块 **  **千万不要理解成隐藏层有t个隐藏单元。**
Pytorch中RNN模块函数为**torch.nn.RNN(input_size,hidden_size,num_layers,batch_first)**，每个参数的含义如下:

input_size：输入数据的编码维度，比如前面举例的房价预测，房价都是用一维的数直接表示的，所以此时input_size为1；如果输入的是字符编码，比如一个字符用3维编码表示，那么此时input_size为3；
hidden_size：隐含层的维数，这个维数要么参考别人的结构设置，要么自行设置，比如可以设置成20；
num_layers：隐含层的层数，也就是上面几幅图有几个h层，上面都是只有1层，所以 num_layers为1。
batch_first：当 batch_first设置为True时，输入的参数顺序变为：x：[batch, seq_len, input_size]，h0：[batch, num_layers, hidden_size]。

**输入的表示形式，输入如下图所示，输入主要有向量x xx、初始的h 0 h_0h **
0 ， 其中x：[seq_len, batch, input_size]，h0：[num_layers, batch, hidden_size]，下面分别介绍每个参数的意义。seq_len：输入的长度，即有多少个x i x_ix i ，上述房价预测中，如果输入的是12个月的房价，那么seq_len就为12；
batch：在训练神经网络时，可以多条数据同时训练，还是以房价预测为例，现在同时拿去年，今年共两年的数据训练网络，也就是将两年的数据batch在了一起，比如输入x i x_ix i 是去年和今年第i月份的房价；一直以来我都不太明白这个 batch是什么意思，直到看了这几篇文章：参考1，参考2，参考3，想了解更多，大家也可以看一下；
input_size：就是torch.nn.RNN(input_size,hidden_size,num_layers)中的input_size，二者要保持一致；
num_layers：与torch.nn.RNN中一致；
hidden_size：与torch.nn.RNN中一致；

**比如我现在想设计一个4层的RNN，用来做语音翻译，输入是一段中文，输出是一段英文。**假设每个中文字符用100维数据进行编码，每个隐含层的维度是20，有4个隐含层。所以input_size = 100，hidden_size = 20，num_layers = 4。再假设模型已经训练好了，现在有个1个长度为10的句子做输入，那么seq_len = 10，batch_size = 1。代码如下：

```python
import torch
import torch.nn as nn

input_size = 100   # 输入数据编码的维度
hidden_size = 20   # 隐含层维度
num_layers = 4     # 隐含层层数

rnn = nn.RNN(input_size=input_size,hidden_size=hidden_size,num_layers=num_layers)
print("rnn:",rnn)

seq_len = 10        # 句子长度
batch_size = 1      
x = torch.randn(seq_len,batch_size,input_size)        # 输入数据
h0 = torch.zeros(num_layers,batch_size,hidden_size)   # 输入数据

out, h = rnn(x, h0)  # 输出数据

print("out.shape:",out.shape)
print("h.shape:",h.shape)


```

```python
class GRUModel(nn.Module):

    def __init__(self, input_num, hidden_num, output_num):
        super(GRUModel, self).__init__()
        self.hidden_size = hidden_num
        # 这里设置了 batch_first=True, 所以应该 inputs = inputs.view(inputs.shape[0], -1, inputs.shape[1])
        # 针对时间序列预测问题，相当于将时间步（seq_len）设置为 1。
        self.GRU_layer = nn.GRU(input_size=input_num, hidden_size=hidden_num, batch_first=True)
        self.output_linear = nn.Linear(hidden_num, output_num)
        self.hidden = None

    def forward(self, x):
        # h_n of shape (num_layers * num_directions, batch, hidden_size)
        # 这里不用显式地传入隐层状态 self.hidden
        x, self.hidden = self.GRU_layer(x)
        x = self.output_linear(x)
        return x, self.hidden

```

