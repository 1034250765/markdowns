<Slide padding={0}>
    <Box style={{
        width: '100%',
        height: 88,
        background: 'linear-gradient(90deg, #1E4FA8 0%, #5B7FCE 100%)',
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        paddingLeft: 40,
        paddingRight: 40,
    }}>
        <Text style={{ color: '#FFFFFF', fontSize: 14, letterSpacing: 3 }}>COUNTS · 目录</Text>
        <Text style={{ color: '#FFFFFF', fontSize: 14 }}>CATALOG</Text>
    </Box>
    <Box style={{
        width: '100%',
        height: 540,
        flexDirection: 'row',
        paddingLeft: 40,
        paddingRight: 40,
        paddingTop: 32,
        paddingBottom: 32,
    }}>
        <Box style={{
            width: '32%',
            height: '100%',
            justifyContent: 'space-between',
            alignItems: 'flex-start',
        }}>
            <Box style={{ gap: 16 }}>
                <Text style={{ color: '#1E4FA8', fontSize: 16, letterSpacing: 4, fontWeight: 'bold' }}>CHAPTER 0</Text>
                <Text style={{
                    color: '#1A2230',
                    fontSize: 96,
                    fontWeight: 'bold',
                    lineHeight: 1,
                    backgroundImage: 'linear-gradient(135deg, #1E4FA8 0%, #5B7FCE 100%)',
                    backgroundClip: 'text',
                }}>目录</Text>
                <Text style={{ color: '#8B97A8', fontSize: 18, fontFamily: 'Georgia, serif', fontStyle: 'italic' }}>Catalog</Text>
            </Box>
            <Box style={{
                paddingLeft: 18,
                paddingRight: 18,
                paddingTop: 10,
                paddingBottom: 10,
                borderRadius: 18,
                background: '#FFC247',
                flexDirection: 'row',
                alignItems: 'center',
                gap: 8,
            }}>
                <Text style={{ color: '#1A2230', fontSize: 16, fontWeight: 'bold' }}>5</Text>
                <Text style={{ color: '#1A2230', fontSize: 13 }}>个章节 · 共 18 页</Text>
            </Box>
        </Box>
        <Box style={{
            width: '68%',
            height: '100%',
            gap: 18,
        }}>
            {[
                { id: '01', title: '研究动机', subtitle: 'OOD 泛化是真实部署的关键挑战', count: '3 页', color: '#1E4FA8' },
                { id: '02', title: '现有研究的不足', subtitle: '细粒度 OOD 评测基准的缺位', count: '2 页', color: '#5B7FCE' },
                { id: '03', title: 'COUNTS 数据集', subtitle: '首个同时支持检测与 grounding 的 OOD 基准', count: '4 页', color: '#2BC5C0' },
                { id: '04', title: 'O(OD)² 与 OODG 基准 + 实验', subtitle: '检测器 + MLLM grounding 的系统评测', count: '6 页', color: '#FF8A4C' },
                { id: '05', title: '结论与应用', subtitle: 'ICL 双刃剑 · 鲁棒视觉系统未来', count: '3 页', color: '#FFC247' },
            ].map((item, idx) => (
                <Box key={idx} style={{
                    width: '100%',
                    height: 72,
                    borderRadius: 12,
                    background: '#FFFFFF',
                    border: '1.5px solid #E5E7EB',
                    flexDirection: 'row',
                    alignItems: 'center',
                    paddingLeft: 18,
                    paddingRight: 18,
                    gap: 18,
                }}>
                    <Box style={{
                        width: 56,
                        height: 56,
                        borderRadius: 10,
                        background: item.color,
                        justifyContent: 'center',
                        alignItems: 'center',
                    }}>
                        <Text style={{ color: '#FFFFFF', fontSize: 22, fontWeight: 'bold' }}>{item.id}</Text>
                    </Box>
                    <Box style={{ flex: 1, gap: 4 }}>
                        <Text style={{ color: '#1A2230', fontSize: 22, fontWeight: 'bold' }}>{item.title}</Text>
                        <Text style={{ color: '#4A5568', fontSize: 14 }}>{item.subtitle}</Text>
                    </Box>
                    <Box style={{
                        paddingLeft: 12,
                        paddingRight: 12,
                        paddingTop: 6,
                        paddingBottom: 6,
                        borderRadius: 12,
                        background: '#F0F5FC',
                    }}>
                        <Text style={{ color: '#1E4FA8', fontSize: 13, fontWeight: 600 }}>{item.count}</Text>
                    </Box>
                </Box>
            ))}
        </Box>
    </Box>
    <Box style={{
        position: 'absolute',
        bottom: 0,
        left: 0,
        width: '100%',
        height: 32,
        background: '#F7F9FC',
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        paddingLeft: 40,
        paddingRight: 40,
        borderTop: '1px solid #E5E7EB',
    }}>
        <Text style={{ color: '#8B97A8', fontSize: 12 }}>COUNTS · 跨域目标检测与多模态 grounding</Text>
        <Text style={{ color: '#4A5568', fontSize: 12 }}>02 / 18</Text>
    </Box>
</Slide>
