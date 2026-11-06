window.slideDataMap.set(5, `
<div class="w-[1440px] h-[810px] shadow-2xl relative overflow-hidden slide-bg">
  <div class="w-[1350px] h-[700px] mx-auto my-[40px] flex gap-14">

    <!-- 左列 -->
    <div class="flex-1 flex flex-col justify-center gap-7">
      <div>
        <h2 class="text-[38px] font-light text-gray-900 mb-5 pb-4 border-b-2 border-gray-300">论文想回答的五个问题</h2>
        <p class="text-gray-700 text-[17px] leading-relaxed mb-4">
          这不是一篇提出新融合网络的论文，而是一次系统性评估：固定检测器、统一标签、只改变训练数据池的组成方式，观察性能如何变化。
        </p>
        <p class="text-gray-700 text-[17px] leading-relaxed">
          作者先承认一个前提——池化能增加样本量与多样性、抑制过拟合，但也可能引入域差与冗余。收益和代价同时存在，才使得下面五个问题必须用实验回答。
        </p>
      </div>

      <div class="border-l-4 border-accent-1 pl-6 py-2">
        <p class="text-gray-700 text-[17px] italic leading-relaxed">"融合的关键不是合得多，而是合得合适。"</p>
        <p class="text-gray-400 text-[14px] mt-2">— 全文的落脚点，也是五个问题共同的指向</p>
      </div>
    </div>

    <!-- 右列：五个问题 -->
    <div class="flex-1 flex flex-col justify-center">
      <h3 class="text-[22px] font-semibold text-gray-500 mb-5 tracking-wide">RESEARCH QUESTIONS</h3>
      <ul class="space-y-[18px]">
        <li class="flex items-start gap-4">
          <span class="flex-shrink-0 w-8 h-8 rounded-full bg-primary text-white text-[14px] flex items-center justify-center mt-0.5">1</span>
          <span class="text-gray-700 text-[16px] leading-relaxed">多个红外数据集合并训练，是否<b>稳定优于</b>单数据集训练？</span>
        </li>
        <li class="flex items-start gap-4">
          <span class="flex-shrink-0 w-8 h-8 rounded-full bg-primary text-white text-[14px] flex items-center justify-center mt-0.5">2</span>
          <span class="text-gray-700 text-[16px] leading-relaxed"><b>同域融合</b>与<b>跨域融合</b>的效果有何差异？</span>
        </li>
        <li class="flex items-start gap-4">
          <span class="flex-shrink-0 w-8 h-8 rounded-full bg-primary text-white text-[14px] flex items-center justify-center mt-0.5">3</span>
          <span class="text-gray-700 text-[16px] leading-relaxed">图像<b>预处理</b>能否减小不同红外数据集之间的域差异？</span>
        </li>
        <li class="flex items-start gap-4">
          <span class="flex-shrink-0 w-8 h-8 rounded-full bg-primary text-white text-[14px] flex items-center justify-center mt-0.5">4</span>
          <span class="text-gray-700 text-[16px] leading-relaxed">能否通过<b>特征分布或 DAS</b> 提前判断哪些数据适合融合？</span>
        </li>
        <li class="flex items-start gap-4">
          <span class="flex-shrink-0 w-8 h-8 rounded-full bg-accent-1 text-white text-[14px] flex items-center justify-center mt-0.5">5</span>
          <span class="text-gray-700 text-[16px] leading-relaxed">融合模型在<b>未参与训练的新数据集</b>上，零样本泛化是否更好？</span>
        </li>
      </ul>
    </div>
  </div>

  <div class="absolute bottom-4 left-12 right-12 flex justify-between text-[12px] text-gray-400 tracking-wide">
    <span>Fusion or Confusion? · Becker et al. · CVPRW 2025</span>
    <span>05 / 26</span>
  </div>
</div>
`);
