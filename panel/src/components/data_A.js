let dataA = {
    nodeList: [
        {
            name: '本地上传',
            enName:'upload',
            anchors: ["BottomCenter"],
            datas: ['数据输出'],
            names: ['bc'],
            params: [{
                param: '数据包名',
                type: 'input',
                name: 'packname',
                init: ''
            },
                {
                    param: '上传',
                    type: 'upload',
                    name: 'upload',
                }
            ]
        },
        {
            name: '个人数据',
            enName:'personal',
            anchors: ["BottomCenter"],
            datas: ['数据输出'],
            names: ['bc'],
            params: [{
                param: '数据包名',
                type: 'select',
                name: 'package',
                // index: 0
                select: [],
                init: '请选择'
            },
            ]
        },
        {
            name: 'node',
            enName:'node',
            anchors: ["BottomCenter"],
            datas: ['数据输出'],
            names: ['bc'],
            params: [],
        },
        {
            name: 'change_detection',
            enName:'change_detection',
            anchors: ["BottomCenter"],
            datas: ['数据输出'],
            names: ['bc'],
            params: [],
        },
        {
            name: 'VOCdevkit',
            enName:'VOCdevkit',
            anchors: ["BottomCenter"],
            datas: ['数据输出'],
            names: ['bc'],
            params: [],
        },
        {
            name: 'cycle_gan',
            enName:'cycle_gan',
            anchors: ["BottomCenter"],
            datas: ['数据输出'],
            names: ['bc'],
            params: [],
        },
        {
            name: '翻转',
            enName:'flip',
            anchors: ["TopCenter", "BottomCenter"],
            datas: ['数据输入', '数据输出'],
            names: ['tc', 'bc'],
            params: [
                {
                    param: '翻转数据比例',
                    type: 'slide',
                    name: 'flip',
                    index: 0,
                    init: 50
                },
                // {
                //     param: '翻转方向',
                //     type: 'select',
                //     name: 'direction',
                //     index: 1,
                //     select: ['上下翻转', '左右翻转']
                // }
            ]
        },
        {
            name: '裁剪',
            enName:'crop',
            anchors: ["TopCenter", "BottomCenter"],
            datas: ['数据输入', '数据输出'],
            names: ['tc', 'bc'],
            params: [
                {
                    param: '左下x坐标',
                    type: 'input',
                    name: 'leftx',
                    init: 100
                },
                {
                    param: '左下y坐标',
                    type: 'input',
                    name: 'lefty',
                    init: 100
                },
                {
                    param: '右上x坐标',
                    type: 'input',
                    name: 'rightx',
                    init: 200
                },
                {
                    param: '右上y坐标',
                    type: 'input',
                    name: 'righty',
                    init: 200
                },
            ]
        },
        // {
        //     name: '划分数据集',
        //     enName:'divide',
        //     anchors: ["TopCenter", "BottomCenter"],
        //     datas: ['数据输入', '训练集输出', '测试集输出'],
        //     names: ['tc', 'bc'],
        //     params: [
        //         {
        //             param: '划分比例（训练集占比）',
        //             type: 'slide',
        //             name: 'divide',
        //             index: 0
        //         },
        //     ]
        // },
        {
            name: 'fea',
            enName:'fea',
            anchors: ["TopCenter"],
            datas: ['训练数据输入', '测试数据输入', 'ground truth目录', '结果输出'],
            names: ['tc','bc'],
            params: [
                {
                    param: 'batch大小',
                    type: 'input',
                    name: 'batch',
                    init: 128
                },
                {
                    param: '学习率',
                    type: 'input',
                    name: 'lr',
                    init: 0.001
                },
                {
                    param: '训练步数',
                    type: 'input',
                    name: 'epoch',
                    init: 10
                },
                {
                    param: 'loss',
                    type: 'select',
                    name: 'loss',
                    select: ['L1Loss','MSELoss'],
                    init: 'MSELoss'
                },
                {
                    param: '优化器',
                    type: 'select',
                    name: 'optimizer',
                    select: ['SGD', 'Adam'],
                    init: 'SGD'
                },
            ]
        },
        {
            name: 'yolo',
            enName:'yolo',
            anchors: ["TopCenter"],
            datas: ['训练数据输入', '测试数据输入', 'ground truth目录', '结果输出'],
            names: ['tc','bc'],
            params: [
                {
                    param: 'batch大小',
                    type: 'input',
                    name: 'batch'
                },
                {
                    param: '学习率',
                    type: 'input',
                    name: 'lr'
                },
                {
                    param: '训练步数',
                    type: 'input',
                    name: 'epoch'
                },
                {
                    param: 'loss',
                    type: 'select',
                    name: 'loss',
                    select: ['交叉熵损失','DICE损失','均方误差损失']
                },
                {
                    param: '优化器',
                    type: 'select',
                    name: 'optimizer',
                    select: ['adam', 'sgd', 'momentum']
                },
                {
                    param: 'momentum',
                    type: 'input',
                    name: 'momentum'
                },
                {
                    param: 'rmsprop_decay',
                    type: 'input',
                    name: 'decay'
                },
            ]
        },
        {
            name: 'ssd',
            enName:'ssd',
            anchors: ["TopCenter"],
            datas: ['训练数据输入', '测试数据输入', 'ground truth目录', '结果输出'],
            names: ['tc', 'bc'],
            params: [
                {
                    param: 'batch大小',
                    type: 'input',
                    name: 'batch'
                },
                {
                    param: '学习率',
                    type: 'input',
                    name: 'lr'
                },
                {
                    param: '训练步数',
                    type: 'input',
                    name: 'epoch'
                },
                {
                    param: 'loss',
                    type: 'select',
                    name: 'loss',
                    select: ['交叉熵损失','DICE损失','均方误差损失']
                },
                {
                    param: '优化器',
                    type: 'select',
                    name: 'optimizer',
                    select: ['adam', 'sgd', 'momentum']
                },
                {
                    param: 'momentum',
                    type: 'input',
                    name: 'momentum'
                },
                {
                    param: 'rmsprop_decay',
                    type: 'input',
                    name: 'decay'
                },
            ]
        },
        {
            name: 'GAN',
            enName:'GAN',
            anchors: ["TopCenter"],
            datas: ['训练数据输入', '测试数据输入', '结果输出'],
            names: ['tc', 'bc'],
            params: [
                {
                    param: 'batch大小',
                    type: 'input',
                    name: 'batch'
                },
                {
                    param: '学习率',
                    type: 'input',
                    name: 'lr'
                },
                {
                    param: '训练步数',
                    type: 'input',
                    name: 'epoch'
                },
                {
                    param: 'loss',
                    type: 'select',
                    name: 'loss',
                    select: ['cross-entropy loss','dice loss','mean square error']
                },
                {
                    param: '优化器',
                    type: 'select',
                    name: 'optimizer',
                    select: ['adam', 'sgd', 'momentum']
                },
                {
                    param: 'momentum',
                    type: 'input',
                    name: 'momentum'
                },
                {
                    param: 'rmsprop_decay',
                    type: 'input',
                    name: 'decay'
                },
            ]
        },
        {
            name: '变化检测',
            enName:'change detection',
            anchors: ["TopCenter"],
            datas: ['训练数据输入', '测试数据输入', '结果输出'],
            names: ['tc', 'bc'],
            params: [
                {
                    param: 'batch大小',
                    type: 'input',
                    name: 'batch',
                    init: '8'
                },
                {
                    param: '学习率',
                    type: 'input',
                    name: 'lr',
                    init: "0.0001"
                },
                {
                    param: '训练步数',
                    type: 'input',
                    name: 'epoch',
                    init: '3'
                },
                {
                    param: 'loss',
                    type: 'select',
                    name: 'loss',
                    select: ['CELoss','L1Loss','MSELoss'],
                    init: 'CELoss'
                },
                {
                    param: '优化器',
                    type: 'select',
                    name: 'optimizer',
                    select: ['SGD', 'Adam'],
                    init: 'SGD'
                },
            ]
        },
        {
            name: 'mask rcnn',
            enName:'mask rcnn',
            anchors: ["TopCenter"],
            datas: ['训练数据输入', '测试数据输入', '结果输出'],
            names: ['tc', 'bc'],
            params: [
                {
                    param: 'batch大小',
                    type: 'input',
                    name: 'batch',
                    init: '8'
                },
                {
                    param: '学习率',
                    type: 'input',
                    name: 'lr',
                    init: "0.01"
                },
                {
                    param: '训练步数',
                    type: 'input',
                    name: 'epoch',
                    init: '2'
                },
                {
                    param: 'loss',
                    type: 'select',
                    name: 'loss',
                    select: ['CELoss'],
                    init: 'CELoss'
                },
                {
                    param: '优化器',
                    type: 'select',
                    name: 'optimizer',
                    select: ['SGD'],
                    init: 'SGD'
                },
            ]
        },
         {
            name: 'cycle gan',
            enName:'cycle gan',
            anchors: ["TopCenter"],
            datas: ['训练数据输入', '测试数据输入', '结果输出'],
            names: ['tc', 'bc'],
            params: [
                {
                    param: 'batch大小',
                    type: 'input',
                    name: 'batch',
                    init: '2'
                },
                {
                    param: '学习率',
                    type: 'input',
                    name: 'lr',
                    init: "0.0002"
                },
                {
                    param: '训练步数',
                    type: 'input',
                    name: 'epoch',
                    init: '10'
                },
                {
                    param: 'loss',
                    type: 'select',
                    name: 'loss',
                    select: ['MSELoss'],
                    init: 'MSELoss'
                },
                {
                    param: '优化器',
                    type: 'select',
                    name: 'optimizer',
                    select: ['Adam'],
                    init: 'Adam'
                },
            ]
        },
    ],
}

