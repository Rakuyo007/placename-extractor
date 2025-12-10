import subprocess
import json
from typing import List, Dict, Any


PLACE_NAME_EXTRACTOR_PROMPT = """
你是一个高精度中文地名识别模型，只负责抽取地名。

【任务要求】
从下面文本中严格提取所有地名词，包括真实与虚构地名，并统计出现次数。

⚠️禁止输出以下内容：
- 人物
- 组织
- 学校
- 公司
- 医院
- 职业
- 情节总结
- 分析解释
- 推理事件
- 医学信息
- 人物关系
- 病情描述
- 任何非地名内容

⚠️注意事项：
- 地名可能多字（如纽约州、东海之滨、魔王城）
- 地名可虚构（如天龙国）
- 必须统计出现次数
- 如果文本中没有地名，返回空数组

【输出要求】
必须严格返回以下结构的 JSON，无其他内容：

[
  {{"place_name": "xxx", "count": 3}},
  {{"place_name": "yyy", "count": 1}},
  ...
]

下面是文本内容：
====================
{text_to_analyze}
====================

⚠️必须只输出 JSON，不允许附加任何说明，如果没有地名输出 []。
"""

class OllamaClient:
    """
    简易封装，用于发送 prompt 给本地 Ollama，并返回响应内容
    支持 text + json 输出解析
    """

    def __init__(self, model_name="qwen2.5:7b"):
        self.model_name = model_name

    def chat(self, prompt: str) -> str:
        """
        调用 ollama chat 接口，返回 string
        """
        cmd = [
            "ollama",
            "run",
            self.model_name,
        ]

        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, stderr = process.communicate(prompt)
        if stderr:
            print("Ollama stderr:", stderr)

        return stdout

    def ask_json(self, prompt: str) -> List[Dict[str, Any]]:
        """
        返回 JSON 格式时自动解析
        """
        msg = self.chat(prompt).strip()

        # 尝试抽取 json 字符串
        try:
            return json.loads(msg)
        except:
            # 如果带额外文本，尝试截取
            try:
                start = msg.index('[')
                end = msg.rindex(']') + 1
                json_str = msg[start:end]
                return json.loads(json_str)
            except:
                raise ValueError("无法解析 JSON：" + msg)


if __name__ == "__main__":
    ollama = OllamaClient("qwen2.5:7b")
    book_content = """
    孙悟空从花果山归来，途经东海龙宫，见龙王正为儿子敖烈的婚事烦恼。
    孙悟空提议帮助龙王解决问题，龙王欣然同意。
    孙悟空变身为一位富有的商人，携带大量珍宝前往天庭，为敖烈求婚。
    天庭众神见孙悟空如此慷慨，纷纷表示支持。
    最终，敖烈与天庭公主喜结良缘，龙王感激不尽，封孙悟空为“齐天大圣”。
    """
    prompt = PLACE_NAME_EXTRACTOR_PROMPT.format(text_to_analyze=book_content)
    result = ollama.ask_json(prompt)
    print(result)



