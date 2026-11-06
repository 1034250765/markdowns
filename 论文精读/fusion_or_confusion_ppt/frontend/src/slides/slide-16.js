window.slideDataMap.set(16, `
<div class="w-[1440px] h-[810px] shadow-2xl relative overflow-hidden slide-bg">
  <div class="w-[1350px] h-[700px] mx-auto my-[40px] flex flex-col items-center justify-center">

    <div class="max-w-4xl text-center">
      <div class="inline-block px-3 py-1 border border-gray-300 text-[13px] tracking-widest text-gray-500 mb-7">
        结论 03 · DOMAIN GAP
      </div>
      <h2 class="text-[40px] font-bold text-gray-900 mb-5">地面与航拍之间存在结构性域差</h2>
      <p class="text-gray-700 text-[17px] leading-relaxed">
        用一类数据训练的模型去测另一类，性能不是「下降」，而是塌到接近随机水平——两者相差两个数量级。
      </p>
    </div>

    <div class="grid grid-cols-4 gap-10 w-full mt-12">
      <div class="text-center">
        <div class="text-[46px] font-light text-gray-900 leading-none mb-3">0.002</div>
        <p class="text-[14px] text-gray-500 leading-relaxed">Ground → DroneVehicle</p>
      </div>
      <div class="text-center">
        <div class="text-[46px] font-light text-gray-900 leading-none mb-3">0.004</div>
        <p class="text-[14px] text-gray-500 leading-relaxed">Ground → HIT-UAV</p>
      </div>
      <div class="text-center">
        <div class="text-[46px] font-light text-gray-900 leading-none mb-3">0.008</div>
        <p class="text-[14px] text-gray-500 leading-relaxed">Aerial → FLIR (v2)</p>
      </div>
      <div class="text-center">
        <div class="text-[46px] font-light text-gray-900 leading-none mb-3">0.008</div>
        <p class="text-[14px] text-gray-500 leading-relaxed">Aerial → M3FD</p>
      </div>
    </div>

    <div class="mt-12 max-w-4xl w-full">
      <p class="text-[15px] text-gray-500 mb-3 tracking-wide">差异来源</p>
      <div class="flex flex-wrap gap-3">
        <span class="px-4 py-2 bg-gray-50 border border-gray-200 text-[15px] text-gray-700">相机高度</span>
        <span class="px-4 py-2 bg-gray-50 border border-gray-200 text-[15px] text-gray-700">目标尺度与长宽比</span>
        <span class="px-4 py-2 bg-gray-50 border border-gray-200 text-[15px] text-gray-700">观察角度</span>
        <span class="px-4 py-2 bg-gray-50 border border-gray-200 text-[15px] text-gray-700">背景结构</span>
        <span class="px-4 py-2 bg-gray-50 border border-gray-200 text-[15px] text-gray-700">传感器与图像处理</span>
      </div>
    </div>

    <div class="mt-9 max-w-4xl text-center border-t border-gray-200 pt-6">
      <p class="text-[17px] text-gray-700 leading-relaxed">
        因此，<b>融合之前应先按视角、设备或场景划分域</b>；否则「加数据」只是给模型增加噪声。
      </p>
    </div>
  </div>

  <div class="absolute bottom-4 left-12 right-12 flex justify-between text-[12px] text-gray-400 tracking-wide">
    <span>Fusion or Confusion? · Becker et al. · CVPRW 2025</span>
    <span>16 / 26</span>
  </div>
</div>
`);