let data_menu = [
    {
        id: '1',
        type: 'group',
        name: '数据',
        open: true,
        children: [
            {
                id: '11',
                type: 'timer',
                name: '个人数据',
                open: false,
                children: [
                    {
                        id: '111',
                        type: 'upload',
                        name: '本地上传',
                        ico: 'el-icon-folder-opened',
                    },
                    {
                        id: '112',
                        type: 'personal',
                        name: '个人数据',
                        ico: 'el-icon-folder-opened',
                    }
                ],
            }, {
                id: '12',
                type: 'task',
                name: '共享数据',
                open: false,
                 children: [
                    {
                        id: '121',
                        type: 'shareone',
                        name: 'node',
                        ico: 'el-icon-folder',
                    },
                     {
                        id: '122',
                        type: 'sharetwo',
                        name: 'change_detection',
                        ico: 'el-icon-folder',
                    },
                    {
                        id: '123',
                        type: 'sharethree',
                        name: 'VOCdevkit',
                        ico: 'el-icon-folder',
                    },
                     {
                        id: '124',
                        type: 'sharefour',
                        name: 'cycle_gan',
                        ico: 'el-icon-folder',
                    },
                ],
            }
        ]
    },
    {
        id: '2',
        type: 'group',
        name: '数据预处理',
        open: true,
        children: [
            {
                id: '21',
                type: 'end',
                name: '预处理方法',
                open: false,
                children: [
                    {
                        id: '211',
                        type: 'flip',
                        name: '翻转',
                        ico: 'el-icon-sort',
                    },
                    {
                        id: '212',
                        type: 'crop',
                        name: '裁剪',
                        ico: 'el-icon-crop',
                    }
                ],
            }
            // }, {
            //     id: '22',
            //     type: 'devide',
            //     name: '划分数据集',
            //     open: false,
            //     children: [
            //         {
            //             id: '221',
            //             type: 'devidedata',
            //             name: '划分数据集',
            //             ico: 'el-icon-files',
            //         }
            //     ],
            // }
        ]
    },
    {
        id: '3',
        type: 'group',
        name: '算法',
        ico: 'el-icon-video-pause',
        open: true,
        children: [
            {
                id: '31',
                type: 'detection',
                name: '目标检测',
                open: false,
                children: [
                    {
                        id: '311',
                        type: 'yolo',
                        name: 'yolo',
                        ico: 'el-icon-search',
                    },
                     {
                        id: '312',
                        type: 'ssd',
                        name: 'ssd',
                        ico: 'el-icon-search',
                    }
                ],
            }, {
                id: '32',
                type: '变化检测',
                name: '变化检测',
                open: false,
                children: [
                    {
                        id: '321',
                        type: '变化检测',
                        name: '变化检测',
                        ico: 'el-icon-refresh',
                    }
                ]
            }, {
                id: '33',
                type: 'generate',
                name: '对抗生成',
                open: false,
                children: [
                    {
                        id: '331',
                        type: 'cycle gan',
                        name: 'cycle gan',
                        ico: 'el-icon-refresh',
                    }
                ]
            },
            {
                id: '34',
                type: 'FE',
                name: '有限元分析',
                open: false,
                children: [
                    {
                        id: '341',
                        type: 'fea',
                        name: 'fea',
                        ico: 'el-icon-refresh',
                    }
                ]
            },
            {
                id: '35',
                type: 'segmentation',
                name: '图像分割',
                open: false,
                children: [
                    {
                        id: '351',
                        type: 'mask rcnn',
                        name: 'mask rcnn',
                        ico: 'el-icon-refresh',
                    }
                ]
            },
        ]
    },
    {
        id: '4',
        type: 'output',
        name: '输出',
        ico: 'el-icon-video-pause',
        open: true,
        children: [
            {
                id: '41',
                type: 'weight',
                name: '是否保存权重',
                ico: 'el-icon-data-line',
            }
        ]
    },
    {
        id: '5',
        type: 'pre',
        name: '预训练',
        ico: 'el-icon-video-pause',
        open: true,
        children: [
            {
                id: '51',
                type: 'pretrain',
                name: '预训练参数',
                ico: 'el-icon-data-line',
            }
        ]
    },
]

