## FCN

使用一个转置的卷积层替换最后的全连接层

![image-20260115144151158](C:\Users\LYX10\AppData\Roaming\Typora\typora-user-images\image-20260115144151158.png)

```python
num_classes = 21
net.add_module('final_conv', nn.Conv2d(512, num_classes, kernel_size=1))
net.add_module('transpose_conv', nn.ConvTranspose2d(num_classes, num_classes,
                                    kernel_size=64, padding=16, stride=32))
```

**双线性插值**

假设源图像大小为mxn，目标图像为axb。那么两幅图像的边长比分别为：m/a和n/b。目标图像的第（i,j）个像素点（i行j列）可以通过边长比对应回源图像。其对应坐标为（i*m/a,j*n/b）。显然，这个对应坐标一般来说不是整数，而非整数的坐标是无法在图像这种离散数据上使用的。双线性插值通过寻找距离这个对应坐标最近的四个像素点，来计算该点的值（灰度值或者RGB值）。

**单线性插值**
已知中P1点和P2点，坐标分别为(x1, y1)、(x2, y2)，要计算 [x1, x2] 区间内某一位置 x 在直线上的y值

![image-20260115161205484](C:\Users\LYX10\AppData\Roaming\Typora\typora-user-images\image-20260115161205484.png)

双线性插值

![image-20260115162004674](C:\Users\LYX10\AppData\Roaming\Typora\typora-user-images\image-20260115162004674.png)

双线性插值是分别在两个方向计算了共3次单线性插值，如图所示，先在x方向求2次单线性插值，获得R1(x, y1)、R2(x, y2)两个临时点，再在y方向计算1次单线性插值得出P(x, y)（实际上调换2次轴的方向先y后x也是一样的结果）。

***f*(*x*,*y*)=(*x*2−*x*1)(*y*2−*y*1)*f*(*Q*11)(*x*2−*x*)(*y*2−*y*)+(*x*2−*x*1)(*y*2−*y*1)*f*(*Q*21)(*x*−*x*1)(*y*2−*y*)+(*x*2−*x*1)(*y*2−*y*1)*f*(*Q*12)(*x*2−*x*)(*y*−*y*1)**

![image-20260115162523444](C:\Users\LYX10\AppData\Roaming\Typora\typora-user-images\image-20260115162523444.png)

**初始化卷积层**

```python
def bilinear_kernel(in_channels, out_channels, kernel_size):
    factor = (kernel_size + 1) // 2
    if kernel_size % 2 == 1:
        center = factor - 1
    else:
        center = factor - 0.5
    og = (torch.arange(kernel_size).reshape(-1, 1),
          torch.arange(kernel_size).reshape(1, -1))
    filt = (1 - torch.abs(og[0] - center) / factor) * \
           (1 - torch.abs(og[1] - center) / factor)
    weight = torch.zeros((in_channels, out_channels,
                          kernel_size, kernel_size))
    weight[range(in_channels), range(out_channels), :, :] = filt
    return weight
```

