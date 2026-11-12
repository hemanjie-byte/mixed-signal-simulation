"""Build self-contained bilingual learning pages from reviewed lesson data."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
def load(p):return json.loads((HERE/p).read_text(encoding='utf8'))
def main():
    lessons=load('lessons/lessons.json');prints=load('lessons/print_lessons.json');audit=load('evidence/validity_audit.json')
    template=(HERE/'learning_template.html').read_text(encoding='utf8')
    common={'__NAV__':'<a href="index.html">Learn / 学习</a><a href="simulation/index.html">Simulate / 仿真</a><a href="printing/index.html">Print / 打印</a><a href="fab/index.html">FAB</a><a href="Mixed_Signal_Simulation_V3-5_EN_ZH.xlsx">Excel</a><a href="../VERSIONS.md">History / 历史</a>'}
    jobs=[('index.html','simulation','',lessons['lessons'],'Explore circuits, one idea at a time','一次理解一个电路概念','Choose the explanation that fits you. Every level uses the same twenty models and the same recorded animations.','选择适合自己的解释方式。三个层级使用相同的二十项模型和已记录动画。'),('printing/index.html','print','../',prints.get('print_lessons',prints.get('models',prints.get('entries',prints.get('lessons',[])))),'Hold a semiconductor idea in your hand','把半导体概念拿在手里','75 enlarged teaching entries. Select a structure, then choose a beginner, undergraduate or graduate explanation.','75 项放大教学条目。先选择结构，再选择入门、本科或研究生解释。')]
    for output,mode,base,records,en,zh,intro,introzh in jobs:
        assert len(records)==(20 if mode=='simulation' else 75), (output,len(records))
        data={'records':records,'audit':audit['models'],'sources':lessons.get('sources',[]) or audit['sources']}
        values=dict(common, __PAGE_TITLE__=en,__HEADING_EN__=en,__HEADING_ZH__=zh,__INTRO_EN__=intro,__INTRO_ZH__=introzh,__MODE__=mode,__BASE__=base,__DATA__=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/'))
        if mode=='print':values['__NAV__']='<a href="../index.html">Learn / 学习</a><a href="../simulation/index.html">Simulate / 仿真</a><a href="index.html">Print / 打印</a><a href="../fab/index.html">FAB</a><a href="../Mixed_Signal_Simulation_V3-5_EN_ZH.xlsx">Excel</a><a href="../../VERSIONS.md">History / 历史</a>'
        html=template
        for key,value in values.items():html=html.replace(key,value)
        (HERE/output).write_text(html,encoding='utf8',newline='\n')
    print('Built 20 numerical lessons and 75 printing lessons at three levels.')
if __name__=='__main__':main()
