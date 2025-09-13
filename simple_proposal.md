# ReadyTensor Multi-Agent Demo - 简化版方案

## 核心要求实现

### 1. 多智能体系统 (3个智能体)

**智能体1: 研究员 (Researcher Agent)**
- 负责网络搜索和信息收集
- 使用搜索工具获取相关信息

**智能体2: 分析师 (Analyst Agent)**  
- 负责数据计算和分析
- 使用计算工具处理数字数据

**智能体3: 报告员 (Reporter Agent)**
- 负责文件处理和报告生成
- 使用文件工具读写文档

### 2. 工具集成 (3个工具)

**工具1: 搜索工具 (Search Tool)**
- 模拟网络搜索功能
- 返回相关信息

**工具2: 计算工具 (Calculator Tool)**  
- 执行数学计算
- 处理数值分析

**工具3: 文件工具 (File Tool)**
- 读取和写入文件
- 处理文档操作

### 3. 编排框架
- **LangGraph** 作为编排框架
- 简单的状态流转
- 顺序执行模式

## 简化的项目结构

```
multi_agent_demo/
├── README.md
├── requirements.txt
├── main.py                  # 主程序入口
├── agents/
│   ├── __init__.py
│   ├── researcher.py        # 研究员智能体
│   ├── analyst.py          # 分析师智能体
│   └── reporter.py         # 报告员智能体
├── tools/
│   ├── __init__.py
│   ├── search_tool.py      # 搜索工具
│   ├── calc_tool.py        # 计算工具
│   └── file_tool.py        # 文件工具
└── workflow.py             # LangGraph工作流
```

## 工作流程

```
用户输入 → 研究员搜索信息 → 分析师计算分析 → 报告员生成报告 → 输出结果
```

## 技术栈

- **Python 3.8+**
- **LangGraph**: 智能体编排
- **LangChain**: 基础工具和LLM集成
- **gemini**: LLM提供商

## 演示场景

**基础演示**: 
- 用户提问："分析一下苹果公司的股价趋势"
- 研究员搜索苹果股价信息
- 分析师计算相关指标
- 报告员生成分析报告
