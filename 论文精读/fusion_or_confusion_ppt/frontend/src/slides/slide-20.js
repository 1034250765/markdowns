window.slideDataMap.set(20, `
<div class="w-[1440px] h-[810px] shadow-2xl relative overflow-hidden slide-bg">
  <div class="w-[1350px] h-[700px] mx-auto my-[40px] flex flex-col">

    <div class="mb-7">
      <p class="text-[13px] tracking-widest text-gray-400 mb-2">DAS · 5.1–5.3</p>
      <h2 class="text-[36px] font-light text-gray-900 mb-3">DAS 是什么：让检测器自报「这个目标像哪个训练集」</h2>
      <p class="text-[16px] text-gray-500">Dataset Affinity Score（数据集亲和度分数）· 一种 ante-hoc 的解释工具</p>
    </div>

    <!-- 四步流程 -->
    <div class="relative mb-7">
      <div class="absolute top-[34px] left-0 right-0 h-px bg-gray-200"></div>
      <div class="flex justify-between">

        <div class="flex-1 flex flex-col items-center px-3">
          <span class="text-[13px] font-mono text-gray-400 mb-3 tracking-widest">STEP 01</span>
          <div class="w-3 h-3 rounded-full bg-primary relative z-10"></div>
          <div class="mt-6 text-center">
            <h3 class="text-[19px] font-semibold text-gray-900 mb-2">附加来源标签</h3>
            <p class="text-[15px] text-gray-600 leading-relaxed">训练池里每个 GT 框除类别 <span class="font-mono text-[13px]">vehicle</span> 外，还天然带有一个「来自哪个数据集」的标签。</p>
          </div>
        </div>

        <div class="flex-1 flex flex-col items-center px-3">
          <span class="text-[13px] font-mono text-gray-400 mb-3 tracking-widest">STEP 02</span>
          <div class="w-3 h-3 rounded-full bg-primary relative z-10"></div>
          <div class="mt-6 text-center">
            <h3 class="text-[19px] font-semibold text-gray-900 mb-2">复用分类头</h3>
            <p class="text-[15px] text-gray-600 leading-relaxed">因为只检测单一类别，默认分类头是空闲的，可直接改为预测数据集来源，无需新增第二个头。</p>
          </div>
        </div>

        <div class="flex-1 flex flex-col items-center px-3">
          <span class="text-[13px] font-mono text-gray-400 mb-3 tracking-widest">STEP 03</span>
          <div class="w-3 h-3 rounded-full bg-primary relative z-10"></div>
          <div class="mt-6 text-center">
            <h3 class="text-[19px] font-semibold text-gray-900 mb-2">单框归属</h3>
            <p class="text-[15px] text-gray-600 leading-relaxed">对每个检测框取亲和度最大的训练集，作为它的「视觉来源」判断。</p>
          </div>
        </div>

        <div class="flex-1 flex flex-col items-center px-3">
          <span class="text-[13px] font-mono text-gray-400 mb-3 tracking-widest">STEP 04</span>
          <div class="w-3 h-3 rounded-full bg-accent-1 relative z-10"></div>
          <div class="mt-6 text-center">
            <h3 class="text-[19px] font-semibold text-gray-900 mb-2">整集统计</h3>
            <p class="text-[15px] text-gray-600 leading-relaxed">汇总整个测试集里各来源的比例，得到这张测试集的「数据池分布」。</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 说明 -->
    <div class="mb-6 border-l-2 border-gray-300 pl-6 space-y-2">
      <p class="text-[15px] text-gray-600 leading-relaxed">
        <span class="font-semibold text-gray-900">直观含义：</span>如果某个测试集的检测框大量指向少数几个训练集，说明其余数据集对该域贡献有限——这正是「该裁池」的信号。
      </p>
      <p class="text-[15px] text-gray-600 leading-relaxed">
        <span class="font-semibold text-gray-900">容易误用的地方：</span>DAS 回答的是「这个目标<b>看起来像</b>哪个训练集」，而不是「哪个训练集<b>更重要</b>」。
      </p>
    </div>

    <!-- 公式区 -->
    <div class="mt-auto grid grid-cols-2 gap-6">
      <div class="border border-gray-200 bg-gray-50 px-6 py-4">
        <p class="text-[13px] text-gray-500 mb-2">单个检测框的来源归属</p>
        <p class="text-[21px] font-mono text-gray-900">a(x) = argmax<sub>k</sub> p<sub>k</sub>(x)</p>
        <p class="text-[13px] text-gray-500 mt-2">p<sub>k</sub>(x)：框 x 属于第 k 个训练数据集的预测概率</p>
      </div>
      <div class="border border-gray-200 bg-gray-50 px-6 py-4">
        <p class="text-[13px] text-gray-500 mb-2">整个测试集的亲和比例</p>
        <p class="text-[21px] font-mono text-gray-900">A<sub>k</sub> = N<sub>k</sub> / N</p>
        <p class="text-[13px] text-gray-500 mt-2">N 为检测框总数，N<sub>k</sub> 为被归到第 k 个训练集的框数</p>
      </div>
    </div>
  </div>

  <div class="absolute bottom-4 left-12 right-12 flex justify-between text-[12px] text-gray-400 tracking-wide">
    <span>Fusion or Confusion? · Becker et al. · CVPRW 2025</span>
    <span>20 / 26</span>
  </div>
</div>
`);
