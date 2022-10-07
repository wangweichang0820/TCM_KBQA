var myChart = echarts.init(document.getElementById('chart'));
var categories = [{name: "头实体"}, {name: "尾实体"}, {name: "属性"}];
option = {
    // 图的标题
    title: {
        text: '图谱可视化'
    },
    // 提示框的配置
    tooltip: {
        formatter: function (x) {
            return x.data.des;
        }
    },
    // 工具箱
    toolbox: {
        // 显示工具箱
        show: true,
        feature: {
            mark: {
                show: true
            },
            // 还原
            restore: {
                show: true
            },
            // 保存为图片
            saveAsImage: {
                show: true
            }
        }
    },
    legend: [{
        // selectedMode: 'single',
        data: categories.map(function (a) {
            return a.name;
        })
    }],
    series: [{
        type: 'graph', // 类型:关系图
        layout: 'force', //图的布局，类型为力导图
        symbolSize: 40, // 调整节点的大小
        roam: true, // 是否开启鼠标缩放和平移漫游。默认不开启。如果只想要开启缩放或者平移,可以设置成 'scale' 或者 'move'。设置成 true 为都开启
        edgeSymbol: ['circle', 'arrow'],
        edgeSymbolSize: [2, 10],
        edgeLabel: {
            normal: {
                textStyle: {
                    fontSize: 20
                }
            }
        },
        force: {
            repulsion: 2500,
            edgeLength: [10, 50]
        },
        draggable: true,
        lineStyle: {
            normal: {
                width: 2,
                color: '#4b565b',
            }
        },
        edgeLabel: {
            normal: {
                show: true,
                formatter: function (x) {
                    return x.data.name;
                }
            }
        },
        label: {
            normal: {
                show: true,
                textStyle: {}
            }
        },

        // 数据
        data: [{
            name: '感冒',
            des: '疾病', //描述
            symbolSize: 70,
            category: '头实体',
        }, {
            name: '中毒病类', symbolSize: 50, category: '属性',
        }, {
            name: '其他病类', symbolSize: 50, category: '属性',
        }, {
            name: '时兴病类', symbolSize: 50, category: '属性',
        }, {
            name: '风邪冒犯肺表所致', symbolSize: 50, category: '属性',
        }, {
            name: '喉痒咳嗽',
            des: '',//没有描述
            symbolSize: 50,
            category: '尾实体',
        }, {
            name: '鼻塞喷嚏',
            des: 'nodedes3',
            symbolSize: 50,
            category: '尾实体',
        }, {
            name: '头身疼痛',
            des: 'nodedes3',
            symbolSize: 50,
            category: '尾实体',
        }, {
            name: '发热恶寒',
            des: 'nodedes3',
            symbolSize: 50,
            category: '尾实体',
        }],
        links: [{
            source: '感冒',
            target: '中毒病类',
            name: '病类',
            des: ''
        }, {
            source: '感冒',
            target: '其他病类',
            name: '病类',
            des: ''
        }, {
            source: '感冒',
            target: '时兴病类',
            name: '病类',
            des: ''
        }, {
            source: '感冒',
            target: '喉痒咳嗽',
            name: '症状',
            des: ''
        }, {
            source: '感冒',
            target: '鼻塞喷嚏',
            name: '症状',
            des: ''
        }, {
            source: '感冒',
            target: '头身疼痛',
            name: '症状',
            des: ''
        }, {
            source: '感冒',
            target: '发热恶寒',
            name: '症状',
            des: ''
        }, {
            source: '感冒',
            target: '风邪冒犯肺表所致',
            name: '病因',
            des: ''
        }],
        categories: categories,
    }]
};
myChart.setOption(option);