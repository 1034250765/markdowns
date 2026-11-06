window.slideDataMap.set(9, `
<div class="w-[1440px] h-[810px] shadow-2xl relative overflow-hidden slide-bg">
  <div class="w-[1350px] h-[700px] mx-auto my-[40px] flex flex-col justify-center">

    <div class="mb-11">
      <h2 class="text-[38px] font-light text-gray-900 mb-4">第二步：按「平台高度」切分数据池</h2>
      <div class="w-40 h-1 bg-primary mb-4"></div>
      <p class="text-[16px] text-gray-500">检测器与训练配置完全一致，只改变训练数据的组成方式</p>
    </div>

    <div class="grid grid-cols-3 gap-14">

      <div class="border-t-2 border-gray-900 pt-7">
        <div class="text-[64px] font-thin text-gray-200 leading-none mb-4">01</div>
        <h3 class="text-[26px] font-semibold text-gray-900 mb-2">Ground 池</h3>
        <p class="text-[14px] font-mono text-accent-1 tracking-wide mb-4">FLIR v2 + M3FD</p>
        <p class="text-gray-600 text-[16px] leading-relaxed mb-4">
          两个地面视角数据集：车载与执法记录仪拍摄，目标近、尺度大、细节丰富。
        </p>
        <div class="flex gap-8 text-[15px]">
          <div><span class="block text-[24px] font-semibold text-gray-900">12,210</span><span class="text-gray-400">训练图像</span></div>
          <div><span class="block text-[24px] font-semibold text-gray-900">89,029</span><span class="text-gray-400">训练实例</span></div>
        </div>
      </div>

      <div class="border-t-2 border-gray-300 pt-7">
        <div class="text-[64px] font-thin text-gray-200 leading-none mb-4">02</div>
        <h3 class="text-[26px] font-semibold text-gray-900 mb-2">Aerial 池</h3>
        <p class="text-[14px] font-mono text-accent-1 tracking-wide mb-4">DroneVehicle + TrafficNight + HIT-UAV</p>
        <p class="text-gray-600 text-[16px] leading-relaxed mb-4">
          三个中空无人机视角数据集：俯视、目标小、密度高，背景以道路与停车场为主。
        </p>
        <div class="flex gap-8 text-[15px]">
          <div><span class="block text-[24px] font-semibold text-gray-900">8,267</span><span class="text-gray-400">训练图像</span></div>
          <div><span class="block text-[24px] font-semibold text-gray-900">150,908</span><span class="text-gray-400">训练实例</span></div>
        </div>
      </div>

      <div class="border-t-2 border-gray-300 pt-7">
        <div class="text-[64px] font-thin text-gray-200 leading-none mb-4">03</div>
        <h3 class="text-[26px] font-semibold text-gray-900 mb-2">All 池</h3>
        <p class="text-[14px] font-mono text-accent-1 tracking-wide mb-4">5 个数据集全部合并</p>
        <p class="text-gray-600 text-[16px] leading-relaxed mb-4">
          地面 + 航拍混合，是「数据越多越好」这一直觉的直接检验对象。
        </p>
        <div class="flex gap-8 text-[15px]">
          <div><span class="block text-[24px] font-semibold text-gray-900">20,477</span><span class="text-gray-400">训练图像</span></div>
          <div><span class="block text-[24px] font-semibold text-gray-900">239,937</span><span class="text-gray-400">训练实例</span></div>
        </div>
      </div>
    </div>

    <div class="mt-11 bg-gray-50 border border-gray-200 px-6 py-4">
      <p class="text-[15px] text-gray-600 leading-relaxed">
        <span class="font-semibold text-gray-800">对照基线：</span>5 个训练数据集各自的单数据集模型。<span class="mx-3 text-gray-300">|</span>
        <span class="font-semibold text-gray-800">零样本协议：</span>MCNet（地面）与 WIT-UAS（航拍）完全不参与训练，只用于测试。
      </p>
    </div>
  </div>

  <div class="absolute bottom-4 left-12 right-12 flex justify-between text-[12px] text-gray-400 tracking-wide">
    <span>Fusion or Confusion? · Becker et al. · CVPRW 2025</span>
    <span>09 / 26</span>
  </div>
</div>
`);
