## 项目背景
本项目是我航一名学长委托我和lisiqi对其毕业论文中的计算部分予以实现。  
总的来说，学长建立了约束条件，各种计算评价方法。  
我们负责实现验证。
我实现了对江苏省地图的预处理。江苏省地图来源于网络，之后对其进行二值化处理得到一张黑白江苏省地图。   
![处理后江苏省地图]()  
之后我负责用遗传算法分配确定机场的位置，每一个机场分配方案是一个种群中的个体，种群会基因突变、基因重组，之后维持种群大小不变。我会将么一个方案传给lisiqi的部分，它的函数将会给予其适当的评价。之后我根据评价及遗传算法，不断变换种群。    
之后lisiqi的部分对每一个机场分配方案，通过启发式计算，取出不必要的冗余机场，并根据学长基于的评价公式予以评价。  
最后，我们成功的实现了学长论文的验证计算。而且出乎想象的是，效果比其预想的好一些。  