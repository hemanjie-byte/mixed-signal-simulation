# Egg-size printable semiconductor teaching models

# 鸡蛋大小的半导体教学打印模型

**Print edition 1.0 · 2026-11-07 · 75 binary STL files.** Each model has a 60 × 42 mm flat footprint and stays below 25 mm high. These are tactile, enlarged cutaway/relief concepts. Sizes, layer thicknesses and doping boundaries are deliberately exaggerated for teaching, not manufacturing drawings.

**打印版1.0 · 2026-11-07 · 75份二进制STL。** 每件底面60×42毫米，高度低于25毫米，接近鸡蛋大小。模型为便于观察和触摸的放大剖面/浮雕概念；尺寸、薄层及掺杂边界为教学刻意放大，不是制造图纸。

Coverage: all 24 V1 entries, 31 V2 entries and 20 current V3.3 entries. Historical copies of the same A/B/P model are not counted again. **75 catalogue entries do not mean 75 distinct physical devices.** Circuit benches, parameter demonstrations and broader historical devices are explicitly classified.

覆盖V1全部24项、V2全部31项及当前V3.3全部20项，相同A/B/P模型的历史副本不重复统计。**75项目录条目不等于75种独立物理器件。** 电路台、参数演示及历史广义器件分别标注。

- [Offline illustrated atlas](index.html) — 离线图册，可筛选、看图并下载单件STL
- [All STL files](stl/) — 全部单件STL
- [Current V3.3 overview](contact_sheets/V33.png) · [V1](contact_sheets/V1.png) · [V2](contact_sheets/V2.png) — 分组总览
- [Printing and interpretation guide](PRINT_GUIDE_EN_ZH.md) — 打印及教学阅读说明
- [Geometry validation](validation/mesh_validation.json) — 从STL回读的几何检查
- [Structured catalogue](catalogue.json) · [Printable file list](print_index.csv) — 来源、端口及文件映射
- [Portable printing bundle](../Semiconductor_Teaching_STL_20261107.zip) — 打印资料包

STL coordinates must be interpreted as **millimetres**; STL does not embed a unit setting. Import at 100% scale. The preview colours encode height for readability, not material, doping concentration, voltage or current. Printed raised labels are English abbreviations; detailed notes are bilingual.

STL坐标须按**毫米**导入，STL自身不保存单位设置，导入比例为100%。预览颜色仅用高度辅助辨认，不代表材料、掺杂浓度、电压或电流。实物凸字为英文缩写，详细说明英中对照。

Geometry checks address closed meshes and the documented heightfield construction. No physical print, printer-specific slicing or semiconductor-process validation is claimed. The original electrical simulations and their accuracy limits are unchanged.

几何检查针对封闭网格及所记录的高度场构造；尚未进行实物试打、针对具体打印机的切片或半导体工艺验证。原电气仿真及准确性边界保持不变。

