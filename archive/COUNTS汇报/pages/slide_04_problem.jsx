<Slide padding={0}>
    <Box style={{
        width: '100%',
        height: 80,
        flexDirection: 'row',
        alignItems: 'center',
        paddingLeft: 40,
        paddingRight: 40,
        background: '#FFFFFF',
        borderBottom: '2px solid #F0F5FC',
    }}>
        <Box style={{ width: 40, height: 4, borderRadius: 2, background: '#1E4FA8', marginRight: 14 }} />
        <Text style={{ color: '#1E4FA8', fontSize: 14, fontWeight: 'bold', letterSpacing: 2 }}>CHAPTER 01 · 研究问题</Text>
        <Box style={{ flex: 1 }} />
        <Text style={{ color: '#8B97A8', fontSize: 13 }}>页 04 / 18</Text>
    </Box>
    <Box style={{
        width: '100%',
        height: 560,
        paddingLeft: 48,
        paddingRight: 48,
        paddingTop: 28,
        paddingBottom: 28,
        flexDirection: 'row',
        gap: 32,
    }}>
        <Box style={{ width: '26%', height: '100%', gap: 14, justifyContent: 'flex-start' }}>
            <Text style={{ color: '#1E4FA8', fontSize: 14, fontWeight: 'bold', letterSpacing: 3 }}>BACKGROUND</Text>
            <Text style={{ color: '#1A2230', fontSize: 38, fontWeight: 'bold', lineHeight: 1.2 }}>
                为什么<br />OOD 泛化<br />如此重要？
            </Text>
            <Box style={{ width: 60, height: 4, borderRadius: 2, background: '#2BC5C0', marginTop: 6 }} />
            <Text style={{ color: '#4A5568', fontSize: 14, lineHeight: 1.5, marginTop: 10 }}>
                一旦训练数据与真实世界分布不再同分布，
                模型就会从「可用」跌到「不可信」。
            </Text>
        </Box>
        <Box style={{ width: '70%', height: '100%', gap: 18 }}>
            {[
                {
                    tag: 'REAL-WORLD RISK',
                    title: '真实部署中检测器会显著降级',
                    desc: '现有目标检测器在 COCO 等 IID 基准表现强劲，但遇到雪、昏暗、逆光等场景时性能明显下降，难以满足自动驾驶、监控等真实场景要求。',
                    color: '#1E4FA8',
                    bg: '#E8EFF8',
                    icon: 'A',
                },
                {
                    tag: 'MLLM TRAP',
                    title: 'MLLM 在偏置示例下被带偏',
                    desc: '多模态大模型在 Zero-shot 与 IID 上下文示例下表现稳健，但当示例分布与测试样本分布错配时，模型可能学到伪相关而严重降级。',
                    color: '#FF8A4C',
                    bg: '#FFEAD8',
                    icon: 'B',
                },
                {
                    tag: 'GROUNDING GAP',
                    title: 'Grounding 评测尚未系统化',
                    desc: 'grounding（把文本描述对应到图像具体区域）是细粒度视觉理解关键，但此前 OOD 评测极少覆盖这一任务，缺少合适基准。',
                    color: '#2BC5C0',
                    bg: '#DAF6F4',
                    icon: 'C',
                },
            ].map((c, idx) => (
                <Box key={idx} style={{
                    width: '100%',
                    height: 156,
                    borderRadius: 14,
                    background: '#FFFFFF',
                    border: '1.5px solid #E5E7EB',
                    flexDirection: 'row',
                    overflow: 'hidden',
                }}>
                    <Box style={{
                        width: 88,
                        height: '100%',
                        background: c.color,
                        justifyContent: 'center',
                        alignItems: 'center',
                    }}>
                        <Text style={{ color: '#FFFFFF', fontSize: 56, fontWeight: 'bold' }}>{c.icon}</Text>
                    </Box>
                    <Box style={{ flex: 1, paddingTop: 18, paddingBottom: 18, paddingLeft: 22, paddingRight: 22, gap: 8 }}>
                        <Box style={{
                            paddingLeft: 10,
                            paddingRight: 10,
                            paddingTop: 4,
                            paddingBottom: 4,
                            borderRadius: 8,
                            background: c.bg,
                            alignSelf: 'flex-start',
                        }}>
                            <Text style={{ color: c.color, fontSize: 11, fontWeight: 'bold', letterSpacing: 2 }}>{c.tag}</Text>
                        </Box>
                        <Text style={{ color: '#1A2230', fontSize: 22, fontWeight: 'bold', lineHeight: 1.3 }}>{c.title}</Text>
                        <Text style={{ color: '#4A5568', fontSize: 14, lineHeight: 1.5 }}>{c.desc}</Text>
                    </Box>
                </Box>
            ))}
        </Box>
    </Box>
    <Box style={{
        position: 'absolute',
        bottom: 0, left: 0, width: '100%', height: 32,
        background: '#F7F9FC',
        flexDirection: 'row', alignItems: 'center',
        justifyContent: 'space-between',
        paddingLeft: 40, paddingRight: 40,
        borderTop: '1px solid #E5E7EB',
    }}>
        <Text style={{ color: '#8B97A8', fontSize: 12 }}>COUNTS · 跨域目标检测与多模态 grounding</Text>
        <Text style={{ color: '#4A5568', fontSize: 12 }}>04 / 18</Text>
    </Box>
</Slide>
