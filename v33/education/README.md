# Twenty models, twenty animated lessons

# 二十个模型，二十个动画课程

Each model A01–A04, B01–B07 and P01–P09 has its own English-only GIF and poster. The animated cursor selects an actual exported sample. The explanatory text in manifest.json is English first with Chinese counterparts. GIFs use a common 1080 × 720 layout and an 8.4-second loop.

每个A01～A04、B01～B07及P01～P09模型都有独立的英文标注GIF及静态图。移动光标选取实际导出的样本；manifest.json中的说明具有英文与中文对照。GIF采用统一1080 × 720布局，循环时长8.4秒。

[Open all twenty lessons](GALLERY.md)

[打开全部二十个课程](GALLERY.md)

## Read the animation type first

## 先看动画类型

- **DC sweep:** A01, A02, A03 and B01 move through independent static bias points. The animation is not a turn-on or settling transient.
- **Temperature/frequency sweep:** B02 changes the assumed temperature; B03 changes frequency. Neither horizontal axis measures elapsed time.
- **Statistical samples:** A04 visits different Monte Carlo samples. The 512 displayed samples are a subset of the 80,000 samples used for the V3.3 reported statistics; the renderer reads the actual count from its source. Motion is not physical time or device evolution.
- **Sampled signal:** B04 shows input samples, final SAR codes and reconstruction error. It does not claim to resolve internal comparator decisions or charge-redistribution timing.
- **Time response:** B05–B07 and P01–P09 use the physical time axes of their exported data. Their abstraction levels still differ: prescribed stages, switched LC states, linear parasitics, averaged control and thermal RC are not interchangeable.

- **直流扫描：**A01、A02、A03与B01经过不同静态偏置点，不表示开通或稳定瞬态。
- **温度/频率扫描：**B02改变假设温度，B03改变频率，横轴均不是经过的时间。
- **统计样本：**A04逐个查看不同蒙特卡洛样本。图示512个样本是V3.3汇总统计所用80000个样本的子集；绘制器读取来源中的实际样本总数。移动不代表物理时间或器件演化。
- **采样信号：**B04显示输入样本、SAR最终输出码与重建误差，不解析内部比较器判决或电荷再分配时序。
- **时间响应：**B05～B07及P01～P09使用导出数据的物理时间坐标，但分阶段模型、开关LC状态、线性寄生、平均控制与热RC属于不同层级。

The playback allocates time to saved samples, rather than using a universal physical slowdown factor. This deliberately makes P02's short dead-time intervals visible. Every panel retains its actual horizontal coordinate and units. Curves show the exported samples; lines between samples aid reading and do not claim additional solver resolution. The B04 error trace is explicitly derived as reconstructed voltage minus input voltage.

播放时间按保存的样本分配，而非采用统一物理时间放慢倍数，因此P02的短死区也能看清。每幅图保留真实横坐标与单位；样本间连线便于阅读，并不代表增加了求解器分辨率。B04误差轨迹明确由重建电压减去输入电压得到。

## What the diagrams mean

## 示意图的含义

The left panels are simplified device sections, terminal symbols or functional diagrams. Functional arrows indicate information or energy influence; they do not portray electrons, displacement trajectories, current density or electric fields. Geometry is fixed and not to scale. A01's section and A02's junction blocks are conceptual, not TCAD meshes. The buck views identify the active switch/diode state from their own saved data; they do not copy ideal states from another bench.

左侧为简化器件截面、端口符号或功能图。功能箭头表示信息或能量作用关系，不代表电子轨迹、位移轨迹、电流密度或电场。几何形状固定且不按比例绘制。A01截面和A02结结构是概念图，并非TCAD网格。Buck动画依据各自保存的数据识别开关/二极管状态，不从其他测试电路复制理想状态。

Each lesson states its most relevant exclusion. Full model limits remain in the numerical model catalog and are copied into the manifest. No GIF establishes foundry qualification, breakdown rating, safe operating area, layout signoff or experimental agreement.

每个课程都标出相关的主要缺项；完整限制保留在数值模型目录，并复制到清单中。GIF不证明晶圆厂认证、击穿额定、安全工作区、版图签核或实验符合性。

## Reproduce and verify

## 重新生成与核验

Run the V3.3 numerical suites first, then:

先运行V3.3数值模型，再执行：

    python -m pip install Pillow numpy
    python v33/education/render_all.py
    python v33/education/validate_gallery.py

Optional --analog PATH and --dcdc PATH select explicit JSON inputs. --inspection-dir PATH writes representative frames and contact sheets outside the publication folder. --models A01 P07 updates selected models and preserves other existing manifest entries. When starting a new output folder, or when numerical inputs change, publication requires rendering all models.

可用--analog PATH及--dcdc PATH指定JSON输入；--inspection-dir PATH把代表帧及联系表输出到发布目录以外。--models A01 P07可更新所选模型并保留清单中其他已有条目。若新建输出文件夹或数值输入发生变化，正式发布前必须生成全部模型。

The renderer uses Arial on Windows and DejaVu Sans on Linux, without downloading assets. Different fonts or Pillow versions can change raster hashes; the manifest records the actual output hashes. It also records input SHA-256 values, selected case IDs, displayed ranges, sampled source indices, plot signal names, actual decoded GIF frame counts, durations, dimensions and file sizes.

绘制器在Windows使用Arial、在Linux使用DejaVu Sans，不下载素材。字体或Pillow版本差异可能改变栅格图哈希，因此清单记录实际输出哈希，同时记录输入SHA-256、案例ID、显示范围、源样本序号、曲线名称、实际解码帧数、时长、尺寸及文件大小。
