<Slide padding={32}>
    <Box style={{
        width: '100%',
        height: 64,
        position: 'absolute',
        top: 0,
        left: 0,
        background: 'linear-gradient(135deg, #1E4FA8 0%, #5B7FCE 60%, #2BC5C0 100%)',
    }} />
    <Box style={{
        width: 140,
        height: 36,
        paddingLeft: 16,
        justifyContent: 'center',
        position: 'absolute',
        top: 14,
        left: 32,
        borderRadius: 18,
        background: 'rgba(255,255,255,0.18)',
        border: '1px solid rgba(255,255,255,0.4)',
    }}>
        <Text style={{ color: '#FFFFFF', fontSize: 14, fontWeight: 'bold', letterSpacing: 2 }}>COUNTS · CVPR</Text>
    </Box>
    <Box style={{
        paddingTop: 16,
        paddingBottom: 16,
        gap: 8,
        alignItems: 'flex-start',
        justifyContent: 'flex-start',
    }}>
        <Text style={{ color: '#1E4FA8', fontSize: 14, letterSpacing: 4, fontWeight: 600 }}>PAPER READING · DISTRIBUTION SHIFTS</Text>
        <Text style={{
            fontSize: 64,
            fontWeight: 'bold',
            color: '#1A2230',
            lineHeight: 1.1,
            backgroundImage: 'linear-gradient(135deg, #1E4FA8 0%, #5B7FCE 60%, #2BC5C0 100%)',
            backgroundClip: 'text',
        }}>
            分布偏移下评测检测器与多模态大模型
        </Text>
        <Box style={{
            width: 540,
            marginTop: 8,
            paddingTop: 12,
            paddingBottom: 12,
            paddingLeft: 16,
            paddingRight: 16,
            borderLeft: '4px solid #2BC5C0',
            background: '#F7F9FC',
            borderRadius: 4,
        }}>
            <Text style={{ color: '#1A2230', fontSize: 20, fontStyle: 'italic', fontFamily: 'Georgia, serif', lineHeight: 1.5 }}>
                COUNTS: Benchmarking Object Detectors and<br />Multimodal LLMs under Distribution Shifts
            </Text>
        </Box>
    </Box>
    <Box style={{
        width: '100%',
        paddingLeft: 48,
        paddingRight: 48,
        marginTop: 32,
        gap: 16,
        justifyContent: 'flex-start',
        alignItems: 'center',
    }}>
        <Box style={{
            paddingTop: 12,
            paddingBottom: 12,
            paddingLeft: 22,
            paddingRight: 22,
            borderRadius: 8,
            background: '#FFFFFF',
            border: '1.5px solid #1E4FA8',
            flexDirection: 'row',
            alignItems: 'center',
            gap: 10,
        }}>
            <Box style={{ width: 8, height: 8, borderRadius: 4, background: '#FFC247' }} />
            <Text style={{ color: '#1E4FA8', fontSize: 14, fontWeight: 600 }}>arXiv:2504.10158</Text>
        </Box>
        <Box style={{
            paddingTop: 12,
            paddingBottom: 12,
            paddingLeft: 22,
            paddingRight: 22,
            borderRadius: 8,
            background: '#FFFFFF',
            border: '1px solid #2BC5C0',
            flexDirection: 'row',
            alignItems: 'center',
            gap: 10,
        }}>
            <Box style={{ width: 8, height: 8, borderRadius: 4, background: '#2BC5C0' }} />
            <Text style={{ color: '#1A2230', fontSize: 14 }}>清华大学计算机科学系</Text>
        </Box>
        <Box style={{
            paddingTop: 12,
            paddingBottom: 12,
            paddingLeft: 22,
            paddingRight: 22,
            borderRadius: 8,
            background: '#FFFFFF',
            border: '1px solid #D6DCE5',
        }}>
            <Text style={{ color: '#4A5568', fontSize: 14 }}>Jiansheng Li 等 · 2025</Text>
        </Box>
    </Box>
    <Box style={{
        width: '100%',
        flexDirection: 'row',
        alignItems: 'flex-end',
        justifyContent: 'space-between',
        marginTop: 36,
    }}>
        <Box style={{ gap: 6 }}>
            <Text style={{ color: '#4A5568', fontSize: 16, fontWeight: 600 }}>汇报人 · 实验室</Text>
            <Text style={{ color: '#8B97A8', fontSize: 13 }}>2026 年 8 月 · 论文 Reading 小组</Text>
        </Box>
        <Box style={{
            width: 240,
            height: 6,
            borderRadius: 3,
            background: 'linear-gradient(90deg, #1E4FA8 0%, #5B7FCE 50%, #FFC247 100%)',
        }} />
    </Box>
    <Box style={{
        position: 'absolute',
        bottom: 0,
        left: 0,
        width: '100%',
        height: 36,
        background: 'linear-gradient(135deg, #1E4FA8 0%, #5B7FCE 60%, #2BC5C0 100%)',
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        paddingLeft: 32,
        paddingRight: 32,
    }}>
        <Text style={{ color: '#FFFFFF', fontSize: 12, letterSpacing: 1 }}>COMMON OBJECTS UNDER DISTRIBUTION SHIFTS</Text>
        <Text style={{ color: '#FFFFFF', fontSize: 12 }}>01 / 18</Text>
    </Box>
</Slide>