export function getMenu(){
    return data_menu;
}

export function getDataA () {
    return dataA;
}


export function getData(text, x, y){
    text = text.slice(0, text.length-1);
    for(let i = 0; i < dataA.nodeList.length; i++){
        var data = dataA.nodeList[i];
        if(text.indexOf(data.name) !== -1){
            if(data.datas.length === 1){
                return data.datas[0];
            }
            if(data.datas.length === 2){
                return data.datas[y];
            }
            if(data.datas.length === 3){
                return data.datas[(x+y).toFixed(0)];
            }
            if(data.datas.length === 4){
                return data.datas[(x+y)*2];
            }
        }
    }
    return "未设置";
}

export function getParams(text){
    console.log(text)
    for(let i = 0; i < dataA.nodeList.length; i++){
        var data = dataA.nodeList[i];
        console.log(data.name)
        if(text.indexOf(data.name) !== -1){
            return data.params;
        }
    }
    return null;
}

export function getNodeParams(text){
    for(let i = 0; i < dataA.nodeList.length; i++){
        var data = dataA.nodeList[i];
        if(text.indexOf(data.name) !== -1){
            let l = [];
            for(var j = 0; j < data.params.length; j++){
                l.push(data.params[j].name)
            }
            return l;
        }
    }
    return null;
}

export function getEnName(name){
    for(let i = 0; i < dataA.nodeList.length; i++){
        var data = dataA.nodeList[i];
        if(name.indexOf(data.name) !== -1){
            return data.enName;
        }
    }
    return null;
}