| ID | Model / 模型 | Class / 分类 | Files / 文件 |
|---|---|---|---|
| V1_M01 | Isolated high-side NLDMOS<br>高侧隔离NLDMOS | physical_device · legacy | [STL](stl/V1_M01.stl) · [Preview](previews/V1_M01.png) · [Notes](cards/V1_M01.md) |
| V1_M02 | Low-side NLDMOS<br>低侧NLDMOS | physical_device · legacy | [STL](stl/V1_M02.stl) · [Preview](previews/V1_M02.png) · [Notes](cards/V1_M02.md) |
| V1_M03 | High-voltage PLDMOS<br>高压PLDMOS | physical_device · legacy | [STL](stl/V1_M03.stl) · [Preview](previews/V1_M03.png) · [Notes](cards/V1_M03.md) |
| V1_M04 | Drain-extended NMOS<br>高压DENMOS | physical_device · legacy | [STL](stl/V1_M04.stl) · [Preview](previews/V1_M04.png) · [Notes](cards/V1_M04.md) |
| V1_M05 | Low-voltage NMOS<br>低压NMOS | physical_device · legacy | [STL](stl/V1_M05.stl) · [Preview](previews/V1_M05.png) · [Notes](cards/V1_M05.md) |
| V1_M06 | Low-voltage PMOS<br>低压PMOS | physical_device · legacy | [STL](stl/V1_M06.stl) · [Preview](previews/V1_M06.png) · [Notes](cards/V1_M06.md) |
| V1_M07 | Drain-extended PMOS<br>高压DEPMOS | physical_device · legacy | [STL](stl/V1_M07.stl) · [Preview](previews/V1_M07.png) · [Notes](cards/V1_M07.md) |
| V1_Q01 | NPN bipolar transistor<br>NPN双极晶体管 | physical_device · legacy | [STL](stl/V1_Q01.stl) · [Preview](previews/V1_Q01.png) · [Notes](cards/V1_Q01.md) |
| V1_Q02 | PNP bipolar transistor<br>PNP双极晶体管 | physical_device · legacy | [STL](stl/V1_Q02.stl) · [Preview](previews/V1_Q02.png) · [Notes](cards/V1_Q02.md) |
| V1_D01 | MOS body PN freewheel diode<br>体PN续流二极管 | physical_device · legacy | [STL](stl/V1_D01.stl) · [Preview](previews/V1_D01.png) · [Notes](cards/V1_D01.md) |
| V1_D02 | High-voltage bootstrap PN diode<br>高压自举PN二极管 | physical_device · legacy | [STL](stl/V1_D02.stl) · [Preview](previews/V1_D02.png) · [Notes](cards/V1_D02.md) |
| V1_D03 | Schottky diode<br>肖特基二极管 | physical_device · legacy | [STL](stl/V1_D03.stl) · [Preview](previews/V1_D03.png) · [Notes](cards/V1_D03.md) |
| V1_D04 | Gate Zener clamp<br>栅极Zener钳位 | physical_device · legacy | [STL](stl/V1_D04.stl) · [Preview](previews/V1_D04.png) · [Notes](cards/V1_D04.md) |
| V1_J01 | High-voltage startup JFET<br>高压启动JFET | physical_device · legacy | [STL](stl/V1_J01.stl) · [Preview](previews/V1_J01.png) · [Notes](cards/V1_J01.md) |
| V1_R01 | High-voltage polysilicon resistor chain<br>高压多晶硅电阻链 | passive · legacy | [STL](stl/V1_R01.stl) · [Preview](previews/V1_R01.png) · [Notes](cards/V1_R01.md) |
| V1_R02 | Current-sense resistor<br>电流检测电阻 | passive · legacy | [STL](stl/V1_R02.stl) · [Preview](previews/V1_R02.png) · [Notes](cards/V1_R02.md) |
| V1_C01 | MIM capacitor<br>MIM电容 | passive · legacy | [STL](stl/V1_C01.stl) · [Preview](previews/V1_C01.png) · [Notes](cards/V1_C01.md) |
| V1_C02 | MOM capacitor<br>MOM电容 | passive · legacy | [STL](stl/V1_C02.stl) · [Preview](previews/V1_C02.png) · [Notes](cards/V1_C02.md) |
| V1_I01 | Isolation junction and DTI equivalent network<br>隔离结与DTI等效网络 | isolation_structure · legacy | [STL](stl/V1_I01.stl) · [Preview](previews/V1_I01.png) · [Notes](cards/V1_I01.md) |
| V1_E01 | High-voltage ESD clamp equivalent<br>高压ESD钳位等效器件 | mechanism_demo · legacy | [STL](stl/V1_E01.stl) · [Preview](previews/V1_E01.png) · [Notes](cards/V1_E01.md) |
| V1_L01 | External power inductor<br>外接功率电感 | passive · legacy | [STL](stl/V1_L01.stl) · [Preview](previews/V1_L01.png) · [Notes](cards/V1_L01.md) |
| V1_C03 | External output capacitor<br>外接输出电容 | passive · legacy | [STL](stl/V1_C03.stl) · [Preview](previews/V1_C03.png) · [Notes](cards/V1_C03.md) |
| V1_C04 | External input capacitor<br>外接输入电容 | passive · legacy | [STL](stl/V1_C04.stl) · [Preview](previews/V1_C04.png) · [Notes](cards/V1_C04.md) |
| V1_C05 | External bootstrap capacitor<br>外接自举电容 | passive · legacy | [STL](stl/V1_C05.stl) · [Preview](previews/V1_C05.png) · [Notes](cards/V1_C05.md) |
| V2_N01 | SiC vertical MOSFET<br>SiC垂直MOSFET | physical_device · legacy | [STL](stl/V2_N01.stl) · [Preview](previews/V2_N01.png) · [Notes](cards/V2_N01.md) |
| V2_N02 | Enhancement-mode GaN HEMT<br>增强型GaN HEMT | physical_device · legacy | [STL](stl/V2_N02.stl) · [Preview](previews/V2_N02.png) · [Notes](cards/V2_N02.md) |
| V2_N03 | Silicon superjunction MOSFET<br>硅超结MOSFET | physical_device · legacy | [STL](stl/V2_N03.stl) · [Preview](previews/V2_N03.png) · [Notes](cards/V2_N03.md) |
| V2_N04 | IGBT<br>IGBT | physical_device · legacy | [STL](stl/V2_N04.stl) · [Preview](previews/V2_N04.png) · [Notes](cards/V2_N04.md) |
| V2_N05 | SiC JBS rectifier<br>SiC JBS整流二极管 | physical_device · legacy | [STL](stl/V2_N05.stl) · [Preview](previews/V2_N05.png) · [Notes](cards/V2_N05.md) |
| V2_N06 | FinFET<br>FinFET | physical_device · legacy | [STL](stl/V2_N06.stl) · [Preview](previews/V2_N06.png) · [Notes](cards/V2_N06.md) |
| V2_N07 | a-IGZO thin-film transistor<br>a-IGZO TFT | physical_device · legacy | [STL](stl/V2_N07.stl) · [Preview](previews/V2_N07.png) · [Notes](cards/V2_N07.md) |
| V2_N08 | Organic polymer TFT<br>有机聚合物TFT | physical_device · legacy | [STL](stl/V2_N08.stl) · [Preview](previews/V2_N08.png) · [Notes](cards/V2_N08.md) |
| V2_N09 | Contact-limited MoS2 FET<br>MoS2接触受限FET | physical_device · legacy | [STL](stl/V2_N09.stl) · [Preview](previews/V2_N09.png) · [Notes](cards/V2_N09.md) |
| V2_N10 | Ambipolar graphene FET<br>石墨烯双极性FET | physical_device · legacy | [STL](stl/V2_N10.stl) · [Preview](previews/V2_N10.png) · [Notes](cards/V2_N10.md) |
| V2_N11 | Ballistic carbon-nanotube FET<br>碳纳米管弹道FET | physical_device · legacy | [STL](stl/V2_N11.stl) · [Preview](previews/V2_N11.png) · [Notes](cards/V2_N11.md) |
| V2_N12 | Ferroelectric FET memory cell<br>FeFET铁电存储晶体管 | physical_device · legacy | [STL](stl/V2_N12.stl) · [Preview](previews/V2_N12.png) · [Notes](cards/V2_N12.md) |
| V2_N13 | Oxide RRAM cell<br>氧化物RRAM | physical_device · legacy | [STL](stl/V2_N13.stl) · [Preview](previews/V2_N13.png) · [Notes](cards/V2_N13.md) |
| V2_N14 | Phase-change memory cell<br>PCM相变存储单元 | physical_device · legacy | [STL](stl/V2_N14.stl) · [Preview](previews/V2_N14.png) · [Notes](cards/V2_N14.md) |
| V2_N15 | Magnetic tunnel junction<br>MTJ磁隧道结 | physical_device · legacy | [STL](stl/V2_N15.stl) · [Preview](previews/V2_N15.png) · [Notes](cards/V2_N15.md) |
| V2_N16 | Ferroelectric capacitor<br>铁电电容 | passive · legacy | [STL](stl/V2_N16.stl) · [Preview](previews/V2_N16.png) · [Notes](cards/V2_N16.md) |
| V2_N17 | Nitride LED<br>氮化物LED | physical_device · legacy | [STL](stl/V2_N17.stl) · [Preview](previews/V2_N17.png) · [Notes](cards/V2_N17.md) |
| V2_N18 | Quantum-dot LED<br>量子点LED | physical_device · legacy | [STL](stl/V2_N18.stl) · [Preview](previews/V2_N18.png) · [Notes](cards/V2_N18.md) |
| V2_N19 | PIN photodetector<br>PIN光电探测器 | physical_device · legacy | [STL](stl/V2_N19.stl) · [Preview](previews/V2_N19.png) · [Notes](cards/V2_N19.md) |
| V2_N20 | Single-junction photovoltaic cell<br>单结光伏电池 | physical_device · legacy | [STL](stl/V2_N20.stl) · [Preview](previews/V2_N20.png) · [Notes](cards/V2_N20.md) |
| V2_N21 | Thermoelectric generator cell<br>热电发电单元 | physical_device · legacy | [STL](stl/V2_N21.stl) · [Preview](previews/V2_N21.png) · [Notes](cards/V2_N21.md) |
| V2_N22 | On-chip coupled transformer<br>片上耦合变压器 | passive · legacy | [STL](stl/V2_N22.stl) · [Preview](previews/V2_N22.png) · [Notes](cards/V2_N22.md) |
| V2_N23 | Through-silicon via<br>TSV硅通孔 | interconnect · legacy | [STL](stl/V2_N23.stl) · [Preview](previews/V2_N23.png) · [Notes](cards/V2_N23.md) |
| V2_N24 | Mach-Zehnder electro-optic modulator<br>MZI电光调制器 | physical_device · legacy | [STL](stl/V2_N24.stl) · [Preview](previews/V2_N24.png) · [Notes](cards/V2_N24.md) |
| V2_N25 | Semiconductor laser diode<br>半导体激光二极管 | physical_device · legacy | [STL](stl/V2_N25.stl) · [Preview](previews/V2_N25.png) · [Notes](cards/V2_N25.md) |
| V2_X01 | MOS gate charge and Miller coupling<br>MOS栅电荷与Miller耦合 | mechanism_demo · legacy | [STL](stl/V2_X01.stl) · [Preview](previews/V2_X01.png) · [Notes](cards/V2_X01.md) |
| V2_X02 | PN diode reverse recovery<br>PN二极管反向恢复 | mechanism_demo · legacy | [STL](stl/V2_X02.stl) · [Preview](previews/V2_X02.png) · [Notes](cards/V2_X02.md) |
| V2_X03 | MOS conduction-loss thermal feedback<br>MOS导通损耗自热反馈 | mechanism_demo · legacy | [STL](stl/V2_X03.stl) · [Preview](previews/V2_X03.png) · [Notes](cards/V2_X03.md) |
| V2_X04 | PMOS NBTI aging<br>PMOS NBTI老化 | mechanism_demo · legacy | [STL](stl/V2_X04.stl) · [Preview](previews/V2_X04.png) · [Notes](cards/V2_X04.md) |
| V2_X05 | MOS flicker and thermal noise<br>MOS 1/f与热噪声 | mechanism_demo · legacy | [STL](stl/V2_X05.stl) · [Preview](previews/V2_X05.png) · [Notes](cards/V2_X05.md) |
| V2_X06 | MOS threshold and resistance statistics<br>MOS阈值及电阻统计分散 | parameter_demo · legacy | [STL](stl/V2_X06.stl) · [Preview](previews/V2_X06.png) · [Notes](cards/V2_X06.md) |
| V33_A01 | Four-terminal MOS interpolation<br>四端MOS连续插值 | physical_device · current | [STL](stl/V33_A01.stl) · [Preview](previews/V33_A01.png) · [Notes](cards/V33_A01.md) |
| V33_A02 | Junction charge and varactor<br>结电荷与变容二极管 | physical_device · current | [STL](stl/V33_A02.stl) · [Preview](previews/V33_A02.png) · [Notes](cards/V33_A02.md) |
| V33_A03 | Reciprocal NPN Ebers–Moll<br>满足互易关系的NPN Ebers–Moll | physical_device · current | [STL](stl/V33_A03.stl) · [Preview](previews/V33_A03.png) · [Notes](cards/V33_A03.md) |
| V33_A04 | MOS pair mismatch and correlation<br>MOS配对失配与相关性 | parameter_demo · current | [STL](stl/V33_A04.stl) · [Preview](previews/V33_A04.png) · [Notes](cards/V33_A04.md) |
| V33_B01 | MOS differential pair<br>MOS差分对 | circuit_bench · current | [STL](stl/V33_B01.stl) · [Preview](previews/V33_B01.png) · [Notes](cards/V33_B01.md) |
| V33_B02 | CTAT/PTAT reference sum<br>CTAT/PTAT基准合成 | circuit_bench · current | [STL](stl/V33_B02.stl) · [Preview](previews/V33_B02.png) · [Notes](cards/V33_B02.md) |
| V33_B03 | Input noise and sampled kT/C<br>输入噪声与采样kT/C | circuit_bench · current | [STL](stl/V33_B03.stl) · [Preview](previews/V33_B03.png) · [Notes](cards/V33_B03.md) |
| V33_B04 | Capacitor DAC and SAR ADC<br>电容DAC与SAR ADC | circuit_bench · current | [STL](stl/V33_B04.stl) · [Preview](previews/V33_B04.png) · [Notes](cards/V33_B04.md) |
| V33_B05 | LDO loop and load step<br>LDO环路与负载阶跃 | circuit_bench · current | [STL](stl/V33_B05.stl) · [Preview](previews/V33_B05.png) · [Notes](cards/V33_B05.md) |
| V33_B06 | Phase loop and noise transfer<br>相位环路与噪声传递 | circuit_bench · current | [STL](stl/V33_B06.stl) · [Preview](previews/V33_B06.png) · [Notes](cards/V33_B06.md) |
| V33_B07 | 40–150 V synchronous buck<br>40–150V同步降压 | circuit_bench · current | [STL](stl/V33_B07.stl) · [Preview](previews/V33_B07.png) · [Notes](cards/V33_B07.md) |
| V33_P01 | HV MOS gate charge and switching overlap<br>高压MOS栅电荷与开关交叠 | mechanism_demo · current | [STL](stl/V33_P01.stl) · [Preview](previews/V33_P01.png) · [Notes](cards/V33_P01.md) |
| V33_P02 | Dead-time diode and reverse recovery<br>死区二极管与反向恢复 | mechanism_demo · current | [STL](stl/V33_P02.stl) · [Preview](previews/V33_P02.png) · [Notes](cards/V33_P02.md) |
| V33_P03 | Floating bootstrap supply and UVLO margin<br>浮地自举供电与欠压裕量 | circuit_bench · current | [STL](stl/V33_P03.stl) · [Preview](previews/V33_P03.png) · [Notes](cards/V33_P03.md) |
| V33_P04 | Level-shifter common-mode disturbance<br>电平移位接收端共模扰动 | circuit_bench · current | [STL](stl/V33_P04.stl) · [Preview](previews/V33_P04.png) · [Notes](cards/V33_P04.md) |
| V33_P05 | Current-sense amplifier and delayed comparator<br>电流检测放大器与延迟比较器 | circuit_bench · current | [STL](stl/V33_P05.stl) · [Preview](previews/V33_P05.png) · [Notes](cards/V33_P05.md) |
| V33_P06 | HV startup supply and hysteretic UVLO<br>高压启动供电与迟滞欠压锁定 | circuit_bench · current | [STL](stl/V33_P06.stl) · [Preview](previews/V33_P06.png) · [Notes](cards/V33_P06.md) |
| V33_P07 | Switch-node parasitic ringing and damping<br>开关节点寄生振铃与阻尼 | circuit_bench · current | [STL](stl/V33_P07.stl) · [Preview](previews/V33_P07.png) · [Notes](cards/V33_P07.md) |
| V33_P08 | DC/DC separated losses and thermal budget<br>DC/DC分项损耗与热预算 | circuit_bench · current | [STL](stl/V33_P08.stl) · [Preview](previews/V33_P08.png) · [Notes](cards/V33_P08.md) |
| V33_P09 | Averaged buck soft-start and current-reference limit<br>平均Buck软启动与电流参考限幅 | circuit_bench · current | [STL](stl/V33_P09.stl) · [Preview](previews/V33_P09.png) · [Notes](cards/V33_P09.md) |

The complete sharing edition uses two archives: extract the core package to create **V3-3**, then extract **Semiconductor_Teaching_STL_20261107.zip inside that V3-3 folder**. The printing archive also works independently for printing. Its source files overlap some core dependencies with identical bytes; merge folders and keep the matching versions. Both archives and all individual files are available in the repository.

完整分享版采用两个压缩包：先解压核心包得到 **V3-3**，再将 **Semiconductor_Teaching_STL_20261107.zip解压到该V3-3文件夹内部**。打印包也可独立用于打印；其部分源文件与核心依赖字节一致，合并目录并保留匹配版本即可。仓库同时保存两个压缩包及全部单独文件。
