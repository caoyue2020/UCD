# UCD数据集
针对现有水下图像数据集（如UIEB、LSUI等）依赖过时方法增强并人工筛选参考图像所导致的质量受限问题，UCD通过多种退化模型的复合模拟生成高质量配对数据，用于真实水下图像增强。不同于仅基于大气散射模型的合成方式，UCD 同时引入大气散射模型、Retinex低光模型、多尺度高斯模糊和颜色偏移等退化模型并进行组合，更真实地建模水下图像的复合退化特性，显著提升模型的增强效果。
### 复合退化单步处理
输入含有复合退化的水下图像，每次处理单一退化，low->blur->haze，最后一幅为 UIEB 参考图像。
![](image.png)

### 合成数据集训练的模型增强结果与 UIEB 参考图像的对比
Original Image        /        Our Results        /        UIEB Reference

![](https://cdn.nlark.com/yuque/0/2025/png/36204023/1743004730967-f0ac49a0-1ec2-4f7d-90c5-7cf69fd42214.png)

![](https://cdn.nlark.com/yuque/0/2025/png/36204023/1743004737289-c1d47b5f-09b6-45f5-bdd8-7062da875a51.png)

![](https://cdn.nlark.com/yuque/0/2025/png/36204023/1743004760283-e6b2d4cf-ce10-48e9-a726-40fc5ab67b61.png)

![](https://cdn.nlark.com/yuque/0/2025/png/36204023/1743004782234-29e0be1b-caf5-495e-9126-7f58f5ea1610.png)

![](https://cdn.nlark.com/yuque/0/2025/png/36204023/1743004916405-3701d97f-7838-47ee-ab35-bfd2ae8961c4.png)


