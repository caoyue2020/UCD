# UCD
the synthetic code for Underwater Composite Degradation Dataset
合成数据集训练的模型增强结果与 UIEB 参考图像的对比
Original Image        /        Our Results        /        UIEB Reference





复合退化单步处理

输入含有复合退化的水下图像，每次处理单一退化，low->blur->haze,最后一幅为 UIEB 参考图像。
合成方法
偏色预处理
$I_{transfer} = \frac{I_{in} - \text{mean}(I_{in})}{\text{std}(I_{in})} \times \text{std}(I_{temp}) + \text{mean}(I_{temp})$
$\hat{I} = I\times (1-\gamma) + I_{transfer} \times \gamma$
其中$I_{temp}$表示随机选取的偏色模板。该操作对原始干净的陆上自然图像增加蓝绿偏色以更好的模拟水下自然环境。当前$\gamma$设为 0.3。
Blur
$\hat{I}_{blur} =\hat{I}\times \alpha + \mathcal{G} (\hat{I}) \times (1-\alpha) \\
\alpha = e^{-\beta d(x)}$
其中$\mathcal{G}$表示多尺度高斯模糊，$\beta \in [1,3]$,$d(x)$为重映射到 $[0.3,0.7]$的深度图
Haze
$\hat{I}_{haze}=\hat{I} \times t + A(1-t)\\
t = e^{-\beta d(x)}$
其中，$\beta \in [1,3]$，$d(x)$为重映射到$[0.3,0.7]$的深度图。$A$为亮度最亮区域（10%）的平均亮度。注意$\beta$和$A$三通道等量。
low
$\hat{I}_{low} = \frac{\hat{I}}{L}L^{\theta}$
其中，$\theta \in [1.5,2.5]$，$L$为灰度图
偏色
$\hat{I}_{cast} = \hat{I}\times (1-\gamma_2) + I_{transfer} \times \gamma_2$
目前$\gamma_2=1$,即$I_{transfer}$就是$\hat{I}_{cast}$
训练流程
1. 随机读取一幅干净的图像
2. 进行偏色预处理作为 pos
3. 随机生成所有退化类型组合，选择一个作为 inp，其余作为 neg
4. 模型输入 inp 和 退化类型 prompt 进行恢复
5. 计算 L1 损失，SSIM 损失，对比损失（使用 pos 和 neg）
