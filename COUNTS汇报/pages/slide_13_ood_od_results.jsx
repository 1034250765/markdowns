<Slide padding={0}>
    <Box style={{
        width: '100%', height: 80,
        flexDirection: 'row', alignItems: 'center',
        paddingLeft: 40, paddingRight: 40,
        background: '#FFFFFF',
        borderBottom: '2px solid #F0F5FC',
    }}>
        <Box style={{ width: 40, height: 4, borderRadius: 2, background: '#FFC247', marginRight: 14 }} />
        <Text style={{ color: '#FFC247', fontSize: 14, fontWeight: 'bold', letterSpacing: 2 }}>CHAPTER 04 · O(OD)² 实验结果</Text>
        <Box style={{ flex: 1 }} />
        <Text style={{ color: '#8B97A8', fontSize: 13 }}>页 13 / 18</Text>
    </Box>
    <Box style={{
        width: '100%', height: 560,
        paddingLeft: 40, paddingRight: 40,
        paddingTop: 22, paddingBottom: 22,
        gap: 14,
    }}>
        <Box style={{ width: '100%', flexDirection: 'row', alignItems: 'baseline', justifyContent: 'space-between' }}>
            <Box style={{ gap: 4 }}>
                <Text style={{ color: '#1E4FA8', fontSize: 13, fontWeight: 'bold', letterSpacing: 3 }}>TABLE 2 · OOD mAP</Text>
                <Text style={{ color: '#1A2230', fontSize: 24, fontWeight: 'bold' }}>
                    DINO/DINOv2 表现最佳 · IID 强 ≠ OOD 强
                </Text>
            </Box>
            <Text style={{ color: '#8B97A8', fontSize: 12 }}>基于 8 张 RTX 4090 · MMDetection</Text>
        </Box>
        <Box style={{
            width: '100%', flex: 1,
            flexDirection: 'row', gap: 18,
        }}>
            <Box style={{ flex: 1, height: '100%' }}>
                <Chart
                    style={{ width: '100%', height: '100%' }}
                    chartType='barChart'
                    barDirection='bar'
                    grouping='clustered'
                    background='#FFFFFF'
                    colors={['#5B7FCE', '#FFC247']}
                    titleColor='#1A2230'
                    legendColor='#4A5568'
                    axisColor='#8B97A8'
                    title='各检测器 OOD vs IID 性能'
                    data={[
                        ['Detector', 'OOD mAP', 'IID mAP'],
                        ['Faster R-CNN', 0.149, 0.385],
                        ['RetinaNet', 0.146, 0.391],
                        ['YOLOv9', 0.150, 0.402],
                        ['DETR', 0.168, 0.418],
                        ['DINO', 0.213, 0.461],
                        ['DINOv2', 0.213, 0.467],
                    ]}
                />
            </Box>
            <Box style={{ width: 360, height: '100%', gap: 12 }}>
                <Box style={{
                    width: '100%', borderRadius: 12,
                    background: 'linear-gradient(135deg, #FFC247 0%, #FF8A4C 100%)',
                    paddingTop: 16, paddingBottom: 16,
                    paddingLeft: 18, paddingRight: 18,
                    gap: 8,
                }}>
                    <Text style={{ color: '#FFFFFF', fontSize: 11, fontWeight: 'bold', letterSpacing: 2 }}>KEY FINDING</Text>
                    <Text style={{ color: '#FFFFFF', fontSize: 18, fontWeight: 'bold', lineHeight: 1.4 }}>
                        OOD mAP 仅及 IID 的 30-50%
                    </Text>
                    <Text style={{ color: '#FFFFFF', fontSize: 13, lineHeight: 1.6, opacity: 0.95 }}>
                        即使最强检测器 DINO/DINOv2，OOD mAP 也只有 IID 的一半左右。
                    </Text>
                </Box>
                {[
                    { tag: 'neck 升级的反效果', desc: 'NAS-FPN 等更强 neck 在跨域泛化中反而更弱', c: '#1E4FA8' },
                    { tag: 'head 是关键', desc: '两阶段检测器中，修改 head 比增强 backbone 更明显', c: '#2BC5C0' },
                    { tag: '训练策略很重要', desc: 'Sup_timm 相对 ImageNet 预训练提升 18.9%', c: '#FF8A4C' },
                ].map((row, idx) => (
                    <Box key={idx} style={{
                        width: '100%',
                        paddingTop: 12, paddingBottom: 12,
                        paddingLeft: 16, paddingRight: 16,
                        borderRadius: 10,
                        background: '#FFFFFF',
                        border: `1px solid ${row.c}`,
                        gap: 6,
                    }}>
                        <Text style={{ color: row.c, fontSize: 13, fontWeight: 'bold' }}>· {row.tag}</Text>
                        <Text style={{ color: '#4A5568', fontSize: 12, lineHeight: 1.5 }}>{row.desc}</Text>
                    </Box>
                ))}
            </Box>
        </Box>
        <Box style={{
            width: '100%', height: 40,
            borderRadius: 10,
            background: '#F0F5FC',
            paddingLeft: 16, paddingRight: 16,
            flexDirection: 'row', alignItems: 'center',
            gap: 12,
        }}>
            <Box style={{
                paddingLeft: 10, paddingRight: 10,
                paddingTop: 4, paddingBottom: 4,
                borderRadius: 8, background: '#1E4FA8',
            }}>
                <Text style={{ color: '#FFFFFF', fontSize: 11, fontWeight: 'bold', letterSpacing: 1 }}>INSIGHT</Text>
            </Box>
            <Text style={{ color: '#1A2230', fontSize: 14, flex: 1 }}>
                堆 backbone / 扩预训练数据未必提升 OOD 泛化，<span style={{ fontWeight: 'bold', color: '#1E4FA8' }}>head 优化与训练策略是关键路径</span>。
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
        <Text style={{ color: '#4A5568', fontSize: 12 }}>13 / 18</Text>
    </Box>
</Slide>
