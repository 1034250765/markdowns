window.slideDataMap.set(21, `
<div class="w-[1440px] h-[810px] shadow-2xl relative overflow-hidden slide-bg">
  <div class="w-[1350px] h-[700px] mx-auto my-[40px] flex flex-col items-center justify-center">

    <div class="max-w-4xl text-center">
      <div class="inline-block px-3 py-1 border border-gray-300 text-[13px] tracking-widest text-gray-500 mb-7">
        DAS · 5.4
      </div>
      <h2 class="text-[40px] font-bold text-gray-900 mb-5">DAS 看到的域结构，t-SNE 看不到</h2>
      <p class="text-gray-700 text-[17px] leading-relaxed">
        在 All 池上训练带 DAS 的模型，然后统计两个零样本测试集里检测框被分给了谁。
      </p>
    </div>

    <div class="grid grid-cols-3 gap-12 w-full mt-12">
      <div class="text-left border-t-2 border-gray-900 pt-6">
        <p class="text-[13px] font-mono text-accent-1 tracking-widest mb-3">WIT-UAS（航拍）</p>
        <h3 class="text-[20px] font-semibold text-gray-900 mb-3 leading-snug">检测几乎全部指向<br/>其他航拍训练集</h3>
        <p class="text-[15px] text-gray-600 leading-relaxed">这符合「航拍目标应该像航拍数据」的直觉，也是一次基本的合理性检查。</p>
      </div>
      <div class="text-left border-t-2 border-gray-300 pt-6">
        <p class="text-[13px] font-mono text-accent-1 tracking-widest mb-3">MCNet（地面）</p>
        <h3 class="text-[20px] font-semibold text-gray-900 mb-3 leading-snug">检测主要与<br/>地面训练集相关</h3>
        <p class="text-[15px] text-gray-600 leading-relaxed">与 WIT-UAS 形成镜像结果，进一步印证「地面 / 航拍」是主导性的域维度。</p>
      </div>
      <div class="text-left border-t-2 border-gray-300 pt-6">
        <p class="text-[13px] font-mono text-gray-400 tracking-widest mb-3">对照：t-SNE 图</p>
        <h3 class="text-[20px] font-semibold text-gray-900 mb-3 leading-snug">不同域的簇<br/>看起来彼此靠得很近</h3>
        <p class="text-[15px] text-gray-600 leading-relaxed">在低维嵌入里，地面与航拍的簇并没有明显分离，因此看不出 DAS 揭示的那条界线。</p>
      </div>
    </div>

    <div class="mt-11 max-w-4xl w-full border-t border-gray-200 pt-6">
      <p class="text-[16px] text-gray-600 leading-relaxed text-center">
        <span class="font-semibold text-gray-900">结论：</span>两种工具的信息并不重叠——t-SNE 看「图像像不像」，DAS 看「模型认为它来自哪」。
        也正因为如此，<b>DAS 的亲和度分布可作为裁剪数据池的依据</b>：指向少、分布集中的数据集，多半是冗余的。
      </p>
    </div>
  </div>

  <div class="absolute bottom-4 left-12 right-12 flex justify-between text-[12px] text-gray-400 tracking-wide">
    <span>Fusion or Confusion? · Becker et al. · CVPRW 2025</span>
    <span>21 / 26</span>
  </div>
</div>
`);
