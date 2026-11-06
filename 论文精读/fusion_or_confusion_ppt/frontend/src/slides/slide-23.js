window.slideDataMap.set(23, `
<div class="w-[1440px] h-[810px] shadow-2xl relative overflow-hidden slide-bg">
  <div class="w-[1350px] h-[700px] mx-auto my-[40px] flex flex-col justify-center">

    <div class="mb-11">
      <p class="text-[13px] tracking-widest text-gray-400 mb-2">DAS · 5.6</p>
      <h2 class="text-[38px] font-light text-gray-900">正确用法：DAS 缩范围，mAP 做裁决</h2>
      <p class="text-[16px] text-gray-500 mt-3">这条流程在原文中并没有画成图，但从实验设计可以完整还原出来</p>
    </div>

    <div class="relative">
      <div class="absolute top-[52px] left-0 right-0 h-px bg-gray-200"></div>
      <div class="flex justify-between">

        <div class="flex-1 flex flex-col items-center px-3">
          <span class="text-[13px] font-mono text-gray-400 mb-4 tracking-widest">STEP 1</span>
          <div class="w-3 h-3 rounded-full bg-primary relative z-10"></div>
          <div class="mt-8 text-center">
            <h3 class="text-[17px] font-semibold text-gray-900 mb-2">训练带 DAS 的全量池模型</h3>
            <p class="text-[14px] text-gray-600 leading-relaxed">把「来源数据集」作为额外标签一并训练。</p>
          </div>
        </div>

        <div class="flex-1 flex flex-col items-center px-3">
          <span class="text-[13px] font-mono text-gray-400 mb-4 tracking-widest">STEP 2</span>
          <div class="w-3 h-3 rounded-full bg-primary relative z-10"></div>
          <div class="mt-8 text-center">
            <h3 class="text-[17px] font-semibold text-gray-900 mb-2">在目标域统计亲和分布</h3>
            <p class="text-[14px] text-gray-600 leading-relaxed">在目标测试集或零样本集上统计各来源占比。</p>
          </div>
        </div>

        <div class="flex-1 flex flex-col items-center px-3">
          <span class="text-[13px] font-mono text-gray-400 mb-4 tracking-widest">STEP 3</span>
          <div class="w-3 h-3 rounded-full bg-primary relative z-10"></div>
          <div class="mt-8 text-center">
            <h3 class="text-[17px] font-semibold text-gray-900 mb-2">找出高亲和与冗余来源</h3>
            <p class="text-[14px] text-gray-600 leading-relaxed">亲和度低、几乎不被指向的数据集，优先考虑剔除。</p>
          </div>
        </div>

        <div class="flex-1 flex flex-col items-center px-3">
          <span class="text-[13px] font-mono text-gray-400 mb-4 tracking-widest">STEP 4</span>
          <div class="w-3 h-3 rounded-full bg-primary relative z-10"></div>
          <div class="mt-8 text-center">
            <h3 class="text-[17px] font-semibold text-gray-900 mb-2">构造更小的候选池</h3>
            <p class="text-[14px] text-gray-600 leading-relaxed">得到一个「更稀疏但更匹配」的数据组合。</p>
          </div>
        </div>

        <div class="flex-1 flex flex-col items-center px-3">
          <span class="text-[13px] font-mono text-accent-1 mb-4 tracking-widest">STEP 5</span>
          <div class="w-3 h-3 rounded-full bg-accent-1 relative z-10"></div>
          <div class="mt-8 text-center">
            <h3 class="text-[17px] font-semibold text-gray-900 mb-2">重训普通检测器并裁决</h3>
            <p class="text-[14px] text-gray-600 leading-relaxed">用真实 mAP 判断新组合是否更好——这一步不可省。</p>
          </div>
        </div>
      </div>
    </div>

    <div class="mt-12 bg-gray-50 border border-gray-200 px-6 py-4">
      <p class="text-[15px] text-gray-600 leading-relaxed">
        <span class="font-semibold text-gray-800">一句话记住：</span>DAS 用于缩小搜索范围，检测性能用于最终裁决。
        论文反复强调「迭代重训与重新组合仍然必要」，因此它无法替代实验，只能减少实验次数。
      </p>
    </div>
  </div>

  <div class="absolute bottom-4 left-12 right-12 flex justify-between text-[12px] text-gray-400 tracking-wide">
    <span>Fusion or Confusion? · Becker et al. · CVPRW 2025</span>
    <span>23 / 26</span>
  </div>
</div>
`);
