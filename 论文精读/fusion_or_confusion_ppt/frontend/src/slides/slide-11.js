window.slideDataMap.set(11, `
<div class="w-[1440px] h-[810px] shadow-2xl relative overflow-hidden slide-bg">
  <div class="w-[1350px] h-[700px] mx-auto my-[40px] flex flex-col justify-center">

    <div class="mb-14">
      <h2 class="text-[38px] font-light text-gray-900 mb-3">第四步：三种对比度预处理</h2>
      <p class="text-[16px] text-gray-500">目标是把不同数据集的对比度拉到同一水平——但实验结果显示，这一步并没有奏效</p>
    </div>

    <div class="relative">
      <div class="absolute top-[34px] left-0 right-0 h-px bg-gray-200"></div>
      <div class="flex justify-between">

        <div class="flex-1 flex flex-col items-center px-4">
          <span class="text-[13px] font-mono text-gray-400 mb-3 tracking-widest">BASELINE</span>
          <div class="w-3 h-3 rounded-full bg-gray-400 relative z-10"></div>
          <div class="mt-8 text-center">
            <h3 class="text-[20px] font-semibold text-gray-900 mb-2">原始图像</h3>
            <p class="text-[15px] text-gray-600 leading-relaxed">不做任何处理，直接训练。所有对比都以它为基线。</p>
          </div>
        </div>

        <div class="flex-1 flex flex-col items-center px-4">
          <span class="text-[13px] font-mono text-gray-400 mb-3 tracking-widest">METHOD 01</span>
          <div class="w-3 h-3 rounded-full bg-primary relative z-10"></div>
          <div class="mt-8 text-center">
            <h3 class="text-[20px] font-semibold text-gray-900 mb-2">HE 直方图均衡</h3>
            <p class="text-[15px] text-gray-600 leading-relaxed">重分布像素强度、拉大整体对比度；缺点是可能放大噪声，在红外图上容易破坏细微温差。</p>
          </div>
        </div>

        <div class="flex-1 flex flex-col items-center px-4">
          <span class="text-[13px] font-mono text-gray-400 mb-3 tracking-widest">METHOD 02</span>
          <div class="w-3 h-3 rounded-full bg-primary relative z-10"></div>
          <div class="mt-8 text-center">
            <h3 class="text-[20px] font-semibold text-gray-900 mb-2">CLAHE 限制对比度自适应均衡</h3>
            <p class="text-[15px] text-gray-600 leading-relaxed">把图像分块、在每块内做自适应增强，改善局部对比度的同时抑制噪声过度放大。</p>
          </div>
        </div>

        <div class="flex-1 flex flex-col items-center px-4">
          <span class="text-[13px] font-mono text-gray-400 mb-3 tracking-widest">METHOD 03</span>
          <div class="w-3 h-3 rounded-full bg-accent-1 relative z-10"></div>
          <div class="mt-8 text-center">
            <h3 class="text-[20px] font-semibold text-gray-900 mb-2">FieldScale 场式重缩放</h3>
            <p class="text-[15px] text-gray-600 leading-relaxed">专为热红外设计，按空间变化的场而非全局/严格局部来调整像素强度。</p>
          </div>
        </div>
      </div>
    </div>

    <div class="mt-14 border-l-2 border-gray-300 pl-6">
      <p class="text-[16px] text-gray-600 leading-relaxed">
        <span class="font-semibold text-gray-900">一个前提条件值得注意：</span>理想的统一预处理应作用于全动态范围原始红外数据，但公开数据集大多已压缩为低动态范围图像，这从源头上限制了预处理的作用空间。
      </p>
    </div>
  </div>

  <div class="absolute bottom-4 left-12 right-12 flex justify-between text-[12px] text-gray-400 tracking-wide">
    <span>Fusion or Confusion? · Becker et al. · CVPRW 2025</span>
    <span>11 / 26</span>
  </div>
</div>
`);
