<Slide padding={0}>
    <Box style={{
        width: '100%', height: 80,
        flexDirection: 'row', alignItems: 'center',
        paddingLeft: 40, paddingRight: 40,
        background: '#FFFFFF',
        borderBottom: '2px solid #F0F5FC',
    }}>
        <Box style={{ width: 40, height: 4, borderRadius: 2, background: '#2BC5C0', marginRight: 14 }} />
        <Text style={{ color: '#2BC5C0', fontSize: 14, fontWeight: 'bold', letterSpacing: 2 }}>CHAPTER 04 · OODG 基准设计</Text>
        <Box style={{ flex: 1 }} />
        <Text style={{ color: '#8B97A8', fontSize: 13 }}>页 12 / 18</Text>
    </Box>
    <Box style={{
        width: '100%', height: 560,
        paddingLeft: 48, paddingRight: 48,
        paddingTop: 22, paddingBottom: 22,
        gap: 16,
    }}>
        <Box style={{ width: '100%', gap: 6 }}>
            <Text style={{ color: '#1E4FA8', fontSize: 13, fontWeight: 'bold', letterSpacing: 3 }}>5 SETTINGS × 3 TASKS</Text>
            <Text style={{ color: '#1A2230', fontSize: 30, fontWeight: 'bold' }}>
                OODG · 在 ICL 阶段定义 OOD 偏移
            </Text>
            <Text style={{ color: '#4A5568', fontSize: 14, lineHeight: 1.55 }}>
                多模态大模型训练数据通常不透明，因此 OODG 把"分布偏移"定义为
                <span style={{ fontWeight: 'bold', color: '#1E4FA8' }}>ICE（上下文示例）与测试样本</span>之间的差异。
            </Text>
        </Box>
        <Box style={{ width: '100%', flexDirection: 'row', gap: 12 }}>
            {[
                { tag: 'T1', title: 'Visual Grounding', desc: '高亮边界框后模型返回视觉概念', color: '#1E4FA8' },
                { tag: 'T2', title: 'Recognition & Localization', desc: '模型输出指定目标的边界框坐标', color: '#2BC5C0' },
                { tag: 'T3', title: 'Visual & Semantic Mapping', desc: '颜色框与文本描述的跨模态对齐', color: '#FF8A4C' },
            ].map((t, idx) => (
                <Box key={idx} style={{
                    flex: 1,
                    paddingTop: 14, paddingBottom: 14,
                    paddingLeft: 18, paddingRight: 18,
                    borderRadius: 12,
                    background: '#F0F5FC',
                    border: `1.5px solid ${t.color}`,
                    gap: 6,
                }}>
                    <Box style={{ flexDirection: 'row', alignItems: 'center', gap: 8 }}>
                        <Box style={{
                            paddingLeft: 8, paddingRight: 8,
                            paddingTop: 3, paddingBottom: 3,
                            borderRadius: 6, background: t.color,
                        }}>
                            <Text style={{ color: '#FFFFFF', fontSize: 11, fontWeight: 'bold' }}>{t.tag}</Text>
                        </Box>
                        <Text style={{ color: '#1A2230', fontSize: 15, fontWeight: 'bold' }}>{t.title}</Text>
                    </Box>
                    <Text style={{ color: '#4A5568', fontSize: 12, lineHeight: 1.4 }}>{t.desc}</Text>
                </Box>
            ))}
        </Box>
        <Box style={{ width: '100%', flex: 1, gap: 10 }}>
            <Text style={{ color: '#8B97A8', fontSize: 12, fontWeight: 'bold', letterSpacing: 2 }}>5 种评测设置</Text>
            {[
                {
                    n: '①', t: 'Zero-shot Generalization',
                    d: '不提供示例，考察模型跨多个域识别视觉概念的能力——基线水准。',
                    c: '#1E4FA8', bg: '#E8EFF8',
                },
                {
                    n: '②', t: 'IID ICL',
                    d: 'ICE 与测试样本同分布，考察模型在 ICL 下能否提升。',
                    c: '#5B7FCE', bg: '#DCE7F8',
                },
                {
                    n: '③', t: 'Covariate Shift',
                    d: 'ICE 与测试来自不同域，自然发生的输入分布变化。',
                    c: '#FF8A4C', bg: '#FFEAD8',
                },
                {
                    n: '④', t: 'Label Shift',
                    d: 'ICE 与测试之间存在标签分布偏移，测试时未知类别分布。',
                    c: '#FFC247', bg: '#FFEFC9',
                },
                {
                    n: '⑤', t: 'Spurious Correlation',
                    d: 'ICE 中图像特征-标签形成伪相关（如昏暗 → 猫），考察是否被误导。',
                    c: '#2BC5C0', bg: '#DAF6F4',
                },
            ].map((row, idx) => (
                <Box key={idx} style={{
                    width: '100%',
                    flexDirection: 'row', alignItems: 'center',
                    paddingLeft: 16, paddingRight: 16,
                    paddingTop: 10, paddingBottom: 10,
                    borderRadius: 10,
                    background: '#FFFFFF',
                    border: '1px solid #E5E7EB',
                    gap: 14,
                }}>
                    <Box style={{
                        width: 36, height: 36, borderRadius: 18,
                        background: row.c,
                        justifyContent: 'center', alignItems: 'center',
                    }}>
                        <Text style={{ color: '#FFFFFF', fontSize: 14, fontWeight: 'bold' }}>{row.n}</Text>
                    </Box>
                    <Text style={{ color: '#1A2230', fontSize: 16, fontWeight: 'bold', width: 230 }}>{row.t}</Text>
                    <Text style={{ color: '#4A5568', fontSize: 13, flex: 1, lineHeight: 1.5 }}>{row.d}</Text>
                    <Box style={{
                        paddingLeft: 10, paddingRight: 10,
                        paddingTop: 4, paddingBottom: 4,
                        borderRadius: 8, background: row.bg,
                    }}>
                        <Text style={{ color: row.c, fontSize: 11, fontWeight: 'bold', letterSpacing: 1 }}>SETTING {row.n[0]}</Text>
                    </Box>
                </Box>
            ))}
        </Box>
    </Box>
    <Box style={{
        position: 'absolute', bottom: 0, left: 0, width: '100%', height: 32,
        background: '#F7F9FC',
        flexDirection: 'row', alignItems: 'center',
        justifyContent: 'space-between',
        paddingLeft: 40, paddingRight: 40,
        borderTop: '1px solid #E5E7EB',
    }}>
        <Text style={{ color: '#8B97A8', fontSize: 12 }}>COUNTS · 跨域目标检测与多模态 grounding</Text>
        <Text style={{ color: '#4A5568', fontSize: 12 }}>12 / 18</Text>
    </Box>
</Slide>
