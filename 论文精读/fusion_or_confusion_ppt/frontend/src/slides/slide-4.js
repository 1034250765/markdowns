window.slideDataMap.set(4, `
<div class="w-[1440px] h-[810px] shadow-2xl relative overflow-hidden slide-bg">
  <div class="w-[1350px] h-[700px] mx-auto my-[40px] flex">
    <div class="w-2 bg-primary"></div>
    <div class="flex-1 px-14 flex flex-col justify-center">
      <div class="mb-7">
        <h2 class="text-[38px] font-light text-gray-900 mb-3">红外数据为什么天生「难合」</h2>
        <p class="text-[16px] text-gray-500">池化的收益来自多样性，代价来自域差异——红外把这两点都放大了</p>
      </div>

      <div class="space-y-[22px]">
        <div class="flex items-start gap-6">
          <div class="w-3 h-3 bg-primary mt-2 flex-shrink-0"></div>
          <div>
            <h3 class="text-[21px] font-semibold text-gray-800 mb-1.5">数据先天稀缺，且没有「红外基础数据集」</h3>
            <p class="text-gray-600 text-[16px] leading-relaxed">红外数据集规模远小于可见光，论文明确指出目前不存在红外基础数据集。池化只能在领域特定数据集之间进行，多样性先天受限。</p>
          </div>
        </div>

        <div class="flex items-start gap-6">
          <div class="w-3 h-3 bg-primary mt-2 flex-shrink-0"></div>
          <div>
            <h3 class="text-[21px] font-semibold text-gray-800 mb-1.5">外观由成像条件决定，而非物体本身</h3>
            <p class="text-gray-600 text-[16px] leading-relaxed">红外记录热辐射，环境温度、昼夜时段、传感器标定都会改变对比度、噪声与整体分布。同一辆车在两个数据集中可能呈现完全不同的灰度结构。</p>
          </div>
        </div>

        <div class="flex items-start gap-6">
          <div class="w-3 h-3 bg-primary mt-2 flex-shrink-0"></div>
          <div>
            <h3 class="text-[21px] font-semibold text-gray-800 mb-1.5">平台高度与视角造成结构性域偏移</h3>
            <p class="text-gray-600 text-[16px] leading-relaxed">地面车载与执法记录仪、低空固定监控、中空无人机、高空平台，对应截然不同的目标尺度、长宽比与背景结构——这是「地面 / 航拍」两分法的由来。</p>
          </div>
        </div>

        <div class="flex items-start gap-6">
          <div class="w-3 h-3 bg-primary mt-2 flex-shrink-0"></div>
          <div>
            <h3 class="text-[21px] font-semibold text-gray-800 mb-1.5">标注体系互不兼容</h3>
            <p class="text-gray-600 text-[16px] leading-relaxed">各数据集车辆子类从 2 类到 15 类不等（car / bus / truck / van / freight car…），直接合并会出现标签冲突与语义错位。</p>
          </div>
        </div>
      </div>

      <div class="mt-6 bg-gray-50 border border-gray-200 px-6 py-3">
        <p class="text-[15px] text-gray-600"><span class="font-semibold text-gray-800">论文的基本判断：</span>更多数据并不必然带来更好泛化——所以需要一轮系统实验，回答「什么时候该合、和谁合」。</p>
      </div>
    </div>
  </div>

  <div class="absolute bottom-4 left-12 right-12 flex justify-between text-[12px] text-gray-400 tracking-wide">
    <span>Fusion or Confusion? · Becker et al. · CVPRW 2025</span>
    <span>04 / 26</span>
  </div>
</div>
`);
