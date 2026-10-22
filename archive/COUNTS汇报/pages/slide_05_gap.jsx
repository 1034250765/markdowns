<Slide padding={0}>
    <Box style={{
        width: '100%',
        height: 80,
        flexDirection: 'row', alignItems: 'center',
        paddingLeft: 40, paddingRight: 40,
        background: '#FFFFFF',
        borderBottom: '2px solid #F0F5FC',
    }}>
        <Box style={{ width: 40, height: 4, borderRadius: 2, background: '#FF8A4C', marginRight: 14 }} />
        <Text style={{ color: '#FF8A4C', fontSize: 14, fontWeight: 'bold', letterSpacing: 2 }}>CHAPTER 01 · 现有研究的不足</Text>
        <Box style={{ flex: 1 }} />
        <Text style={{ color: '#8B97A8', fontSize: 13 }}>页 05 / 18</Text>
    </Box>
    <Box style={{
        width: '100%',
        height: 560,
        paddingLeft: 48, paddingRight: 48,
        paddingTop: 28, paddingBottom: 28,
        gap: 16,
    }}>
        <Box style={{ width: '100%', gap: 10, alignItems: 'flex-start' }}>
            <Text style={{ color: '#1A2230', fontSize: 36, fontWeight: 'bold', lineHeight: 1.2 }}>
                一个关键空缺：细粒度标注的 OOD 基准
            </Text>
            <Text style={{ color: '#4A5568', fontSize: 16, lineHeight: 1.5 }}>
                现成的 OOD 基准要么只做图像分类，要么缺少域多样性，要么需要合成扰动；目标级 grounding 的细粒度评测至今缺失。
            </Text>
        </Box>
        <Box style={{
            width: '100%',
            flex: 1,
            gap: 14,
            flexDirection: 'row',
        }}>
            <Box style={{ flex: 1, height: '100%', gap: 14 }}>
                <Text style={{ color: '#8B97A8', fontSize: 12, fontWeight: 'bold', letterSpacing: 2 }}>EXISTING · 现有做法</Text>
                {[
                    { tag: 'PACS / VLCS / DomainNet', desc: '图像分类为主，缺目标级定位', color: '#1E4FA8', bg: '#E8EFF8' },
                    { tag: 'COCO-C', desc: '合成扰动，与真实场景差距大', color: '#5B7FCE', bg: '#DCE7F8' },
                    { tag: 'COCO-O', desc: '自然分布偏移但规模有限（6 域）', color: '#FF8A4C', bg: '#FFEAD8' },
                ].map((row, idx) => (
                    <Box key={idx} style={{
                        width: '100%',
                        height: 100,
                        borderRadius: 12,
                        background: '#FFFFFF',
                        border: `1.5px solid ${row.color}`,
                        paddingLeft: 18, paddingRight: 18,
                        paddingTop: 14, paddingBottom: 14,
                        gap: 6,
                    }}>
                        <Box style={{
                            paddingLeft: 10, paddingRight: 10,
                            paddingTop: 4, paddingBottom: 4,
                            borderRadius: 8,
                            background: row.bg,
                            alignSelf: 'flex-start',
                        }}>
                            <Text style={{ color: row.color, fontSize: 11, fontWeight: 'bold', letterSpacing: 1 }}>{row.tag}</Text>
                        </Box>
                        <Text style={{ color: '#1A2230', fontSize: 18, fontWeight: 'bold', lineHeight: 1.3 }}>{row.desc}</Text>
                    </Box>
                ))}
            </Box>
            <Box style={{
                width: 80,
                height: '100%',
                justifyContent: 'center', alignItems: 'center',
            }}>
                <Box style={{
                    width: 60, height: 60,
                    borderRadius: 30,
                    background: 'linear-gradient(135deg, #FFC247 0%, #FF8A4C 100%)',
                    justifyContent: 'center', alignItems: 'center',
                    boxShadow: '0 4px 16px rgba(255,138,76,0.35)',
                }}>
                    <Text style={{ color: '#FFFFFF', fontSize: 28, fontWeight: 'bold' }}>vs</Text>
                </Box>
            </Box>
            <Box style={{ flex: 1, height: '100%', gap: 14 }}>
                <Text style={{ color: '#8B97A8', fontSize: 12, fontWeight: 'bold', letterSpacing: 2 }}>COUNTS · 本文给出的答案</Text>
                {[
                    { tag: '22.2 万张自然图像', desc: '真实世界图像，无人工合成', color: '#2BC5C0', bg: '#DAF6F4' },
                    { tag: '14 个真实分布域', desc: '覆盖日常视觉变化，互相独立', color: '#2BC5C0', bg: '#DAF6F4' },
                    { tag: '细粒度目标级标注', desc: '1,196,114 框，检测 + grounding 双任务', color: '#2BC5C0', bg: '#DAF6F4' },
                ].map((row, idx) => (
                    <Box key={idx} style={{
                        width: '100%',
                        height: 100,
                        borderRadius: 12,
                        background: '#FFFFFF',
                        border: `1.5px solid ${row.color}`,
                        paddingLeft: 18, paddingRight: 18,
                        paddingTop: 14, paddingBottom: 14,
                        gap: 6,
                    }}>
                        <Box style={{
                            paddingLeft: 10, paddingRight: 10,
                            paddingTop: 4, paddingBottom: 4,
                            borderRadius: 8,
                            background: row.bg,
                            alignSelf: 'flex-start',
                        }}>
                            <Text style={{ color: row.color, fontSize: 11, fontWeight: 'bold', letterSpacing: 1 }}>{row.tag}</Text>
                        </Box>
                        <Text style={{ color: '#1A2230', fontSize: 18, fontWeight: 'bold', lineHeight: 1.3 }}>{row.desc}</Text>
                    </Box>
                ))}
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
        <Text style={{ color: '#4A5568', fontSize: 12 }}>05 / 18</Text>
    </Box>
</Slide>
