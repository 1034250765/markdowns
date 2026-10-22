<Slide padding={0}>
    <Box style={{
        width: '100%', height: '100%',
        background: 'linear-gradient(135deg, #1A2230 0%, #1E4FA8 50%, #5B7FCE 100%)',
        paddingLeft: 64, paddingRight: 64,
        paddingTop: 48, paddingBottom: 48,
        justifyContent: 'center',
        alignItems: 'center',
    }}>
        <Box style={{
            width: '100%', maxWidth: 960,
            gap: 24,
            alignItems: 'center',
        }}>
            <Box style={{
                paddingLeft: 16, paddingRight: 16,
                paddingTop: 8, paddingBottom: 8,
                borderRadius: 16,
                background: 'rgba(255,255,255,0.18)',
                border: '1px solid rgba(255,255,255,0.4)',
            }}>
                <Text style={{ color: '#FFC247', fontSize: 14, fontWeight: 'bold', letterSpacing: 4 }}>CHAPTER 05 · 结论</Text>
            </Box>
            <Text style={{
                color: '#FFFFFF', fontSize: 64,
                fontWeight: 'bold', textAlign: 'center',
                lineHeight: 1.3,
            }}>
                把 OOD 评测<br />推到真正困难的任务上
            </Text>
            <Box style={{
                width: 100, height: 4,
                borderRadius: 2, background: '#FFC247',
            }} />
            <Box style={{
                width: '100%', maxWidth: 880,
                paddingLeft: 32, paddingRight: 32,
                paddingTop: 24, paddingBottom: 24,
                borderRadius: 18,
                background: 'rgba(255,255,255,0.10)',
                border: '1.5px solid rgba(255,255,255,0.32)',
                gap: 14,
            }}>
                <Text style={{ color: '#FFC247', fontSize: 13, fontWeight: 'bold', letterSpacing: 2 }}>TWO KEY CONCLUSIONS</Text>
                <Text style={{ color: '#FFFFFF', fontSize: 22, lineHeight: 1.5 }}>
                    <span style={{ fontWeight: 'bold' }}>①</span> 目标检测器在 IID 上变强，并不等于在 OOD 上也稳——head 优化与训练策略是关键。
                </Text>
                <Text style={{ color: '#FFFFFF', fontSize: 22, lineHeight: 1.5 }}>
                    <span style={{ fontWeight: 'bold' }}>②</span> 多模态大模型的 ICL 是双刃剑——同分布下能帮忙，错配时反而把模型带偏。
                </Text>
            </Box>
            <Text style={{ color: '#FFFFFF', fontSize: 16, lineHeight: 1.6, opacity: 0.85, textAlign: 'center', maxWidth: 720 }}>
                COUNTS 让我们第一次能够系统考察目标检测和 grounding 在自然分布偏移下的真实能力——
                这是推动鲁棒视觉系统走向真实部署的关键基础设施。
            </Text>
        </Box>
    </Box>
    <Box style={{
        position: 'absolute', bottom: 0, left: 0, width: '100%', height: 36,
        background: 'rgba(0,0,0,0.25)',
        flexDirection: 'row', alignItems: 'center',
        justifyContent: 'space-between',
        paddingLeft: 40, paddingRight: 40,
    }}>
        <Text style={{ color: '#FFFFFF', fontSize: 12, letterSpacing: 1, opacity: 0.7 }}>COUNTS · 结论</Text>
        <Text style={{ color: '#FFFFFF', fontSize: 12, opacity: 0.7 }}>16 / 18</Text>
    </Box>
</Slide>
