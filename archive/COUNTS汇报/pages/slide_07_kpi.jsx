<Slide padding={0}>
    <Box style={{
        width: '100%', height: 80,
        flexDirection: 'row', alignItems: 'center',
        paddingLeft: 40, paddingRight: 40,
        background: '#FFFFFF',
        borderBottom: '2px solid #F0F5FC',
    }}>
        <Box style={{ width: 40, height: 4, borderRadius: 2, background: '#2BC5C0', marginRight: 14 }} />
        <Text style={{ color: '#2BC5C0', fontSize: 14, fontWeight: 'bold', letterSpacing: 2 }}>CHAPTER 03 · COUNTS 关键数字</Text>
        <Box style={{ flex: 1 }} />
        <Text style={{ color: '#8B97A8', fontSize: 13 }}>页 07 / 18</Text>
    </Box>
    <Box style={{
        width: '100%', height: 560,
        paddingLeft: 48, paddingRight: 48,
        paddingTop: 24, paddingBottom: 24,
        flexDirection: 'row', gap: 32,
    }}>
        <Box style={{ width: '56%', height: '100%' }}>
            <Box style={{ width: '100%', height: '100%', gap: 14 }}>
                <Box style={{ width: '100%', height: '100%', gap: 18 }}>
                    {[
                        { num: '222,234', label: '图像总数', note: '全数据 246,983，含训练/测试/验证', color: '#1E4FA8' },
                        { num: '1,196,114', label: '带标注边界框', note: '细粒度目标级标注', color: '#5B7FCE' },
                        { num: '35', label: '目标类别', note: '覆盖日常常见物体', color: '#2BC5C0' },
                        { num: '14', label: '自然分布域', note: '互相独立且场景常见', color: '#FF8A4C' },
                    ].map((kpi, idx) => (
                        <Box key={idx} style={{
                            width: '100%',
                            height: 110,
                            borderRadius: 14,
                            background: '#FFFFFF',
                            border: '1.5px solid #E5E7EB',
                            paddingLeft: 22, paddingRight: 22,
                            paddingTop: 16, paddingBottom: 16,
                            flexDirection: 'row', alignItems: 'center',
                            gap: 20,
                        }}>
                            <Box style={{ width: 6, height: 70, borderRadius: 3, background: kpi.color }} />
                            <Box style={{ flex: 1, gap: 2 }}>
                                <Text style={{ color: '#4A5568', fontSize: 13 }}>{kpi.label}</Text>
                                <Text style={{ color: kpi.color, fontSize: 56, fontWeight: 'bold', lineHeight: 1 }}>{kpi.num}</Text>
                                <Text style={{ color: '#8B97A8', fontSize: 12 }}>{kpi.note}</Text>
                            </Box>
                        </Box>
                    ))}
                </Box>
            </Box>
        </Box>
        <Box style={{ width: '42%', height: '100%', gap: 18 }}>
            <Text style={{ color: '#1E4FA8', fontSize: 13, fontWeight: 'bold', letterSpacing: 3 }}>KEY INSIGHT</Text>
            <Text style={{ color: '#1A2230', fontSize: 28, fontWeight: 'bold', lineHeight: 1.3 }}>
                每个域都包含完整的类别空间
            </Text>
            <Text style={{ color: '#4A5568', fontSize: 15, lineHeight: 1.7 }}>
                这是 COUNTS 与此前基准的一个关键差异——每个分布域都覆盖全部 35 个目标类别。
                这让训练分布和测试分布可以灵活组合，从而构造受控的偏移实验，
                既能评估模型鲁棒性，也能避免域信息泄露造成的虚高指标。
            </Text>
            <Box style={{
                width: '100%', height: 140,
                borderRadius: 14,
                background: 'linear-gradient(135deg, #F0F5FC 0%, #E8EFF8 100%)',
                paddingLeft: 22, paddingRight: 22,
                paddingTop: 18, paddingBottom: 18,
                gap: 12,
            }}>
                <Box style={{
                    paddingLeft: 12, paddingRight: 12,
                    paddingTop: 4, paddingBottom: 4,
                    borderRadius: 10, background: '#1E4FA8',
                    alignSelf: 'flex-start',
                }}>
                    <Text style={{ color: '#FFFFFF', fontSize: 11, fontWeight: 'bold', letterSpacing: 1 }}>SOTA 数据对比</Text>
                </Box>
                <Text style={{ color: '#1A2230', fontSize: 16, lineHeight: 1.5 }}>
                    PACS 仅 9,991 张，VLCS 10,729 张，<span style={{ fontWeight: 'bold', color: '#1E4FA8' }}>COUNTS 是首个跨过 20 万张的检测级 OOD 基准</span>。
                </Text>
                <Box style={{ flexDirection: 'row', gap: 16, marginTop: 4 }}>
                    <Box style={{ flex: 1, gap: 2 }}>
                        <Text style={{ color: '#1E4FA8', fontSize: 22, fontWeight: 'bold' }}>14</Text>
                        <Text style={{ color: '#4A5568', fontSize: 11 }}>vs COCO-O 6 域</Text>
                    </Box>
                    <Box style={{ width: 1, background: '#D6DCE5' }} />
                    <Box style={{ flex: 1, gap: 2 }}>
                        <Text style={{ color: '#1E4FA8', fontSize: 22, fontWeight: 'bold' }}>35 类</Text>
                        <Text style={{ color: '#4A5568', fontSize: 11 }}>vs 主流基准 65-345</Text>
                    </Box>
                    <Box style={{ width: 1, background: '#D6DCE5' }} />
                    <Box style={{ flex: 1, gap: 2 }}>
                        <Text style={{ color: '#1E4FA8', fontSize: 22, fontWeight: 'bold' }}>222k</Text>
                        <Text style={{ color: '#4A5568', fontSize: 11 }}>vs COCO-O 6.7k</Text>
                    </Box>
                </Box>
            </Box>
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
        <Text style={{ color: '#4A5568', fontSize: 12 }}>07 / 18</Text>
    </Box>
</Slide>
