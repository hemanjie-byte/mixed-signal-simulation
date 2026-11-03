# Animation and teaching materials

# 动画与教学资料

`buck_energy_flow.gif` is an English-only, looping animation of the P02 idealized positive-current CCM teaching trace. `buck_energy_flow_poster.png` is one still frame. The [undergraduate tutorial](UNDERGRADUATE_TUTORIAL.md) is English first with Chinese explanations below.

`buck_energy_flow.gif`为仅英文标注、循环播放的P02正向连续导通教学动画，`buck_energy_flow_poster.png`为静态图。[大学生教程](UNDERGRADUATE_TUTORIAL.md)采用英文在前、中文解释在下。

The source is [teaching_buck_100V_25C.json](../results/teaching_buck_100V_25C.json). Numeric current and switch-node voltage come from that exported trace. The displayed 0/10 V gate commands are an additional visual assumption, not a gate-charge calculation. Capacitor current is derived from KCL at a fixed 1 A load; the teaching trace holds Vout at 12 V and does not solve its ripple. The separate reverse-recovery pulse, finite gate transition, Coss and ringing are not inserted into this GIF.

数据源为[teaching_buck_100V_25C.json](../results/teaching_buck_100V_25C.json)。电感电流和开关节点电压取自导出轨迹。显示的0/10 V栅极命令属于额外绘图假设，并非栅电荷计算。电容电流由固定1 A负载下的KCL得到；教学轨迹把Vout固定为12 V，不求解纹波。单独的反向恢复脉冲、有限栅转换、Coss与振铃未叠加到GIF中。

Each physical phase is slowed by a different factor so a 40 ns dead time is visible. The waveform horizontal axis retains physical time. Arrows denote conventional current direction; their motion does not represent carrier velocity or current magnitude. The low-side body diode is drawn; the inactive high-side body diode is omitted from the simplified schematic. Low-side channel current travels from ground toward SW during positive-current freewheel.

各物理阶段按不同倍数放慢，使40 ns死区也能看清；波形横轴仍为物理时间。箭头表示传统电流方向，不表示载流子速度或电流大小。简化图画出低侧体二极管，省略未参与该轨迹的高侧体二极管；正向续流期间，低侧沟道电流从地流向SW。

## Rebuild

## 重新生成

After the V3.2 model suite produces its teaching trace:

V3.2模型生成教学数据后运行：

```bash
python -m pip install Pillow numpy
python v32/education/render_buck_animation.py
```

The renderer uses Arial on Windows or DejaVu Sans on Linux. It does not download fonts, illustrations or third-party images. It writes the GIF, poster and `gif_validation.json`. Optional `--inspection-dir /path/to/private/work` saves six inspection frames outside the delivery folder. Geometry, timing rules and all English annotations are in the source. `gif_validation.json` records actual GIF frames, duration, dimensions and SHA-256 hashes of the GIF and numerical source.

绘制器在Windows使用Arial、在Linux使用DejaVu Sans，不下载字体、插图或第三方图片；输出GIF、静态图及`gif_validation.json`。可选`--inspection-dir /path/to/private/work`把六张检查帧保存到交付文件夹之外。几何、时间规则及全部英文标注均在源码中；校验JSON记录GIF实际帧数、时长、尺寸及GIF和数值来源的SHA-256。

The animation is a teaching artifact, not a layout, TCAD solution or device validation. The tutorial explains where the approximation ends and which simulation models investigate the omitted effects.

动画属于教学材料，不是版图、TCAD场解或器件认证；教程说明近似边界，并指向研究缺失效应的对应模型。
