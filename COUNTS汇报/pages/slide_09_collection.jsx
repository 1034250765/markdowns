<Slide padding={0}>
    <Box style={{
        width: '100%', height: 80,
        flexDirection: 'row', alignItems: 'center',
        paddingLeft: 40, paddingRight: 40,
        background: '#FFFFFF',
        borderBottom: '2px solid #F0F5FC',
    }}>
        <Box style={{ width: 40, height: 4, borderRadius: 2, background: '#2BC5C0', marginRight: 14 }} />
        <Text style={{ color: '#2BC5C0', fontSize: 14, fontWeight: 'bold', letterSpacing: 2 }}>CHAPTER 03 · 数据收集流程</Text>
        <Box style={{ flex: 1 }} />
        <Text style={{ color: '#8B97A8', fontSize: 13 }}>页 09 / 18</Text>
    </Box>
    <Box style={{
        width: '100%', height: 560,
        paddingLeft: 48, paddingRight: 48,
        paddingTop: 26, paddingBottom: 26,
        gap: 22,
    }}>
        <Box style={{ width: '100%', gap: 8 }}>
            <Text style={{ color: '#1E4FA8', fontSize: 13, fontWeight: 'bold', letterSpacing: 3 }}>PIPELINE</Text>
            <Text style={{ color: '#1A2230', fontSize: 32, fontWeight: 'bold' }}>
                三阶段过滤：从 500 万 到 22.2 万张高质量标注
            </Text>
            <Text style={{ color: '#4A5568', fontSize: 15, lineHeight: 1.5 }}>
                自动化筛选 + 双人验证 + 人工复核，三步把噪声过滤到测试级别。
            </Text>
        </Box>
        <Box style={{
            width: '100%', flex: 1,
            flexDirection: 'row', alignItems: 'stretch',
            gap: 14,
        }}>
            {[
                {
                    step: '01',
                    title: '候选筛选',
                    desc: '从 Open Images、Visual Genome、RefCOCO/+/g、Flickr30K、GranD 等公开数据集按预定义域空间初筛。',
                    metric: '500 万+ 候选',
                    color: '#1E4FA8',
                    bg: '#E8EFF8',
                },
                {
                    step: '02',
                    title: '域标签双验',
                    desc: '两位独立标注者共同判定图像所属域，标签一致才保留作为真实域标签。',
                    metric: '双人独立',
                    color: '#5B7FCE',
                    bg: '#DCE7F8',
                },
                {
                    step: '03',
                    title: '随机划分',
                    desc: '每域随机抽 10% 作为测试与验证集；Open Images 等部分样本需重新标注。',
                    metric: '10% 测试验证',
                    color: '#2BC5C0',
                    bg: '#DAF6F4',
                },
                {
                    step: '04',
                    title: '边界框复核',
                    desc: '测试 / 验证集全部经两位标注者独立标注并验证，确保评估可靠。',
                    metric: '23,000 张重标',
                    color: '#FFC247',
                    bg: '#FFEFC9',
                },
            ].map((node, idx) => (
                <Box key={idx} style={{
                    flex: 1, height: '100%',
                    borderRadius: 14,
                    background: '#FFFFFF',
                    border: `1.5px solid ${node.color}`,
                    paddingTop: 20, paddingBottom: 20,
                    paddingLeft: 18, paddingRight: 18,
                    gap: 12,
                    justifyContent: 'space-between',
                }}>
                    <Box style={{ gap: 10 }}>
                        <Box style={{
                            width: 48, height: 48, borderRadius: 24,
                            background: node.color,
                            justifyContent: 'center', alignItems: 'center',
                        }}>
                            <Text style={{ color: '#FFFFFF', fontSize: 20, fontWeight: 'bold' }}>{node.step}</Text>
                        </Box>
                        <Text style={{ color: '#1A2230', fontSize: 20, fontWeight: 'bold' }}>{node.title}</Text>
                        <Text style={{ color: '#4A5568', fontSize: 13, lineHeight: 1.6 }}>{node.desc}</Text>
                    </Box>
                    <Box style={{
                        paddingLeft: 12, paddingRight: 12,
                        paddingTop: 6, paddingBottom: 6,
                        borderRadius: 10,
                        background: node.bg,
                        alignSelf: 'flex-start',
                    }}>
                        <Text style={{ color: node.color, fontSize: 12, fontWeight: 'bold', letterSpacing: 1 }}>{node.metric}</Text>
                    </Box>
                </Box>
            ))}
        </Box>
        <Box style={{
            width: '100%',
            borderRadius: 12,
            background: 'linear-gradient(90deg, #1E4FA8 0%, #2BC5C0 100%)',
            paddingLeft: 22, paddingRight: 22,
            paddingTop: 14, paddingBottom: 14,
            flexDirection: 'row', alignItems: 'center',
            gap: 18,
        }}>
            <Box style={{
                width: 36, height: 36, borderRadius: 18,
                background: 'rgba(255,255,255,0.2)',
                justifyContent: 'center', alignItems: 'center',
            }}>
                <Text style={{ color: '#FFFFFF', fontSize: 18, fontWeight: 'bold' }}>✓</Text>
            </Box>
            <Text style={{ color: '#FFFFFF', fontSize: 18, lineHeight: 1.5, flex: 1 }}>
                <span style={{ fontWeight: 'bold' }}>自然图像 + 全程人工把关</span>——避免合成扰动的"伪迁移"，让评估反映真实部署挑战。
            </Text>
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
        <Text style={{ color: '#4A5568', fontSize: 12 }}>09 / 18</Text>
    </Box>
</Slide>
