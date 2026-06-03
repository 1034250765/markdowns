## Conda 常用命令

conda env list

conda create -n 环境名 python=版本号

conda activate 环境名

conda deactivate

conda remove -n 环境名 --all

conda install 包名==版本号

conda list -n 环境名  查看指定环境的包

conda update 包名

conda update --all

conda remove 包名

conda remove -n 环境名 包名

conda update conda

 添加Anaconda仓库镜像
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
 添加conda-forge仓库镜像（包含更多包）
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
 添加PyTorch镜像（如需安装PyTorch）
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/

#### 导出环境配置（用于复现环境）

conda env export > 环境名.yaml