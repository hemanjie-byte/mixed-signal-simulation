# Printing and teaching guide
# 打印及教学指南

Each binary STL is one connected, closed solid with a 60 × 42 mm footprint, a 2.4 mm flat base and height below 25 mm. Place the broad flat face on the build plate, with Z pointing up. Use **millimetres** and **100% scale**. Scaling down also shrinks the deliberately enlarged text and layers.

每份二进制STL为单个相连封闭实体，底面60×42毫米、平底厚2.4毫米、总高低于25毫米。宽平底朝向打印平台，Z朝上；采用**毫米**、**100%比例**。缩小模型也会缩小刻意放大的字和层结构。

STL is the primary interchange format. It stores triangle geometry, not a printer profile or an embedded unit setting. Select the intended printer and material in your slicer; these files contain no G-code. For format context, see [Prusa's explanation of STL and 3MF](https://help.prusa3d.com/article/saving-projects-as-3mf_1773).

主交付格式为STL，保存三角网格几何，不包含打印机配置或内嵌单位设置。请在切片软件中选择实际打印机及材料；本套文件不含G-code。格式说明见上方Prusa官方文档。

Suggested first slicing assumptions: 0.4 mm nozzle, 0.2 mm layers, three perimeters and 15–20% infill. These are starting assumptions, not tested machine settings. The heightfield construction is vertically filled to the base, so it has no suspended roofs or downward-facing internal overhangs. Inspect the actual layer preview, lettering and bed fit before printing; this release has not been physically printed or sliced for a specific machine.

首次切片可从0.4毫米喷嘴、0.2毫米层高、3道外壁、15%～20%填充开始。这些是起始假设，不是已验证的机型参数。高度场向底座填实，因此没有悬空顶盖或内部向下悬挑。打印前检查实际逐层预览、字形和平台尺寸；本版未实物试打，也未为某一具体机型完成切片。

Main construction features are declared at least 1.2 mm wide; raised letter strokes are a separate 0.8 mm teaching exception. These are construction rules, not a universal wall-thickness certification. Layer steps are snapped to the 0.4 mm geometry grid. Monotone corner repairs remove diagonal-only contacts; per-model reports record their count and added volume.

主要构造特征的声明宽度不小于1.2毫米；凸字笔画单独采用0.8毫米。它们是构造规则，不是通用壁厚认证。层台阶落在0.4毫米几何网格上；局部抬高修复仅对角接触，每件报告记录修补数量与增加体积。

Use the printed ID to open the matching atlas card. First identify the substrate and insulating ledges, then contacts and active regions. Ask students which portions were enlarged, which are material regions versus electrical terminals, and which mechanisms cannot be inferred from a static shape. For example, a raised gate-dielectric ledge represents insulation; plastic joining it to a contact does not represent an electrical short. The TEG model labels thermal boundaries separately from electrical terminals.

按实物编号打开对应图册，先辨认衬底和绝缘台阶，再辨认接触与有源区。可让学生说明哪些部分被放大、哪些是材料区而哪些是电端，以及静态形状无法表达哪些物理过程。例如凸起栅介质表示绝缘，塑料与接触连成整体不表示电气短路；热电模型把热边界和电端分别标注。

These are monolithic tactile cutaway/relief models. Some ledges are widened or offset to remain visible, and support material is merged underneath every feature. They do not reproduce a foundry cross-section, fabrication mask, exact layer thickness or doping profile. A static STL contains no current, voltage, field solution or operating semiconductor. Circuit/parameter displays represent concepts rather than a fabricated circuit layout. Broader legacy devices remain labelled legacy; printing them does not expand the validated analog simulation scope.

这些是单体触觉剖面/浮雕，部分台阶加宽或错位以便观察，每个特征下方都向底座填实。它们不复现晶圆厂真实截面、掩模、精确层厚或掺杂分布。静态STL没有电流、电压、场求解或可工作的半导体功能。电路/参数展示表达概念，不表示真实制成版图；历史广义器件仍标为legacy，打印不扩大已验证模拟仿真的范围。

Reproduce with Python 3.12 and the local requirements: `python build_models.py`, `python build_preview.py`, `python build_atlas.py`, then `python validation/validate_meshes.py`. Geometry validation rereads STL and checks edges, vertex links, connectedness, outward orientation, positive volume and exact agreement with the heightfield boundary. Render colours encode height only. Original simulation and FAB evidence files are preserved.

使用Python 3.12和本目录依赖，依次运行上述四条命令复现。几何验证从STL重新读取，检查边、顶点邻接环、连通性、外向法线、正体积及与高度场外边界的严格对应。渲染颜色仅表示高度；原仿真及FAB依据文件保留。
