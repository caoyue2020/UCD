### 合成数据集训练的模型增强结果与 UIEB 参考图像的对比
Original Image        /        Our Results        /        UIEB Reference

![](https://cdn.nlark.com/yuque/0/2025/png/36204023/1743004730967-f0ac49a0-1ec2-4f7d-90c5-7cf69fd42214.png)

![](https://cdn.nlark.com/yuque/0/2025/png/36204023/1743004737289-c1d47b5f-09b6-45f5-bdd8-7062da875a51.png)

![](https://cdn.nlark.com/yuque/0/2025/png/36204023/1743004760283-e6b2d4cf-ce10-48e9-a726-40fc5ab67b61.png)

![](https://cdn.nlark.com/yuque/0/2025/png/36204023/1743004782234-29e0be1b-caf5-495e-9126-7f58f5ea1610.png)

![](https://cdn.nlark.com/yuque/0/2025/png/36204023/1743004916405-3701d97f-7838-47ee-ab35-bfd2ae8961c4.png)

### 复合退化单步处理
![](https://cdn.nlark.com/yuque/0/2025/png/36204023/1742640471239-527fbd1d-e7b3-4927-8ee6-b2c11d6c1769.png)

输入含有复合退化的水下图像，每次处理单一退化，`low`->`blur`->`haze`,最后一幅为 UIEB 参考图像。

### 合成方法
#### 偏色预处理
![image](https://cdn.nlark.com/yuque/__latex/eeb43c6ee8b7ea44b5c6dc50b6c72526.svg)

![image](https://cdn.nlark.com/yuque/__latex/1e83eafefdea9779f7af4a52876dc198.svg)

其中![image](https://cdn.nlark.com/yuque/__latex/ad7445a4870af88fc0d3893611ae93dd.svg)表示随机选取的偏色模板。该操作对原始干净的陆上自然图像增加蓝绿偏色以更好的模拟水下自然环境。当前![image](https://cdn.nlark.com/yuque/__latex/4aa418d6f0b6fbada90489b4374752e5.svg)设为 0.3。

#### Blur
![image](https://cdn.nlark.com/yuque/__latex/3d0541dfac079c76487e59ae998f64d8.svg)

其中![image](https://cdn.nlark.com/yuque/__latex/742feea1e00938322008014d1e5b27d2.svg)表示多尺度高斯模糊，![image](https://cdn.nlark.com/yuque/__latex/52f99e4a24c52b13fb462fa108545c10.svg),![image](https://cdn.nlark.com/yuque/__latex/9a17313a5d24383eca69ac68f594454d.svg)为重映射到 ![image](https://cdn.nlark.com/yuque/__latex/a219921b2927d1536a49a978f2120aae.svg)的深度图

#### Haze
![image](https://cdn.nlark.com/yuque/__latex/5ead04de30be777761a0c7fe91f978e7.svg)

其中，![image](https://cdn.nlark.com/yuque/__latex/9f24e890d6813efd24240a87fe8cb6fb.svg)，![image](https://cdn.nlark.com/yuque/__latex/9a17313a5d24383eca69ac68f594454d.svg)为重映射到![image](https://cdn.nlark.com/yuque/__latex/a219921b2927d1536a49a978f2120aae.svg)的深度图。![image](https://cdn.nlark.com/yuque/__latex/de951302f41d4707b9d80ca1af34dd0f.svg)为亮度最亮区域（10%）的平均亮度。注意![image](https://cdn.nlark.com/yuque/__latex/6100158802e722a88c15efc101fc275b.svg)和![image](https://cdn.nlark.com/yuque/__latex/de951302f41d4707b9d80ca1af34dd0f.svg)三通道等量。

#### low
![image](https://cdn.nlark.com/yuque/__latex/340b14faf4489528f968fcb4984521fc.svg)

其中，![image](https://cdn.nlark.com/yuque/__latex/654c6f219b5d0964021bd64a05d4e79c.svg)，![image](https://cdn.nlark.com/yuque/__latex/c895173d3be4872abf206be4268a58cb.svg)为灰度图

#### 偏色
![image](https://cdn.nlark.com/yuque/__latex/4aa5dca555d82d52b852bfa88dd13286.svg)

目前![image](https://cdn.nlark.com/yuque/__latex/13d1ef28e4ebbb24aebfafeee1049d53.svg),即![image](https://cdn.nlark.com/yuque/__latex/cc59974adfd4f4a3a9ebe3624edb92cd.svg)就是![image](https://cdn.nlark.com/yuque/__latex/5bc9388a3806aca44a50eb8acbf4817d.svg)

### 训练流程
1. 随机读取一幅干净的图像
2. 进行偏色预处理作为 pos
3. 随机生成所有退化类型组合，选择一个作为 inp，其余作为 neg
4. 模型输入 inp 和 退化类型 prompt 进行恢复
5. 计算 L1 损失，SSIM 损失，对比损失（使用 pos 和 neg）

